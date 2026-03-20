# Common Use Cases

This guide helps you choose the right endpoint and parameters for common market-wide data goals.

## Table of Contents

1. [Get Current Market Sentiment](#1-get-current-market-sentiment-fear--greed)
2. [Get Total Crypto Market Cap](#2-get-total-crypto-market-cap)
3. [Get BTC Dominance](#3-get-btc-dominance)
4. [Track Market Cap History](#4-track-market-cap-history)
5. [Track Fear & Greed History](#5-track-fear--greed-history)
6. [Get CMC100 Index Performance](#6-get-cmc100-index-performance)
7. [Compare CMC100 vs CMC20](#7-compare-cmc100-vs-cmc20)
8. [Get OHLCV Candlestick Data](#8-get-ohlcv-candlestick-data-for-charts)
9. [Get Simple Price Time Series](#9-get-simple-price-time-series-no-ohlcv)
10. [Get Community Trending Tokens](#10-get-community-trending-tokens)
11. [Get Trending Discussion Topics](#11-get-trending-discussion-topics)
12. [Get Latest Crypto News](#12-get-latest-crypto-news)
13. [Convert Currency Amounts](#13-convert-currency-amounts)
14. [Check API Usage and Limits](#14-check-api-usage-and-limits)
15. [Get Fiat Currency IDs](#15-get-fiat-currency-ids)
16. [Quick Reference](#quick-reference)

---

## 1. Get Current Market Sentiment (Fear & Greed)

**Goal:** Check if the market is in fear or greed.

**Endpoint:** `GET /v3/fear-and-greed/latest`

**Steps:**
1. Call the endpoint (no parameters needed)
2. Check `value` (0-100) and `value_classification`

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v3/fear-and-greed/latest" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Value interpretation:**
- 0-24: Extreme Fear (potential buying opportunity)
- 25-44: Fear
- 45-55: Neutral
- 56-75: Greed
- 76-100: Extreme Greed (potential market top)

---

## 2. Get Total Crypto Market Cap

**Goal:** Fetch the current total market capitalization.

**Endpoint:** `GET /v1/global-metrics/quotes/latest`

**Steps:**
1. Call the endpoint
2. Read `quote.USD.total_market_cap`

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key fields:** `total_market_cap`, `total_volume_24h`, `btc_dominance`, `eth_dominance`

---

## 3. Get BTC Dominance

**Goal:** Check Bitcoin's share of total market cap.

**Endpoint:** `GET /v1/global-metrics/quotes/latest`

**Steps:**
1. Call the endpoint
2. Read `btc_dominance` (percentage)

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Related fields:** `btc_dominance_24h_percentage_change`, `eth_dominance`

---

## 4. Track Market Cap History

**Goal:** Analyze total market cap over time.

**Endpoint:** `GET /v1/global-metrics/quotes/historical`

**Steps:**
1. Set `interval` (daily, weekly, etc.)
2. Use `count` or date range parameters

**Example:**
```bash
# Daily market cap for last 30 days
curl -X GET "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/historical?interval=daily&count=30" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `interval`, `count`, `time_start`, `time_end`

---

## 5. Track Fear & Greed History

**Goal:** Analyze sentiment changes over time.

**Endpoint:** `GET /v3/fear-and-greed/historical`

**Steps:**
1. Set `limit` for number of days
2. Optionally set `start` timestamp

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v3/fear-and-greed/historical?limit=30" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `limit`, `start`

---

## 6. Get CMC100 Index Performance

**Goal:** Track the top 100 cryptocurrencies as an index.

**Endpoint:** `GET /v3/index/cmc100-latest`

**Steps:**
1. Call the endpoint (no parameters needed)
2. Response includes price, volume, and percent changes

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v3/index/cmc100-latest" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key fields:** `price`, `percent_change_24h`, `percent_change_7d`, `market_cap`

---

## 7. Compare CMC100 vs CMC20

**Goal:** Compare broad market (100) vs large-cap (20) performance.

**Endpoints:**
- `GET /v3/index/cmc100-latest`
- `GET /v3/index/cmc20-latest`

**Steps:**
1. Call both endpoints
2. Compare `percent_change_24h` or `percent_change_7d`
3. CMC20 outperforming = large caps leading; CMC100 outperforming = mid/small caps rallying

**Example:**
```bash
# Get both in parallel
curl -X GET "https://pro-api.coinmarketcap.com/v3/index/cmc100-latest" -H "X-CMC_PRO_API_KEY: your-api-key"
curl -X GET "https://pro-api.coinmarketcap.com/v3/index/cmc20-latest" -H "X-CMC_PRO_API_KEY: your-api-key"
```

---

## 8. Get OHLCV Candlestick Data for Charts

**Goal:** Build price charts with candlestick data.

**Endpoint:** `GET /v1/k-line/candles`

**Steps:**
1. Set `id` or `symbol` for the cryptocurrency
2. Choose `interval` (1h, 4h, 1d, etc.)
3. Set `count` for number of candles

**Example:**
```bash
# 24 hourly candles for Bitcoin
curl -X GET "https://pro-api.coinmarketcap.com/v1/k-line/candles?id=1&interval=1h&count=24" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Daily candles for ETH
curl -X GET "https://pro-api.coinmarketcap.com/v1/k-line/candles?symbol=ETH&interval=1d&count=30" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `id`/`symbol`, `interval`, `count`

---

## 9. Get Simple Price Time Series (No OHLCV)

**Goal:** Get price points for line charts.

**Endpoint:** `GET /v1/k-line/points`

**Steps:**
1. Set `id` or `symbol`
2. Choose `interval` and `count`
3. Use `metrics` to specify what data you need

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/k-line/points?id=1&interval=1h&count=24&metrics=price,market_cap" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `metrics` (price, market_cap, volume)

---

## 10. Get Community Trending Tokens

**Goal:** See what tokens the community is talking about.

**Endpoint:** `GET /v1/community/trending/token`

**Steps:**
1. Set `time_period` (24h, 7d, 30d)
2. Set `limit` for number of results

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/community/trending/token?limit=10&time_period=24h" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key fields:** `trending_score`, `mention_count`, `sentiment_score`

---

## 11. Get Trending Discussion Topics

**Goal:** See what themes the community is discussing.

**Endpoint:** `GET /v1/community/trending/topic`

**Steps:**
1. Set `time_period` and `limit`
2. Response includes related tokens for each topic

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/community/trending/topic?limit=10&time_period=24h" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key fields:** `trending_score`, `post_count`, `related_tokens`

---

## 12. Get Latest Crypto News

**Goal:** Fetch recent news articles.

**Endpoint:** `GET /v1/content/latest`

**Steps:**
1. Set `content_type=news` for news only
2. Optionally filter by `category` or cryptocurrency `id`

**Example:**
```bash
# Latest news
curl -X GET "https://pro-api.coinmarketcap.com/v1/content/latest?content_type=news&limit=10" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# News about Bitcoin
curl -X GET "https://pro-api.coinmarketcap.com/v1/content/latest?content_type=news&id=1&limit=10" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `content_type`, `category`, `id`/`slug`

---

## 13. Convert Currency Amounts

**Goal:** Convert between crypto and fiat currencies.

**Endpoint:** `GET /v2/tools/price-conversion`

**Steps:**
1. Set `amount` to convert
2. Set source currency with `id` or `symbol`
3. Set target currency with `convert`

**Example:**
```bash
# Convert 1 BTC to USD and EUR
curl -X GET "https://pro-api.coinmarketcap.com/v2/tools/price-conversion?amount=1&symbol=BTC&convert=USD,EUR" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Convert 1000 USD to BTC
curl -X GET "https://pro-api.coinmarketcap.com/v2/tools/price-conversion?amount=1000&id=2781&convert=BTC" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key parameters:** `amount`, `symbol`/`id`, `convert`

---

## 14. Check API Usage and Limits

**Goal:** Monitor your API credit consumption.

**Endpoint:** `GET /v1/key/info`

**Steps:**
1. Call the endpoint (no parameters)
2. Check `usage.current_day.credits_left`

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/key/info" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Key fields:** `credits_used`, `credits_left`, `rate_limit_minute`

---

## 15. Get Fiat Currency IDs

**Goal:** Find CMC IDs for fiat currencies to use in conversions.

**Endpoint:** `GET /v1/fiat/map`

**Steps:**
1. Call to get all fiat currencies
2. Use returned `id` values in other API calls

**Example:**
```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/fiat/map?limit=20" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

**Common fiat IDs:** USD=2781, EUR=2790, GBP=2791, JPY=2792

---

## Quick Reference

| Goal | Endpoint | Key Parameter |
|------|----------|---------------|
| Fear & Greed | `/v3/fear-and-greed/latest` | - |
| Total market cap | `/v1/global-metrics/quotes/latest` | - |
| BTC dominance | `/v1/global-metrics/quotes/latest` | - |
| Market cap history | `/v1/global-metrics/quotes/historical` | `interval`, `count` |
| Fear & Greed history | `/v3/fear-and-greed/historical` | `limit` |
| CMC100 index | `/v3/index/cmc100-latest` | - |
| CMC20 index | `/v3/index/cmc20-latest` | - |
| OHLCV candles | `/v1/k-line/candles` | `id`, `interval` |
| Price time series | `/v1/k-line/points` | `id`, `metrics` |
| Trending tokens | `/v1/community/trending/token` | `time_period` |
| Trending topics | `/v1/community/trending/topic` | `time_period` |
| Latest news | `/v1/content/latest` | `content_type` |
| Convert currency | `/v2/tools/price-conversion` | `amount`, `convert` |
| API usage | `/v1/key/info` | - |
| Fiat currency IDs | `/v1/fiat/map` | - |
