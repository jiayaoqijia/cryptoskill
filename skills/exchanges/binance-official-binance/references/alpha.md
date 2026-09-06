## Market Data

| Endpoint | Key params | Description |
|---|---|---|
| aggregated-trades | `symbol` [`from-id` `start-time` `end-time` `limit`] | Aggregated Trades |
| full-depth | `symbol` [`limit`] | Full Depth |
| get-exchange-info | [] | Get Exchange Info |
| klines | `symbol` `interval` [`limit` `start-time` `end-time`] | Klines |
| ticker | `symbol` [] | Ticker |
| token-list | [] | Token List |

### Enums

**interval:** `1s` `15s` `1m` `3m` `5m` `15m` `30m` `1h` `2h` `4h` `6h` `8h` `12h` `1d` `3d` `1w` `1M`
**limit:** `5` `10` `20` `50` `100` `500` `1000`