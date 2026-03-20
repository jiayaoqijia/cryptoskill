# DEX Discovery APIs

## Gainers and Losers

**Path:** `POST /v1/dex/gainer-loser/list`

**Description:** Get top gaining and losing DEX tokens by price change. Useful for finding momentum trades and market movers.

### Body Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| network_slug | string | No | Filter by network |
| platform_crypto_id | integer | No | Alternative network filter |
| type | string | No | Filter type (gainer, loser, all) default: all |
| time_period | string | No | Period for calculation (1h, 24h, 7d) default: 24h |
| sort | string | No | Sort field (percent_change, volume_24h, liquidity) |
| sort_dir | string | No | Sort direction (asc, desc) |
| start | integer | No | Pagination offset |
| limit | integer | No | Results per page (default: 100, max: 500) |
| min_liquidity | number | No | Minimum liquidity in USD |
| min_volume_24h | number | No | Minimum 24h volume in USD |
| min_market_cap | number | No | Minimum market cap in USD |

### Response Fields

| Field | Description |
|-------|-------------|
| tokens | Array of token objects |
| tokens[].id | Token CMC DEX ID |
| tokens[].name | Token name |
| tokens[].symbol | Token symbol |
| tokens[].contract_address | Contract address |
| tokens[].network_slug | Network identifier |
| tokens[].price | Current price |
| tokens[].percent_change_1h | 1-hour change % |
| tokens[].percent_change_24h | 24-hour change % |
| tokens[].percent_change_7d | 7-day change % |
| tokens[].volume_24h | 24-hour volume |
| tokens[].liquidity | Total liquidity |
| tokens[].market_cap | Market cap |
| tokens[].logo | Token logo URL |
| tokens[].type | gainer or loser |
| total_count | Total matching tokens |

### Example

```bash
# Get top 24h gainers with decent liquidity
curl -X POST "https://pro-api.coinmarketcap.com/v1/dex/gainer-loser/list" \
  -H "X-CMC_PRO_API_KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "gainer",
    "time_period": "24h",
    "sort": "percent_change",
    "sort_dir": "desc",
    "limit": 20,
    "min_liquidity": 50000,
    "min_volume_24h": 10000
  }'
```

```bash
# Get top losers on Solana
curl -X POST "https://pro-api.coinmarketcap.com/v1/dex/gainer-loser/list" \
  -H "X-CMC_PRO_API_KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "network_slug": "solana",
    "type": "loser",
    "time_period": "24h",
    "limit": 10
  }'
```

---

## Liquidity Change List

**Path:** `GET /v1/dex/liquidity-change/list`

**Description:** Get tokens with significant liquidity changes. Useful for detecting liquidity additions (bullish) or removals (potential rug pull).

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| network_slug | string | No | Filter by network |
| platform_crypto_id | integer | No | Alternative network filter |
| change_type | string | No | Filter by change (increase, decrease, all) |
| time_period | string | No | Period for calculation (1h, 24h, 7d) |
| sort | string | No | Sort field (liquidity_change, liquidity_change_percent) |
| sort_dir | string | No | Sort direction (asc, desc) |
| start | integer | No | Pagination offset |
| limit | integer | No | Results per page (default: 100, max: 500) |
| min_liquidity | number | No | Minimum current liquidity |
| min_change_percent | number | No | Minimum change percentage (absolute) |

### Response Fields

| Field | Description |
|-------|-------------|
| tokens | Array of token objects |
| tokens[].id | Token CMC DEX ID |
| tokens[].name | Token name |
| tokens[].symbol | Token symbol |
| tokens[].contract_address | Contract address |
| tokens[].network_slug | Network identifier |
| tokens[].price | Current price |
| tokens[].liquidity | Current liquidity |
| tokens[].liquidity_change | Absolute liquidity change |
| tokens[].liquidity_change_percent | Percentage liquidity change |
| tokens[].volume_24h | 24-hour volume |
| tokens[].change_type | increase or decrease |
| tokens[].logo | Token logo URL |
| total_count | Total matching tokens |

### Example

```bash
# Get tokens with biggest liquidity increases
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/liquidity-change/list?change_type=increase&time_period=24h&sort=liquidity_change_percent&sort_dir=desc&limit=20&min_liquidity=10000" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

```bash
# Detect potential rug pulls (large liquidity decreases)
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/liquidity-change/list?change_type=decrease&time_period=1h&sort=liquidity_change_percent&sort_dir=asc&limit=20&min_change_percent=20" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

---

## Meme Tokens List

**Path:** `POST /v1/dex/meme/list`

**Description:** Get a list of meme tokens trading on DEXs. Filtered for tokens tagged as meme coins with social signals.

### Body Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| network_slug | string | No | Filter by network |
| platform_crypto_id | integer | No | Alternative network filter |
| sort | string | No | Sort field (volume_24h, price_change_24h, liquidity, trending_score, market_cap) |
| sort_dir | string | No | Sort direction (asc, desc) |
| start | integer | No | Pagination offset |
| limit | integer | No | Results per page (default: 100, max: 500) |
| min_liquidity | number | No | Minimum liquidity in USD |
| min_volume_24h | number | No | Minimum 24h volume in USD |
| min_market_cap | number | No | Minimum market cap |

### Response Fields

| Field | Description |
|-------|-------------|
| tokens | Array of meme token objects |
| tokens[].id | Token CMC DEX ID |
| tokens[].name | Token name |
| tokens[].symbol | Token symbol |
| tokens[].contract_address | Contract address |
| tokens[].network_slug | Network identifier |
| tokens[].price | Current price |
| tokens[].percent_change_1h | 1-hour change % |
| tokens[].percent_change_24h | 24-hour change % |
| tokens[].percent_change_7d | 7-day change % |
| tokens[].volume_24h | 24-hour volume |
| tokens[].liquidity | Total liquidity |
| tokens[].market_cap | Market cap |
| tokens[].holders | Number of holders |
| tokens[].trending_score | Trending/social score |
| tokens[].logo | Token logo URL |
| tokens[].socials | Social media links |
| total_count | Total meme tokens |

### Example

```bash
# Get top meme coins by volume
curl -X POST "https://pro-api.coinmarketcap.com/v1/dex/meme/list" \
  -H "X-CMC_PRO_API_KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "sort": "volume_24h",
    "sort_dir": "desc",
    "limit": 50,
    "min_liquidity": 10000
  }'
```

```bash
# Get Solana meme coins sorted by trending score
curl -X POST "https://pro-api.coinmarketcap.com/v1/dex/meme/list" \
  -H "X-CMC_PRO_API_KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "network_slug": "solana",
    "sort": "trending_score",
    "sort_dir": "desc",
    "limit": 20
  }'
```

---

## New Tokens List

**Path:** `POST /v1/dex/new/list`

**Description:** Get newly discovered DEX tokens. Useful for finding new launches and early opportunities.

### Body Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| network_slug | string | No | Filter by network |
| platform_crypto_id | integer | No | Alternative network filter |
| time_period | string | No | How recent (1h, 6h, 24h, 7d) default: 24h |
| sort | string | No | Sort field (date_added, volume_24h, liquidity, price_change_24h) |
| sort_dir | string | No | Sort direction (asc, desc) |
| start | integer | No | Pagination offset |
| limit | integer | No | Results per page (default: 100, max: 500) |
| min_liquidity | number | No | Minimum liquidity in USD |
| min_volume_24h | number | No | Minimum 24h volume in USD |

### Response Fields

| Field | Description |
|-------|-------------|
| tokens | Array of new token objects |
| tokens[].id | Token CMC DEX ID |
| tokens[].name | Token name |
| tokens[].symbol | Token symbol |
| tokens[].contract_address | Contract address |
| tokens[].network_slug | Network identifier |
| tokens[].price | Current price |
| tokens[].percent_change_1h | 1-hour change % |
| tokens[].percent_change_24h | 24-hour change % |
| tokens[].volume_24h | 24-hour volume |
| tokens[].liquidity | Total liquidity |
| tokens[].market_cap | Market cap (if calculable) |
| tokens[].date_added | When first discovered |
| tokens[].age_hours | Hours since discovery |
| tokens[].pool_count | Number of liquidity pools |
| tokens[].logo | Token logo URL |
| total_count | Total new tokens |

### Example

```bash
# Get tokens launched in last 24 hours with decent liquidity
curl -X POST "https://pro-api.coinmarketcap.com/v1/dex/new/list" \
  -H "X-CMC_PRO_API_KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "time_period": "24h",
    "sort": "volume_24h",
    "sort_dir": "desc",
    "limit": 30,
    "min_liquidity": 5000
  }'
```

```bash
# Get newest tokens on Base chain
curl -X POST "https://pro-api.coinmarketcap.com/v1/dex/new/list" \
  -H "X-CMC_PRO_API_KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "network_slug": "base",
    "time_period": "6h",
    "sort": "date_added",
    "sort_dir": "desc",
    "limit": 20
  }'
```

```bash
# Find promising new launches (volume > liquidity suggests demand)
curl -X POST "https://pro-api.coinmarketcap.com/v1/dex/new/list" \
  -H "X-CMC_PRO_API_KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "time_period": "24h",
    "sort": "volume_24h",
    "sort_dir": "desc",
    "limit": 50,
    "min_liquidity": 10000,
    "min_volume_24h": 20000
  }'
```
