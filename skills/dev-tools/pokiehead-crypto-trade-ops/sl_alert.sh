#!/usr/bin/env bash
# SL alert watcher: fires ONE chat alert when price crosses ALERT_ABOVE (short positions).
# This is the CHAT ALERT, not a real stop. For server-side protection pass SLPRICE
# to bitunix_client.py open (presetStopLossPrice) so the exchange holds it.
set -u
SYMBOL=${SYMBOL:-BTCUSDT}; ALERT_ABOVE=${ALERT_ABOVE:-88000}
SL_LEVEL=${SL_LEVEL:-88400}; LIQ_ZONE=${LIQ_ZONE:-88500}
FLAG=${FLAG:-$HOME/.crypto-ops/.sl-alert-done}
PY=${PY:-python3}
mkdir -p "$(dirname "$FLAG")"
[ -f "$FLAG" ] && exit 0
price=$(curl -s -m 10 "https://fapi.bitunix.com/api/v1/futures/market/tickers?symbols=$SYMBOL" | "$PY" -c "import json,sys; print(json.load(sys.stdin)['data'][0]['lastPrice'])" 2>/dev/null)
[ -z "$price" ] && exit 0
hit=$("$PY" -c "print(1 if float('$price') >= float('$ALERT_ABOVE') else 0)")
[ "$hit" = "1" ] || exit 0
touch "$FLAG"
echo "ALERTA: $SYMBOL a $price - zona de SL $SL_LEVEL (liquidacion ~$LIQ_ZONE). Revisa la posicion YA."
exit 0
