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

# perp exits 1 on {"ok":false} and prints exactly one JSON document: capture it as-is
# (never append a fallback document); empty output (crash / not installed) → {"ok":false}.
pj() { local out; out=$($PERP "$@" 2>/dev/null) || true; if [[ -n "$out" ]]; then printf '%s\n' "$out"; else echo '{"ok":false}'; fi; }
isok() { jq -e '.ok == true' >/dev/null 2>&1 <<<"$1"; }

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
  FUNDING=$(pj --json arb scan --history "$SYMBOL")
  COMPARE=$(pj --json arb scan --compare "$SYMBOL")
  SCAN=$(pj --json arb scan --mode perp-perp --min 0)
  SPOT_SCAN=$(pj --json arb scan --mode spot-perp --min 0)

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
      "  \(.longExch // .longExchange)→\(.shortExch // .shortExchange): net \(.netSpread)% annual"
    ' 2>/dev/null || echo "  (no opportunity)"
    echo ""
    echo "--- Spot+Perp Arb ---"
    echo "$SPOT_SCAN" | jq -r '
      .data // [] | map(select(.symbol == "'"$SYMBOL"'")) | .[] |
      "  \(.direction) spot:\((.spotExchanges // []) | join("/"))→\(.perpExchange): net \(.netSpreadPct)% annual"
    ' 2>/dev/null || echo "  (no opportunity)"
  fi
else
  # All symbols scan
  SCAN=$(pj --json arb scan --mode all --min 0)
  FUNDING_DETAIL=$(pj --json arb scan --rates)

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
      \"  \(.symbol) | \(.mode // \"perp\") | net \(.netSpread // .netSpreadPct)%/yr | \(.longExch // (\"spot:\" + ((.spotExchanges // []) | join(\"/\"))))→\(.shortExch // .perpExchange)\"
    " 2>/dev/null || echo "(no data)"
  fi
fi
