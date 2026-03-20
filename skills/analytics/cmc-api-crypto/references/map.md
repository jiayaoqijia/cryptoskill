# Map API Reference

## Cryptocurrency Map

**Path:** `GET /v1/cryptocurrency/map`

**Description:** Returns a mapping of all cryptocurrencies to unique CMC IDs. This is essential for converting symbol or name lookups to the IDs required by other endpoints. Best practice is to cache this data and refresh periodically.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| listing_status | string | No | Filter by listing status: active, inactive, untracked. Default: active. Pass multiple comma-separated values. |
| start | integer | No | Offset for pagination. Default: 1 |
| limit | integer | No | Number of results. Default: returns all. Max: 5000 |
| sort | string | No | Sort field: cmc_rank, id, name. Default: id |
| symbol | string | No | Filter by one or more comma-separated symbols (e.g., BTC,ETH) |
| aux | string | No | Additional fields: platform, first_historical_data, last_historical_data, is_active, status. Default: platform,first_historical_data,last_historical_data,is_active |

### Response Fields

| Field | Description |
|-------|-------------|
| data[].id | CMC cryptocurrency ID (use this for other API calls) |
| data[].rank | CMC rank by market cap |
| data[].name | Full cryptocurrency name |
| data[].symbol | Cryptocurrency symbol/ticker |
| data[].slug | URL-friendly slug |
| data[].is_active | Whether the crypto is actively tracked (1=yes, 0=no) |
| data[].first_historical_data | First date with historical data |
| data[].last_historical_data | Last date with historical data |
| data[].platform | Platform details for tokens (null for native coins) |
| data[].platform.id | Platform CMC ID |
| data[].platform.name | Platform name |
| data[].platform.symbol | Platform symbol |
| data[].platform.slug | Platform slug |
| data[].platform.token_address | Token contract address |

### Example

```bash
# Get all active cryptocurrencies
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map?listing_status=active" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Look up specific symbols
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map?symbol=BTC,ETH,SOL" \
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
      "id": 1,
      "rank": 1,
      "name": "Bitcoin",
      "symbol": "BTC",
      "slug": "bitcoin",
      "is_active": 1,
      "first_historical_data": "2010-07-13T00:00:00.000Z",
      "last_historical_data": "2024-01-15T00:00:00.000Z",
      "platform": null
    },
    {
      "id": 1027,
      "rank": 2,
      "name": "Ethereum",
      "symbol": "ETH",
      "slug": "ethereum",
      "is_active": 1,
      "first_historical_data": "2015-08-07T00:00:00.000Z",
      "last_historical_data": "2024-01-15T00:00:00.000Z",
      "platform": null
    },
    {
      "id": 825,
      "rank": 3,
      "name": "Tether",
      "symbol": "USDT",
      "slug": "tether",
      "is_active": 1,
      "first_historical_data": "2015-02-25T00:00:00.000Z",
      "last_historical_data": "2024-01-15T00:00:00.000Z",
      "platform": {
        "id": 1027,
        "name": "Ethereum",
        "symbol": "ETH",
        "slug": "ethereum",
        "token_address": "0xdac17f958d2ee523a2206206994597c13d831ec7"
      }
    }
  ]
}
```

### Important Notes

1. **Symbol collisions**: Multiple cryptocurrencies can share the same symbol. When querying by symbol, you may receive multiple results. Always verify by name or check the rank.

2. **Token platforms**: Tokens will include platform information showing which blockchain they exist on and their contract address.

3. **Inactive cryptocurrencies**: Set `listing_status=inactive` to find delisted or inactive cryptocurrencies.

4. **Caching**: This endpoint returns relatively static data. Cache results and refresh every 24 hours to reduce API calls.

5. **ID stability**: CMC IDs are stable and never change. Use these IDs instead of symbols for reliable lookups.
