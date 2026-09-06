# Market OpenAPI: Market Data Actions (market.*)

> 3 actions for trading volume, liquidity events, and K-line charts.

---

## Action 7: market.volume_stats

Trading volume stats across 5m/1h/4h/24h periods. Shows buy/sell volume, amounts, tx counts.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| chain_id | int | Yes | Chain ID |
| token_address | string | Yes | Contract address |
| pair_address | string | No | Trading pair address |

```bash
python3 gate-dex-market/scripts/gate-api-call.py "market.volume_stats" '{"chain_id":56,"token_address":"0xdAC17F..."}'
```

Response: Map keyed by period (`5m`/`1h`/`4h`/`24h`), each containing `buyVolume`, `sellVolume`, `buyAmount`, `sellAmount`, `txCountBuy`, `txCountSell`.

Display all 4 periods, highlight buy/sell pressure comparison.

---

## Action 8: market.pair.liquidity.list

Liquidity add/remove events. For tracking market maker behavior and Rug Pull warnings.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| chain_id | int | Yes | Chain ID |
| token_address | string | Yes | Contract address |
| pair_address | string | No | Trading pair address |
| page_index | int | No | Page (default 1) |
| page_size | int | No | Per page (default 15, max 15) |

```bash
python3 gate-dex-market/scripts/gate-api-call.py "market.pair.liquidity.list" '{"chain_id":1,"token_address":"0xdAC17F...","page_index":1,"page_size":15}'
```

Response events: `side` (add/remove), `maker`, `total_volume_usd`, `token0_symbol/amount0`, `token1_symbol/amount1`, `dex`, `txn_hash`.

**Warning**: Highlight large `remove` operations — potential liquidity withdrawal risk.

---

## Action 9: market.candles

K-line (candlestick) data. Max 1440 points per request.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| chain_id | int | Yes | Chain ID |
| token_address | string | Yes | Contract address (**lowercase for EVM**) |
| period | int | Yes | Seconds: 60=1m, 300=5m, 3600=1h, 86400=1d |
| start | int | No | After this timestamp (UTC seconds) |
| end | int | No | Before this timestamp (UTC seconds) |
| limit | int | No | Count (max 300, default 100) |

Supported periods (seconds): 1, 5, 10, 30, 60, 300, 900, 1800, 3600, 7200, 14400, 21600, 28800, 43200, 86400, 259200, 432000, 604800

```bash
python3 gate-dex-market/scripts/gate-api-call.py "market.candles" '{"chain_id":56,"token_address":"0x9dd3...","period":300,"limit":100}'
```

Response: Array of `{ts, o, h, l, c, vU}` (timestamp, open, high, low, close, volume USD).
