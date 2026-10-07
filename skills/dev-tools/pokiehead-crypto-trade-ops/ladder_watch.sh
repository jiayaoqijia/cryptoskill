#!/usr/bin/env bash
# Tiered take-profit watcher (state machine 1 -> 2 -> 3).
# T1 closes when price <= T1_BELOW, T2 when <= T2_BELOW. State file survives restarts.
set -u
SYMBOL=${SYMBOL:-BTCUSDT}; T1_BELOW=${T1_BELOW:-85600}; T2_BELOW=${T2_BELOW:-85200}
T1_QTY=${T1_QTY:-0.0057}; T2_QTY=${T2_QTY:-0.0057}
STATE=${STATE:-$HOME/.crypto-ops/.tier-state}; CLIENT=${CLIENT:-$HOME/crypto-ops/bitunix_client.py}
PY=${PY:-python3}
mkdir -p "$(dirname "$STATE")"
[ -f "$STATE" ] || echo 1 > "$STATE"
ST=$(cat "$STATE"); [ "$ST" -ge 3 ] && exit 0
price=$(curl -s -m 10 "https://fapi.bitunix.com/api/v1/futures/market/tickers?symbols=$SYMBOL" | "$PY" -c "import json,sys; print(json.load(sys.stdin)['data'][0]['lastPrice'])" 2>/dev/null)
[ -z "$price" ] && exit 0
if [ "$ST" -eq 1 ] && [ "$("$PY" -c "print(1 if float('$price') <= float('$T1_BELOW') else 0)")" = "1" ]; then
  "$PY" "$CLIENT" close "$SYMBOL" BUY "$T1_QTY"; echo 2 > "$STATE"; ST=2
fi
if [ "$ST" -eq 2 ] && [ "$("$PY" -c "print(1 if float('$price') <= float('$T2_BELOW') else 0)")" = "1" ]; then
  "$PY" "$CLIENT" close "$SYMBOL" BUY "$T2_QTY"; echo 3 > "$STATE"
fi
exit 0
