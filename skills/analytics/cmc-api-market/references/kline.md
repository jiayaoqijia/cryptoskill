# K-Line (Charts) API Reference

K-Line endpoints provide candlestick (OHLCV) and time series data for building cryptocurrency charts and performing technical analysis.

## Candles (OHLCV)

**Path:** `GET /v1/k-line/candles`

**Description:** Returns OHLCV (Open, High, Low, Close, Volume) candlestick data for charting. Essential for technical analysis and building trading charts.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Yes* | CMC cryptocurrency ID. Required if symbol not provided |
| symbol | string | Yes* | Cryptocurrency symbol. Required if id not provided |
| time_start | string | No | Start time (ISO 8601 or Unix timestamp). Default: 24 hours ago |
| time_end | string | No | End time (ISO 8601 or Unix timestamp). Default: current time |
| count | integer | No | Number of candles to return. Default: 100, Max: 10000 |
| interval | string | No | Candle interval. Options: 1m, 5m, 10m, 15m, 30m, 45m, 1h, 2h, 3h, 4h, 6h, 12h, 1d, 2d, 3d, 7d, 14d, 15d, 30d. Default: 1h |
| convert | string | No | Quote currency. Default: USD |
| convert_id | string | No | CMC ID of quote currency (alternative to convert) |

### Response Fields

| Field | Description |
|-------|-------------|
| id | CMC cryptocurrency ID |
| name | Cryptocurrency name |
| symbol | Cryptocurrency symbol |
| quotes | Array of OHLCV candles |
| quotes[].time_open | Candle open timestamp |
| quotes[].time_close | Candle close timestamp |
| quotes[].time_high | Timestamp of high price |
| quotes[].time_low | Timestamp of low price |
| quotes[].open | Opening price |
| quotes[].high | Highest price in interval |
| quotes[].low | Lowest price in interval |
| quotes[].close | Closing price |
| quotes[].volume | Trading volume in quote currency |
| quotes[].market_cap | Market cap at close |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/k-line/candles?id=1&interval=1h&count=24" \
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
    "name": "Bitcoin",
    "symbol": "BTC",
    "quotes": [
      {
        "time_open": "2024-01-15T09:00:00.000Z",
        "time_close": "2024-01-15T09:59:59.999Z",
        "time_high": "2024-01-15T09:23:00.000Z",
        "time_low": "2024-01-15T09:45:00.000Z",
        "open": 43150.00,
        "high": 43450.00,
        "low": 43050.00,
        "close": 43380.00,
        "volume": 1250000000,
        "market_cap": 850000000000
      },
      {
        "time_open": "2024-01-15T08:00:00.000Z",
        "time_close": "2024-01-15T08:59:59.999Z",
        "time_high": "2024-01-15T08:15:00.000Z",
        "time_low": "2024-01-15T08:42:00.000Z",
        "open": 43000.00,
        "high": 43200.00,
        "low": 42950.00,
        "close": 43150.00,
        "volume": 980000000,
        "market_cap": 845000000000
      }
    ]
  }
}
```

---

## Time Series Points

**Path:** `GET /v1/k-line/points`

**Description:** Returns time series data points for price, market cap, and volume. Useful for line charts and trend analysis without full OHLCV data.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Yes* | CMC cryptocurrency ID. Required if symbol not provided |
| symbol | string | Yes* | Cryptocurrency symbol. Required if id not provided |
| time_start | string | No | Start time (ISO 8601 or Unix timestamp). Default: 24 hours ago |
| time_end | string | No | End time (ISO 8601 or Unix timestamp). Default: current time |
| count | integer | No | Number of points to return. Default: 100, Max: 10000 |
| interval | string | No | Point interval. Options: 5m, 10m, 15m, 30m, 45m, 1h, 2h, 3h, 4h, 6h, 12h, 1d, 2d, 3d, 7d, 14d, 15d, 30d. Default: 1h |
| convert | string | No | Quote currency. Default: USD |
| convert_id | string | No | CMC ID of quote currency (alternative to convert) |
| metrics | string | No | Metrics to include. Options: price, market_cap, volume. Default: all |

### Response Fields

| Field | Description |
|-------|-------------|
| id | CMC cryptocurrency ID |
| name | Cryptocurrency name |
| symbol | Cryptocurrency symbol |
| points | Array of time series points |
| points[].timestamp | Data point timestamp |
| points[].price | Price at timestamp |
| points[].market_cap | Market cap at timestamp |
| points[].volume_24h | 24h rolling volume at timestamp |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/k-line/points?id=1&interval=1h&count=24&metrics=price,market_cap" \
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
    "name": "Bitcoin",
    "symbol": "BTC",
    "points": [
      {
        "timestamp": "2024-01-15T10:00:00.000Z",
        "price": 43380.00,
        "market_cap": 850000000000,
        "volume_24h": 28500000000
      },
      {
        "timestamp": "2024-01-15T09:00:00.000Z",
        "price": 43150.00,
        "market_cap": 845500000000,
        "volume_24h": 27800000000
      }
    ]
  }
}
```

---

## Interval Guide

Choose the appropriate interval based on your use case:

| Use Case | Recommended Intervals |
|----------|----------------------|
| Scalping / Intraday | 1m, 5m, 15m |
| Day Trading | 15m, 30m, 1h |
| Swing Trading | 1h, 4h, 1d |
| Position Trading | 1d, 7d |
| Long-term Analysis | 1d, 7d, 30d |

## Use Cases

### Candlestick Charts

Build interactive trading charts:
1. Fetch OHLCV data with `/k-line/candles`
2. Use libraries like TradingView, Chart.js, or D3
3. Implement zoom and pan for different timeframes

### Technical Indicators

Calculate technical indicators from candle data:
1. Moving Averages (SMA, EMA) from close prices
2. RSI from price changes
3. MACD from EMA calculations
4. Bollinger Bands from close prices and standard deviation

### Price Alerts

Build price tracking systems:
1. Fetch time series points regularly
2. Compare against user-defined thresholds
3. Trigger alerts on price crossovers

### Performance Tracking

Track price performance over time:
1. Fetch daily points for extended periods
2. Calculate returns over different timeframes
3. Compare performance across multiple assets

### Market Cap Analysis

Analyze market cap trends:
1. Fetch points with market_cap metric
2. Track market cap changes over time
3. Identify market cap breakouts or breakdowns

### Volume Analysis

Study trading volume patterns:
1. Combine volume from candles with price
2. Identify volume spikes
3. Calculate volume-weighted average price (VWAP)
