# Market Pairs API Reference

## Market Pairs Latest

**Path:** `GET /v2/cryptocurrency/market-pairs/latest`

**Description:** Returns all active trading pairs for a cryptocurrency across all exchanges. Useful for finding where a coin trades, analyzing liquidity, and finding arbitrage opportunities.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Conditional | CMC cryptocurrency ID |
| slug | string | Conditional | Cryptocurrency slug |
| symbol | string | Conditional | Cryptocurrency symbol |
| start | integer | No | Offset for pagination. Default: 1 |
| limit | integer | No | Number of results. Default: 100, Max: 5000 |
| sort_dir | string | No | Sort direction: asc, desc. Default: desc |
| sort | string | No | Sort field: volume_24h_strict, cmc_rank_advanced, effective_liquidity, market_score, market_reputation. Default: volume_24h_strict |
| aux | string | No | Additional fields: num_market_pairs, category, fee_type, market_url, currency_name, currency_slug, price_quote, notice, cmc_rank, effective_liquidity, market_score, market_reputation. Default: all |
| matched_id | string | No | Filter by specific pairing cryptocurrency ID |
| matched_symbol | string | No | Filter by specific pairing cryptocurrency symbol |
| category | string | No | Filter by category: all, spot, derivatives, otc. Default: all |
| fee_type | string | No | Filter by fee type: all, percentage, no-fees, transactional-mining, unknown. Default: all |
| convert | string | No | Currency to convert volumes |
| convert_id | string | No | CMC ID of currency to convert to |

**Note:** At least one of `id`, `slug`, or `symbol` is required.

### Response Fields

| Field | Description |
|-------|-------------|
| data.id | CMC cryptocurrency ID |
| data.name | Cryptocurrency name |
| data.symbol | Cryptocurrency symbol |
| data.num_market_pairs | Total number of trading pairs |
| data.market_pairs[].exchange.id | Exchange CMC ID |
| data.market_pairs[].exchange.name | Exchange name |
| data.market_pairs[].exchange.slug | Exchange slug |
| data.market_pairs[].market_id | Unique market pair ID |
| data.market_pairs[].market_pair | Pair string (e.g., BTC/USD) |
| data.market_pairs[].category | Pair category (spot, derivatives) |
| data.market_pairs[].fee_type | Fee type |
| data.market_pairs[].market_pair_base.currency_id | Base currency CMC ID |
| data.market_pairs[].market_pair_base.currency_symbol | Base currency symbol |
| data.market_pairs[].market_pair_base.currency_type | Base currency type |
| data.market_pairs[].market_pair_base.exchange_symbol | Exchange-specific symbol |
| data.market_pairs[].market_pair_quote.currency_id | Quote currency CMC ID |
| data.market_pairs[].market_pair_quote.currency_symbol | Quote currency symbol |
| data.market_pairs[].market_pair_quote.currency_type | Quote currency type |
| data.market_pairs[].market_pair_quote.exchange_symbol | Exchange-specific symbol |
| data.market_pairs[].quote.exchange_reported.price | Price reported by exchange |
| data.market_pairs[].quote.exchange_reported.volume_24h_base | 24h volume in base currency |
| data.market_pairs[].quote.exchange_reported.volume_24h_quote | 24h volume in quote currency |
| data.market_pairs[].quote.exchange_reported.last_updated | Last update time |
| data.market_pairs[].quote.USD.price | Price in USD |
| data.market_pairs[].quote.USD.volume_24h | 24h volume in USD |
| data.market_pairs[].quote.USD.effective_liquidity | Effective liquidity score |
| data.market_pairs[].quote.USD.last_updated | Last update time |
| data.market_pairs[].market_url | Direct URL to trading pair |
| data.market_pairs[].market_score | Market quality score |
| data.market_pairs[].market_reputation | Market reputation score |

### Example

```bash
# Get all BTC trading pairs
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/market-pairs/latest?id=1&limit=100" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get ETH pairs on spot markets only
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/market-pairs/latest?symbol=ETH&category=spot" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Find BTC/USDT pairs specifically
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/market-pairs/latest?id=1&matched_symbol=USDT" \
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
    "num_market_pairs": 10892,
    "market_pairs": [
      {
        "exchange": {
          "id": 270,
          "name": "Binance",
          "slug": "binance"
        },
        "market_id": 9933,
        "market_pair": "BTC/USDT",
        "category": "spot",
        "fee_type": "percentage",
        "market_pair_base": {
          "currency_id": 1,
          "currency_symbol": "BTC",
          "currency_type": "cryptocurrency",
          "exchange_symbol": "BTC"
        },
        "market_pair_quote": {
          "currency_id": 825,
          "currency_symbol": "USDT",
          "currency_type": "cryptocurrency",
          "exchange_symbol": "USDT"
        },
        "quote": {
          "exchange_reported": {
            "price": 42567.89,
            "volume_24h_base": 45678.90,
            "volume_24h_quote": 1943567890.12,
            "last_updated": "2024-01-15T12:00:00.000Z"
          },
          "USD": {
            "price": 42567.89,
            "volume_24h": 1943567890.12,
            "effective_liquidity": 98765432.10,
            "last_updated": "2024-01-15T12:00:00.000Z"
          }
        },
        "market_url": "https://www.binance.com/en/trade/BTC_USDT",
        "market_score": 9.8,
        "market_reputation": 9.5
      }
    ]
  }
}
```

### Important Notes

1. **Large result sets**: Popular cryptocurrencies have thousands of trading pairs. Use pagination and limit parameters to manage response size.

2. **Sorting options**: Sort by `volume_24h_strict` for most liquid pairs, or `market_score` for highest quality markets.

3. **Exchange filtering**: Use the exchange endpoints separately to filter by specific exchanges.

4. **Fee types**: `transactional-mining` pairs may have inflated volumes due to fee rebates.

5. **Market URL**: The `market_url` field provides a direct link to trade on that exchange.

6. **Effective liquidity**: This score accounts for spread and order book depth, not just volume.

7. **Derivatives**: Set `category=derivatives` to find perpetual futures and options pairs.
