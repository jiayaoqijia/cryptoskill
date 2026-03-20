# Exchange Info and Mapping APIs

## Exchange Map

**Path:** `GET /v1/exchange/map`

**Description:** Returns a mapping of all exchanges to their unique CoinMarketCap IDs. Use this endpoint to look up exchange IDs before calling other endpoints that require an ID parameter.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| listing_status | string | No | Filter by status: "active", "inactive", or "untracked". Default: "active" |
| slug | string | No | Filter by exchange slug (e.g., "binance", "coinbase-exchange") |
| start | integer | No | Offset for pagination. Default: 1 |
| limit | integer | No | Number of results. Default: 100, Max: 5000 |
| sort | string | No | Sort field: "id" or "volume_24h". Default: "id" |
| aux | string | No | Additional fields: "first_historical_data", "last_historical_data", "is_active", "status" |
| crypto_id | string | No | Filter exchanges that support a specific cryptocurrency ID |

### Response Fields

| Field | Description |
|-------|-------------|
| id | Unique CoinMarketCap exchange ID |
| name | Exchange display name |
| slug | URL-friendly identifier |
| is_active | Whether the exchange is currently active (1 = active) |
| status | Exchange status string |
| first_historical_data | Timestamp of first data point |
| last_historical_data | Timestamp of most recent data point |

### Example

```bash
# Get all active exchanges
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/map?listing_status=active&limit=100" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Look up a specific exchange by slug
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/map?slug=binance" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Find exchanges that list Bitcoin (ID: 1)
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/map?crypto_id=1" \
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
      "is_active": 1,
      "status": "active",
      "first_historical_data": "2018-04-26T00:45:00.000Z",
      "last_historical_data": "2024-01-15T12:00:00.000Z"
    }
  ]
}
```

---

## Exchange Info

**Path:** `GET /v1/exchange/info`

**Description:** Returns detailed metadata for one or more exchanges including logo, description, official URLs, social links, and launch date. Ideal for displaying exchange profiles.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | No* | One or more exchange IDs (comma-separated) |
| slug | string | No* | One or more exchange slugs (comma-separated) |
| aux | string | No | Additional fields: "urls", "logo", "description", "date_launched", "notice", "status" |

*At least one of `id` or `slug` is required.

### Response Fields

| Field | Description |
|-------|-------------|
| id | Unique CoinMarketCap exchange ID |
| name | Exchange display name |
| slug | URL-friendly identifier |
| logo | URL to exchange logo image |
| description | Text description of the exchange |
| date_launched | Exchange launch date |
| notice | Any important notices about the exchange |
| countries | Array of countries where exchange operates |
| fiats | Array of supported fiat currencies |
| tags | Array of tags (e.g., "spot", "derivatives") |
| type | Exchange type (e.g., "cex", "dex") |
| maker_fee | Default maker fee percentage |
| taker_fee | Default taker fee percentage |
| weekly_visits | Estimated weekly website visits |
| spot_volume_usd | 24h spot trading volume in USD |
| spot_volume_last_updated | Timestamp of last volume update |
| urls | Object containing website, twitter, chat, fee, blog URLs |

### Example

```bash
# Get info by exchange ID
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/info?id=270" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get info by slug
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/info?slug=binance,coinbase-exchange" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get specific fields only
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/info?id=270&aux=urls,logo,description" \
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
      "logo": "https://s2.coinmarketcap.com/static/img/exchanges/64x64/270.png",
      "description": "Binance is a cryptocurrency exchange...",
      "date_launched": "2017-07-14T00:00:00.000Z",
      "notice": null,
      "countries": [],
      "fiats": ["USD", "EUR", "GBP"],
      "tags": ["spot", "margin", "futures"],
      "type": "cex",
      "maker_fee": 0.1,
      "taker_fee": 0.1,
      "weekly_visits": 50000000,
      "spot_volume_usd": 15000000000,
      "spot_volume_last_updated": "2024-01-15T12:00:00.000Z",
      "urls": {
        "website": ["https://www.binance.com"],
        "twitter": ["https://twitter.com/binance"],
        "blog": ["https://www.binance.com/en/blog"],
        "chat": ["https://t.me/binanceexchange"],
        "fee": ["https://www.binance.com/en/fee/schedule"]
      }
    }
  }
}
```

### Notes

1. The response data is keyed by exchange ID when using the `id` parameter
2. Use `slug` for human-readable lookups when you do not know the numeric ID
3. The `urls` object may contain multiple URLs per category as arrays
4. Fee information may not be available for all exchanges
