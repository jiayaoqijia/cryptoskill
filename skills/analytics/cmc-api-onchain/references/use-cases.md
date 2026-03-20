# Common Use Cases

This guide helps you choose the right endpoint and parameters for common DEX data goals.

## 1. Get DEX Token Price by Contract Address

**Goal:** Fetch the current price for a token using its contract address.

**Endpoint:** `GET /v1/dex/token/price`

**Steps:**
1. You need the network slug and contract address
2. Call the price endpoint directly

**Example:**
```bash
# Get PEPE price on Ethereum
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/token/price?network_slug=ethereum&contract_address=0x6982508145454Ce325dDbE47a25d4ec3d2311933" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `network_slug`, `contract_address`

---

## 2. Find a Token's Contract Address by Name

**Goal:** Look up a token's contract address when you only know its name or symbol.

**Endpoint:** `GET /v1/dex/search`

**Steps:**
1. Search by keyword (name or symbol)
2. Filter by network if needed
3. Get the contract_address from results

**Example:**
```bash
# Search for BONK token on Solana
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/search?keyword=BONK&network_slug=solana&search_type=token" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `keyword`, `network_slug`, `search_type`

**Watch out:** Multiple tokens may share the same name or symbol. Verify by checking liquidity and volume.

---

## 3. Get Prices for Multiple Tokens at Once

**Goal:** Fetch prices for several tokens in a single API call.

**Endpoint:** `POST /v1/dex/token/price/batch`

**Steps:**
1. Build an array of token objects with network and address
2. POST the request with JSON body

**Example:**
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

**Key parameters:** `tokens` array with `network_slug` and `contract_address`

---

## 4. Check Token Security Before Trading

**Goal:** Get risk analysis and security signals for a token.

**Endpoint:** `GET /v1/dex/security/detail`

**Steps:**
1. Call with network and contract address
2. Check `overall_risk_score` and `risk_level`
3. Review specific flags (honeypot, taxes, ownership)

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/security/detail?network_slug=ethereum&contract_address=0x6982508145454Ce325dDbE47a25d4ec3d2311933" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key checks:**
- `has_honeypot_risk`: If true, do not buy
- `buy_tax_percent` / `sell_tax_percent`: High taxes eat into profits
- `liquidity_lock.is_locked`: Locked liquidity is safer
- `ownership.is_renounced`: Renounced ownership reduces rug risk
- `top_10_percent`: High concentration is risky

---

## 5. Find Liquidity Pools for a Token

**Goal:** See which pools a token trades in and their liquidity.

**Endpoint:** `GET /v1/dex/token/pools`

**Steps:**
1. Call with network and contract address
2. Sort by liquidity or volume
3. Use for finding best trading venues

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/token/pools?network_slug=ethereum&contract_address=0x6982508145454Ce325dDbE47a25d4ec3d2311933&sort=liquidity&sort_dir=desc&limit=10" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `sort` (liquidity, volume_24h), `sort_dir`, `limit`

---

## 6. Find Trending DEX Tokens

**Goal:** Discover tokens gaining attention on DEXs.

**Endpoint:** `POST /v1/dex/tokens/trending/list`

**Steps:**
1. Optionally filter by network
2. Set minimum liquidity to filter out dust
3. Sort by volume or trending score

**Example:**
```bash
curl -X POST "https://pro-api.coinmarketcap.com/v1/dex/tokens/trending/list" \
  -H "X-CMC_PRO_API_KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "time_period": "24h",
    "sort": "volume_24h",
    "sort_dir": "desc",
    "limit": 20,
    "min_liquidity": 50000
  }'
```

**Key parameters:** `time_period`, `min_liquidity`, `min_volume_24h`

---

## 7. Find Today's Biggest DEX Gainers

**Goal:** Identify tokens with the highest price increase.

**Endpoint:** `POST /v1/dex/gainer-loser/list`

**Steps:**
1. Set `type: "gainer"` for gainers
2. Use `min_liquidity` to filter scams
3. Set time period (1h, 24h, 7d)

**Example:**
```bash
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

**Key parameters:** `type` (gainer, loser), `time_period`, `min_liquidity`

---

## 8. Find Newly Launched Tokens

**Goal:** Discover tokens recently added to DEXs.

**Endpoint:** `POST /v1/dex/new/list`

**Steps:**
1. Set time period for how recent (1h, 6h, 24h, 7d)
2. Filter by minimum liquidity
3. Sort by volume to find active ones

**Example:**
```bash
curl -X POST "https://pro-api.coinmarketcap.com/v1/dex/new/list" \
  -H "X-CMC_PRO_API_KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "time_period": "24h",
    "sort": "volume_24h",
    "sort_dir": "desc",
    "limit": 30,
    "min_liquidity": 10000
  }'
```

**Key parameters:** `time_period`, `min_liquidity`, `min_volume_24h`

---

## 9. Detect Potential Rug Pulls (Liquidity Removal)

**Goal:** Find tokens with significant liquidity decreases.

**Endpoint:** `GET /v1/dex/liquidity-change/list`

**Steps:**
1. Set `change_type: "decrease"`
2. Use short time period (1h) for early detection
3. Set minimum change percentage

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/liquidity-change/list?change_type=decrease&time_period=1h&sort=liquidity_change_percent&sort_dir=asc&limit=20&min_change_percent=20" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `change_type`, `time_period`, `min_change_percent`

---

## 10. Get Recent Trades for a Token

**Goal:** See real-time buy/sell activity.

**Endpoint:** `GET /v1/dex/tokens/transactions`

**Steps:**
1. Call with network and contract address
2. Optionally filter by transaction type (buy, sell)

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/tokens/transactions?network_slug=solana&contract_address=DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263&limit=50&tx_type=all" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `tx_type` (buy, sell, all), `limit`

---

## 11. Get Supported Networks and DEXs

**Goal:** Find valid network slugs and see what DEXs are tracked.

**Endpoint:** `GET /v1/dex/platform/list`

**Steps:**
1. Call to get all supported platforms
2. Use returned `slug` values as `network_slug` in other calls
3. Use returned `id` values as `platform_crypto_id`

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/dex/platform/list?sort=total_liquidity&sort_dir=desc&limit=20" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Common network slugs:** `ethereum`, `solana`, `bsc`, `arbitrum`, `base`, `polygon`

---

## 12. Get Meme Coins

**Goal:** List meme tokens trading on DEXs.

**Endpoint:** `POST /v1/dex/meme/list`

**Steps:**
1. Optionally filter by network
2. Sort by volume or trending score
3. Set minimum liquidity

**Example:**
```bash
curl -X POST "https://pro-api.coinmarketcap.com/v1/dex/meme/list" \
  -H "X-CMC_PRO_API_KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "network_slug": "solana",
    "sort": "trending_score",
    "sort_dir": "desc",
    "limit": 20,
    "min_liquidity": 10000
  }'
```

**Key parameters:** `network_slug`, `sort`, `min_liquidity`

---

## Quick Reference

| Goal | Endpoint | Method | Key Parameter |
|------|----------|--------|---------------|
| Token price by address | `/v1/dex/token/price` | GET | `contract_address` |
| Find token by name | `/v1/dex/search` | GET | `keyword` |
| Batch prices | `/v1/dex/token/price/batch` | POST | `tokens` array |
| Security check | `/v1/dex/security/detail` | GET | `contract_address` |
| Token pools | `/v1/dex/token/pools` | GET | `contract_address` |
| Trending tokens | `/v1/dex/tokens/trending/list` | POST | `min_liquidity` |
| Gainers/losers | `/v1/dex/gainer-loser/list` | POST | `type`, `time_period` |
| New tokens | `/v1/dex/new/list` | POST | `time_period` |
| Liquidity changes | `/v1/dex/liquidity-change/list` | GET | `change_type` |
| Recent trades | `/v1/dex/tokens/transactions` | GET | `tx_type` |
| Supported networks | `/v1/dex/platform/list` | GET | - |
| Meme coins | `/v1/dex/meme/list` | POST | `network_slug` |
