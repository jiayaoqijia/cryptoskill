# Exchange Listings API

## Listings Latest

**Path:** `GET /v1/exchange/listings/latest`

**Description:** Returns a paginated list of all cryptocurrency exchanges with the latest market data. Use this endpoint to get ranked exchange data sorted by volume, number of markets, or other metrics.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| start | integer | No | Offset for pagination. Default: 1 |
| limit | integer | No | Number of results. Default: 100, Max: 5000 |
| sort | string | No | Sort field. Options: "name", "volume_24h", "volume_24h_adjusted", "exchange_score". Default: "volume_24h" |
| sort_dir | string | No | Sort direction: "asc" or "desc". Default: "desc" |
| market_type | string | No | Filter by market type: "fees", "no_fees", "all". Default: "all" |
| category | string | No | Filter by category: "all", "spot", "derivatives", "dex". Default: "all" |
| aux | string | No | Additional fields: "num_market_pairs", "date_launched", "traffic_score", "rank", "exchange_score", "effective_liquidity_24h" |
| convert | string | No | Currency for volume conversion. Default: "USD" |
| convert_id | string | No | CoinMarketCap currency ID for conversion |

### Response Fields

| Field | Description |
|-------|-------------|
| id | Unique CoinMarketCap exchange ID |
| name | Exchange display name |
| slug | URL-friendly identifier |
| num_market_pairs | Number of active trading pairs |
| date_launched | Exchange launch date |
| traffic_score | Website traffic score |
| rank | Exchange rank by volume |
| exchange_score | Overall exchange score |
| effective_liquidity_24h | Liquidity metric |
| quote | Object containing market data by currency |
| quote[currency].volume_24h | 24-hour trading volume |
| quote[currency].volume_24h_adjusted | Adjusted 24h volume (excludes wash trading) |
| quote[currency].volume_7d | 7-day trading volume |
| quote[currency].volume_30d | 30-day trading volume |
| quote[currency].percent_change_volume_24h | 24h volume change percentage |
| quote[currency].percent_change_volume_7d | 7d volume change percentage |
| quote[currency].percent_change_volume_30d | 30d volume change percentage |
| last_updated | Timestamp of last data update |

### Example

```bash
# Get top 10 exchanges by volume
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/listings/latest?limit=10&sort=volume_24h&sort_dir=desc" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get spot exchanges only
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/listings/latest?category=spot&limit=20" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get derivatives exchanges sorted by score
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/listings/latest?category=derivatives&sort=exchange_score" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Include all auxiliary fields
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/listings/latest?aux=num_market_pairs,date_launched,traffic_score,rank,exchange_score,effective_liquidity_24h" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Convert volumes to EUR
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/listings/latest?convert=EUR&limit=10" \
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
  "data": [
    {
      "id": 270,
      "name": "Binance",
      "slug": "binance",
      "num_market_pairs": 1500,
      "date_launched": "2017-07-14T00:00:00.000Z",
      "traffic_score": 1000,
      "rank": 1,
      "exchange_score": 9.8,
      "effective_liquidity_24h": 850000000,
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
    },
    {
      "id": 89,
      "name": "Coinbase Exchange",
      "slug": "coinbase-exchange",
      "num_market_pairs": 550,
      "date_launched": "2014-01-01T00:00:00.000Z",
      "traffic_score": 850,
      "rank": 2,
      "exchange_score": 9.5,
      "effective_liquidity_24h": 420000000,
      "quote": {
        "USD": {
          "volume_24h": 3500000000,
          "volume_24h_adjusted": 3200000000,
          "volume_7d": 22000000000,
          "volume_30d": 90000000000,
          "percent_change_volume_24h": 3.2,
          "percent_change_volume_7d": 1.1,
          "percent_change_volume_30d": 8.5
        }
      },
      "last_updated": "2024-01-15T12:00:00.000Z"
    }
  ]
}
```

### Notes

1. The `volume_24h_adjusted` field attempts to filter out wash trading and provides a more accurate volume estimate
2. Use `category=derivatives` to see futures and perpetual exchanges separately from spot exchanges
3. The `exchange_score` is a composite metric based on liquidity, volume, and other factors
4. Pagination starts at 1, not 0. The second page of 100 results uses `start=101`
5. The `market_type` filter can help identify exchanges with fee-free trading promotions
