# Common Use Cases

This guide helps you choose the right endpoint and parameters for common exchange data goals.

## 1. Get Exchange Information by Name

**Goal:** Look up details about a specific exchange (logo, fees, URLs).

**Endpoint:** `GET /v1/exchange/info`

**Steps:**
1. Call with the exchange `slug` (e.g., "binance")
2. Or first get the ID from `/v1/exchange/map`, then call with `id`

**Example:**
```bash
# By slug (easier)
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/info?slug=binance" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Multiple exchanges
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/info?slug=binance,coinbase-exchange,kraken" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `slug` or `id`, `aux` for specific fields

---

## 2. Find an Exchange's CMC ID

**Goal:** Convert an exchange name to its CMC ID for use in other endpoints.

**Endpoint:** `GET /v1/exchange/map`

**Steps:**
1. Call with `slug` parameter
2. Use the returned `id` in other API calls

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/map?slug=binance" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `slug`, `listing_status` (active, inactive)

---

## 3. Get Top Exchanges by Volume

**Goal:** List exchanges ranked by trading volume.

**Endpoint:** `GET /v1/exchange/listings/latest`

**Steps:**
1. Set `sort=volume_24h` and `sort_dir=desc`
2. Use `limit` for number of results

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/listings/latest?limit=20&sort=volume_24h&sort_dir=desc" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `sort` (volume_24h, exchange_score), `sort_dir`, `limit`

---

## 4. Get Only Spot Exchanges (or Only Derivatives)

**Goal:** Filter exchanges by market type.

**Endpoint:** `GET /v1/exchange/listings/latest`

**Steps:**
1. Set `category` to filter (spot, derivatives, dex)

**Example:**
```bash
# Spot exchanges only
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/listings/latest?category=spot&limit=20" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Derivatives exchanges
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/listings/latest?category=derivatives&sort=exchange_score&limit=10" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `category` (spot, derivatives, dex, all)

---

## 5. Get Current Volume for a Specific Exchange

**Goal:** Fetch real-time volume metrics for one exchange.

**Endpoint:** `GET /v1/exchange/quotes/latest`

**Steps:**
1. Call with exchange `id` or `slug`
2. Response includes 24h, 7d, and 30d volumes

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/quotes/latest?slug=binance" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `slug` or `id`, `aux` for additional fields

---

## 6. Compare Volume Across Multiple Exchanges

**Goal:** Get volume data for several exchanges at once.

**Endpoint:** `GET /v1/exchange/quotes/latest`

**Steps:**
1. Pass multiple slugs or IDs comma-separated
2. Compare `volume_24h` across responses

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/quotes/latest?slug=binance,coinbase-exchange,kraken,okx" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** Multiple `slug` or `id` values

---

## 7. Get Historical Volume for an Exchange

**Goal:** Analyze volume trends over time.

**Endpoint:** `GET /v1/exchange/quotes/historical`

**Steps:**
1. Set `interval` (daily, weekly, hourly)
2. Use `count` or `time_start`/`time_end` for range

**Example:**
```bash
# Daily volume for last 30 days
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/quotes/historical?slug=binance&interval=daily&count=30" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Hourly for specific date range
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/quotes/historical?slug=binance&time_start=2024-01-01T00:00:00Z&time_end=2024-01-07T00:00:00Z&interval=hourly" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `interval`, `count`, `time_start`, `time_end`

**Note:** Historical data requires a paid plan.

---

## 8. Get All Trading Pairs on an Exchange

**Goal:** List all cryptocurrencies traded on an exchange.

**Endpoint:** `GET /v1/exchange/market-pairs/latest`

**Steps:**
1. Call with exchange `id` or `slug`
2. Use `category` to filter spot vs derivatives

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/market-pairs/latest?slug=binance&limit=100&category=spot" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `category`, `limit`, pagination with `start`

---

## 9. Find BTC Pairs on an Exchange

**Goal:** Get all trading pairs for a specific cryptocurrency.

**Endpoint:** `GET /v1/exchange/market-pairs/latest`

**Steps:**
1. Use `matched_symbol` for symbol or `matched_id` for CMC ID
2. Returns all pairs containing that asset

**Example:**
```bash
# All BTC pairs on Coinbase
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/market-pairs/latest?slug=coinbase-exchange&matched_symbol=BTC" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# ETH pairs by CMC ID
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/market-pairs/latest?slug=binance&matched_id=1027" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `matched_symbol` or `matched_id`

---

## 10. Get Perpetual/Futures Pairs on an Exchange

**Goal:** List derivatives trading pairs.

**Endpoint:** `GET /v1/exchange/market-pairs/latest`

**Steps:**
1. Set `category=perpetual` or `category=futures`

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/market-pairs/latest?slug=binance&category=perpetual&limit=50" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `category` (perpetual, futures, options)

---

## 11. Check Exchange Reserves (Proof-of-Reserves)

**Goal:** View cryptocurrency holdings for an exchange.

**Endpoint:** `GET /v1/exchange/assets`

**Steps:**
1. Call with exchange `slug` or `id`
2. Response shows wallet addresses and balances

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/assets?slug=binance" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `slug` or `id`

**Note:** Not all exchanges provide proof-of-reserves data.

---

## 12. Find Exchanges That List a Specific Coin

**Goal:** Discover which exchanges trade a particular cryptocurrency.

**Endpoint:** `GET /v1/exchange/map`

**Steps:**
1. Use `crypto_id` parameter with the coin's CMC ID

**Example:**
```bash
# Find exchanges that list Bitcoin (ID: 1)
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/map?crypto_id=1" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `crypto_id`

---

## Quick Reference

| Goal | Endpoint | Key Parameter |
|------|----------|---------------|
| Exchange info | `/v1/exchange/info` | `slug` or `id` |
| Name to ID | `/v1/exchange/map` | `slug` |
| Top exchanges | `/v1/exchange/listings/latest` | `sort=volume_24h` |
| Spot/derivatives only | `/v1/exchange/listings/latest` | `category` |
| Current volume | `/v1/exchange/quotes/latest` | `slug` or `id` |
| Compare volumes | `/v1/exchange/quotes/latest` | Multiple `slug` values |
| Historical volume | `/v1/exchange/quotes/historical` | `interval`, `count` |
| All trading pairs | `/v1/exchange/market-pairs/latest` | `slug`, `category` |
| Find BTC pairs | `/v1/exchange/market-pairs/latest` | `matched_symbol=BTC` |
| Perpetual pairs | `/v1/exchange/market-pairs/latest` | `category=perpetual` |
| Exchange reserves | `/v1/exchange/assets` | `slug` or `id` |
| Exchanges for coin | `/v1/exchange/map` | `crypto_id` |
