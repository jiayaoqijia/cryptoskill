# OKX API v5 — WebSocket Reference

## Base URLs

| Channel | URL |
|---------|-----|
| Public | `wss://ws.okx.com:8443/ws/v5/public` |
| Private | `wss://ws.okx.com:8443/ws/v5/private` |
| Business (public) | `wss://ws.okx.com:8443/ws/v5/business` |

**Demo/sandbox**: same URLs, but authenticate with demo API key and credentials.

---

## Connection Management

- Send a `ping` text frame every 20–25 seconds to keep the connection alive. OKX responds with `pong`.
- If no message is received for 30 seconds, reconnect.
- Max subscriptions per connection: 240 channels.

---

## Subscribe / Unsubscribe

```json
{
  "op": "subscribe",
  "args": [
    { "channel": "tickers", "instId": "BTC-USDT" },
    { "channel": "tickers", "instId": "ETH-USDT" }
  ]
}
```

**Confirmation response**:
```json
{
  "event": "subscribe",
  "arg": { "channel": "tickers", "instId": "BTC-USDT" }
}
```

**Error response**:
```json
{
  "event": "error",
  "code": "60012",
  "msg": "Invalid request: invalid arg instId:BTC-USDT"
}
```

To unsubscribe, use `"op": "unsubscribe"` with the same args.

---

## Private Channel Authentication

Private channels require logging in first. Send a `login` op immediately after connecting:

```json
{
  "op": "login",
  "args": [{
    "apiKey": "your_api_key",
    "passphrase": "your_passphrase",
    "timestamp": "1705312200",
    "sign": "computed_signature"
  }]
}
```

**Signature** (different from REST auth):
```
pre_sign = timestamp + "GET" + "/users/self/verify" + ""
signature = base64(hmac_sha256(pre_sign, secret_key))
```
- `timestamp`: Unix seconds as a string (not ISO format)
- `/users/self/verify`: fixed constant path

**Login success response**:
```json
{ "event": "login", "code": "0", "msg": "" }
```

Subscribe to private channels after receiving the login success event.

---

## Public Channels

### tickers
Real-time best bid/ask and last price.

```json
{ "channel": "tickers", "instId": "BTC-USDT" }
```

**Push data fields**: `instId`, `last`, `lastSz`, `askPx`, `askSz`, `bidPx`, `bidSz`, `open24h`, `high24h`, `low24h`, `vol24h`, `volCcy24h`, `ts`

### candle{bar}
Real-time candlestick updates.

```json
{ "channel": "candle1H", "instId": "BTC-USDT" }
```

Bar values: `candle1s`, `candle1m`, `candle5m`, `candle15m`, `candle30m`, `candle1H`, `candle4H`, `candle1D`, etc.

**Push data**: `[timestamp, open, high, low, close, vol, volCcy, volCcyQuote, confirm]`

### trades
Real-time trade stream.

```json
{ "channel": "trades", "instId": "BTC-USDT" }
```

**Push data fields**: `instId`, `tradeId`, `px`, `sz`, `side`, `ts`

### books
Real-time order book (snapshot + incremental updates).

```json
{ "channel": "books", "instId": "BTC-USDT" }
```

Push type `"snapshot"` on first message, then `"update"` for changes. Apply updates as diffs to your local book. A size of `"0"` means the price level was removed.

### books5
Top-5 order book levels (always full snapshot, no incremental).

### funding-rate
Funding rate updates for perpetual swaps.

```json
{ "channel": "funding-rate", "instId": "BTC-USDT-SWAP" }
```

### mark-price
Mark price updates.

```json
{ "channel": "mark-price", "instId": "BTC-USDT-SWAP" }
```

---

## Private Channels

All require login (see above).

### orders
Real-time order updates for all your orders.

```json
{ "channel": "orders", "instType": "ANY" }
```

Use `instType`: `SPOT`, `MARGIN`, `SWAP`, `FUTURES`, `OPTION`, or `ANY`.

**Push data fields**: `ordId`, `clOrdId`, `instId`, `side`, `ordType`, `px`, `sz`, `fillSz`, `avgPx`, `state`, `fee`, `feeCcy`, `uTime`

### positions
Real-time position updates.

```json
{ "channel": "positions", "instType": "ANY" }
```

**Push data fields**: same as REST positions response (`pos`, `avgPx`, `upl`, `liqPx`, etc.)

### account
Real-time account balance updates.

```json
{ "channel": "account", "ccy": "BTC" }
```

Omit `ccy` to receive updates for all currencies.

### balance_and_position
Combined account and position push (lower latency than separate channels).

```json
{ "channel": "balance_and_position" }
```

---

## Message Format

All push messages follow this structure:

```json
{
  "arg": { "channel": "tickers", "instId": "BTC-USDT" },
  "action": "snapshot",
  "data": [{ ... }]
}
```

- `action`: `"snapshot"` (full state) or `"update"` (incremental diff)
- `data`: array of objects; parse each element for the relevant fields

---

## Common Error Codes

| Code | Meaning |
|------|---------|
| `60001` | Invalid op |
| `60012` | Invalid args |
| `60014` | Connection limit reached |
| `60018` | Token expired (reconnect and re-login) |
| `60019` | Not logged in (subscribe to private channel without login) |
