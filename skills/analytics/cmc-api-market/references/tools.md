# Tools API Reference

Utility endpoints for fiat currency mapping, API key information, and currency conversion.

## Fiat Currency Map

**Path:** `GET /v1/fiat/map`

**Description:** Returns a mapping of all supported fiat currencies with their CMC IDs. Use this to identify the correct ID for fiat conversions and display formatting.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| start | integer | No | Offset for pagination. Default: 1 |
| limit | integer | No | Number of results to return. Default: 100, Max: 5000 |
| sort | string | No | Sort field. Options: id, name. Default: id |
| include_metals | boolean | No | Include precious metals (gold, silver, etc.). Default: false |

### Response Fields

| Field | Description |
|-------|-------------|
| data | Array of fiat currency objects |
| data[].id | CMC fiat currency ID |
| data[].name | Full currency name (e.g., "United States Dollar") |
| data[].sign | Currency symbol (e.g., "$", "€", "£") |
| data[].symbol | Currency code (e.g., USD, EUR, GBP) |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/fiat/map?limit=10&include_metals=true" \
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
  "data": [
    {
      "id": 2781,
      "name": "United States Dollar",
      "sign": "$",
      "symbol": "USD"
    },
    {
      "id": 2790,
      "name": "Euro",
      "sign": "€",
      "symbol": "EUR"
    },
    {
      "id": 2791,
      "name": "Pound Sterling",
      "sign": "£",
      "symbol": "GBP"
    },
    {
      "id": 3575,
      "name": "Gold Troy Ounce",
      "sign": "",
      "symbol": "XAU"
    }
  ]
}
```

### Common Fiat IDs

| ID | Symbol | Name |
|----|--------|------|
| 2781 | USD | United States Dollar |
| 2790 | EUR | Euro |
| 2791 | GBP | Pound Sterling |
| 2792 | JPY | Japanese Yen |
| 2793 | AUD | Australian Dollar |
| 2794 | CAD | Canadian Dollar |
| 2795 | CHF | Swiss Franc |
| 2796 | CNY | Chinese Yuan |
| 2797 | HKD | Hong Kong Dollar |
| 2798 | NZD | New Zealand Dollar |
| 2801 | INR | Indian Rupee |
| 2806 | KRW | South Korean Won |
| 3575 | XAU | Gold Troy Ounce |
| 3574 | XAG | Silver Troy Ounce |

---

## API Key Info

**Path:** `GET /v1/key/info`

**Description:** Returns information about your API key including plan details, credit usage, and rate limits. Essential for monitoring API consumption and staying within limits.

### Parameters

This endpoint has no parameters.

### Response Fields

| Field | Description |
|-------|-------------|
| plan | API plan information |
| plan.credit_limit_daily | Daily credit limit |
| plan.credit_limit_daily_reset | Time of daily reset (UTC) |
| plan.credit_limit_daily_reset_timestamp | Unix timestamp of reset |
| plan.credit_limit_monthly | Monthly credit limit |
| plan.credit_limit_monthly_reset | Time of monthly reset |
| plan.credit_limit_monthly_reset_timestamp | Unix timestamp of reset |
| plan.rate_limit_minute | Requests per minute limit |
| usage | Current usage statistics |
| usage.current_minute | Object with current minute usage |
| usage.current_minute.requests_made | Requests made this minute |
| usage.current_minute.requests_left | Requests remaining this minute |
| usage.current_day | Object with current day usage |
| usage.current_day.credits_used | Credits used today |
| usage.current_day.credits_left | Credits remaining today |
| usage.current_month | Object with current month usage |
| usage.current_month.credits_used | Credits used this month |
| usage.current_month.credits_left | Credits remaining this month |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v1/key/info" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

### Example Response

```json
{
  "status": {
    "timestamp": "2024-01-15T10:30:00.000Z",
    "error_code": 0,
    "error_message": null,
    "credit_count": 0
  },
  "data": {
    "plan": {
      "credit_limit_daily": 333,
      "credit_limit_daily_reset": "2024-01-16T00:00:00.000Z",
      "credit_limit_daily_reset_timestamp": 1705363200,
      "credit_limit_monthly": 10000,
      "credit_limit_monthly_reset": "2024-02-01T00:00:00.000Z",
      "credit_limit_monthly_reset_timestamp": 1706745600,
      "rate_limit_minute": 30
    },
    "usage": {
      "current_minute": {
        "requests_made": 5,
        "requests_left": 25
      },
      "current_day": {
        "credits_used": 150,
        "credits_left": 183
      },
      "current_month": {
        "credits_used": 2500,
        "credits_left": 7500
      }
    }
  }
}
```

---

## Price Conversion

**Path:** `GET /v2/tools/price-conversion`

**Description:** Converts an amount from one currency to another. Supports conversions between cryptocurrencies and fiat currencies in any direction.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| amount | number | Yes | Amount to convert |
| id | string | Yes* | CMC ID of source currency. Required if symbol not provided |
| symbol | string | Yes* | Symbol of source currency. Required if id not provided |
| time | string | No | Historical time for conversion (ISO 8601). Default: current time |
| convert | string | No | Target currency symbol. Default: USD |
| convert_id | string | No | CMC ID of target currency (alternative to convert) |

### Response Fields

| Field | Description |
|-------|-------------|
| id | CMC ID of source currency |
| symbol | Symbol of source currency |
| name | Name of source currency |
| amount | Original amount converted |
| last_updated | Timestamp of price data used |
| quote | Conversion results |
| quote[CURRENCY].price | Converted price per unit |
| quote[CURRENCY].last_updated | Price timestamp |

### Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v2/tools/price-conversion?amount=1&symbol=BTC&convert=USD,EUR" \
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
    "id": 1,
    "symbol": "BTC",
    "name": "Bitcoin",
    "amount": 1,
    "last_updated": "2024-01-15T10:25:00.000Z",
    "quote": {
      "USD": {
        "price": 43250.00,
        "last_updated": "2024-01-15T10:25:00.000Z"
      },
      "EUR": {
        "price": 39850.00,
        "last_updated": "2024-01-15T10:25:00.000Z"
      }
    }
  }
}
```

### Historical Conversion Example

```bash
curl -X GET "https://pro-api.coinmarketcap.com/v2/tools/price-conversion?amount=10&symbol=ETH&convert=USD&time=2024-01-01T00:00:00Z" \
  -H "X-CMC_PRO_API_KEY: your-api-key"
```

---

## Use Cases

### Multi-Currency Display

Display prices in user's preferred currency:
1. Get fiat map to build currency selector
2. Use price conversion to show values in selected currency
3. Cache conversion rates for performance

### Portfolio Valuation

Calculate portfolio value in different currencies:
1. Convert each holding to USD (or base currency)
2. Optionally convert total to user's local currency
3. Use historical conversions for past portfolio values

### API Usage Monitoring

Track and optimize API usage:
1. Check key info at application start
2. Monitor credits used vs remaining
3. Implement request throttling near limits

### Invoice Generation

Generate crypto invoices:
1. Convert fiat amount to crypto equivalent
2. Use current conversion rate
3. Display both values with rate timestamp

### Historical Analysis

Analyze historical values:
1. Use time parameter in price conversion
2. Calculate historical portfolio values
3. Track value changes over time
