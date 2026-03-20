# Global Metrics API Reference

Global market metrics provide aggregate cryptocurrency market data including total market capitalization, trading volume, and Bitcoin dominance.

## Historical Global Metrics

**Path:** `GET /v1/global-metrics/quotes/historical`

**Description:** Returns historical aggregate market metrics over a time range. Useful for tracking market trends, analyzing total market cap changes, and monitoring BTC dominance shifts over time.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| time_start | string | No | Start timestamp (ISO 8601 or Unix). Default: earliest available |
| time_end | string | No | End timestamp (ISO 8601 or Unix). Default: current time |
| count | integer | No | Number of intervals to return. Default: 10, Max: 10000 |
| interval | string | No | Time interval between points. Options: hourly, daily, weekly, monthly, yearly, 5m, 10m, 15m, 30m, 45m, 1h, 2h, 3h, 4h, 6h, 12h, 1d, 2d, 3d, 7d, 14d, 15d, 30d, 60d, 90d, 365d. Default: 1d |
| convert | string | No | Currency to convert to (e.g., USD, EUR, BTC). Default: USD |
| convert_id | string | No | CMC ID of currency to convert to (alternative to convert) |
| aux | string | No | Auxiliary fields to include. Options: btc_dominance, active_cryptocurrencies, active_exchanges, active_market_pairs, total_volume_24h, total_volume_24h_reported, altcoin_volume_24h, altcoin_volume_24h_reported, altcoin_market_cap, defi_volume_24h, defi_volume_24h_reported, defi_24h_percentage_change, defi_market_cap, stablecoin_volume_24h, stablecoin_volume_24h_reported, stablecoin_24h_percentage_change, stablecoin_market_cap, derivatives_volume_24h, derivatives_volume_24h_reported, derivatives_24h_percentage_change |

### Response Fields

| Field | Description |
|-------|-------------|
| quotes | Array of historical data points |
| quotes[].timestamp | ISO 8601 timestamp for the data point |
| quotes[].btc_dominance | Bitcoin's percentage of total market cap |
| quotes[].eth_dominance | Ethereum's percentage of total market cap |
| quotes[].active_cryptocurrencies | Number of tracked cryptocurrencies |
| quotes[].active_exchanges | Number of tracked exchanges |
| quotes[].active_market_pairs | Number of active trading pairs |
| quotes[].quote | Price data in requested currency |
| quotes[].quote.total_market_cap | Total crypto market capitalization |
| quotes[].quote.total_volume_24h | 24-hour trading volume |
| quotes[].quote.altcoin_market_cap | Market cap excluding BTC |
| quotes[].quote.altcoin_volume_24h | 24h volume excluding BTC |
| quotes[].quote.defi_volume_24h | DeFi protocol 24h volume |
| quotes[].quote.defi_market_cap | DeFi protocol market cap |
| quotes[].quote.stablecoin_volume_24h | Stablecoin 24h volume |
| quotes[].quote.stablecoin_market_cap | Stablecoin market cap |
| quotes[].quote.derivatives_volume_24h | Derivatives 24h volume |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/historical?interval=daily&count=7&convert=USD" \
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
    "quotes": [
      {
        "timestamp": "2024-01-14T00:00:00.000Z",
        "btc_dominance": 52.5,
        "eth_dominance": 17.2,
        "active_cryptocurrencies": 10234,
        "active_exchanges": 756,
        "active_market_pairs": 89432,
        "quote": {
          "USD": {
            "total_market_cap": 1750000000000,
            "total_volume_24h": 85000000000,
            "altcoin_market_cap": 831250000000,
            "altcoin_volume_24h": 42500000000
          }
        }
      }
    ]
  }
}
```

---

## Latest Global Metrics

**Path:** `GET /v1/global-metrics/quotes/latest`

**Description:** Returns the latest aggregate market metrics. This is the primary endpoint for getting current total market cap, BTC dominance, active crypto count, and overall market statistics.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| convert | string | No | Currency to convert to (e.g., USD, EUR, BTC). Default: USD |
| convert_id | string | No | CMC ID of currency to convert to (alternative to convert) |

### Response Fields

| Field | Description |
|-------|-------------|
| btc_dominance | Bitcoin's percentage of total market cap |
| eth_dominance | Ethereum's percentage of total market cap |
| btc_dominance_24h_percentage_change | 24h change in BTC dominance |
| eth_dominance_24h_percentage_change | 24h change in ETH dominance |
| active_cryptocurrencies | Total number of tracked cryptocurrencies |
| total_cryptocurrencies | Total cryptocurrencies including inactive |
| active_exchanges | Number of active exchanges |
| total_exchanges | Total exchanges including inactive |
| active_market_pairs | Number of active trading pairs |
| last_updated | ISO 8601 timestamp of last data update |
| quote | Price data in requested currency |
| quote.total_market_cap | Total crypto market capitalization |
| quote.total_volume_24h | Total 24-hour trading volume |
| quote.total_volume_24h_reported | Reported 24h volume (may differ from adjusted) |
| quote.total_market_cap_yesterday | Market cap 24 hours ago |
| quote.total_volume_24h_yesterday | Volume 24 hours ago |
| quote.total_market_cap_yesterday_percentage_change | 24h market cap percent change |
| quote.total_volume_24h_yesterday_percentage_change | 24h volume percent change |
| quote.altcoin_volume_24h | 24h volume excluding Bitcoin |
| quote.altcoin_volume_24h_reported | Reported altcoin volume |
| quote.altcoin_market_cap | Market cap excluding Bitcoin |
| quote.defi_volume_24h | DeFi protocol 24h volume |
| quote.defi_volume_24h_reported | Reported DeFi volume |
| quote.defi_24h_percentage_change | DeFi volume 24h change |
| quote.defi_market_cap | DeFi protocol total market cap |
| quote.stablecoin_volume_24h | Stablecoin 24h volume |
| quote.stablecoin_volume_24h_reported | Reported stablecoin volume |
| quote.stablecoin_24h_percentage_change | Stablecoin volume 24h change |
| quote.stablecoin_market_cap | Stablecoin total market cap |
| quote.derivatives_volume_24h | Derivatives 24h volume |
| quote.derivatives_volume_24h_reported | Reported derivatives volume |
| quote.derivatives_24h_percentage_change | Derivatives volume 24h change |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest?convert=USD" \
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
    "btc_dominance": 52.5,
    "eth_dominance": 17.2,
    "btc_dominance_24h_percentage_change": 0.15,
    "eth_dominance_24h_percentage_change": -0.08,
    "active_cryptocurrencies": 10234,
    "total_cryptocurrencies": 25678,
    "active_exchanges": 756,
    "total_exchanges": 1245,
    "active_market_pairs": 89432,
    "last_updated": "2024-01-15T10:25:00.000Z",
    "quote": {
      "USD": {
        "total_market_cap": 1750000000000,
        "total_volume_24h": 85000000000,
        "total_volume_24h_reported": 92000000000,
        "total_market_cap_yesterday": 1720000000000,
        "total_volume_24h_yesterday": 78000000000,
        "total_market_cap_yesterday_percentage_change": 1.74,
        "total_volume_24h_yesterday_percentage_change": 8.97,
        "altcoin_volume_24h": 42500000000,
        "altcoin_market_cap": 831250000000,
        "defi_volume_24h": 12500000000,
        "defi_market_cap": 95000000000,
        "stablecoin_volume_24h": 65000000000,
        "stablecoin_market_cap": 145000000000,
        "derivatives_volume_24h": 120000000000
      }
    }
  }
}
```

---

## Use Cases

### Market Overview Dashboard

Fetch latest global metrics to display:
1. Total market cap with 24h change
2. BTC and ETH dominance percentages
3. Active cryptocurrencies and exchanges count
4. DeFi and stablecoin market shares

### Historical Analysis

Use historical endpoint to:
1. Track market cap trends over weeks or months
2. Analyze BTC dominance cycles
3. Compare DeFi growth against total market
4. Identify volume spikes during market events

### Market Health Indicators

Combine metrics to assess:
1. Volume to market cap ratio (market activity)
2. Altcoin dominance trends (risk appetite)
3. Stablecoin market cap changes (capital inflows/outflows)
4. Derivatives volume (leverage in the market)
