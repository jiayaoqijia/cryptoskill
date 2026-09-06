---
name: cdcx-advanced
description: Advanced contingency orders — OCO, OTO, OTOCO. Triggered orders with linked cancellation logic.
---

# Advanced Orders

## When to Use

- Place a stop-loss and take-profit that cancel each other (OCO)
- Place an entry order that spawns a protection order when filled (OTO)
- Place an entry with both a stop-loss and take-profit (OTOCO — "bracket order")
- Manage or cancel an advanced order by its contingency ID

Requires authentication. All placement commands are tier `mutate`.

## Order Types

| Type | Meaning | Shape |
|------|---------|-------|
| OCO  | One-Cancels-the-Other | 2 protection legs; one fill cancels the other |
| OTO  | One-Triggers-the-Other | 1 entry leg + 1 protection leg (fires only after entry fills) |
| OTOCO | Bracket | 1 entry leg + 2 protection legs (stop-loss + take-profit) |

## Tools Used

| Tool                              | Purpose                          | Tier   |
|-----------------------------------|----------------------------------|--------|
| cdcx_advanced_oco                 | Create OCO pair                  | mutate |
| cdcx_advanced_create_oto          | Create OTO pair                  | mutate |
| cdcx_advanced_create_otoco        | Create OTOCO bracket             | mutate |
| cdcx_advanced_cancel_oco          | Cancel an OCO by list ID         | mutate |
| cdcx_advanced_cancel_oto          | Cancel an OTO by list ID         | mutate |
| cdcx_advanced_cancel_otoco        | Cancel an OTOCO by list ID       | mutate |
| cdcx_advanced_cancel              | Cancel a single child order      | mutate |
| cdcx_advanced_cancel_all          | Cancel all advanced orders       | dangerous |
| cdcx_advanced_open_orders         | List open advanced orders        | sensitive_read |
| cdcx_advanced_order_detail        | Lookup by order_id / client_oid  | sensitive_read |
| cdcx_advanced_order_history       | Historical advanced orders       | sensitive_read |
| cdcx_advanced_order_list_detail   | Lookup by list IDs               | sensitive_read |

## Workflow

Each `create-*` command takes a single positional `<order_list>` — a JSON array of order objects. The order list captures the entire contingency in one request.

### OTOCO Bracket (most common)

```
cdcx advanced create-otoco '[
    {"instrument_name":"BTC_USDT","side":"BUY","type":"LIMIT","price":"50000","quantity":"0.01"},
    {"instrument_name":"BTC_USDT","side":"SELL","type":"STOP_LOSS","trigger_price":"48000","quantity":"0.01","ref_price_type":"MARK_PRICE"},
    {"instrument_name":"BTC_USDT","side":"SELL","type":"TAKE_PROFIT","trigger_price":"55000","quantity":"0.01","ref_price_type":"MARK_PRICE"}
]' --dry-run -o json
```

Exactly 3 orders: one entry (LIMIT or MARKET), one stop leg (STOP_LOSS or STOP_LIMIT), one take-profit leg (TAKE_PROFIT or TAKE_PROFIT_LIMIT). `ref_price_type` supports `MARK_PRICE` (default), `INDEX_PRICE`, `LAST_PRICE`.

### OTO (entry + protection)

```
cdcx advanced create-oto '[
    {"instrument_name":"BTC_USDT","side":"BUY","type":"LIMIT","price":"50000","quantity":"0.01"},
    {"instrument_name":"BTC_USDT","side":"SELL","type":"STOP_LOSS","trigger_price":"48000","quantity":"0.01","ref_price_type":"MARK_PRICE"}
]' -o json
```

Exactly 2 orders: one entry, one protection leg.

### OCO (bare pair, already in position)

```
cdcx advanced oco '[
    {"instrument_name":"BTC_USDT","side":"SELL","type":"LIMIT","price":"55000","quantity":"0.01"},
    {"instrument_name":"BTC_USDT","side":"SELL","type":"STOP_LOSS","trigger_price":"48000","quantity":"0.01","ref_price_type":"MARK_PRICE"}
]' -o json
```

Use after you already hold a position — exits at either the take-profit limit or stop-loss trigger.

### Single Trigger Order

```
cdcx advanced order BTCUSD-PERP \
    --side SELL --type STOP_LOSS \
    --quantity 0.01 \
    --trigger-price 48000 \
    --ref-price-type MARK_PRICE \
    -o json
```

Use when you want an unattached stop or take-profit with no linked leg.

### Cancel by List ID

```
cdcx advanced cancel-otoco --list-id <list_id> -o json
cdcx advanced cancel-oco --list-id <list_id> -o json
cdcx advanced cancel-oto --list-id <list_id> -o json
```

List IDs are returned in the response body of the `create-*` call — capture and store them.

### List and Inspect

```
cdcx advanced open-orders BTC_USDT -o json
cdcx advanced order-detail --order-id <id> -o json
cdcx advanced order-list-detail --list-id <list_id>,<list_id2> -o json
cdcx advanced order-history --instrument-name BTC_USDT --limit 50 -o json
```

### Cancel Every Advanced Order (dangerous)

```
cdcx advanced cancel-all BTC_USDT -o json     # Per-instrument
cdcx advanced cancel-all -o json               # Account-wide — very rare
```

## Notes

- Advanced orders live in their own namespace — they do not appear in `cdcx trade open-orders`
- `ref_price_type` defaults to `MARK_PRICE`. For perpetuals stick to MARK_PRICE to avoid liquidation-edge scenarios
- OTO/OTOCO child orders are only created after the entry fills — until then they are virtual
- Always `--dry-run` before a live OTOCO — the JSON payload is easy to get wrong
