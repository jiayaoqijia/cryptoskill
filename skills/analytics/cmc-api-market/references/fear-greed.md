# Fear and Greed Index API Reference

The Fear and Greed Index measures market sentiment on a scale from 0 (Extreme Fear) to 100 (Extreme Greed). It aggregates multiple data sources to provide a single sentiment indicator.

## Historical Fear and Greed Index

**Path:** `GET /v3/fear-and-greed/historical`

**Description:** Returns historical fear and greed index values over a specified time range. Useful for analyzing sentiment trends, identifying market turning points, and backtesting sentiment-based strategies.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| start | integer | No | Start timestamp (Unix epoch in seconds). Default: 30 days ago |
| limit | integer | No | Number of records to return. Default: 50, Max: 1000 |

### Response Fields

| Field | Description |
|-------|-------------|
| data | Array of historical index values |
| data[].timestamp | Unix timestamp for the data point |
| data[].value | Fear and greed score (0-100) |
| data[].value_classification | Text classification of the score |

### Value Classifications

| Range | Classification |
|-------|----------------|
| 0-24 | Extreme Fear |
| 25-44 | Fear |
| 45-55 | Neutral |
| 56-75 | Greed |
| 76-100 | Extreme Greed |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v3/fear-and-greed/historical?limit=30" \
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
  "data": [
    {
      "timestamp": 1705276800,
      "value": 72,
      "value_classification": "Greed"
    },
    {
      "timestamp": 1705190400,
      "value": 68,
      "value_classification": "Greed"
    },
    {
      "timestamp": 1705104000,
      "value": 65,
      "value_classification": "Greed"
    }
  ]
}
```

---

## Latest Fear and Greed Index

**Path:** `GET /v3/fear-and-greed/latest`

**Description:** Returns the current fear and greed index value. This endpoint provides the most recent sentiment reading for the cryptocurrency market.

### Parameters

This endpoint has no parameters.

### Response Fields

| Field | Description |
|-------|-------------|
| value | Current fear and greed score (0-100) |
| value_classification | Text classification of the current score |
| timestamp | Unix timestamp of the reading |
| update_time | ISO 8601 formatted update time |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v3/fear-and-greed/latest" \
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
    "value": 72,
    "value_classification": "Greed",
    "timestamp": 1705276800,
    "update_time": "2024-01-15T00:00:00.000Z"
  }
}
```

---

## Index Methodology

The Fear and Greed Index incorporates multiple factors:

1. **Volatility (25%)** - Current volatility compared to 30/90 day averages
2. **Market Momentum/Volume (25%)** - Current volume compared to averages
3. **Social Media (15%)** - Crypto mentions and engagement rates
4. **Surveys (15%)** - Polling data when available
5. **Bitcoin Dominance (10%)** - BTC share of total market cap
6. **Google Trends (10%)** - Search interest for crypto terms

## Use Cases

### Contrarian Indicator

Use extreme readings as potential reversal signals:
1. Extreme Fear (0-24) may indicate buying opportunities
2. Extreme Greed (76-100) may signal market tops

### Sentiment Tracking

Monitor sentiment shifts over time:
1. Track weekly changes in the index
2. Compare current reading to 30-day average
3. Identify sentiment divergence from price

### Risk Management

Adjust position sizing based on sentiment:
1. Reduce exposure during extreme greed
2. Consider accumulation during extreme fear
3. Maintain normal positions during neutral readings

### Historical Analysis

Use historical data to:
1. Correlate sentiment with price movements
2. Identify sentiment patterns before major moves
3. Backtest sentiment-based trading strategies
