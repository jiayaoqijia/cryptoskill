# OKX API v5 — Market Data Endpoints Reference

All endpoints are public (no authentication required).

Base URL: `https://www.okx.com`

---

## Instruments

### GET /api/v5/public/instruments

List all tradeable instruments.

**Params**:
| Param | Required | Description |
|-------|----------|-------------|
| `instType` | Yes | `SPOT`, `MARGIN`, `SWAP`, `FUTURES`, `OPTION` |
| `uly` | No | Underlying (e.g. `BTC-USD`, for derivatives) |
| `instId` | No | Specific instrument ID |

**Key response fields** (per instrument):
- `instId` — e.g. `BTC-USDT`, `BTC-USDT-SWAP`
- `baseCcy` / `quoteCcy` — base and quote currencies (SPOT)
- `tickSz` — minimum price increment
- `lotSz` — minimum order size
- `minSz` — minimum order quantity
- `state` — `live`, `suspend`, `preopen`

---

## Ticker

### GET /api/v5/market/ticker

Single instrument ticker.

**Params**: `instId` (required)

**Key response fields**:
- `last` — last traded price
- `lastSz` — size of last trade
- `askPx` / `askSz` — best ask price/size
- `bidPx` / `bidSz` — best bid price/size
- `open24h` — 24h opening price
- `high24h` / `low24h` — 24h high/low
- `vol24h` — 24h volume (base currency)
- `volCcy24h` — 24h volume (quote currency)
- `ts` — timestamp (milliseconds)

### GET /api/v5/market/tickers

All tickers for an instrument type.

**Params**: `instType` (required), `uly` (optional)

---

## Order Book

### GET /api/v5/market/books

Full order book (up to 400 levels).

**Params**:
- `instId` (required)
- `sz` — depth levels (1–400, default 1)

**Response**:
```json
{
  "asks": [["price", "size", "0", "count"], ...],
  "bids": [["price", "size", "0", "count"], ...],
  "ts": "1705312200123"
}
```

### GET /api/v5/market/books-lite

Lightweight order book (5 levels, lower latency).

**Params**: same as above

---

## Trades

### GET /api/v5/market/trades

Recent trades.

**Params**:
- `instId` (required)
- `limit` — number of trades (1–500, default 100)

**Key response fields** (per trade):
- `tradeId`, `price`, `sz`, `side` (`buy`/`sell`), `ts`

---

## Candlesticks

### GET /api/v5/market/candles

Recent candlestick data (up to 300 candles).

**Params**:
- `instId` (required)
- `bar` — timeframe (default `1m`)
- `before` / `after` — pagination by timestamp
- `limit` — number of candles (1–300)

**Bar values**: `1s`, `1m`, `3m`, `5m`, `15m`, `30m`, `1H`, `2H`, `4H`, `6H`, `12H`, `1D`, `1W`, `1M`, `3M`

**Response format** (each candle is an array):
```
[timestamp, open, high, low, close, vol, volCcy, volCcyQuote, confirm]
```
- `confirm`: `"0"` = incomplete (current candle), `"1"` = confirmed (closed)

### GET /api/v5/market/history-candles

Historical candlesticks beyond 300 candles (same params).

---

## Funding Rate

### GET /api/v5/public/funding-rate

Current funding rate for perpetual swaps.

**Params**: `instId` (required, must be SWAP type, e.g. `BTC-USDT-SWAP`)

**Key response fields**:
- `fundingRate` — current funding rate
- `nextFundingRate` — estimated next funding rate
- `fundingTime` — next settlement timestamp (milliseconds)

### GET /api/v5/public/funding-rate-history

Historical funding rates.

**Params**: `instId` (required), `before`/`after`, `limit` (1–100, default 100)

---

## Index & Mark Price

### GET /api/v5/market/index-tickers

Index price (composite of exchange prices).

**Params**: `quoteCcy` (e.g. `USD`, `USDT`) or `instId`

### GET /api/v5/public/mark-price

Mark price (used for liquidation calculation).

**Params**: `instType` (required), `instId` (optional)

---

## Open Interest

### GET /api/v5/public/open-interest

Open interest for derivatives.

**Params**: `instType` (required, `SWAP`/`FUTURES`/`OPTION`), `instId` (optional)

**Key response fields**: `oi` (contracts), `oiCcy` (base currency), `ts`

---

## Notes

- All public endpoints do not require authentication headers.
- Rate limit: 20 requests per 2 seconds per IP for most market data endpoints.
- `instId` format:
  - Spot: `BTC-USDT`
  - Perpetual swap: `BTC-USDT-SWAP`
  - Futures: `BTC-USD-YYMMDD` (e.g. `BTC-USD-241227`)
  - Option: `BTC-USD-241227-50000-C`
