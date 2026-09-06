# Wallet PnL & Holdings History

**Base URL:** `https://api.allium.so` · **Auth:** `X-API-KEY: $API_KEY`

For current balance snapshots and transaction transfers, route to `alchemy-api` (Portfolio, Token, Transfers APIs). For **historical balances** (per-block or as a timeseries), also route to `alchemy-api` — derivable via archive RPC (`eth_call balanceOf` at a historical block) or by reducing `alchemy_getAssetTransfers` history.

---

## Current PnL by wallet

`POST /api/v1/developer/wallet/pnl`

Returns realized + unrealized PnL for one or more wallets, with per-token breakdown plus aggregate totals.

### Request

Body is an array of `{chain, address}` objects.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `chain` | string | Yes | Lowercase chain name (`ethereum`, `solana`, ...) |
| `address` | string | Yes | Wallet address |

Optional query params:

| Field | Type | Description |
| --- | --- | --- |
| `min_liquidity` | number | Minimum USD liquidity for a token to be included |

### Example

```bash
curl -X POST "https://api.allium.so/api/v1/developer/wallet/pnl" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '[{"chain": "solana", "address": "125Z6k4ZAxsgdG7JxrKZpwbcS1rxqpAeqM9GSCKd66Wp"}]'
```

### Key response fields

- `items[].tokens[].realized_pnl` / `unrealized_pnl` (USD)
- `items[].tokens[].average_cost` — cost basis (USD)
- `items[].tokens[].current_balance` / `current_price` (USD)
- `items[].tokens[].historical_breakdown[]` — trade-by-trade history
- `items[].total_balance`, `total_realized_pnl`, `total_unrealized_pnl`

---

## Historical PnL by wallet

`POST /api/v1/developer/wallet/pnl/history`

Returns PnL snapshots over time per wallet.

### Request

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `addresses` | array of `{chain, address}` | Yes | Wallets to query |
| `start_timestamp` | string (UTC ISO 8601) | Yes | Start of range |
| `end_timestamp` | string (UTC ISO 8601) | Yes | End of range |
| `granularity` | string | Yes | `15s`, `1m`, `5m`, `1h`, `1d` |

### Example

```bash
curl -X POST "https://api.allium.so/api/v1/developer/wallet/pnl/history" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{
    "addresses": [{"chain": "solana", "address": "125Z6k4ZAxsgdG7JxrKZpwbcS1rxqpAeqM9GSCKd66Wp"}],
    "start_timestamp": "2026-04-01T00:00:00Z",
    "end_timestamp": "2026-04-10T00:00:00Z",
    "granularity": "1h"
  }'
```

### Response shape

```json
{
  "items": [{
    "address": "...",
    "chain": "solana",
    "pnl": [
      {"timestamp": "...", "realized_pnl": {"amount": "...", "currency": "USD"}, "unrealized_pnl": {...}}
    ]
  }]
}
```

---

## Current PnL by wallet & token

`POST /api/v1/developer/wallet/pnl-by-token`

Same as `/wallet/pnl` but scoped to a specific (wallet, token) pair — useful when you only care about one position.

### Request

Array of `{chain, address, token_address}`.

```bash
curl -X POST "https://api.allium.so/api/v1/developer/wallet/pnl-by-token" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '[{"chain": "solana", "address": "...", "token_address": "So11111111111111111111111111111111111111112"}]'
```

---

## Historical PnL by wallet & token

`POST /api/v1/developer/wallet/pnl-by-token/history`

PnL timeseries for a specific (wallet, token) pair.

### Request

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `addresses` | array of `{chain, address, token_address}` | Yes | (wallet, token) pairs |
| `start_timestamp` | string (UTC ISO 8601) | Yes | Start |
| `end_timestamp` | string (UTC ISO 8601) | Yes | End |
| `granularity` | string | Yes | `15s`, `1m`, `5m`, `1h`, `1d` |

```bash
curl -X POST "https://api.allium.so/api/v1/developer/wallet/pnl-by-token/history" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{
    "addresses": [{"chain": "solana", "address": "...", "token_address": "So11..."}],
    "start_timestamp": "2026-04-01T00:00:00Z",
    "end_timestamp": "2026-04-10T00:00:00Z",
    "granularity": "1h"
  }'
```

---

## Holdings history (timeseries)

`POST /api/v1/developer/wallet/holdings/history`

Returns total USD-denominated holdings over time per wallet, with optional per-token breakdown at each interval.

### Request

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `addresses` | array of `{chain, address}` | Yes | Wallets to query |
| `start_timestamp` | string (UTC ISO 8601) | Yes | Start |
| `end_timestamp` | string (UTC ISO 8601) | Yes | End |
| `granularity` | string | Yes | `15s`, `1m`, `5m`, `1h`, `1d` |
| `include_token_breakdown` | boolean | No | Per-token detail per interval (default `false`) |

Optional query params: `cursor`, `min_liquidity`.

### Example

```bash
curl -X POST "https://api.allium.so/api/v1/developer/wallet/holdings/history" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{
    "addresses": [{"chain": "solana", "address": "125Z6k4ZAxsgdG7JxrKZpwbcS1rxqpAeqM9GSCKd66Wp"}],
    "start_timestamp": "2026-04-01T00:00:00Z",
    "end_timestamp": "2026-04-10T00:00:00Z",
    "granularity": "1h",
    "include_token_breakdown": false
  }'
```

### Response shape

```json
{
  "items": [{
    "chain": "solana",
    "address": "...",
    "timestamp": "2026-04-01T00:00:00Z",
    "amount": {"amount": 1234.56, "currency": "USD"},
    "token_breakdown": [...]
  }]
}
```

---

## Common gotchas

- `/history` endpoints take an **`addresses[]` array** of objects, not a flat `address` + `chain` (422 if you send the flat shape).
- Chain names are **lowercase** — uppercase fails silently.
- All timestamps are **UTC ISO 8601** strings.
- Granularity choices: `15s`, `1m`, `5m`, `1h`, `1d`.
