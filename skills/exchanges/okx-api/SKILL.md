---
name: okx-api
description: This skill should be used when the user asks to "query OKX account balance", "place an order on OKX", "get OKX market data", "check OKX positions", "cancel OKX order", or mentions OKX exchange trading, crypto trading via OKX API. Provides guidance for interacting with OKX REST API v5 including authentication, market data, and order management.
version: 1.0.0
---

# OKX API v5 Skill

## Overview

OKX API v5 provides REST and WebSocket interfaces for spot trading, derivatives (perpetual swaps, futures, options), market data, and account management.

- **Base URL**: `https://www.okx.com`
- **API version prefix**: `/api/v5/`
- **Demo/sandbox**: same base URL, add header `x-simulated-trading: 1`
- **Auth**: HMAC SHA256 signature (private endpoints only)
- **Rate limits**: public endpoints by IP; private endpoints by User ID

All examples use `scripts/okx_auth.py` — a reusable helper that handles credential loading, signing, and response parsing.

---

## Configuration Setup

Store credentials in `~/.openclaw/openclaw.json` under the top-level `env` field. OpenClaw automatically injects these into the agent environment:

```json
{
  "env": {
    "OKX_API_KEY": "your-api-key",
    "OKX_SECRET_KEY": "your-secret-key",
    "OKX_PASSPHRASE": "your-passphrase",
    "OKX_DEMO": "1"
  }
}
```

Set `OKX_DEMO=1` to use sandbox mode (paper trading). Remove or set to `0` for live trading.

You can also export these in your shell:

```bash
export OKX_API_KEY="your-api-key"
export OKX_SECRET_KEY="your-secret-key"
export OKX_PASSPHRASE="your-passphrase"
export OKX_DEMO="1"
```

---

## Authentication

Private endpoints require four request headers:

| Header | Value |
|--------|-------|
| `OK-ACCESS-KEY` | Your API key |
| `OK-ACCESS-SIGN` | Base64(HmacSHA256(pre-sign, secret)) |
| `OK-ACCESS-TIMESTAMP` | ISO 8601 UTC timestamp with milliseconds |
| `OK-ACCESS-PASSPHRASE` | Your passphrase |
| `Content-Type` | `application/json` (POST only) |

**Signature formula**:
```
pre_sign = timestamp + METHOD + path_with_query + body
signature = base64(hmac_sha256(pre_sign, secret_key))
```

- `timestamp`: e.g. `2024-01-15T10:30:00.123Z`
- `METHOD`: uppercase GET or POST
- `path_with_query`: e.g. `/api/v5/account/balance` or `/api/v5/market/ticker?instId=BTC-USDT`
- `body`: JSON string for POST, empty string `""` for GET

**Use `scripts/okx_auth.py`** — it handles all of this automatically. See `references/authentication.md` for edge cases and error codes.

---

## Common Operations Quick Reference

| Intent | Method | Endpoint |
|--------|--------|----------|
| Get account balance | GET | `/api/v5/account/balance` |
| Get positions | GET | `/api/v5/account/positions` |
| Get ticker (spot price) | GET | `/api/v5/market/ticker?instId=BTC-USDT` |
| Get candlestick data | GET | `/api/v5/market/candles?instId=BTC-USDT&bar=1H` |
| Get order book | GET | `/api/v5/market/books?instId=BTC-USDT&sz=20` |
| Get recent trades | GET | `/api/v5/market/trades?instId=BTC-USDT` |
| Place order | POST | `/api/v5/trade/order` |
| Amend order | POST | `/api/v5/trade/amend-order` |
| Cancel order | POST | `/api/v5/trade/cancel-order` |
| Get open orders | GET | `/api/v5/trade/orders-pending` |
| Get order history | GET | `/api/v5/trade/orders-history` |
| Get instruments | GET | `/api/v5/public/instruments?instType=SPOT` |
| Get funding rate | GET | `/api/v5/public/funding-rate?instId=BTC-USDT-SWAP` |

---

## Response Handling

All REST responses follow this envelope:

```json
{
  "code": "0",
  "msg": "",
  "data": [...]
}
```

- `code: "0"` — success
- Any other code — error; check `msg` for details
- `data` is always an array (even for single objects)

**Common error codes**:

| Code | Meaning |
|------|---------|
| `50011` | Rate limit exceeded — back off and retry |
| `50111` | Invalid API key |
| `50113` | Invalid signature |
| `50114` | Timestamp out of range (±30s tolerance) |
| `51000` | Parameter error — check required fields |
| `51008` | Insufficient balance |

The `make_request()` function in `scripts/okx_auth.py` raises a `RuntimeError` when `code != "0"`, so you can catch errors cleanly.

---

## Rate Limits

OKX enforces rate limits per endpoint group:

| Category | Limit |
|----------|-------|
| Public market data | 20 req/2s per IP |
| Account endpoints | 10 req/2s per UID |
| Trade order placement | 60 req/2s per UID |
| Order cancellation | 60 req/2s per UID |

If you hit `50011`, sleep 2 seconds and retry. For bulk operations, use batch endpoints:
- `POST /api/v5/trade/batch-orders` — place up to 20 orders
- `POST /api/v5/trade/cancel-batch-orders` — cancel up to 20 orders

---

## Place Order — Key Parameters

```json
{
  "instId": "BTC-USDT",
  "tdMode": "cash",
  "side": "buy",
  "ordType": "limit",
  "px": "42000",
  "sz": "0.001"
}
```

| Field | Values |
|-------|--------|
| `instId` | `BTC-USDT` (spot), `BTC-USDT-SWAP` (perp), `BTC-USD-241227` (futures) |
| `tdMode` | `cash` (spot), `cross` (cross margin), `isolated` |
| `side` | `buy` or `sell` |
| `ordType` | `limit`, `market`, `post_only`, `fok`, `ioc` |
| `px` | Price (required for limit orders) |
| `sz` | Size in base currency (spot) or contracts (derivatives) |

See `examples/place-order.py` for a complete working example.

---

## WebSocket

For real-time data (prices, order updates, position changes), use WebSocket instead of polling REST.

- **Public**: `wss://ws.okx.com:8443/ws/v5/public`
- **Private**: `wss://ws.okx.com:8443/ws/v5/private`

Subscribe to channels by sending JSON messages. Private channels require a `login` operation first using the same HMAC signature scheme.

See `references/websocket.md` and `examples/websocket-ticker.py`.

---

## References

- `references/authentication.md` — Signature details, edge cases, auth error troubleshooting
- `references/market-data-endpoints.md` — All public REST endpoints with params and response fields
- `references/trading-endpoints.md` — All private REST endpoints, order types, instrument types
- `references/websocket.md` — WebSocket URLs, subscription format, private channel auth, common channels
- `examples/get-balance.py` — Fetch and display account balance
- `examples/get-market-data.py` — Ticker and candlestick data
- `examples/place-order.py` — Place a limit buy order
- `examples/websocket-ticker.py` — Real-time price subscription
- `scripts/okx_auth.py` — Reusable auth/request helper (import in your scripts)
