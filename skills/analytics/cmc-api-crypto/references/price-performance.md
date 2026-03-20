# Price Performance API Reference

## Price Performance Stats Latest

**Path:** `GET /v2/cryptocurrency/price-performance-stats/latest`

**Description:** Returns price performance statistics for one or more cryptocurrencies including all-time high/low, price changes over multiple timeframes, and percentage from ATH. Useful for understanding historical context of current prices.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | Conditional | One or more comma-separated CMC IDs |
| slug | string | Conditional | One or more comma-separated slugs |
| symbol | string | Conditional | One or more comma-separated symbols |
| time_period | string | No | Time periods to return: all_time, yesterday, 24h, 7d, 30d, 90d, 365d, ytd. Pass multiple comma-separated. Default: all_time |
| convert | string | No | Currency to convert prices (e.g., USD, BTC) |
| convert_id | string | No | CMC ID of currency to convert to |
| skip_invalid | boolean | No | Skip invalid IDs instead of erroring. Default: false |

**Note:** At least one of `id`, `slug`, or `symbol` is required.

### Response Fields

| Field | Description |
|-------|-------------|
| data[id].id | CMC cryptocurrency ID |
| data[id].name | Cryptocurrency name |
| data[id].symbol | Cryptocurrency symbol |
| data[id].slug | URL slug |
| data[id].last_updated | Last update timestamp |
| data[id].periods | Object containing stats for each time period |
| data[id].periods.all_time.open_timestamp | First recorded timestamp |
| data[id].periods.all_time.high_timestamp | All-time high timestamp |
| data[id].periods.all_time.low_timestamp | All-time low timestamp |
| data[id].periods.all_time.close_timestamp | Current timestamp |
| data[id].periods.all_time.quote.USD.open | First recorded price |
| data[id].periods.all_time.quote.USD.open_timestamp | Open price timestamp |
| data[id].periods.all_time.quote.USD.high | All-time high price |
| data[id].periods.all_time.quote.USD.high_timestamp | ATH timestamp |
| data[id].periods.all_time.quote.USD.low | All-time low price |
| data[id].periods.all_time.quote.USD.low_timestamp | ATL timestamp |
| data[id].periods.all_time.quote.USD.close | Current price |
| data[id].periods.all_time.quote.USD.close_timestamp | Current timestamp |
| data[id].periods.all_time.quote.USD.percent_change | % change since open |
| data[id].periods.all_time.quote.USD.price_change | Absolute price change |
| data[id].periods.24h.quote.USD.open | Price 24h ago |
| data[id].periods.24h.quote.USD.high | 24h high |
| data[id].periods.24h.quote.USD.low | 24h low |
| data[id].periods.24h.quote.USD.close | Current price |
| data[id].periods.24h.quote.USD.percent_change | 24h % change |
| data[id].periods.7d.quote.USD.percent_change | 7d % change |
| data[id].periods.30d.quote.USD.percent_change | 30d % change |
| data[id].periods.90d.quote.USD.percent_change | 90d % change |
| data[id].periods.365d.quote.USD.percent_change | 1 year % change |
| data[id].periods.ytd.quote.USD.percent_change | Year-to-date % change |

### Example

```bash
# Get all-time stats for Bitcoin
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/price-performance-stats/latest?id=1&time_period=all_time" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get multiple timeframes for multiple coins
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/price-performance-stats/latest?id=1,1027&time_period=all_time,24h,7d,30d,90d,365d" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get year-to-date performance
curl -X GET "https://pro-api.coinmarketcap.com/v2/cryptocurrency/price-performance-stats/latest?symbol=BTC,ETH,SOL&time_period=ytd" \
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
    "1": {
      "id": 1,
      "name": "Bitcoin",
      "symbol": "BTC",
      "slug": "bitcoin",
      "last_updated": "2024-01-15T12:00:00.000Z",
      "periods": {
        "all_time": {
          "open_timestamp": "2010-07-13T00:00:00.000Z",
          "high_timestamp": "2021-11-10T00:00:00.000Z",
          "low_timestamp": "2010-07-13T00:00:00.000Z",
          "close_timestamp": "2024-01-15T12:00:00.000Z",
          "quote": {
            "USD": {
              "open": 0.0008,
              "open_timestamp": "2010-07-13T00:00:00.000Z",
              "high": 69044.77,
              "high_timestamp": "2021-11-10T00:00:00.000Z",
              "low": 0.0008,
              "low_timestamp": "2010-07-13T00:00:00.000Z",
              "close": 42567.89,
              "close_timestamp": "2024-01-15T12:00:00.000Z",
              "percent_change": 5320986150.0,
              "price_change": 42567.8892
            }
          }
        },
        "24h": {
          "open_timestamp": "2024-01-14T12:00:00.000Z",
          "high_timestamp": "2024-01-14T18:30:00.000Z",
          "low_timestamp": "2024-01-14T06:15:00.000Z",
          "close_timestamp": "2024-01-15T12:00:00.000Z",
          "quote": {
            "USD": {
              "open": 41567.89,
              "high": 43200.00,
              "low": 41200.00,
              "close": 42567.89,
              "percent_change": 2.41,
              "price_change": 1000.00
            }
          }
        },
        "7d": {
          "open_timestamp": "2024-01-08T12:00:00.000Z",
          "close_timestamp": "2024-01-15T12:00:00.000Z",
          "quote": {
            "USD": {
              "open": 40234.56,
              "high": 43500.00,
              "low": 39800.00,
              "close": 42567.89,
              "percent_change": 5.80,
              "price_change": 2333.33
            }
          }
        },
        "30d": {
          "quote": {
            "USD": {
              "open": 37000.00,
              "high": 44000.00,
              "low": 36500.00,
              "close": 42567.89,
              "percent_change": 15.05,
              "price_change": 5567.89
            }
          }
        },
        "90d": {
          "quote": {
            "USD": {
              "percent_change": 45.67
            }
          }
        },
        "365d": {
          "quote": {
            "USD": {
              "percent_change": 156.78
            }
          }
        },
        "ytd": {
          "quote": {
            "USD": {
              "open": 42000.00,
              "close": 42567.89,
              "percent_change": 1.35
            }
          }
        }
      }
    }
  }
}
```

### Important Notes

1. **ATH/ATL context**: The `all_time` period gives you all-time high and low prices with timestamps. Calculate "% from ATH" as: `(close - high) / high * 100`.

2. **Time periods**: Available periods are:
   - `all_time`: Since first listing
   - `yesterday`: Previous UTC day
   - `24h`: Rolling 24 hours
   - `7d`: Rolling 7 days
   - `30d`: Rolling 30 days
   - `90d`: Rolling 90 days
   - `365d`: Rolling 365 days
   - `ytd`: Year-to-date (from Jan 1)

3. **Multiple periods**: Request multiple periods in one call by comma-separating them in the `time_period` parameter.

4. **Use cases**:
   - Compare current price to ATH to gauge potential upside
   - Track YTD performance for year-over-year comparisons
   - Identify coins recovering from lows (close near ATL but improving)

5. **Data availability**: Newer coins will have limited historical data. The `all_time` period starts from when CMC began tracking.

6. **Price change vs percent change**: `price_change` is the absolute dollar change. `percent_change` is the percentage change. Both are provided for convenience.
