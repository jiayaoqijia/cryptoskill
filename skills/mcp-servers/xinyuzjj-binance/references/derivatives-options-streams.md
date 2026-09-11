## Market

| Endpoint | Key params | Description |
|---|---|---|
| index-price-streams | [`id`] | Index Price Streams |
| kline-candlestick-streams | `symbol` `interval` [`id`] | Kline/Candlestick Streams |
| new-symbol-info | [`id`] | New Symbol Info |
| open-interest | `underlying` `expiration-date` [`id`] | Open Interest |
| option-mark-price | `underlying` [`id`] | Option Mark Price |

## Public

| Endpoint | Key params | Description |
|---|---|---|
| diff-book-depth-streams | `symbol` `update-speed` [`id`] | Diff Book Depth Streams |
| hour24-ticker | `symbol` [`id` `expiration-date`] | 24-hour TICKER |
| individual-symbol-book-ticker-streams | `symbol` [`id`] | Individual Symbol Book Ticker Streams |
| partial-book-depth-streams | `symbol` `level` `update-speed` [`id`] | Partial Book Depth Streams |
| trade-streams | `symbol` [`id`] | Trade Streams |

## Other streams

| Endpoint | Key params | Description |
|---|---|---|
| user-data | listen-key [id] | Subscribes to the user data WebSocket stream using the provided listen key. |
### Enums

**interval:** `1m` `3m` `5m` `15m` `30m` `1h` `2h` `4h` `6h` `12h` `1d` `3d` `1w`
**level:** `5` `10` `20`
**update-speed:** `100ms` `500ms`