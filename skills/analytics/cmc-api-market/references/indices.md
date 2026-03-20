# Market Indices API Reference

CoinMarketCap provides market indices that track the performance of top cryptocurrencies. The CMC100 tracks the top 100 cryptocurrencies by market cap, while CMC20 tracks the top 20.

## Table of Contents

1. [CMC100 Historical](#cmc100-historical)
2. [CMC100 Latest](#cmc100-latest)
3. [CMC20 Historical](#cmc20-historical)
4. [CMC20 Latest](#cmc20-latest)
5. [Use Cases](#use-cases)

---

## CMC100 Historical

**Path:** `GET /v3/index/cmc100-historical`

**Description:** Returns historical values for the CMC100 index over a specified time range. The CMC100 represents the performance of the top 100 cryptocurrencies weighted by market capitalization.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| time_start | string | No | Start time (ISO 8601 or Unix timestamp). Default: earliest available |
| time_end | string | No | End time (ISO 8601 or Unix timestamp). Default: current time |
| count | integer | No | Number of data points to return. Default: 10, Max: 10000 |
| interval | string | No | Time interval between data points. Options: 5m, 10m, 15m, 30m, 45m, 1h, 2h, 3h, 4h, 6h, 12h, 1d, 2d, 3d, 7d, 14d, 15d, 30d, 60d, 90d, 365d. Default: 1d |

### Response Fields

| Field | Description |
|-------|-------------|
| id | Index identifier |
| name | Index name (CMC Crypto 100) |
| symbol | Index symbol (CMC100) |
| quotes | Array of historical data points |
| quotes[].timestamp | ISO 8601 timestamp |
| quotes[].open | Opening value for the interval |
| quotes[].high | Highest value in the interval |
| quotes[].low | Lowest value in the interval |
| quotes[].close | Closing value for the interval |
| quotes[].volume | Trading volume in the interval |
| quotes[].market_cap | Total market cap of constituents |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v3/index/cmc100-historical?interval=1d&count=30" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

### Example Response

```json
{
  "status": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "error_code": 0,
    "error_message": null,
    "credit_count": 1
  },
  "data": {
    "id": 1,
    "name": "CMC Crypto 100",
    "symbol": "CMC100",
    "quotes": [
      {
        "timestamp": "2024-01-14T00:00:00.000Z",
        "open": 145.23,
        "high": 148.56,
        "low": 143.12,
        "close": 147.89,
        "volume": 85000000000,
        "market_cap": 1650000000000
      }
    ]
  }
}
```

---

## CMC100 Latest

**Path:** `GET /v3/index/cmc100-latest`

**Description:** Returns the current value of the CMC100 index. Provides real-time tracking of the top 100 cryptocurrency market performance.

### Parameters

This endpoint has no parameters.

### Response Fields

| Field | Description |
|-------|-------------|
| id | Index identifier |
| name | Index name (CMC Crypto 100) |
| symbol | Index symbol (CMC100) |
| last_updated | ISO 8601 timestamp of last update |
| quote | Current index values |
| quote.price | Current index price/value |
| quote.volume_24h | 24-hour trading volume |
| quote.volume_change_24h | 24h volume change percentage |
| quote.percent_change_1h | 1 hour price change percentage |
| quote.percent_change_24h | 24 hour price change percentage |
| quote.percent_change_7d | 7 day price change percentage |
| quote.percent_change_30d | 30 day price change percentage |
| quote.market_cap | Total market cap of index constituents |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v3/index/cmc100-latest" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

### Example Response

```json
{
  "status": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "error_code": 0,
    "error_message": null,
    "credit_count": 1
  },
  "data": {
    "id": 1,
    "name": "CMC Crypto 100",
    "symbol": "CMC100",
    "last_updated": "2024-01-15T10:25:00.000Z",
    "quote": {
      "USD": {
        "price": 147.89,
        "volume_24h": 85000000000,
        "volume_change_24h": 5.23,
        "percent_change_1h": 0.35,
        "percent_change_24h": 2.15,
        "percent_change_7d": 8.45,
        "percent_change_30d": 15.67,
        "market_cap": 1650000000000
      }
    }
  }
}
```

---

## CMC20 Historical

**Path:** `GET /v3/index/cmc20-historical`

**Description:** Returns historical values for the CMC20 index. The CMC20 tracks the performance of the top 20 cryptocurrencies by market cap, providing a focused view of large-cap crypto performance.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| time_start | string | No | Start time (ISO 8601 or Unix timestamp). Default: earliest available |
| time_end | string | No | End time (ISO 8601 or Unix timestamp). Default: current time |
| count | integer | No | Number of data points to return. Default: 10, Max: 10000 |
| interval | string | No | Time interval between data points. Options: 5m, 10m, 15m, 30m, 45m, 1h, 2h, 3h, 4h, 6h, 12h, 1d, 2d, 3d, 7d, 14d, 15d, 30d, 60d, 90d, 365d. Default: 1d |

### Response Fields

| Field | Description |
|-------|-------------|
| id | Index identifier |
| name | Index name (CMC Crypto 20) |
| symbol | Index symbol (CMC20) |
| quotes | Array of historical data points |
| quotes[].timestamp | ISO 8601 timestamp |
| quotes[].open | Opening value for the interval |
| quotes[].high | Highest value in the interval |
| quotes[].low | Lowest value in the interval |
| quotes[].close | Closing value for the interval |
| quotes[].volume | Trading volume in the interval |
| quotes[].market_cap | Total market cap of constituents |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v3/index/cmc20-historical?interval=1d&count=30" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

### Example Response

```json
{
  "status": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "error_code": 0,
    "error_message": null,
    "credit_count": 1
  },
  "data": {
    "id": 2,
    "name": "CMC Crypto 20",
    "symbol": "CMC20",
    "quotes": [
      {
        "timestamp": "2024-01-14T00:00:00.000Z",
        "open": 312.45,
        "high": 318.23,
        "low": 308.12,
        "close": 316.78,
        "volume": 72000000000,
        "market_cap": 1450000000000
      }
    ]
  }
}
```

---

## CMC20 Latest

**Path:** `GET /v3/index/cmc20-latest`

**Description:** Returns the current value of the CMC20 index. Tracks real-time performance of the top 20 cryptocurrencies.

### Parameters

This endpoint has no parameters.

### Response Fields

| Field | Description |
|-------|-------------|
| id | Index identifier |
| name | Index name (CMC Crypto 20) |
| symbol | Index symbol (CMC20) |
| last_updated | ISO 8601 timestamp of last update |
| quote | Current index values |
| quote.price | Current index price/value |
| quote.volume_24h | 24-hour trading volume |
| quote.volume_change_24h | 24h volume change percentage |
| quote.percent_change_1h | 1 hour price change percentage |
| quote.percent_change_24h | 24 hour price change percentage |
| quote.percent_change_7d | 7 day price change percentage |
| quote.percent_change_30d | 30 day price change percentage |
| quote.market_cap | Total market cap of index constituents |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v3/index/cmc20-latest" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

### Example Response

```json
{
  "status": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "error_code": 0,
    "error_message": null,
    "credit_count": 1
  },
  "data": {
    "id": 2,
    "name": "CMC Crypto 20",
    "symbol": "CMC20",
    "last_updated": "2024-01-15T10:25:00.000Z",
    "quote": {
      "USD": {
        "price": 316.78,
        "volume_24h": 72000000000,
        "volume_change_24h": 4.89,
        "percent_change_1h": 0.28,
        "percent_change_24h": 1.95,
        "percent_change_7d": 7.82,
        "percent_change_30d": 14.23,
        "market_cap": 1450000000000
      }
    }
  }
}
```

---

## Use Cases

### Benchmark Comparison

Compare individual crypto performance against indices:
1. Track how a specific coin performs vs CMC100
2. Identify outperformers and underperformers
3. Measure portfolio alpha against the index

### Large-Cap vs Broad Market

Compare CMC20 to CMC100:
1. CMC20 outperforming suggests large-cap strength
2. CMC100 outperforming suggests mid/small-cap rally
3. Use ratio for market rotation analysis

### Historical Performance Analysis

Use historical endpoints to:
1. Calculate annualized returns
2. Measure volatility over time
3. Identify drawdown periods
4. Backtest index-based strategies

### Portfolio Allocation

Use indices to inform allocation:
1. Track market cap concentration in top 20
2. Monitor index volatility for risk assessment
3. Compare index performance across timeframes
