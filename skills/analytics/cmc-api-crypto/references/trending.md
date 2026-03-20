# Trending API Reference

## Trending Gainers & Losers

**Path:** `GET /v1/cryptocurrency/trending/gainers-losers`

**Description:** Returns the top cryptocurrencies by price change over a specified time period. Use this to identify momentum plays and market sentiment.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| start | integer | No | Offset for pagination. Default: 1 |
| limit | integer | No | Number of results per direction. Default: 10, Max: 200 |
| time_period | string | No | Time period for change calculation: 1h, 24h, 7d, 30d. Default: 24h |
| convert | string | No | Currency to convert prices |
| convert_id | string | No | CMC ID of currency to convert to |
| sort | string | No | Sort field: percent_change_24h. Default: percent_change_24h |
| sort_dir | string | No | Sort direction: asc (losers), desc (gainers). Default: desc |

### Response Fields

| Field | Description |
|-------|-------------|
| data[].id | CMC cryptocurrency ID |
| data[].name | Cryptocurrency name |
| data[].symbol | Cryptocurrency symbol |
| data[].slug | URL slug |
| data[].cmc_rank | CMC rank |
| data[].num_market_pairs | Number of trading pairs |
| data[].circulating_supply | Circulating supply |
| data[].total_supply | Total supply |
| data[].max_supply | Maximum supply |
| data[].last_updated | Last update time |
| data[].date_added | Date added to CMC |
| data[].tags | Array of tags |
| data[].platform | Token platform details |
| data[].quote.USD.price | Current price |
| data[].quote.USD.volume_24h | 24h volume |
| data[].quote.USD.volume_change_24h | Volume change % |
| data[].quote.USD.percent_change_1h | 1h price change |
| data[].quote.USD.percent_change_24h | 24h price change |
| data[].quote.USD.percent_change_7d | 7d price change |
| data[].quote.USD.percent_change_30d | 30d price change |
| data[].quote.USD.market_cap | Market cap |
| data[].quote.USD.market_cap_dominance | Market dominance % |
| data[].quote.USD.fully_diluted_market_cap | Fully diluted market cap |

### Example

```bash
# Get top 10 gainers in last 24h
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/trending/gainers-losers?limit=10&time_period=24h&sort_dir=desc" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get top 10 losers in last 24h
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/trending/gainers-losers?limit=10&time_period=24h&sort_dir=asc" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get top gainers over 7 days
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/trending/gainers-losers?limit=20&time_period=7d&sort_dir=desc" \
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
      "id": 12345,
      "name": "MoonCoin",
      "symbol": "MOON",
      "slug": "mooncoin",
      "cmc_rank": 234,
      "num_market_pairs": 45,
      "circulating_supply": 1000000000,
      "total_supply": 10000000000,
      "max_supply": 10000000000,
      "last_updated": "2024-01-15T12:00:00.000Z",
      "date_added": "2023-06-15T00:00:00.000Z",
      "tags": ["meme", "ethereum-ecosystem"],
      "platform": {
        "id": 1027,
        "name": "Ethereum",
        "symbol": "ETH",
        "slug": "ethereum",
        "token_address": "0x1234567890abcdef1234567890abcdef12345678"
      },
      "quote": {
        "USD": {
          "price": 0.00456,
          "volume_24h": 12345678,
          "volume_change_24h": 234.56,
          "percent_change_1h": 5.67,
          "percent_change_24h": 156.78,
          "percent_change_7d": 345.67,
          "percent_change_30d": 567.89,
          "market_cap": 4567890,
          "market_cap_dominance": 0.0001,
          "fully_diluted_market_cap": 45678900
        }
      }
    }
  ]
}
```

---

## Trending Latest

**Path:** `GET /v1/cryptocurrency/trending/latest`

**Description:** Returns the currently trending cryptocurrencies based on search volume and social activity on CoinMarketCap. Different from gainers/losers which is based purely on price change.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| start | integer | No | Offset for pagination. Default: 1 |
| limit | integer | No | Number of results. Default: 10, Max: 200 |
| time_period | string | No | Trending time window: 24h, 30d, 7d. Default: 24h |
| convert | string | No | Currency to convert prices |
| convert_id | string | No | CMC ID of currency to convert to |

### Response Fields

| Field | Description |
|-------|-------------|
| data[].id | CMC cryptocurrency ID |
| data[].name | Cryptocurrency name |
| data[].symbol | Cryptocurrency symbol |
| data[].slug | URL slug |
| data[].cmc_rank | CMC rank |
| data[].num_market_pairs | Number of trading pairs |
| data[].circulating_supply | Circulating supply |
| data[].total_supply | Total supply |
| data[].max_supply | Maximum supply |
| data[].last_updated | Last update time |
| data[].date_added | Date added to CMC |
| data[].tags | Array of tags |
| data[].platform | Token platform details |
| data[].quote.USD.price | Current price |
| data[].quote.USD.volume_24h | 24h volume |
| data[].quote.USD.percent_change_24h | 24h price change |
| data[].quote.USD.market_cap | Market cap |

### Example

```bash
# Get top 20 trending coins
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/trending/latest?limit=20&time_period=24h" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get trending coins over 7 days
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/trending/latest?limit=10&time_period=7d" \
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
      "name": "Bitcoin",
      "symbol": "BTC",
      "slug": "bitcoin",
      "cmc_rank": 1,
      "num_market_pairs": 10892,
      "circulating_supply": 19590000,
      "total_supply": 19590000,
      "max_supply": 21000000,
      "last_updated": "2024-01-15T12:00:00.000Z",
      "date_added": "2010-07-13T00:00:00.000Z",
      "tags": ["mineable", "pow", "sha-256"],
      "platform": null,
      "quote": {
        "USD": {
          "price": 42567.89,
          "volume_24h": 23456789012,
          "percent_change_24h": 2.45,
          "market_cap": 834567890123
        }
      }
    }
  ]
}
```

---

## Trending Most Visited

**Path:** `GET /v1/cryptocurrency/trending/most-visited`

**Description:** Returns the most visited cryptocurrency pages on CoinMarketCap. This reflects user interest and attention regardless of price movement.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| start | integer | No | Offset for pagination. Default: 1 |
| limit | integer | No | Number of results. Default: 10, Max: 200 |
| time_period | string | No | Visit tracking window: 24h, 30d, 7d. Default: 24h |
| convert | string | No | Currency to convert prices |
| convert_id | string | No | CMC ID of currency to convert to |

### Response Fields

| Field | Description |
|-------|-------------|
| data[].id | CMC cryptocurrency ID |
| data[].name | Cryptocurrency name |
| data[].symbol | Cryptocurrency symbol |
| data[].slug | URL slug |
| data[].cmc_rank | CMC rank |
| data[].num_market_pairs | Number of trading pairs |
| data[].circulating_supply | Circulating supply |
| data[].total_supply | Total supply |
| data[].max_supply | Maximum supply |
| data[].last_updated | Last update time |
| data[].date_added | Date added to CMC |
| data[].tags | Array of tags |
| data[].platform | Token platform details |
| data[].quote.USD.price | Current price |
| data[].quote.USD.volume_24h | 24h volume |
| data[].quote.USD.percent_change_24h | 24h price change |
| data[].quote.USD.market_cap | Market cap |

### Example

```bash
# Get most visited coins today
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/trending/most-visited?limit=20&time_period=24h" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get most visited over last week
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/trending/most-visited?limit=20&time_period=7d" \
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
      "name": "Bitcoin",
      "symbol": "BTC",
      "slug": "bitcoin",
      "cmc_rank": 1,
      "num_market_pairs": 10892,
      "circulating_supply": 19590000,
      "total_supply": 19590000,
      "max_supply": 21000000,
      "last_updated": "2024-01-15T12:00:00.000Z",
      "date_added": "2010-07-13T00:00:00.000Z",
      "tags": ["mineable", "pow", "sha-256"],
      "platform": null,
      "quote": {
        "USD": {
          "price": 42567.89,
          "volume_24h": 23456789012,
          "percent_change_24h": 2.45,
          "market_cap": 834567890123
        }
      }
    }
  ]
}
```

### Important Notes

1. **Trending vs Gainers**: Trending endpoints measure social interest and attention. Gainers/losers measure pure price performance. A coin can be trending without significant price movement.

2. **Time periods**: Available time periods are 24h, 7d, and 30d. Shorter periods capture momentum, longer periods show sustained interest.

3. **Use cases**:
   - `gainers-losers`: Find momentum trading opportunities
   - `trending/latest`: Discover coins getting social attention
   - `most-visited`: See what retail users are researching

4. **Filtering**: Results include all cryptocurrency types. Use additional filtering based on market cap or volume for more relevant results.

5. **Market cap considerations**: Trending lists may include low-cap coins with inflated percentage gains. Consider filtering by minimum market cap for more meaningful results.
