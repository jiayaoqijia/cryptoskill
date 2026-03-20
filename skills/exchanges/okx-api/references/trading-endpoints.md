# OKX API v5 — Trading Endpoints Reference

All endpoints require authentication. See `authentication.md` for signing details.

---

## Account

### GET /api/v5/account/balance

Account equity and per-currency balances.

**Params**: `ccy` (optional, comma-separated, e.g. `BTC,ETH`)

**Key response fields** (account object):
- `totalEq` — total equity in USD
- `adjEq` — adjusted equity (risk-adjusted)
- `imr` — initial margin requirement
- `mmr` — maintenance margin requirement
- `details[]` — per-currency breakdown:
  - `ccy`, `eq` (equity), `availEq` (available), `frozenBal`, `upl` (unrealized PnL)

### GET /api/v5/account/positions

Open positions.

**Params**:
- `instType` — `MARGIN`, `SWAP`, `FUTURES`, `OPTION` (optional)
- `instId` — specific instrument (optional)
- `posId` — specific position ID (optional)

**Key response fields** (per position):
- `instId`, `instType`, `mgnMode` (`cross`/`isolated`)
- `pos` — position size (positive = long, negative = short)
- `avgPx` — average entry price
- `upl` — unrealized PnL
- `uplRatio` — unrealized PnL ratio
- `liqPx` — estimated liquidation price
- `lever` — leverage
- `adl` — auto-deleverage indicator (1–5)

### GET /api/v5/account/positions-history

Closed position history.

**Params**: `instType`, `instId`, `mgnMode`, `type`, `posId`, `after`, `before`, `limit` (1–100)

---

## Order Management

### POST /api/v5/trade/order

Place a single order.

**Required body fields**:
| Field | Description |
|-------|-------------|
| `instId` | Instrument ID (e.g. `BTC-USDT`) |
| `tdMode` | Trade mode: `cash` (spot), `cross`, `isolated` |
| `side` | `buy` or `sell` |
| `ordType` | Order type (see table below) |
| `sz` | Order size (base currency for spot, contracts for derivatives) |

**Conditional fields**:
| Field | When required |
|-------|---------------|
| `px` | Required for `limit`, `post_only`, `fok`, `ioc` |
| `ccy` | Required for MARGIN cross orders (currency to borrow) |
| `tgtCcy` | `base_ccy` or `quote_ccy` (market orders only — specify which currency `sz` refers to) |
| `clOrdId` | Optional client order ID (max 32 chars, alphanumeric + `-_`) |

**Order types**:
| `ordType` | Description |
|-----------|-------------|
| `market` | Market order — fills immediately at best price |
| `limit` | Limit order — fills at `px` or better |
| `post_only` | Maker-only limit — rejected if it would immediately fill |
| `fok` | Fill-or-kill — fill entirely or cancel |
| `ioc` | Immediate-or-cancel — fill what's available, cancel remainder |
| `optimal_limit_ioc` | Market order with limit price protection |

**Response** (per order in `data` array):
- `ordId` — exchange order ID
- `clOrdId` — client order ID
- `sCode` — `"0"` success, otherwise error code
- `sMsg` — error message if failed

### POST /api/v5/trade/batch-orders

Place up to 20 orders in one request.

**Body**: JSON array of order objects (same fields as single order).

### POST /api/v5/trade/cancel-order

Cancel a single order.

**Body**:
```json
{
  "instId": "BTC-USDT",
  "ordId": "123456789"
}
```
Use `clOrdId` instead of `ordId` if you set a client order ID.

### POST /api/v5/trade/cancel-batch-orders

Cancel up to 20 orders.

**Body**: JSON array of cancel objects.

### POST /api/v5/trade/amend-order

Modify an existing unfilled order.

**Body**:
```json
{
  "instId": "BTC-USDT",
  "ordId": "123456789",
  "newPx": "41000",
  "newSz": "0.002"
}
```

---

## Order Queries

### GET /api/v5/trade/order

Get a single order by ID.

**Params**: `instId` (required), `ordId` or `clOrdId` (one required)

**Key response fields**:
- `ordId`, `clOrdId`, `instId`, `side`, `ordType`
- `px` (price), `sz` (size), `fillSz` (filled), `avgPx` (avg fill price)
- `state` — `live`, `partially_filled`, `filled`, `canceled`
- `fee`, `feeCcy`
- `cTime` (create time), `uTime` (update time)

### GET /api/v5/trade/orders-pending

All open/pending orders.

**Params**: `instType`, `instId`, `ordType`, `state`, `after`, `before`, `limit` (1–100)

### GET /api/v5/trade/orders-history

Recent order history (last 7 days).

**Params**: `instType` (required), `instId`, `ordType`, `state`, `after`, `before`, `limit` (1–100)

### GET /api/v5/trade/orders-history-archive

Order history beyond 7 days (up to 3 months).

Same params as above.

---

## Instrument Types

| `instType` | Description | Example `instId` |
|------------|-------------|------------------|
| `SPOT` | Spot trading | `BTC-USDT` |
| `MARGIN` | Margin trading | `BTC-USDT` with `tdMode: cross` |
| `SWAP` | Perpetual futures | `BTC-USDT-SWAP`, `BTC-USD-SWAP` |
| `FUTURES` | Delivery futures | `BTC-USD-241227` |
| `OPTION` | Options | `BTC-USD-241227-50000-C` |

**USDT-margined vs coin-margined**:
- `BTC-USDT-SWAP` — linear, settled in USDT
- `BTC-USD-SWAP` — inverse, settled in BTC
- `sz` unit: number of contracts (each contract = 0.01 BTC for BTC-USDT-SWAP)

Check `GET /api/v5/public/instruments` for `ctVal` (contract value) and `ctMult` per instrument.

---

## Trade Mode (`tdMode`)

| Mode | Description |
|------|-------------|
| `cash` | Spot trading (no leverage) |
| `cross` | Cross margin (shared collateral pool) |
| `isolated` | Isolated margin (per-position collateral) |

For spot orders, always use `cash`. For derivatives, use `cross` or `isolated`.
