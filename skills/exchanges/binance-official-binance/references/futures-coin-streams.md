## Default

| Endpoint | Key params | Description |
|---|---|---|
| aggregate-trade-streams | `symbol` [`id`] | Aggregate Trade Streams |
| all-book-tickers-stream | [`id`] | All Book Tickers Stream |
| all-market-liquidation-order-streams | [`id`] | All Market Liquidation Order Streams |
| all-market-mini-tickers-stream | [`id`] | All Market Mini Tickers Stream |
| all-market-tickers-streams | [`id`] | All Market Tickers Streams |
| continuous-contract-kline-candlestick-streams | `pair` `contract-type` `interval` [`id`] | Continuous Contract Kline/Candlestick Streams |
| contract-info-stream | [`id`] | Contract Info Stream |
| diff-book-depth-streams | `symbol` [`id` `update-speed`] | Diff. Book Depth Streams |
| index-kline-candlestick-streams | `pair` `interval` [`id`] | Index Kline/Candlestick Streams |
| index-price-stream | `pair` [`id` `update-speed`] | Index Price Stream |
| individual-symbol-book-ticker-streams | `symbol` [`id`] | Individual Symbol Book Ticker Streams |
| individual-symbol-mini-ticker-stream | `symbol` [`id`] | Individual Symbol Mini Ticker Stream |
| individual-symbol-ticker-streams | `symbol` [`id`] | Individual Symbol Ticker Streams |
| kline-candlestick-streams | `symbol` `interval` [`id`] | Kline/Candlestick Streams |
| mark-price-kline-candlestick-streams | `symbol` `interval` [`id`] | Mark Price Kline/Candlestick Streams |
| mark-price-of-all-symbols-of-a-pair | `pair` [`id` `update-speed`] | Mark Price of All Symbols of a Pair |
| mark-price-stream | `symbol` [`id` `update-speed`] | Mark Price Stream |
| market-liquidation-order-streams | `symbol` [`id`] | Market Liquidation Order Streams |
| partial-book-depth-streams | `symbol` `levels` [`id` `update-speed`] | Partial Book Depth Streams |

## Other streams

| Endpoint | Key params | Description |
|---|---|---|
| user-data | listen-key [id] | Subscribes to the user data WebSocket stream using the provided listen key. |
### Enums

**contract-type:** `perpetual` `current_quarter` `next_quarter`
**interval:** `1m` `3m` `5m` `15m` `30m` `1h` `2h` `4h` `6h` `8h` `12h` `1d` `3d` `1w` `1M`
**levels:** `5` `10` `20`
**update-speed:** `100ms` `500ms`