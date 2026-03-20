# DEX Token APIs

## Table of Contents

1. [Token Details](#token-details)
2. [Token Price](#token-price)
3. [Batch Token Prices](#batch-token-prices)
4. [Token Pools](#token-pools)
5. [Token Liquidity Query](#token-liquidity-query)
6. [Batch Token Query](#batch-token-query)
7. [Token Transactions](#token-transactions)
8. [Trending Tokens](#trending-tokens)

---

## Token Details

**Path:** `GET /v1/dex/token`

**Description:** Get detailed information about a specific DEX token by its contract address and network.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| network_slug | string | Yes* | Network identifier (e.g., ethereum, solana, bsc) |
| platform_crypto_id | integer | Yes* | Alternative to network_slug, use platform's CMC ID |
| contract_address | string | Yes | Token's contract address on the network |

*One of network_slug or platform_crypto_id is required.

### Response Fields

| Field | Description |
|-------|-------------|
| id | CMC DEX token ID |
| name | Token name |
| symbol | Token ticker symbol |
| contract_address | On-chain contract address |
| platform | Network/blockchain info |
| total_supply | Total token supply |
| circulating_supply | Circulating supply |
| market_cap | Market capitalization |
| fully_diluted_market_cap | FDV based on total supply |
| price | Current price in USD |
| volume_24h | 24-hour trading volume |
| percent_change_1h | 1-hour price change % |
| percent_change_24h | 24-hour price change % |
| percent_change_7d | 7-day price change % |
| logo | Token logo URL |
| description | Token description |
| date_added | When token was first tracked |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/token?network_slug=ethereum&contract_address=0x6982508145454Ce325dDbE47a25d4ec3d2311933" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

---

## Token Price

**Path:** `GET /v1/dex/token/price`

**Description:** Get the latest DEX price for a specific token. Faster than full token details when you only need price.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| network_slug | string | Yes* | Network identifier |
| platform_crypto_id | integer | Yes* | Alternative to network_slug |
| contract_address | string | Yes | Token's contract address |

### Response Fields

| Field | Description |
|-------|-------------|
| price | Current USD price |
| price_quote | Price in quote token (if applicable) |
| percent_change_1h | 1-hour change % |
| percent_change_24h | 24-hour change % |
| percent_change_7d | 7-day change % |
| volume_24h | 24-hour volume |
| last_updated | Timestamp of last update |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/token/price?network_slug=solana&contract_address=DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

---

## Batch Token Prices

**Path:** `POST /v1/dex/token/price/batch`

**Description:** Get prices for multiple tokens in a single request. More efficient than multiple single calls.

### Body Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| tokens | array | Yes | Array of token objects |
| tokens[].network_slug | string | Yes* | Network identifier |
| tokens[].platform_crypto_id | integer | Yes* | Alternative to network_slug |
| tokens[].contract_address | string | Yes | Token's contract address |

### Response Fields

| Field | Description |
|-------|-------------|
| prices | Array of price objects for each requested token |
| prices[].contract_address | Token address |
| prices[].network_slug | Network of the token |
| prices[].price | Current USD price |
| prices[].percent_change_24h | 24-hour change % |
| prices[].volume_24h | 24-hour volume |

### Example

```bash
curl -X POST "https://pro-api.coinmarketcap.com/v1/dex/token/price/batch" \
  -H "X-CMC_PRO_API_KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "tokens": [
      {"network_slug": "ethereum", "contract_address": "0x6982508145454Ce325dDbE47a25d4ec3d2311933"},
      {"network_slug": "solana", "contract_address": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"}
    ]
  }'
```

---

## Token Pools

**Path:** `GET /v1/dex/token/pools`

**Description:** Get all liquidity pools that include a specific token. Useful for finding trading venues and liquidity depth.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| network_slug | string | Yes* | Network identifier |
| platform_crypto_id | integer | Yes* | Alternative to network_slug |
| contract_address | string | Yes | Token's contract address |
| start | integer | No | Pagination offset (default: 1) |
| limit | integer | No | Results per page (default: 100, max: 1000) |
| sort | string | No | Sort field (liquidity, volume_24h) |
| sort_dir | string | No | Sort direction (asc, desc) |

### Response Fields

| Field | Description |
|-------|-------------|
| pools | Array of liquidity pool objects |
| pools[].pool_address | Pool contract address |
| pools[].dex_name | DEX name (Uniswap, Raydium, etc.) |
| pools[].dex_slug | DEX identifier |
| pools[].base_token | Base token info |
| pools[].quote_token | Quote token info |
| pools[].liquidity | Total liquidity in USD |
| pools[].volume_24h | 24-hour volume |
| pools[].fee_tier | Pool fee percentage |
| pools[].price | Current price |
| total_count | Total pools available |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/token/pools?network_slug=ethereum&contract_address=0x6982508145454Ce325dDbE47a25d4ec3d2311933&sort=liquidity&sort_dir=desc&limit=10" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

---

## Token Liquidity Query

**Path:** `GET /v1/dex/token-liquidity/query`

**Description:** Get historical liquidity data for a token over time. Useful for analyzing liquidity trends.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| network_slug | string | Yes* | Network identifier |
| platform_crypto_id | integer | Yes* | Alternative to network_slug |
| contract_address | string | Yes | Token's contract address |
| time_period | string | No | Time range (1h, 24h, 7d, 30d, 90d, 1y) |
| interval | string | No | Data interval (5m, 1h, 1d) |

### Response Fields

| Field | Description |
|-------|-------------|
| liquidity_history | Array of liquidity data points |
| liquidity_history[].timestamp | Data point timestamp |
| liquidity_history[].liquidity | Total liquidity in USD |
| liquidity_history[].liquidity_change | Change from previous period |
| current_liquidity | Current total liquidity |
| liquidity_change_24h | 24-hour liquidity change % |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/token-liquidity/query?network_slug=ethereum&contract_address=0x6982508145454Ce325dDbE47a25d4ec3d2311933&time_period=7d&interval=1h" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

---

## Batch Token Query

**Path:** `POST /v1/dex/tokens/batch-query`

**Description:** Get metadata for multiple tokens in a single request. Returns full token details, not just prices.

### Body Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| tokens | array | Yes | Array of token identifiers |
| tokens[].network_slug | string | Yes* | Network identifier |
| tokens[].platform_crypto_id | integer | Yes* | Alternative to network_slug |
| tokens[].contract_address | string | Yes | Token's contract address |

### Response Fields

| Field | Description |
|-------|-------------|
| tokens | Array of full token objects |
| tokens[].id | CMC DEX token ID |
| tokens[].name | Token name |
| tokens[].symbol | Token symbol |
| tokens[].contract_address | Contract address |
| tokens[].platform | Network info |
| tokens[].price | Current price |
| tokens[].market_cap | Market cap |
| tokens[].volume_24h | 24-hour volume |
| tokens[].total_supply | Total supply |
| tokens[].logo | Logo URL |

### Example

```bash
curl -X POST "https://pro-api.coinmarketcap.com/v1/dex/tokens/batch-query" \
  -H "X-CMC_PRO_API_KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "tokens": [
      {"network_slug": "ethereum", "contract_address": "0x6982508145454Ce325dDbE47a25d4ec3d2311933"},
      {"network_slug": "ethereum", "contract_address": "0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE"}
    ]
  }'
```

---

## Token Transactions

**Path:** `GET /v1/dex/tokens/transactions`

**Description:** Get recent DEX transactions for a specific token. Shows buys, sells, and swaps.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| network_slug | string | Yes* | Network identifier |
| platform_crypto_id | integer | Yes* | Alternative to network_slug |
| contract_address | string | Yes | Token's contract address |
| start | integer | No | Pagination offset (default: 1) |
| limit | integer | No | Results per page (default: 100, max: 500) |
| tx_type | string | No | Filter by type (buy, sell, all) |

### Response Fields

| Field | Description |
|-------|-------------|
| transactions | Array of transaction objects |
| transactions[].tx_hash | Transaction hash |
| transactions[].block_number | Block number |
| transactions[].timestamp | Transaction timestamp |
| transactions[].tx_type | Transaction type (buy/sell) |
| transactions[].maker_address | Wallet that initiated |
| transactions[].token_amount | Amount of tokens traded |
| transactions[].quote_amount | Amount in quote currency |
| transactions[].price | Price at transaction |
| transactions[].usd_value | USD value of transaction |
| transactions[].dex_name | DEX where trade occurred |
| transactions[].pool_address | Pool used for trade |
| total_count | Total transactions available |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/tokens/transactions?network_slug=solana&contract_address=DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263&limit=50&tx_type=all" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

---

## Trending Tokens

**Path:** `POST /v1/dex/tokens/trending/list`

**Description:** Get trending DEX tokens based on various metrics like volume, price change, or social activity.

### Body Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| network_slug | string | No | Filter by network |
| platform_crypto_id | integer | No | Alternative network filter |
| time_period | string | No | Trending period (1h, 6h, 24h) |
| sort | string | No | Sort by (volume_24h, price_change, trending_score) |
| sort_dir | string | No | Sort direction (asc, desc) |
| start | integer | No | Pagination offset |
| limit | integer | No | Results per page (default: 100, max: 500) |
| min_liquidity | number | No | Minimum liquidity filter |
| min_volume_24h | number | No | Minimum 24h volume filter |

### Response Fields

| Field | Description |
|-------|-------------|
| tokens | Array of trending token objects |
| tokens[].id | CMC DEX token ID |
| tokens[].name | Token name |
| tokens[].symbol | Token symbol |
| tokens[].contract_address | Contract address |
| tokens[].network_slug | Network identifier |
| tokens[].price | Current price |
| tokens[].percent_change_1h | 1-hour change % |
| tokens[].percent_change_24h | 24-hour change % |
| tokens[].volume_24h | 24-hour volume |
| tokens[].liquidity | Total liquidity |
| tokens[].trending_score | Trending score |
| tokens[].market_cap | Market cap |
| tokens[].logo | Logo URL |
| total_count | Total trending tokens |

### Example

```bash
curl -X POST "https://pro-api.coinmarketcap.com/v1/dex/tokens/trending/list" \
  -H "X-CMC_PRO_API_KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "network_slug": "solana",
    "time_period": "24h",
    "sort": "volume_24h",
    "sort_dir": "desc",
    "limit": 20,
    "min_liquidity": 10000
  }'
```
