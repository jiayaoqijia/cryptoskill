#!/bin/bash
# Scan spot+perp funding rate arbitrage opportunities
# Usage: ./spot-perp-scan.sh [--json] [--mode all|spot-perp|perp-perp] [--min 10]
# Combines perp-perp and spot-perp scans with validation

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
MODE="all"
MIN_SPREAD=10
while [[ $# -gt 0 ]]; do
  case "$1" in
    --json) JSON_MODE=true; shift ;;
    --mode) MODE="$2"; shift 2 ;;
    --min) MIN_SPREAD="$2"; shift 2 ;;
    *) shift ;;
  esac
done

# 1. Portfolio check (ensure we have balances)
PORTFOLIO=$(pj --json portfolio)
if ! isok "$PORTFOLIO"; then
  if $JSON_MODE; then
    echo '{"ok":false,"error":"Cannot fetch portfolio — check wallet setup"}'
  else
    echo "ERROR: Cannot fetch portfolio. Check wallet setup first."
  fi
  exit 1
fi

# 2. Run appropriate scan
SCAN_RESULT=$(pj --json arb scan --mode "$MODE" --min "$MIN_SPREAD")

# 3. Get exchange health for context (proxy via market prices fetch)
HEALTH=$(pj --json market prices)

if $JSON_MODE; then
  cat <<EOF
{
  "ok": true,
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "mode": "$MODE",
  "minSpread": $MIN_SPREAD,
  "portfolio": $PORTFOLIO,
  "scan": $SCAN_RESULT,
  "health": $HEALTH
}
EOF
else
  echo "=== Spot+Perp Arb Scanner ==="
  echo "Mode: $MODE | Min spread: ${MIN_SPREAD}% annual"
  echo ""

  # Show balances
  echo "--- Balances ---"
  echo "$PORTFOLIO" | jq -r '
    .data.exchanges // [] | .[] |
    "  \(.name): equity $\(.perp.equity // "N/A")"
  ' 2>/dev/null || echo "  (unable to parse)"
  echo ""

  # Show opportunities
  echo "--- Opportunities ---"
  echo "$SCAN_RESULT" | jq -r '
    .data // [] | .[] |
    "  \(.symbol) | \(.mode // "perp-perp") | net: \(.netSpread // .netSpreadPct)%/yr | \(.longExch // ("spot:" + ((.spotExchanges // []) | join("/"))))→\(.shortExch // .perpExchange)"
  ' 2>/dev/null || echo "  (no opportunities or parse error)"

  # Show exchange health
  echo ""
  echo "--- Exchange Health ---"
  echo "$HEALTH" | jq -r '
    .data // {} | to_entries[] |
    "  \(.key): \(.value.status // .value // "unknown")"
  ' 2>/dev/null || echo "  (unable to check)"
fi
