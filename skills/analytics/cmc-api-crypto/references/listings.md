# Listings API Reference

## Listings Latest

**Path:** `GET /v1/cryptocurrency/listings/latest`

**Description:** Returns a paginated list of all active cryptocurrencies with latest market data. This is the primary endpoint for getting a ranked list of coins by market cap, volume, or other metrics.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| start | integer | No | Offset for pagination. Default: 1 |
| limit | integer | No | Number of results. Default: 100, Max: 5000 |
| price_min | number | No | Filter by minimum price |
| price_max | number | No | Filter by maximum price |
| market_cap_min | number | No | Filter by minimum market cap |
| market_cap_max | number | No | Filter by maximum market cap |
| volume_24h_min | number | No | Filter by minimum 24h volume |
| volume_24h_max | number | No | Filter by maximum 24h volume |
| circulating_supply_min | number | No | Filter by minimum circulating supply |
| circulating_supply_max | number | No | Filter by maximum circulating supply |
| percent_change_24h_min | number | No | Filter by minimum 24h percent change |
| percent_change_24h_max | number | No | Filter by maximum 24h percent change |
| convert | string | No | Currency to convert prices (e.g., USD, EUR, BTC) |
| convert_id | string | No | CMC ID of currency to convert to |
| sort | string | No | Sort field: market_cap, name, symbol, date_added, price, circulating_supply, total_supply, max_supply, num_market_pairs, volume_24h, percent_change_1h, percent_change_24h, percent_change_7d, market_cap_by_total_supply_strict, volume_7d, volume_30d. Default: market_cap |
| sort_dir | string | No | Sort direction: asc, desc. Default: desc |
| cryptocurrency_type | string | No | Filter by type: all, coins, tokens. Default: all |
| tag | string | No | Filter by tag (e.g., defi, filesharing) |
| aux | string | No | Additional fields to include: num_market_pairs, cmc_rank, date_added, tags, platform, max_supply, circulating_supply, total_supply, market_cap_by_total_supply, volume_24h_reported, volume_7d, volume_7d_reported, volume_30d, volume_30d_reported, is_market_cap_included_in_calc |

### Response Fields

| Field | Description |
|-------|-------------|
| data[].id | CMC cryptocurrency ID |
| data[].name | Cryptocurrency name |
| data[].symbol | Cryptocurrency symbol |
| data[].slug | URL slug |
| data[].cmc_rank | CMC rank by market cap |
| data[].num_market_pairs | Number of trading pairs |
| data[].circulating_supply | Circulating supply |
| data[].total_supply | Total supply |
| data[].max_supply | Maximum supply |
| data[].last_updated | Last data update |
| data[].date_added | Date added to CMC |
| data[].tags | Array of tags |
| data[].platform | Platform details for tokens |
| data[].quote.USD.price | Current USD price |
| data[].quote.USD.volume_24h | 24h trading volume |
| data[].quote.USD.volume_change_24h | 24h volume change % |
| data[].quote.USD.percent_change_1h | 1h price change % |
| data[].quote.USD.percent_change_24h | 24h price change % |
| data[].quote.USD.percent_change_7d | 7d price change % |
| data[].quote.USD.market_cap | Market cap |
| data[].quote.USD.market_cap_dominance | Market cap dominance % |
| data[].quote.USD.fully_diluted_market_cap | Fully diluted market cap |
| data[].quote.USD.last_updated | Quote last updated |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit=100&sort=market_cap&convert=USD" \
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
          "volume_change_24h": 12.34,
          "percent_change_1h": 0.23,
          "percent_change_24h": 2.45,
          "percent_change_7d": 5.67,
          "market_cap": 834567890123,
          "market_cap_dominance": 52.3,
          "fully_diluted_market_cap": 893925690000,
          "last_updated": "2024-01-15T12:00:00.000Z"
        }
      }
    }
  ]
}
```

---

## Listings Historical

**Path:** `GET /v1/cryptocurrency/listings/historical`

**Description:** Returns a ranked list of all cryptocurrencies at a specific historical point in time. Useful for analyzing past market conditions.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| date | string | Yes | Historical date in ISO 8601 format (e.g., 2024-01-01) |
| start | integer | No | Offset for pagination. Default: 1 |
| limit | integer | No | Number of results. Default: 100, Max: 5000 |
| convert | string | No | Currency to convert prices |
| convert_id | string | No | CMC ID of currency to convert to |
| sort | string | No | Sort field: cmc_rank, name, symbol, market_cap, price, circulating_supply, total_supply, max_supply, num_market_pairs, volume_24h, percent_change_1h, percent_change_24h, percent_change_7d. Default: cmc_rank |
| sort_dir | string | No | Sort direction: asc, desc. Default: desc |
| cryptocurrency_type | string | No | Filter by type: all, coins, tokens. Default: all |
| aux | string | No | Additional fields to include |

### Response Fields

| Field | Description |
|-------|-------------|
| data[].id | CMC cryptocurrency ID |
| data[].name | Cryptocurrency name |
| data[].symbol | Cryptocurrency symbol |
| data[].slug | URL slug |
| data[].cmc_rank | CMC rank at that date |
| data[].circulating_supply | Circulating supply at date |
| data[].total_supply | Total supply at date |
| data[].max_supply | Maximum supply |
| data[].quote.USD.price | Price at date |
| data[].quote.USD.volume_24h | 24h volume at date |
| data[].quote.USD.market_cap | Market cap at date |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/historical?date=2024-01-01&limit=100" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

---

## Listings New

**Path:** `GET /v1/cryptocurrency/listings/new`

**Description:** Returns a paginated list of the most recently added cryptocurrencies to CoinMarketCap. Useful for discovering new tokens.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| start | integer | No | Offset for pagination. Default: 1 |
| limit | integer | No | Number of results. Default: 100, Max: 5000 |
| convert | string | No | Currency to convert prices |
| convert_id | string | No | CMC ID of currency to convert to |
| sort_dir | string | No | Sort direction: asc, desc. Default: desc |

### Response Fields

| Field | Description |
|-------|-------------|
| data[].id | CMC cryptocurrency ID |
| data[].name | Cryptocurrency name |
| data[].symbol | Cryptocurrency symbol |
| data[].slug | URL slug |
| data[].date_added | Date added to CMC |
| data[].tags | Array of tags |
| data[].platform | Platform details for tokens |
| data[].quote.USD.price | Current USD price |
| data[].quote.USD.volume_24h | 24h trading volume |
| data[].quote.USD.percent_change_24h | 24h price change % |
| data[].quote.USD.market_cap | Market cap |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/new?limit=50" \
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
      "id": 29384,
      "name": "New Token",
      "symbol": "NEW",
      "slug": "new-token",
      "date_added": "2024-01-14T10:00:00.000Z",
      "tags": ["defi", "ethereum-ecosystem"],
      "platform": {
        "id": 1027,
        "name": "Ethereum",
        "symbol": "ETH",
        "slug": "ethereum",
        "token_address": "0x1234567890abcdef1234567890abcdef12345678"
      },
      "quote": {
        "USD": {
          "price": 0.0234,
          "volume_24h": 1234567,
          "percent_change_24h": 45.67,
          "market_cap": 2345678
        }
      }
    }
  ]
}
```
