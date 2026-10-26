#!/bin/bash
# Funding rate analysis across all exchanges
# Usage: ./funding-analysis.sh [--json] [--symbol ETH] [--top 10] [--hours 24] [-n mainnet|testnet]
# --symbol: cross-venue compare + each verified venue's SETTLED funding history
#   (`-e <venue> market funding <SYM> -l <hours>`, averaged per venue). `arb scan --history` is only
#   the locally recorded snapshots (written by earlier `arb scan --rates` runs) and is often empty.
# Testnet funding / spreads are not meaningful — use mainnet (the default) for yield analysis.

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
SYMBOL=""
TOP=10
HOURS=24
NETWORK="mainnet"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --json) JSON_MODE=true; shift ;;
    --symbol) SYMBOL="$2"; shift 2 ;;
    --top) TOP="$2"; shift 2 ;;
    --hours) HOURS="$2"; shift 2 ;;
    -n|--network) NETWORK="$2"; shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done
PERP="perp -n $NETWORK"

# Row label per scan mode (perp-perp rows: longExch/shortExch; spot-perp rows: spotExchanges/perpExchange/direction)
ROW_JQ='if .mode == "spot-perp" then
    "  \(.symbol) | spot-perp | net \(.netSpread)%/yr | \(.direction) spot:\(.spotExchanges | join("/")) perp:\(.perpExchange)"
    + (if .direction == "long-spot-short-perp" then "" else "  [NOT executable with arb exec]" end)
  else
    "  \(.symbol) | perp-perp | net \(.netSpread)%/yr | long \(.longExch) / short \(.shortExch)"
  end'

if [[ -n "$SYMBOL" ]]; then
  # Single symbol detailed analysis
  COMPARE=$(pj --json arb scan --compare "$SYMBOL")
  LOCAL_HISTORY=$(pj --json arb scan --history "$SYMBOL" --hours "$HOURS")
  SCAN=$(pj --json arb scan --mode perp-perp --min 0)
  SPOT_SCAN=$(pj --json arb scan --mode spot-perp --min 0)

  # Settled funding history per verified venue of the compare (rows newest first; rate = fraction per intervalHours)
  SETTLED="[]"
  if isok "$COMPARE" && [[ "$(jq -r '.data.available' <<<"$COMPARE")" != "false" ]]; then
    for VENUE in $(jq -r '.data.rates[] | select(.fundingVerified) | .exchange' <<<"$COMPARE"); do
      H=$(pj --json -e "$VENUE" market funding "$SYMBOL" -l "$HOURS")
      ROW=$(jq -c --arg v "$VENUE" '
        if .ok then
          { exchange: $v, rows: (.data | length),
            avgHourlyRate: (if (.data | length) > 0 and all(.data[]; .rate != null and .intervalHours != null)
                            then ([.data[] | ((.rate | tonumber) / .intervalHours)] | add / length) else null end) }
          | .avgAnnualPct = (if .avgHourlyRate == null then null else .avgHourlyRate * 8760 * 100 end)
        else { exchange: $v, error: .error.code, message: .error.message } end' <<<"$H")
      SETTLED=$(jq -c --argjson r "$ROW" '. + [$r]' <<<"$SETTLED")
    done
  fi

  if $JSON_MODE; then
    cat <<EOF
{
  "ok": true,
  "network": "$NETWORK",
  "symbol": "$SYMBOL",
  "hours": $HOURS,
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "compare": $COMPARE,
  "settledHistory": $SETTLED,
  "localSnapshotHistory": $LOCAL_HISTORY,
  "perpPerpArb": $SCAN,
  "spotPerpArb": $SPOT_SCAN
}
EOF
  else
    echo "=== Funding Analysis: $SYMBOL ($NETWORK) ==="
    echo ""
    echo "--- Cross-Exchange Compare ---"
    if isok "$COMPARE"; then jq -r '.data' <<<"$COMPARE"; else echo "  ERROR: $(jq -r '.error.code' <<<"$COMPARE")"; fi
    echo ""
    echo "--- Settled funding, last $HOURS rows per venue (avg annualized %) ---"
    jq -r '.[] | if .error then "  \(.exchange): ERROR \(.error)" else "  \(.exchange): \(.rows) rows, avg \(.avgAnnualPct)%/yr" end' <<<"$SETTLED"
    echo ""
    echo "--- Perp-Perp Arb ---"
    if isok "$SCAN"; then jq -r --arg s "$SYMBOL" ".data[] | select(.symbol == \$s) | $ROW_JQ" <<<"$SCAN"; else echo "  ERROR: $(jq -r '.error.code' <<<"$SCAN")"; fi
    echo ""
    echo "--- Spot+Perp Arb ---"
    if isok "$SPOT_SCAN"; then jq -r --arg s "$SYMBOL" ".data[] | select(.symbol == \$s) | $ROW_JQ" <<<"$SPOT_SCAN"; else echo "  ERROR: $(jq -r '.error.code' <<<"$SPOT_SCAN")"; fi
  fi
else
  # All symbols scan
  SCAN=$(pj --json arb scan --mode all --min 0)
  FUNDING_DETAIL=$(pj --json arb scan --rates)

  if $JSON_MODE; then
    cat <<EOF
{
  "ok": true,
  "network": "$NETWORK",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "topN": $TOP,
  "allOpportunities": $SCAN,
  "ratesDetail": $FUNDING_DETAIL
}
EOF
  else
    echo "=== Funding Rate Overview (top $TOP, $NETWORK) ==="
    echo ""
    if isok "$SCAN"; then jq -r ".data[0:$TOP][] | $ROW_JQ" <<<"$SCAN"; else echo "  ERROR: $(jq -r '.error.code' <<<"$SCAN")"; fi
  fi
fi
