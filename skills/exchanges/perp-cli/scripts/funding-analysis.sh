#!/bin/bash
# Funding rate analysis across all exchanges
# Usage: ./funding-analysis.sh [--json] [--symbol ETH] [--top 10]
# Fetches current + historical funding data for comparison

set -euo pipefail

# Auto-detect perp command (supports npx fallback for agents without install permissions)
if command -v perp &>/dev/null; then
  PERP="perp"
else
  PERP="npx -y perp-cli@latest"
fi

JSON_MODE=false
SYMBOL=""
TOP=10
while [[ $# -gt 0 ]]; do
  case "$1" in
    --json) JSON_MODE=true; shift ;;
    --symbol) SYMBOL="$2"; shift 2 ;;
    --top) TOP="$2"; shift 2 ;;
    *) shift ;;
  esac
done

if [[ -n "$SYMBOL" ]]; then
  # Single symbol detailed analysis
  FUNDING=$($PERP --json arb scan --history "$SYMBOL" 2>/dev/null || echo '{"ok":false}')
  COMPARE=$($PERP --json arb scan --compare "$SYMBOL" 2>/dev/null || echo '{"ok":false}')
  SCAN=$($PERP --json arb scan --mode perp-perp --min 0 2>/dev/null || echo '{"ok":false}')
  SPOT_SCAN=$($PERP --json arb scan --mode spot-perp --min 0 2>/dev/null || echo '{"ok":false}')

  if $JSON_MODE; then
    cat <<EOF
{
  "ok": true,
  "symbol": "$SYMBOL",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "fundingHistory": $FUNDING,
  "compare": $COMPARE,
  "perpPerpArb": $SCAN,
  "spotPerpArb": $SPOT_SCAN
}
EOF
  else
    echo "=== Funding Analysis: $SYMBOL ==="
    echo ""
    echo "--- Cross-Exchange Compare ---"
    echo "$COMPARE" | jq -r '.data // empty' 2>/dev/null || echo "(unavailable)"
    echo ""
    echo "--- Funding History ---"
    echo "$FUNDING" | jq -r '.data // empty' 2>/dev/null || echo "(unavailable)"
    echo ""
    echo "--- Perp-Perp Arb ---"
    echo "$SCAN" | jq -r '
      .data // [] | map(select(.symbol == "'"$SYMBOL"'")) | .[] |
      "  \(.longExch // .longExchange)→\(.shortExch // .shortExchange): \(.netSpread // .spread)% annual"
    ' 2>/dev/null || echo "  (no opportunity)"
    echo ""
    echo "--- Spot+Perp Arb ---"
    echo "$SPOT_SCAN" | jq -r '
      .data // [] | map(select(.symbol == "'"$SYMBOL"'")) | .[] |
      "  \(.direction): \(.annualSpreadPct // .spread)% annual"
    ' 2>/dev/null || echo "  (no opportunity)"
  fi
else
  # All symbols scan
  SCAN=$($PERP --json arb scan --mode all --min 0 2>/dev/null || echo '{"ok":false}')
  FUNDING_DETAIL=$($PERP --json arb scan --rates 2>/dev/null || echo '{"ok":false}')

  if $JSON_MODE; then
    cat <<EOF
{
  "ok": true,
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "topN": $TOP,
  "allOpportunities": $SCAN,
  "ratesDetail": $FUNDING_DETAIL
}
EOF
  else
    echo "=== Funding Rate Overview (top $TOP) ==="
    echo ""
    echo "$SCAN" | jq -r "
      .data // [] | .[0:$TOP] | .[] |
      \"  \(.symbol) | \(.mode // \"perp\") | \(.netSpread // .spread)bps | \(.longExch // .longExchange)→\(.shortExch // .shortExchange)\"
    " 2>/dev/null || echo "(no data)"
  fi
fi
