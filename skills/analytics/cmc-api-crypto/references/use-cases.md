# Common Use Cases

This guide helps you choose the right endpoint and parameters for common goals.

## 1. Get the Current Price of a Token

**Goal:** Fetch the latest price for a specific cryptocurrency.

**Endpoint:** `/v2/cryptocurrency/quotes/latest`

**Steps:**
1. If you have the CMC ID, call directly with `id` parameter
2. If you only have the symbol, use `symbol` parameter (but note: symbols can collide)
3. For tokens, you can also use the contract address via `/v2/cryptocurrency/info` first

**Example:**
```bash
# By ID (most reliable)
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?id=1" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# By symbol (may return multiple if symbol collides)
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?symbol=BTC" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `id`, `symbol`, `convert` (for different quote currencies)

---

## 2. Find a Token's CMC ID from Symbol or Name

**Goal:** Convert a symbol like "ETH" or name like "Ethereum" to a CMC ID for use in other endpoints.

**Endpoint:** `/v1/cryptocurrency/map`

**Steps:**
1. Call with `symbol` parameter
2. If multiple results return (symbol collision), verify by `name` or `rank`
3. Cache the result since IDs are stable

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map?symbol=ETH" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `symbol`, `listing_status` (use `active` for current coins only)

**Watch out:** Symbols like "USDT" exist on multiple chains. The map returns all of them. Pick the one with the highest rank or check the `platform` field.

---

## 3. Get a Token by Contract Address

**Goal:** Look up a token when you only have its contract address (e.g., from a blockchain transaction).

**Endpoint:** `/v2/cryptocurrency/info`

**Steps:**
1. Call with the `address` parameter
2. Response includes the CMC ID you can use for other endpoints

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/info?address=0xdac17f958d2ee523a2206206994597c13d831ec7" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `address`

---

## 4. Get the Top 100 Coins by Market Cap

**Goal:** Fetch a ranked list of the largest cryptocurrencies.

**Endpoint:** `/v1/cryptocurrency/listings/latest`

**Steps:**
1. Call with `limit=100` and `sort=market_cap`
2. Default sort direction is descending (largest first)

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit=100&sort=market_cap" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `limit`, `sort`, `sort_dir`

---

## 5. Find Coins in a Price Range

**Goal:** Filter cryptocurrencies by price (e.g., all coins under $1).

**Endpoint:** `/v1/cryptocurrency/listings/latest`

**Steps:**
1. Use `price_min` and `price_max` parameters
2. Combine with `market_cap_min` to filter out dust coins

**Example:**
```bash
# Coins between $0.10 and $1.00 with at least $10M market cap
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?price_min=0.1&price_max=1&market_cap_min=10000000&limit=100" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `price_min`, `price_max`, `market_cap_min`, `volume_24h_min`

---

## 6. Get Historical Price at a Specific Date

**Goal:** Find what a coin's price was on a specific day.

**Endpoint:** `/v3/cryptocurrency/quotes/historical`

**Steps:**
1. Set `time_start` and `time_end` to the same day
2. Use `interval=daily` for day-level precision

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v3/cryptocurrency/quotes/historical?id=1&time_start=2024-01-01&time_end=2024-01-01&interval=daily" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `time_start`, `time_end`, `interval`

**Note:** Historical data requires a paid plan. Free tier has limited access.

---

## 7. Build a Price Chart (OHLCV Data)

**Goal:** Get candlestick data for charting.

**Endpoint:** `/v2/cryptocurrency/ohlcv/historical`

**Steps:**
1. Choose your interval (hourly, daily, weekly)
2. Set time range or count
3. Response includes open, high, low, close, volume for each period

**Example:**
```bash
# Daily candles for last 30 days
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/ohlcv/historical?id=1&interval=daily&count=30" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Hourly candles for a specific week
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/ohlcv/historical?id=1&time_start=2024-01-01&time_end=2024-01-07&interval=hourly" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `interval`, `count`, `time_start`, `time_end`

---

## 8. Find Where a Coin Trades

**Goal:** Get all exchanges and trading pairs for a cryptocurrency.

**Endpoint:** `/v2/cryptocurrency/market-pairs/latest`

**Steps:**
1. Call with the coin's CMC ID
2. Sort by `volume_24h_strict` for most liquid pairs first
3. Filter by `category=spot` or `category=derivatives` as needed

**Example:**
```bash
# All BTC trading pairs sorted by volume
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/market-pairs/latest?id=1&sort=volume_24h_strict&limit=50" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Only spot pairs
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/market-pairs/latest?id=1&category=spot&limit=50" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `sort`, `category`, `matched_symbol` (to find specific pairs like BTC/USDT)

---

## 9. Get All-Time High and Distance from ATH

**Goal:** Find a coin's ATH and calculate how far current price is from it.

**Endpoint:** `/v2/cryptocurrency/price-performance-stats/latest`

**Steps:**
1. Call with `time_period=all_time`
2. ATH is in `periods.all_time.quote.USD.high`
3. Calculate: `(current - ATH) / ATH * 100` for % from ATH

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/price-performance-stats/latest?id=1&time_period=all_time" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `time_period` (all_time, 24h, 7d, 30d, 90d, 365d, ytd)

---

## 10. Find Today's Biggest Gainers

**Goal:** Identify coins with the highest price increase.

**Endpoint:** `/v1/cryptocurrency/trending/gainers-losers`

**Steps:**
1. Use `sort_dir=desc` for gainers
2. Set `time_period` to your desired timeframe

**Example:**
```bash
# Top 20 gainers in last 24h
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/trending/gainers-losers?limit=20&time_period=24h&sort_dir=desc" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Top losers (use sort_dir=asc)
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/trending/gainers-losers?limit=20&time_period=24h&sort_dir=asc" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `time_period` (1h, 24h, 7d, 30d), `sort_dir`, `limit`

---

## 11. Discover Newly Listed Coins

**Goal:** Find cryptocurrencies recently added to CoinMarketCap.

**Endpoint:** `/v1/cryptocurrency/listings/new`

**Steps:**
1. Call with desired limit
2. Results are sorted by date added (newest first)

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/new?limit=50" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `limit`, `sort_dir`

---

## 12. Get All DeFi Tokens

**Goal:** List all tokens in the DeFi category.

**Endpoint:** `/v1/cryptocurrency/category`

**Steps:**
1. First get the category ID from `/v1/cryptocurrency/categories`
2. Then call `/v1/cryptocurrency/category` with that ID

**Example:**
```bash
# Step 1: Find DeFi category ID
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/categories?limit=100" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Step 2: Get tokens in that category (example ID)
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/category?id=6051a82566fc1b42617d6dc6&limit=100" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `id` (category ID), `limit`

---

## Quick Reference

| Goal | Endpoint | Key Parameter |
|------|----------|---------------|
| Current price | `/v2/cryptocurrency/quotes/latest` | `id` or `symbol` |
| Symbol to ID | `/v1/cryptocurrency/map` | `symbol` |
| Contract to ID | `/v2/cryptocurrency/info` | `address` |
| Top coins | `/v1/cryptocurrency/listings/latest` | `sort=market_cap` |
| Price filter | `/v1/cryptocurrency/listings/latest` | `price_min`, `price_max` |
| Historical price | `/v3/cryptocurrency/quotes/historical` | `time_start`, `time_end` |
| OHLCV chart data | `/v2/cryptocurrency/ohlcv/historical` | `interval`, `count` |
| Trading pairs | `/v2/cryptocurrency/market-pairs/latest` | `id`, `category` |
| ATH/ATL | `/v2/cryptocurrency/price-performance-stats/latest` | `time_period=all_time` |
| Gainers/losers | `/v1/cryptocurrency/trending/gainers-losers` | `sort_dir`, `time_period` |
| New listings | `/v1/cryptocurrency/listings/new` | `limit` |
| By category | `/v1/cryptocurrency/category` | `id` (category ID) |
