# Exchange Assets API

## Exchange Assets

**Path:** `GET /v1/exchange/assets`

**Description:** Returns a list of all cryptocurrency assets held by an exchange. This endpoint provides transparency into exchange reserves and holdings when available. Useful for verifying proof-of-reserves data.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| id | string | No* | Exchange ID |
| slug | string | No* | Exchange slug |

*At least one of `id` or `slug` is required.

### Response Fields

| Field | Description |
|-------|-------------|
| id | Exchange ID |
| name | Exchange name |
| slug | Exchange slug |
| assets | Array of asset holdings |
| assets[].wallet_address | Wallet address holding the asset |
| assets[].balance | Current balance in the wallet |
| assets[].platform | Blockchain platform details |
| assets[].platform.crypto_id | CoinMarketCap ID of the platform |
| assets[].platform.name | Platform name (e.g., "Ethereum") |
| assets[].platform.symbol | Platform symbol (e.g., "ETH") |
| assets[].currency | Currency details |
| assets[].currency.crypto_id | CoinMarketCap ID of the asset |
| assets[].currency.name | Asset name |
| assets[].currency.symbol | Asset symbol |
| assets[].currency.price_usd | Current USD price |
| assets[].usd_value | Total USD value of holdings |
| assets[].last_updated | Timestamp of last balance update |

### Example

```bash
# Get assets for Binance by ID
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/assets?id=270" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get assets by exchange slug
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/assets?slug=binance" \
  -H "X-CMC_PRO_API_KEY: your-api-key"

# Get assets for Coinbase
curl -X GET "https://pro-api.coinmarketcap.com/v1/exchange/assets?slug=coinbase-exchange" \
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
    "assets": [
      {
        "wallet_address": "0x28C6c06298d514Db089934071355E5743bf21d60",
        "balance": 248597.52,
        "platform": {
          "crypto_id": 1027,
          "name": "Ethereum",
          "symbol": "ETH"
        },
        "currency": {
          "crypto_id": 1027,
          "name": "Ethereum",
          "symbol": "ETH",
          "price_usd": 2500.00
        },
        "usd_value": 621493800.00,
        "last_updated": "2024-01-15T12:00:00.000Z"
      },
      {
        "wallet_address": "bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h",
        "balance": 125000.00,
        "platform": {
          "crypto_id": 1,
          "name": "Bitcoin",
          "symbol": "BTC"
        },
        "currency": {
          "crypto_id": 1,
          "name": "Bitcoin",
          "symbol": "BTC",
          "price_usd": 42500.00
        },
        "usd_value": 5312500000.00,
        "last_updated": "2024-01-15T12:00:00.000Z"
      },
      {
        "wallet_address": "0x28C6c06298d514Db089934071355E5743bf21d60",
        "balance": 2500000000.00,
        "platform": {
          "crypto_id": 1027,
          "name": "Ethereum",
          "symbol": "ETH"
        },
        "currency": {
          "crypto_id": 825,
          "name": "Tether USDt",
          "symbol": "USDT",
          "price_usd": 1.00
        },
        "usd_value": 2500000000.00,
        "last_updated": "2024-01-15T12:00:00.000Z"
      }
    ]
  }
}
```

### Notes

1. Not all exchanges provide proof-of-reserves data. This endpoint returns data only for participating exchanges.
2. The `platform` field indicates which blockchain the asset is held on. A single asset (like USDT) may appear multiple times across different chains.
3. The `wallet_address` can be verified independently on block explorers.
4. The `usd_value` is calculated as `balance * price_usd` at the time of the last update.
5. Assets are typically updated periodically, not in real-time. Check `last_updated` for data freshness.
6. This data is particularly useful for:
   - Proof-of-reserves verification
   - Tracking large exchange holdings
   - Monitoring exchange wallet movements
   - Assessing exchange solvency and transparency
