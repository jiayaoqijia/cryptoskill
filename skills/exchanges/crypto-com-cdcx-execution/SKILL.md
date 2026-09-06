---
name: cdcx-execution
description: Order placement and management — place, amend, cancel, close-position. Safety-first with dry-run and preflight checks.
---

# Order Execution

## When to Use

- Place a LIMIT or MARKET order
- Amend price or quantity of a live order
- Cancel one or many open orders
- Close an open derivatives position
- Batch order placement

Requires authentication.

## Safety Model

Every order command lives in one of two tiers:

| Tier | Commands | Behaviour |
|------|----------|-----------|
| `mutate` | `order`, `amend`, `cancel`, `order-list`, `cancel-list`, `close-position` | Requires `acknowledged=true` in MCP mode; CLI prompts unless `--yes` |
| `dangerous` | `cancel-all` | Requires `--allow-dangerous` on the MCP server |

Always use `--dry-run` first to preview the request body.

## Tools Used

| Tool                          | Purpose                              | Tier      |
|-------------------------------|--------------------------------------|-----------|
| cdcx_trade_order              | Place a new BUY or SELL              | mutate    |
| cdcx_trade_amend              | Amend price/quantity of open order   | mutate    |
| cdcx_trade_cancel             | Cancel a single order                | mutate    |
| cdcx_trade_cancel_all         | Cancel every order                   | dangerous |
| cdcx_trade_order_list         | Place up to 10 orders in one call    | mutate    |
| cdcx_trade_cancel_list        | Cancel up to 10 orders in one call   | mutate    |
| cdcx_trade_close_position     | Close an open position (async)       | mutate    |
| cdcx_trade_open_orders        | List open orders                     | sensitive_read |
| cdcx_trade_order_detail       | Lookup by order_id or client_oid     | sensitive_read |

## Workflow

### Place a Limit Order (preferred path)

```
# 1. Preflight — verify funds and current price
cdcx account summary -o json
cdcx market ticker BTC_USDT -o json

# 2. Preview
cdcx trade order BUY BTC_USDT 0.01 \
    --type LIMIT --price 50000 \
    --dry-run -o json

# 3. Place
cdcx trade order BUY BTC_USDT 0.01 \
    --type LIMIT --price 50000 \
    --client-oid my-buy-001 \
    -o json

# 4. Confirm
cdcx trade order-detail --client-oid my-buy-001 -o json
```

Positional args: `<side> <instrument> <quantity>`. Side is `BUY` or `SELL`.

### Market Order

```
cdcx trade order BUY BTC_USDT 0.01 --type MARKET -o json
```

For MARKET BUYs you can alternatively use `--notional` to spend a fixed USDT amount: `cdcx trade order BUY BTC_USDT --type MARKET --notional 500`.

### Amend (Price / Quantity)

```
cdcx trade amend \
    --order-id 123456789 \
    --new-price 51000 \
    --new-quantity 0.01 \
    -o json
```

Both `--new-price` and `--new-quantity` are required — re-submit the original value for the field you don't want to change.

### Cancel a Single Order

```
cdcx trade cancel --order-id 123456789 -o json
# or
cdcx trade cancel --client-oid my-buy-001 -o json
```

### Cancel All (dangerous)

```
cdcx trade cancel-all BTC_USDT -o json      # Per-instrument
cdcx trade cancel-all -o json                # Every instrument — extreme caution
```

Omitting the instrument cancels everything account-wide. MCP mode rejects this unless the server was started with `--allow-dangerous`.

### Close a Position

```
cdcx account positions BTCUSD-PERP -o json   # Find the position
cdcx trade close-position BTCUSD-PERP --type MARKET -o json
```

`--type MARKET` closes at market. `--type LIMIT --price <p>` closes with a working limit. `--quantity <q>` closes partially.

### Batch Orders

```
cdcx trade order-list --order-list '[
    {"instrument_name":"BTC_USDT","side":"BUY","type":"LIMIT","price":"49000","quantity":"0.01"},
    {"instrument_name":"BTC_USDT","side":"BUY","type":"LIMIT","price":"48000","quantity":"0.01"}
]' -o json
```

Up to 10 orders per call. Use `cdcx trade cancel-list` with matching IDs to revert.

### List Open Orders

```
cdcx trade open-orders BTC_USDT -o json      # Per-instrument
cdcx trade open-orders -o json                # All instruments
```

## Notes

- Always supply a `--client-oid` (≤36 chars) for correlation between your code and exchange records
- `--dry-run` is free — use it before every live order while the strategy is new
- The API rejects prices that don't match `price_tick_size` and quantities that don't match `quantity_tick_size` — get these from `cdcx market instruments`
- `close-position` is async: the reply is an ack, not a fill. Verify with `cdcx account positions` afterwards
- Historical fills live under `cdcx history trades`, not under `trade`
