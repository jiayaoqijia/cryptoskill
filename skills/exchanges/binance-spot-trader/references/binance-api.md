# Binance REST API Reference

## Base URL
`https://api.binance.com`

## Authentication
- API key in header: `X-MBX-APIKEY`
- HMAC SHA256 signature of query string using secret key
- Timestamp required within 5000ms of server time

## Key Endpoints
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/v3/ticker/price` | No | Current price |
| GET | `/api/v3/klines` | No | Candlestick data |
| GET | `/api/v3/account` | Yes | Account balances |
| POST | `/api/v3/order` | Yes | Place order |
| GET | `/api/v3/openOrders` | Yes | Open orders |
| DELETE | `/api/v3/order` | Yes | Cancel order |

## Order Types
- `MARKET` — immediate execution at best price
- `LIMIT` — execute at specified price or better
- `STOP_LOSS_LIMIT` — triggered stop loss

## Minimum Order
- Most pairs: $10 USDT equivalent
- Check `/api/v3/exchangeInfo` for exact filters per symbol
