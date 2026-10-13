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

# perp exits 1 on {"ok":false} and prints exactly one JSON document: capture it as-is
# (never append a fallback document); empty output (crash / not installed) → {"ok":false}.
pj() { local out; out=$($PERP "$@" 2>/dev/null) || true; if [[ -n "$out" ]]; then printf '%s\n' "$out"; else echo '{"ok":false}'; fi; }
isok() { jq -e '.ok == true' >/dev/null 2>&1 <<<"$1"; }

JSON_MODE=false
[[ "${1:-}" == "--json" ]] && JSON_MODE=true

issues=()
checks=()

add_check() {
  local name="$1" status="$2" detail="$3"
  checks+=("{\"name\":\"$name\",\"status\":\"$status\",\"detail\":\"$detail\"}")
  if [[ "$status" == "fail" ]]; then issues+=("$name: $detail"); fi
}

# 1. perp-cli installed and version check
VERSION=$($PERP --version 2>/dev/null || echo "unknown")
if [[ "$VERSION" != "unknown" ]]; then
  add_check "install" "pass" "perp-cli $VERSION ($(command -v perp &>/dev/null && echo 'global' || echo 'npx'))"
else
  add_check "install" "fail" "perp-cli not found — ask the user before installing (npm i -g perp-cli@latest) or use npx"
fi

# 2. Wallet configured
WALLET_OUT=$(pj --json wallet show)
if isok "$WALLET_OUT"; then
  add_check "wallet" "pass" "Wallet configured"
else
  add_check "wallet" "fail" "No wallet configured — run: perp wallet set <exchange>  (key via hidden prompt or stdin)"
fi

# 3. Exchange connectivity (proxy via unauthenticated market prices fetch)
HEALTH_OUT=$(pj --json market prices)
if isok "$HEALTH_OUT"; then
  add_check "connectivity" "pass" "Exchange reachable"
else
  add_check "connectivity" "warn" "Exchange unreachable"
fi

# 4. Portfolio & balances
PORTFOLIO_OUT=$(pj --json portfolio)
if isok "$PORTFOLIO_OUT"; then
  add_check "portfolio" "pass" "Portfolio accessible"
else
  add_check "portfolio" "warn" "Could not fetch portfolio"
fi

# 5. Risk status
RISK_OUT=$(pj --json risk status)
CAN_TRADE=$(jq -r '.data.canTrade // empty' <<<"$RISK_OUT" 2>/dev/null || true)
if [[ "$CAN_TRADE" == "true" ]]; then
  add_check "risk" "pass" "Trading allowed (canTrade=true)"
elif [[ "$CAN_TRADE" == "false" ]]; then
  add_check "risk" "fail" "Trading blocked — check risk violations"
else
  add_check "risk" "warn" "Could not check risk status"
fi

# Output
READY=true
if [[ ${#issues[@]} -gt 0 ]]; then READY=false; fi

if $JSON_MODE; then
  CHECKS_JSON=$(IFS=,; echo "${checks[*]}")
  ISSUES_JSON='[]'
  if [[ ${#issues[@]} -gt 0 ]]; then ISSUES_JSON=$(printf '%s\n' "${issues[@]}" | jq -R . | jq -s .); fi
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
