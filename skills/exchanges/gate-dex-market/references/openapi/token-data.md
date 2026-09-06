# Market OpenAPI: Token Data Actions (base.token.*)

> 6 actions for token information, rankings, discovery, security, and holders.

---

## Action 1: base.token.swap_list

Query tradable tokens on a chain. Supports filtering by favorites, recommendations, search.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| chain_id | string | No | Chain ID (1=ETH, 501=SOL, etc.). Omit for all chains |
| tag | string | No | `"favorite"` or `"recommend"`. Omit for normal list |
| wallet | string | No | Wallet address (comma-separated) for favorites/balance |
| search | string | No | Token symbol or contract address |
| search_auth | string | No | `"true"` = verified tokens only |

```bash
python3 gate-dex-market/scripts/gate-api-call.py "base.token.swap_list" '{"chain_id":"1","search":"USDT","search_auth":"true"}'
```

---

## Action 2: base.token.get_base_info

Get token name, symbol, logo, decimals.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| chain_id | string | Yes | Chain ID |
| token_address | string | Yes | Contract address |

```bash
python3 gate-dex-market/scripts/gate-api-call.py "base.token.get_base_info" '{"chain_id":"1","token_address":"0x382bb369d343125bfb2117af9c149795c6c65c52"}'
```

---

## Action 3: base.token.ranking

Universal token ranking. Sort by any trend field with pagination.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| chain_id | object | No | Filter: `{"eq":"56"}` or `{"in":["1","501"]}` |
| sort | object[] | Yes | `[{"field":"trend_info.price_change_24h","order":"desc"}]` |
| limit | int | Yes | Count (default 10) |
| cursor | string | No | Pagination cursor |

Sort fields: `trend_info.price_change_24h`, `trend_info.volume_24h`, `trend_info.tx_count_24h`, `liquidity`, `holder_count`, `total_supply`

```bash
python3 gate-dex-market/scripts/gate-api-call.py "base.token.ranking" '{"chain_id":{"eq":"56"},"sort":[{"field":"trend_info.volume_24h","order":"desc"}],"limit":5}'
```

---

## Action 4: base.token.range_by_created_at

Discover new tokens by creation time range. Sorted by `created_at DESC`.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| start | string | Yes | RFC3339, e.g. `"2025-03-01T00:00:00Z"` |
| end | string | Yes | RFC3339 |
| chain_id | string | No | Filter chain |
| limit | string | No | 1-100 (default 20) |

```bash
python3 gate-dex-market/scripts/gate-api-call.py "base.token.range_by_created_at" '{"start":"2025-03-01T00:00:00Z","end":"2025-03-07T00:00:00Z","chain_id":"501","limit":"10"}'
```

---

## Action 5: base.token.risk_infos

Security audit: risk items, buy/sell tax, holder concentration.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| chain_id | string | Yes | Chain ID |
| address | string | Yes | Token contract address |
| lan | string | No | Language (`en`, `zh`) |
| ignore | string | No | `"true"` = hide empty risk items |

```bash
python3 gate-dex-market/scripts/gate-api-call.py "base.token.risk_infos" '{"chain_id":"56","address":"0x55d398...","lan":"en","ignore":"true"}'
```

Key response fields: `high_risk_num`, `middle_risk_num`, `low_risk_num`, `tax_analysis.token_tax.buy_tax/sell_tax`, `data_analysis.top10_percent`.

**Warning triggers**: High risk count > 0, buy/sell tax > 10% (honeypot indicator), top10 concentration > 80%.

---

## Action 6: base.token.get_holder_topn

Top N holders with wallet addresses and amounts.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| chain_id | string | Yes | Chain ID |
| token_address | string | Yes | Contract address |

```bash
python3 gate-dex-market/scripts/gate-api-call.py "base.token.get_holder_topn" '{"chain_id":"1","token_address":"0xdAC17F958D2ee523a2206206994597C13D831ec7"}'
```

Returns `holders[]` with `wallet` and `amount` (raw precision). Convert using token's `decimal` from `get_base_info`.
