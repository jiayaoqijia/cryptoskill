# Exchange Quotes APIs

## Quotes Latest

**Path:** `GET /v1/exchange/quotes/latest`

**Description:** Returns the latest aggregate market data for one or more exchanges including volume metrics and percent changes. Use this for real-time exchange volume monitoring.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | No* | One or more exchange IDs (comma-separated) |
| slug | string | No* | One or more exchange slugs (comma-separated) |
| convert | string | No | Currency for conversion. Default: "USD" |
| convert_id | string | No | CoinMarketCap currency ID for conversion |
| aux | string | No | Additional fields: "num_market_pairs", "traffic_score", "rank", "exchange_score", "effective_liquidity_24h", "date_launched" |

*At least one of `id` or `slug` is required.

### Response Fields

| Field | Description |
|-------|-------------|
| id | Unique CoinMarketCap exchange ID |
| name | Exchange display name |
| slug | URL-friendly identifier |
| num_market_pairs | Number of active trading pairs |
| traffic_score | Website traffic score |
| rank | Exchange rank by volume |
| exchange_score | Overall exchange score |
| effective_liquidity_24h | 24h liquidity metric |
| date_launched | Exchange launch date |
| quote | Object containing market data by currency |
| quote[currency].volume_24h | 24-hour trading volume |
| quote[currency].volume_24h_adjusted | Adjusted 24h volume |
| quote[currency].volume_7d | 7-day trading volume |
| quote[currency].volume_30d | 30-day trading volume |
| quote[currency].percent_change_volume_24h | 24h volume change % |
| quote[currency].percent_change_volume_7d | 7d volume change % |
| quote[currency].percent_change_volume_30d | 30d volume change % |
| last_updated | Timestamp of last data update |

### Example

```bash
# Get latest quotes for Binance by ID
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/quotes/latest?id=270" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get quotes for multiple exchanges by slug
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/quotes/latest?slug=binance,coinbase-exchange,kraken" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Include auxiliary data
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/quotes/latest?id=270&aux=num_market_pairs,rank,exchange_score" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Convert to BTC
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/quotes/latest?id=270&convert=BTC" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

### Example Response

```json
{
  "status": {
    "timestamp": "2024-01-15T12:00:00.000Z",
    "error_code": 0,
    "error_message": null,
    "credit_count": 1
  },
  "data": {
    "270": {
      "id": 270,
      "name": "Binance",
      "slug": "binance",
      "num_market_pairs": 1500,
      "traffic_score": 1000,
      "rank": 1,
      "exchange_score": 9.8,
      "effective_liquidity_24h": 850000000,
      "date_launched": "2017-07-14T00:00:00.000Z",
      "quote": {
        "USD": {
          "volume_24h": 15000000000,
          "volume_24h_adjusted": 12000000000,
          "volume_7d": 95000000000,
          "volume_30d": 400000000000,
          "percent_change_volume_24h": 5.5,
          "percent_change_volume_7d": -2.3,
          "percent_change_volume_30d": 15.2
        }
      },
      "last_updated": "2024-01-15T12:00:00.000Z"
    }
  }
}
```

---

## Quotes Historical

**Path:** `GET /v1/exchange/quotes/historical`

**Description:** Returns historical market data for an exchange within a specified time range. Use this for analyzing volume trends over time or building historical charts.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | No* | Exchange ID |
| slug | string | No* | Exchange slug |
| time_start | string | No | Start time (ISO 8601 or Unix timestamp) |
| time_end | string | No | End time (ISO 8601 or Unix timestamp) |
| count | integer | No | Number of intervals. Default: 10, Max: 10000 |
| interval | string | No | Time interval. Options: "hourly", "daily", "weekly", "monthly", "yearly", "5m", "10m", "15m", "30m", "45m", "1h", "2h", "3h", "4h", "6h", "12h", "1d", "2d", "3d", "7d", "14d", "15d", "30d", "60d", "90d", "365d". Default: "5m" |
| convert | string | No | Currency for conversion. Default: "USD" |
| convert_id | string | No | CoinMarketCap currency ID for conversion |

*At least one of `id` or `slug` is required.

### Response Fields

| Field | Description |
|-------|-------------|
| id | Unique CoinMarketCap exchange ID |
| name | Exchange display name |
| slug | URL-friendly identifier |
| quotes | Array of historical data points |
| quotes[].timestamp | Data point timestamp |
| quotes[].quote | Market data for this timestamp |
| quotes[].quote[currency].volume_24h | 24h volume at this point |
| quotes[].quote[currency].volume_24h_adjusted | Adjusted 24h volume |
| quotes[].quote[currency].volume_7d | 7d volume |
| quotes[].quote[currency].volume_30d | 30d volume |
| quotes[].num_market_pairs | Number of pairs at this point |

### Example

```bash
# Get daily historical data for last 30 days
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/quotes/historical?id=270&interval=daily&count=30" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get hourly data for specific date range
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/quotes/historical?slug=binance&time_start=2024-01-01T00:00:00Z&time_end=2024-01-07T00:00:00Z&interval=hourly" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get weekly data for the past year
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/quotes/historical?id=270&interval=weekly&count=52" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Use Unix timestamps
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/quotes/historical?id=270&time_start=1704067200&time_end=1706745600&interval=daily" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

### Example Response

```json
{
  "status": {
    "timestamp": "2024-01-15T12:00:00.000Z",
    "error_code": 0,
    "error_message": null,
    "credit_count": 1
  },
  "data": {
    "id": 270,
    "name": "Binance",
    "slug": "binance",
    "quotes": [
      {
        "timestamp": "2024-01-14T00:00:00.000Z",
        "quote": {
          "USD": {
            "volume_24h": 14500000000,
            "volume_24h_adjusted": 11800000000,
            "volume_7d": 92000000000,
            "volume_30d": 395000000000
          }
        },
        "num_market_pairs": 1498
      },
      {
        "timestamp": "2024-01-15T00:00:00.000Z",
        "quote": {
          "USD": {
            "volume_24h": 15000000000,
            "volume_24h_adjusted": 12000000000,
            "volume_7d": 95000000000,
            "volume_30d": 400000000000
          }
        },
        "num_market_pairs": 1500
      }
    ]
  }
}
```

### Notes

1. Historical data availability depends on your subscription plan
2. Smaller intervals (5m, hourly) are only available for recent data
3. Use `time_start` and `time_end` for specific date ranges, or `count` for the most recent N intervals
4. The `volume_24h` at each timestamp represents the trailing 24-hour volume as of that point
5. Higher tier plans allow access to older historical data
