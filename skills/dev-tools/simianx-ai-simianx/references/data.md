# Market data and Pulse

Crypto exchange data is sold; US stock quotes and candles are not exposed (they appear inside analyses only).

| Call | Points | Notes |
|---|---|---|
| `GET /v1/instruments/search?q=sol&asset=all&limit=20` | 0 (heavy limit) | stocks and coins, best match first; each item has `asset`, `symbol` (pass it to start an autopilot or a live run on the default instrument: the USDT perpetual for a coin, the ticker for a stock) and `start_with` (this exact pair / ticker) |
| `GET /v1/market/status` | 0 | US equity session window |
| `GET /v1/quotes?symbols=BTC,ETH,SOL` | 0.1 (≤ 20 symbols), 0.5 (≤ 120) | crypto only; `missing[]` lists symbols without a quote |
| `GET /v1/market/{symbol}/candles?timeframe=1H&limit=200&before=<ms>` | 0.2 | `columns` names the array positions; `before` pages back |
| `GET /v1/market/{symbol}/indicators?timeframe=1H` | 0.3 (0 when 202 pending) | SMA/EMA/RSI/MACD/ATR… snapshot |
| `GET /v1/pulse/events?asset=crypto&min_severity=2&symbol=BTC&since=<iso>` | 0.3 (0.05 when `since` finds nothing) | price, level, indicator, volume and news events with an AI summary; delayed 15 min on delayed plans |
| `GET /v1/pulse/summary` | 0.2 | 24h counts, highlights, breadth |

`symbol` for crypto accepts `BTC`, `BTC-USDT`, `BTC-USDT-SWAP`, `BTCUSDT`; the perpetual on the first exchange that lists it is used.
