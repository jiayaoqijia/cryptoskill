#!/usr/bin/env bash
# Entry trigger: fires ONE market order when price crosses ENTRY_ABOVE (self-disables via flag).
# SL_PCT=2.5 attaches a SERVER-SIDE stop-loss 2.5% above entry (short) - survives bot death.
# Empty SL_PCT = no SL attached (until presetStopLossPrice is verified against the live API).
# Idempotent: the flag file prevents double entries across cron runs.
set -u
SYMBOL=${SYMBOL:-BTCUSDT}; ENTRY_ABOVE=${ENTRY_ABOVE:-87000}
QTY_USD=${QTY_USD:-600}; LEV=${LEV:-40}
SL_PCT=${SL_PCT:-}
FLAG=${FLAG:-$HOME/.crypto-ops/.entry-done}; CLIENT=${CLIENT:-$HOME/crypto-ops/bitunix_client.py}
PY=${PY:-python3}
mkdir -p "$(dirname "$FLAG")"
[ -f "$FLAG" ] && exit 0
price=$(curl -s -m 10 "https://fapi.bitunix.com/api/v1/futures/market/tickers?symbols=$SYMBOL" | "$PY" -c "import json,sys; print(json.load(sys.stdin)['data'][0]['lastPrice'])" 2>/dev/null)
[ -z "$price" ] && exit 0
hit=$("$PY" -c "print(1 if float('$price') >= float('$ENTRY_ABOVE') else 0)")
[ "$hit" = "1" ] || exit 0
touch "$FLAG"
qty=$("$PY" -c "print(round(float('$QTY_USD') / float('$price'), 4))")
if [ -n "$SL_PCT" ]; then
  sl=$("$PY" -c "print(round(float('$price') * (1 + float('$SL_PCT')/100), 1))")
  "$PY" "$CLIENT" open "$SYMBOL" SELL OPEN "$qty" "$LEV" "$sl"
else
  "$PY" "$CLIENT" open "$SYMBOL" SELL OPEN "$qty" "$LEV"
fi
exit 0
