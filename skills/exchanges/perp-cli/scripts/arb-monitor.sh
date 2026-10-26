#!/bin/bash
# Monitor open arb positions and evaluate exit conditions
# Usage: ./arb-monitor.sh [--json] [--min-spread 5]
# Checks: current spread vs entry, funding earned (from arb status), PnL, liquidation distance
# Returns JSON with position health + actionable recommendations

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
MIN_SPREAD=5
while [[ $# -gt 0 ]]; do
  case "$1" in
    --json) JSON_MODE=true; shift ;;
    --min-spread) MIN_SPREAD="$2"; shift 2 ;;
    *) shift ;;
  esac
done

# 1. Get current arb status (already includes funding earned per period)
ARB_STATUS=$(pj --json arb status)
# A failed read is an error, never "no positions" (arb status fails as a whole when one
# configured venue's read fails — check that venue: perp --json -e <venue> account positions).
if ! isok "$ARB_STATUS"; then
  if $JSON_MODE; then
    jq -c '{ok:false, error:{code:.error.code, message:.error.message, source:"perp --json arb status"}}' <<<"$ARB_STATUS"
  else
    echo "ERROR: arb status failed: $(jq -r '"\(.error.code): \(.error.message)"' <<<"$ARB_STATUS")" >&2
  fi
  exit 1
fi

# 2. Get current spreads (all modes)
ARB_SCAN=$(pj --json arb scan --mode all --min 0)

# 3. Get liquidation distances
LIQ_DIST=$(pj --json risk liquidation-distance)

# 4. Get risk overview
RISK_STATUS=$(pj --json risk status)

# 5. Output combined analysis
if $JSON_MODE; then
  cat <<EOF
{
  "ok": true,
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "positions": $ARB_STATUS,
  "currentSpreads": $ARB_SCAN,
  "liquidationDistance": $LIQ_DIST,
  "riskStatus": $RISK_STATUS,
  "minSpreadThreshold": $MIN_SPREAD
}
EOF
else
  echo "=== Arb Position Monitor ==="
  echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo ""
  echo "--- Positions (with funding earned) ---"
  echo "$ARB_STATUS" | jq -r '.data // empty'
  echo ""
  echo "--- Liquidation Distance ---"
  echo "$LIQ_DIST" | jq -r '.data // empty'
  echo ""
  echo "--- Risk Status ---"
  echo "$RISK_STATUS" | jq -r '.data // empty'
  echo ""
  echo "Min spread threshold: ${MIN_SPREAD}% annual"
  echo "Recommendation: Check if current spreads exceed ${MIN_SPREAD}% to continue holding."
fi
