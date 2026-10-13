#!/bin/bash
# Monitor open arb positions and evaluate exit conditions
# Usage: ./arb-monitor.sh [--json] [--min-spread 5]
# Checks: current spread vs entry, funding earned (from arb status), PnL, liquidation distance
# Returns JSON with position health + actionable recommendations

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
if ! isok "$ARB_STATUS"; then
  if $JSON_MODE; then
    echo '{"ok":false,"error":"No arb positions or arb status unavailable"}'
  else
    echo "No open arb positions found."
  fi
  exit 0
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
