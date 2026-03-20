# Exchange Market Pairs API

## Market Pairs Latest

**Path:** `GET /v1/exchange/market-pairs/latest`

**Description:** Returns all active trading pairs for an exchange with current market data. Use this to see what cryptocurrencies are traded on an exchange and their current prices and volumes.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | No* | Exchange ID |
| slug | string | No* | Exchange slug |
| start | integer | No | Offset for pagination. Default: 1 |
| limit | integer | No | Number of results. Default: 100, Max: 5000 |
| aux | string | No | Additional fields: "num_market_pairs", "category", "fee_type", "market_url", "currency_name", "currency_slug", "price_quote", "notice", "cmc_rank", "effective_liquidity", "market_score", "market_reputation" |
| matched_id | string | No | Filter pairs containing a specific cryptocurrency ID |
| matched_symbol | string | No | Filter pairs containing a specific symbol (e.g., "BTC") |
| category | string | No | Filter by category: "all", "spot", "perpetual", "futures", "options". Default: "all" |
| fee_type | string | No | Filter by fee type: "all", "percentage", "no-fees", "transactional-mining", "unknown". Default: "all" |
| convert | string | No | Currency for price conversion. Default: "USD" |
| convert_id | string | No | CoinMarketCap currency ID for conversion |

*At least one of `id` or `slug` is required.

### Response Fields

| Field | Description |
|-------|-------------|
| id | Exchange ID |
| name | Exchange name |
| slug | Exchange slug |
| num_market_pairs | Total number of market pairs |
| market_pairs | Array of trading pairs |
| market_pairs[].market_id | Unique market pair ID |
| market_pairs[].market_pair | Trading pair string (e.g., "BTC/USDT") |
| market_pairs[].category | Market category (spot, perpetual, futures) |
| market_pairs[].fee_type | Fee type for this pair |
| market_pairs[].market_url | Direct URL to the trading pair |
| market_pairs[].market_score | Market quality score |
| market_pairs[].market_reputation | Reputation score |
| market_pairs[].effective_liquidity | Liquidity metric |
| market_pairs[].currency_id | Base currency CMC ID |
| market_pairs[].currency_name | Base currency name |
| market_pairs[].currency_symbol | Base currency symbol |
| market_pairs[].currency_slug | Base currency slug |
| market_pairs[].currency_type | Base currency type |
| market_pairs[].currency_cmc_rank | Base currency rank |
| market_pairs[].exchange_id | Exchange ID |
| market_pairs[].exchange_name | Exchange name |
| market_pairs[].exchange_slug | Exchange slug |
| market_pairs[].quote | Market data object |
| market_pairs[].quote.exchange_reported | Data reported by exchange |
| market_pairs[].quote.exchange_reported.price | Price in quote currency |
| market_pairs[].quote.exchange_reported.volume_24h_base | 24h volume in base currency |
| market_pairs[].quote.exchange_reported.volume_24h_quote | 24h volume in quote currency |
| market_pairs[].quote.exchange_reported.last_updated | Last update timestamp |
| market_pairs[].quote[currency] | Converted price data |
| market_pairs[].quote[currency].price | Price in converted currency |
| market_pairs[].quote[currency].volume_24h | 24h volume in converted currency |
| market_pairs[].quote[currency].depth_negative_two | Order book depth at -2% |
| market_pairs[].quote[currency].depth_positive_two | Order book depth at +2% |
| market_pairs[].quote[currency].last_updated | Last update timestamp |

### Example

```bash
# Get all market pairs for Binance
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/market-pairs/latest?slug=binance&limit=100" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get spot pairs only
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/market-pairs/latest?id=270&category=spot" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get perpetual futures pairs
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/market-pairs/latest?slug=binance&category=perpetual" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Find all BTC pairs on an exchange
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/market-pairs/latest?id=270&matched_symbol=BTC" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Find pairs for a specific cryptocurrency by ID
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/market-pairs/latest?slug=coinbase-exchange&matched_id=1" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Include all auxiliary fields
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/market-pairs/latest?id=270&aux=num_market_pairs,category,fee_type,market_url,currency_name,market_score,effective_liquidity" \
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
    "num_market_pairs": 1500,
    "market_pairs": [
      {
        "market_id": 12345,
        "market_pair": "BTC/USDT",
        "category": "spot",
        "fee_type": "percentage",
        "market_url": "https://www.binance.com/en/trade/BTC_USDT",
        "market_score": 9.8,
        "market_reputation": 9.5,
        "effective_liquidity": 50000000,
        "currency_id": 1,
        "currency_name": "Bitcoin",
        "currency_symbol": "BTC",
        "currency_slug": "bitcoin",
        "currency_type": "cryptocurrency",
        "currency_cmc_rank": 1,
        "exchange_id": 270,
        "exchange_name": "Binance",
        "exchange_slug": "binance",
        "quote": {
          "exchange_reported": {
            "price": 42500.00,
            "volume_24h_base": 15000,
            "volume_24h_quote": 637500000,
            "last_updated": "2024-01-15T12:00:00.000Z"
          },
          "USD": {
            "price": 42500.00,
            "volume_24h": 637500000,
            "depth_negative_two": 5000000,
            "depth_positive_two": 4800000,
            "last_updated": "2024-01-15T12:00:00.000Z"
          }
        }
      },
      {
        "market_id": 12346,
        "market_pair": "ETH/USDT",
        "category": "spot",
        "fee_type": "percentage",
        "market_url": "https://www.binance.com/en/trade/ETH_USDT",
        "market_score": 9.7,
        "market_reputation": 9.5,
        "effective_liquidity": 35000000,
        "currency_id": 1027,
        "currency_name": "Ethereum",
        "currency_symbol": "ETH",
        "currency_slug": "ethereum",
        "currency_type": "cryptocurrency",
        "currency_cmc_rank": 2,
        "exchange_id": 270,
        "exchange_name": "Binance",
        "exchange_slug": "binance",
        "quote": {
          "exchange_reported": {
            "price": 2500.00,
            "volume_24h_base": 150000,
            "volume_24h_quote": 375000000,
            "last_updated": "2024-01-15T12:00:00.000Z"
          },
          "USD": {
            "price": 2500.00,
            "volume_24h": 375000000,
            "depth_negative_two": 3000000,
            "depth_positive_two": 2900000,
            "last_updated": "2024-01-15T12:00:00.000Z"
          }
        }
      }
    ]
  }
}
```

### Notes

1. Use `matched_id` or `matched_symbol` to find specific trading pairs (e.g., all BTC pairs)
2. The `exchange_reported` data shows raw values from the exchange before conversion
3. Order book depth fields (`depth_negative_two`, `depth_positive_two`) show liquidity at +/- 2% from mid price
4. Pagination starts at 1. Use `start` and `limit` for large result sets
5. The `category` filter is useful for separating spot markets from derivatives
6. The `market_url` provides a direct link to the trading interface when available
