# Categories API Reference

## List All Categories

**Path:** `GET /v1/cryptocurrency/categories`

**Description:** Returns a paginated list of all cryptocurrency categories with market cap and volume data. Use this to discover category IDs for the category detail endpoint.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| start | integer | No | Offset for pagination. Default: 1 |
| limit | integer | No | Number of results. Default: 1, Max: 5000 |
| id | string | No | Filter by one or more category IDs (comma-separated) |
| slug | string | No | Filter by one or more category slugs (comma-separated) |
| symbol | string | No | Filter by cryptocurrency symbol to find its categories |

### Response Fields

| Field | Description |
|-------|-------------|
| data[].id | Category ID |
| data[].name | Category name |
| data[].title | Category title |
| data[].description | Category description |
| data[].num_tokens | Number of tokens in category |
| data[].avg_price_change | Average price change |
| data[].market_cap | Total market cap of category |
| data[].market_cap_change | Market cap change percentage |
| data[].volume | Total 24h volume |
| data[].volume_change | Volume change percentage |
| data[].last_updated | Last update timestamp |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/categories?limit=10" \
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
      "id": "6051a82566fc1b42617d6dc6",
      "name": "DeFi",
      "title": "DeFi Coins",
      "description": "Decentralized Finance tokens",
      "num_tokens": 534,
      "avg_price_change": 2.45,
      "market_cap": 89234567890,
      "market_cap_change": 1.23,
      "volume": 12345678901,
      "volume_change": 5.67,
      "last_updated": "2024-01-15T12:00:00.000Z"
    }
  ]
}
```

---

## Get Category Details

**Path:** `GET /v1/cryptocurrency/category`

**Description:** Returns detailed information about a single category including all tokens within it.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Yes | Category ID from the categories list endpoint |
| start | integer | No | Offset for token pagination. Default: 1 |
| limit | integer | No | Number of tokens to return. Default: 100 |
| convert | string | No | Currency to convert prices (e.g., USD, EUR, BTC) |
| convert_id | string | No | CMC ID of currency to convert to |

### Response Fields

| Field | Description |
|-------|-------------|
| data.id | Category ID |
| data.name | Category name |
| data.title | Category display title |
| data.description | Category description |
| data.num_tokens | Total tokens in category |
| data.avg_price_change | Average price change across all tokens |
| data.market_cap | Total category market cap |
| data.market_cap_change | Market cap change percentage |
| data.volume | Total 24h trading volume |
| data.volume_change | Volume change percentage |
| data.coins[].id | Token CMC ID |
| data.coins[].name | Token name |
| data.coins[].symbol | Token symbol |
| data.coins[].slug | Token URL slug |
| data.coins[].cmc_rank | CMC ranking |
| data.coins[].quote.USD.price | Current price |
| data.coins[].quote.USD.percent_change_24h | 24h price change |
| data.coins[].quote.USD.market_cap | Token market cap |
| data.coins[].quote.USD.volume_24h | 24h volume |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/category?id=6051a82566fc1b42617d6dc6&limit=50" \
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
    "id": "6051a82566fc1b42617d6dc6",
    "name": "DeFi",
    "title": "DeFi Coins",
    "description": "Decentralized Finance tokens",
    "num_tokens": 534,
    "avg_price_change": 2.45,
    "market_cap": 89234567890,
    "market_cap_change": 1.23,
    "volume": 12345678901,
    "volume_change": 5.67,
    "last_updated": "2024-01-15T12:00:00.000Z",
    "coins": [
      {
        "id": 7083,
        "name": "Uniswap",
        "symbol": "UNI",
        "slug": "uniswap",
        "cmc_rank": 18,
        "quote": {
          "USD": {
            "price": 6.23,
            "percent_change_24h": 3.45,
            "market_cap": 4678901234,
            "volume_24h": 234567890
          }
        }
      }
    ]
  }
}
```
