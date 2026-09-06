# Hyperliquid HyperCore (off-chain trading)

**Base URL:** `https://api.allium.so` · **Auth:** `X-API-KEY: $API_KEY`

Hyperliquid has two distinct surfaces:

- **HyperCore** — the off-chain CLOB matching engine (orders, fills, positions, funding, orderbook). **This doc covers HyperCore.**
- **HyperEVM** — the on-chain EVM L1 smart contract layer (chain ID 999, gas paid in HYPE). **Use Alchemy for HyperEVM** at `https://hyperliquid-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY` (via `alchemy-api` or `alchemy-cli`).

---

## Info (general proxy)

`POST /api/v1/developer/trading/hyperliquid/info`

Hyperliquid `info` API exposed without Hyperliquid's native rate limits.

### Request

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | string | No | Request type (Hyperliquid info type) |
| `user` | string | No | User address |
| `dex` | string | No | DEX parameter |

```bash
curl -X POST "https://api.allium.so/api/v1/developer/trading/hyperliquid/info" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{"type": "...", "user": "0x..."}'
```

---

## Fills

`POST /api/v1/developer/trading/hyperliquid/info/fills`

Fills by user wallet address.

### Request

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | string | Yes | Fill type — `userFills`, `userFillsByTime` |
| `user` | string | Yes | User wallet address (hex) |
| `startTime` | int | No | Start (Unix ms) — required for `userFillsByTime` |
| `endTime` | int | No | End (Unix ms) — only `userFillsByTime` |
| `aggregateByTime` | bool | No | Combine fills from same order/timestamp into one (size, weighted-avg price, summed fees/PnL) |
| `twapMode` | string | No | `none` (default), `include`, `only` — controls TWAP fill filtering |

### Example

```bash
curl -X POST "https://api.allium.so/api/v1/developer/trading/hyperliquid/info/fills" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{"type": "userFills", "user": "0x..."}'
```

### Key response fields

Each item:
- `coin` — trading pair symbol
- `side` — `B` (buy) / `A` (sell)
- `dir` — direction (e.g. `Open Long`, `Close Short`)
- `px`, `sz` — execution price and fill size
- `fee`, `feeToken` — trading fee
- `closedPnl` — realized PnL from closing a position
- `crossed` — whether this was a taker order
- `liquidation` — present only for liquidation fills
- `twapId` — if part of a TWAP order
- `time` — fill timestamp (Unix ms)
- `hash`, `oid`, `tid` — tx hash, order id, trade id

---

## Order history

`POST /api/v1/developer/trading/hyperliquid/info/order/history`

Historical orders by user.

### Request

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | string | Yes | Must be `historicalOrders` |
| `user` | string | Yes | User wallet address (hex) |
| `startTime` | int | No | Start (Unix ms) |
| `endTime` | int | No | End (Unix ms) |

```bash
curl -X POST "https://api.allium.so/api/v1/developer/trading/hyperliquid/info/order/history" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{"type": "historicalOrders", "user": "0x..."}'
```

### Key response fields

Each item:
- `order.coin`, `order.side`, `order.limitPx`, `order.sz`, `order.origSz`
- `order.oid`, `order.cloid`
- `order.timestamp`
- `order.orderType`, `order.tif` (time-in-force)
- `order.isTrigger`, `order.triggerPx`, `order.triggerCondition` — for conditional orders
- `order.isPositionTpsl`, `order.reduceOnly`
- `status`, `statusTimestamp`

---

## Order status

`POST /api/v1/developer/trading/hyperliquid/info/order/status`

Status of a specific order by ID.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | string | Yes | Must be `orderStatus` |
| `user` | string | Yes | User wallet address (hex) |
| `oid` | int or string | Yes | Order ID (numeric `oid` or string client `cloid`) |

```bash
curl -X POST "https://api.allium.so/api/v1/developer/trading/hyperliquid/info/order/status" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{"type": "orderStatus", "user": "0x...", "oid": 12345}'
```

---

## L4 orderbook snapshot

`GET /api/v1/developer/trading/hyperliquid/orderbook/snapshot`

Full orderbook snapshot for all pairs.

```bash
curl -X GET "https://api.allium.so/api/v1/developer/trading/hyperliquid/orderbook/snapshot" \
  -H "X-API-KEY: $API_KEY"
```

---

## When to route elsewhere

| Need | Use instead |
| --- | --- |
| HyperCore trading data (orders, fills, positions, funding, orderbook) | These endpoints |
| HyperEVM smart contract reads/writes / live EVM RPC (chain ID 999) | `alchemy-api` or `alchemy-cli` at `https://hyperliquid-mainnet.g.alchemy.com/v2/$ALCHEMY_API_KEY` |
| Historical / indexed HyperEVM analytics (cross-chain queries, MEV on HyperEVM, labeled wallets, etc.) | Allium custom SQL via the `hyperevm` chain name — see [custom-sql.md](./custom-sql.md) |

HyperCore (off-chain matching) and HyperEVM (on-chain smart contracts) are separate products of the Hyperliquid ecosystem with different APIs. Don't conflate them.
