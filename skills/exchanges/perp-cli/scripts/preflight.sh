#!/bin/bash
# Pre-flight validation for perp-cli operations
# Checks: install, wallet, connectivity, balances, risk
# Usage: ./preflight.sh [--json]
# Returns JSON with { ready: bool, checks: [...], issues: [...] }

set -euo pipefail

# perp must be installed (no npx / auto-install path: the user decides what gets installed).
if ! command -v perp &>/dev/null; then
  echo "perp not found — ask the user to install perp-cli >= 0.16.0" >&2
  echo '{"ok":false,"error":{"code":"PERP_NOT_FOUND","message":"perp not found — ask the user to install perp-cli >= 0.16.0"}}'
  exit 1
fi
PERP="perp"

# perp exits 1 on {"ok":false} and prints exactly one JSON document: capture it as-is
# (never append a fallback document); empty output (crash) → an explicit NO_OUTPUT error document.
pj() { local out; out=$($PERP "$@" 2>/dev/null) || true; if [[ -n "$out" ]]; then printf '%s\n' "$out"; else echo '{"ok":false,"error":{"code":"NO_OUTPUT","message":"perp printed nothing (crashed?)"}}'; fi; }
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

# 1. perp-cli version (must be >= 0.16.0)
VERSION=$($PERP --version 2>/dev/null || true)
MIN_VERSION="0.16.0"
if [[ -z "$VERSION" ]]; then
  add_check "install" "fail" "perp --version printed nothing — ask the user to (re)install perp-cli >= $MIN_VERSION"
elif [[ "$(printf '%s\n%s\n' "$MIN_VERSION" "$VERSION" | sort -V | head -1)" != "$MIN_VERSION" ]]; then
  add_check "install" "fail" "perp-cli $VERSION < $MIN_VERSION — ask the user to upgrade"
else
  add_check "install" "pass" "perp-cli $VERSION"
fi

# 2. Wallet configured (with an OWS wallet, `exchanges: []` in wallet show is normal)
WALLET_OUT=$(pj --json wallet show)
if isok "$WALLET_OUT"; then
  add_check "wallet" "pass" "Wallet configured"
else
  add_check "wallet" "fail" "wallet show failed ($(jq -r '.error.code' <<<"$WALLET_OUT")) — the user registers a key: perp wallet set <exchange> (stdin / hidden prompt)"
fi

# 3. Venue connectivity: perp health (healthy = every OFFICIAL-API venue is up;
#    allHealthy also counts unofficial APIs such as TxFlow)
HEALTH_OUT=$(pj --json health)
if ! isok "$HEALTH_OUT"; then
  add_check "connectivity" "fail" "perp health failed ($(jq -r '.error.code' <<<"$HEALTH_OUT"))"
elif [[ "$(jq -r '.data.healthy' <<<"$HEALTH_OUT")" == "true" ]]; then
  add_check "connectivity" "pass" "All official venues reachable"
else
  DOWN=$(jq -r '[.data.exchanges[] | select(.status != "ok") | .exchange] | join(",")' <<<"$HEALTH_OUT")
  add_check "connectivity" "warn" "Official venues down: $DOWN — do not use them until perp health shows them ok"
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
