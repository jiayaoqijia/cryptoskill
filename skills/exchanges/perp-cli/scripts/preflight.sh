#!/bin/bash
# Pre-flight validation for perp-cli operations
# Checks: install, wallet, connectivity, balances, risk
# Usage: ./preflight.sh [--json]
# Returns JSON with { ready: bool, checks: [...], issues: [...] }

set -euo pipefail

# Auto-detect perp command (supports npx fallback for agents without install permissions)
if command -v perp &>/dev/null; then
  PERP="perp"
else
  PERP="npx -y perp-cli@latest"
fi

JSON_MODE=false
[[ "${1:-}" == "--json" ]] && JSON_MODE=true

issues=()
checks=()

add_check() {
  local name="$1" status="$2" detail="$3"
  checks+=("{\"name\":\"$name\",\"status\":\"$status\",\"detail\":\"$detail\"}")
  [[ "$status" == "fail" ]] && issues+=("$name: $detail")
}

# 1. perp-cli installed and version check
VERSION=$($PERP --version 2>/dev/null || echo "unknown")
if [[ "$VERSION" != "unknown" ]]; then
  add_check "install" "pass" "perp-cli $VERSION ($(command -v perp &>/dev/null && echo 'global' || echo 'npx'))"
else
  add_check "install" "fail" "perp-cli not found — run: npm i -g perp-cli@latest or use npx"
fi

# 2. Wallet configured
WALLET_OUT=$($PERP --json wallet show 2>/dev/null || echo '{"ok":false}')
if echo "$WALLET_OUT" | grep -q '"ok":true'; then
  add_check "wallet" "pass" "Wallet configured"
else
  add_check "wallet" "fail" "No wallet configured — run: perp wallet set <exchange> <key>"
fi

# 3. Exchange connectivity (proxy via unauthenticated market prices fetch)
HEALTH_OUT=$($PERP --json market prices 2>/dev/null || echo '{"ok":false}')
if echo "$HEALTH_OUT" | grep -q '"ok":true'; then
  add_check "connectivity" "pass" "Exchange reachable"
else
  add_check "connectivity" "warn" "Exchange unreachable"
fi

# 4. Portfolio & balances
PORTFOLIO_OUT=$($PERP --json portfolio 2>/dev/null || echo '{"ok":false}')
if echo "$PORTFOLIO_OUT" | grep -q '"ok":true'; then
  add_check "portfolio" "pass" "Portfolio accessible"
else
  add_check "portfolio" "warn" "Could not fetch portfolio"
fi

# 5. Risk status
RISK_OUT=$($PERP --json risk status 2>/dev/null || echo '{"ok":false}')
if echo "$RISK_OUT" | grep -q '"canTrade":true'; then
  add_check "risk" "pass" "Trading allowed (canTrade=true)"
elif echo "$RISK_OUT" | grep -q '"canTrade":false'; then
  add_check "risk" "fail" "Trading blocked — check risk violations"
else
  add_check "risk" "warn" "Could not check risk status"
fi

# Output
READY=true
[[ ${#issues[@]} -gt 0 ]] && READY=false

if $JSON_MODE; then
  CHECKS_JSON=$(IFS=,; echo "${checks[*]}")
  ISSUES_JSON=$(printf '%s\n' "${issues[@]}" | jq -R . | jq -s .)
  echo "{\"ready\":$READY,\"checks\":[$CHECKS_JSON],\"issues\":$ISSUES_JSON}"
else
  echo "=== perp-cli Pre-flight Check ==="
  for c in "${checks[@]}"; do
    name=$(echo "$c" | jq -r .name)
    status=$(echo "$c" | jq -r .status)
    detail=$(echo "$c" | jq -r .detail)
    case "$status" in
      pass) icon="✓" ;;
      warn) icon="⚠" ;;
      fail) icon="✗" ;;
    esac
    printf "  %s %-15s %s\n" "$icon" "$name" "$detail"
  done
  echo ""
  if $READY; then
    echo "Ready to trade."
  else
    echo "Issues found:"
    for i in "${issues[@]}"; do echo "  - $i"; done
  fi
fi
