## Default

| Endpoint | Key params | Description |
|---|---|---|
| aggregate-trade-stream | `symbol` [`id`] | Aggregate Trade Stream |
| all-book-ticker-stream | [`id`] | All Book Ticker Stream |
| all-mini-ticker-stream | [`id`] | All Mini Ticker Stream |
| all-ticker-stream | [`id`] | All Ticker Stream |
| all-tokens24h-ticker-stream | [`id`] | All Tokens 24h Ticker Stream |
| book-ticker-stream | `symbol` [`id`] | Book Ticker Stream |
| contract-kline-stream | `contract-address` `chain-id` `interval` [`id`] | Contract Kline Stream |
| full-depth-stream | `symbol` `interval` [`id`] | Full Depth Stream |
| kline-stream | `symbol` `interval` [`id`] | Kline Stream |
| mini-ticker-stream | `symbol` [`id`] | Mini Ticker Stream |
| partial-depth-stream | `symbol` `levels` `interval` [`id`] | Partial Depth Stream |
| ticker-stream | `symbol` [`id`] | Ticker Stream |
| trade-stream | `symbol` [`id`] | Trade Stream |

### Enums

**interval:** `1m` `3m` `5m` `15m` `30m` `1h` `2h` `4h` `6h` `8h` `12h` `1d` `3d` `1w` `1M`
**levels:** `5` `10` `20`