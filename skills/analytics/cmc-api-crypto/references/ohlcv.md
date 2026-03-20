# OHLCV API Reference

## OHLCV Latest

**Path:** `GET /v2/cryptocurrency/ohlcv/latest`

**Description:** Returns the latest OHLCV (Open, High, Low, Close, Volume) data for one or more cryptocurrencies. Returns the last completed UTC day by default.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Conditional | One or more comma-separated CMC IDs |
| slug | string | Conditional | One or more comma-separated slugs |
| symbol | string | Conditional | One or more comma-separated symbols |
| convert | string | No | Currency to convert (e.g., USD, EUR, BTC). Default: USD |
| convert_id | string | No | CMC ID of currency to convert to |
| skip_invalid | boolean | No | Skip invalid IDs instead of erroring. Default: false |

**Note:** At least one of `id`, `slug`, or `symbol` is required.

### Response Fields

| Field | Description |
|-------|-------------|
| data[id].id | CMC cryptocurrency ID |
| data[id].name | Cryptocurrency name |
| data[id].symbol | Cryptocurrency symbol |
| data[id].last_updated | Last update timestamp |
| data[id].time_open | Period open time |
| data[id].time_close | Period close time |
| data[id].time_high | Time of period high |
| data[id].time_low | Time of period low |
| data[id].quote.USD.open | Opening price |
| data[id].quote.USD.high | Highest price in period |
| data[id].quote.USD.low | Lowest price in period |
| data[id].quote.USD.close | Closing price |
| data[id].quote.USD.volume | Total volume in period |
| data[id].quote.USD.market_cap | Market cap at close |
| data[id].quote.USD.timestamp | Quote timestamp |

### Example

```bash
# Get latest OHLCV by ID
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/ohlcv/latest?id=1,1027" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get latest OHLCV by symbol
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/ohlcv/latest?symbol=BTC,ETH&convert=USD" \
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
    "1": {
      "id": 1,
      "name": "Bitcoin",
      "symbol": "BTC",
      "last_updated": "2024-01-15T00:00:00.000Z",
      "time_open": "2024-01-14T00:00:00.000Z",
      "time_close": "2024-01-14T23:59:59.999Z",
      "time_high": "2024-01-14T14:35:00.000Z",
      "time_low": "2024-01-14T03:20:00.000Z",
      "quote": {
        "USD": {
          "open": 42100.00,
          "high": 43200.00,
          "low": 41800.00,
          "close": 42567.89,
          "volume": 23456789012,
          "market_cap": 834567890123,
          "timestamp": "2024-01-15T00:00:00.000Z"
        }
      }
    }
  }
}
```

---

## OHLCV Historical

**Path:** `GET /v2/cryptocurrency/ohlcv/historical`

**Description:** Returns historical OHLCV candles for a cryptocurrency. Useful for building price charts and technical analysis.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Conditional | CMC cryptocurrency ID |
| slug | string | Conditional | Cryptocurrency slug |
| symbol | string | Conditional | Cryptocurrency symbol |
| time_period | string | No | Time period for each candle: daily, hourly. Default: daily |
| time_start | string | No | Start time (ISO 8601 or Unix timestamp) |
| time_end | string | No | End time (ISO 8601 or Unix timestamp) |
| count | integer | No | Number of candles. Default: 10, Max: 10000 |
| interval | string | No | Candle interval: hourly, daily, weekly, monthly, yearly, 1h, 2h, 3h, 4h, 6h, 12h, 1d, 2d, 3d, 7d, 14d, 15d, 30d, 60d, 90d, 365d. Default: daily |
| convert | string | No | Currency to convert (e.g., USD) |
| convert_id | string | No | CMC ID of currency to convert to |
| skip_invalid | boolean | No | Skip invalid values. Default: false |

**Note:** At least one of `id`, `slug`, or `symbol` is required.

### Response Fields

| Field | Description |
|-------|-------------|
| data.id | CMC cryptocurrency ID |
| data.name | Cryptocurrency name |
| data.symbol | Cryptocurrency symbol |
| data.quotes[].time_open | Candle open time |
| data.quotes[].time_close | Candle close time |
| data.quotes[].time_high | Time of high |
| data.quotes[].time_low | Time of low |
| data.quotes[].quote.USD.open | Opening price |
| data.quotes[].quote.USD.high | High price |
| data.quotes[].quote.USD.low | Low price |
| data.quotes[].quote.USD.close | Closing price |
| data.quotes[].quote.USD.volume | Volume in period |
| data.quotes[].quote.USD.market_cap | Market cap at close |
| data.quotes[].quote.USD.timestamp | Data timestamp |

### Example

```bash
# Get daily candles for last 30 days
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/ohlcv/historical?id=1&interval=daily&count=30" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get hourly candles for specific date range
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/ohlcv/historical?id=1&time_start=2024-01-01&time_end=2024-01-07&interval=hourly" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get weekly candles for 2023
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/ohlcv/historical?symbol=BTC&time_start=2023-01-01&time_end=2023-12-31&interval=weekly" \
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
    "id": 1,
    "name": "Bitcoin",
    "symbol": "BTC",
    "quotes": [
      {
        "time_open": "2024-01-01T00:00:00.000Z",
        "time_close": "2024-01-01T23:59:59.999Z",
        "time_high": "2024-01-01T18:30:00.000Z",
        "time_low": "2024-01-01T06:15:00.000Z",
        "quote": {
          "USD": {
            "open": 42345.67,
            "high": 43456.78,
            "low": 41234.56,
            "close": 42890.12,
            "volume": 22345678901,
            "market_cap": 840123456789,
            "timestamp": "2024-01-02T00:00:00.000Z"
          }
        }
      },
      {
        "time_open": "2024-01-02T00:00:00.000Z",
        "time_close": "2024-01-02T23:59:59.999Z",
        "time_high": "2024-01-02T12:45:00.000Z",
        "time_low": "2024-01-02T22:10:00.000Z",
        "quote": {
          "USD": {
            "open": 42890.12,
            "high": 44567.89,
            "low": 42100.00,
            "close": 43567.89,
            "volume": 24567890123,
            "market_cap": 853456789012,
            "timestamp": "2024-01-03T00:00:00.000Z"
          }
        }
      }
    ]
  }
}
```

### Important Notes

1. **Interval selection**: Match your interval to your analysis needs. Daily candles for long-term trends, hourly for intraday analysis.

2. **Time alignment**: Candles align to UTC boundaries. Daily candles open at 00:00 UTC.

3. **Historical availability**: Historical data availability varies by plan and cryptocurrency. Older, less popular coins may have limited history.

4. **Volume calculation**: Volume represents total trading volume across all exchanges tracked by CMC during the period.

5. **Missing data**: Some candles may be missing due to data gaps. Handle null values in your code.

6. **Credit usage**: Each historical request consumes credits based on the amount of data returned.
