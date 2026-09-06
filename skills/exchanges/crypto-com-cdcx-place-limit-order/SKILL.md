---
name: cdcx-place-limit-order
description: End-to-end limit order workflow with preflight checks, dry-run, placement, monitoring, amend, and cancel.
---

# Place Limit Order

## When to Use

- Patient entry at a specific price
- Split a large order into laddered rungs
- Anchor a position before attaching stop/take-profit legs

Requires authentication. Order placement is tier `mutate`.

## The Command

```
cdcx trade order <SIDE> <INSTRUMENT> <QUANTITY> \
    --type LIMIT --price <PRICE> \
    [--time-in-force GOOD_TILL_CANCEL|FILL_OR_KILL|IMMEDIATE_OR_CANCEL|POST_ONLY] \
    [--client-oid <ID>] \
    [--exec-inst POST_ONLY|REDUCE_ONLY|SMART_POST_ONLY|ISOLATED_MARGIN]
```

Positional args: `<side> <instrument_name> <quantity>`. Side is `BUY` or `SELL`. Omitting `--type` defaults to `MARKET`.

## Preflight (mandatory before going live)

```
# 1. Verify auth
cdcx account info -o json > /dev/null

# 2. Cash check
cdcx account summary -o json | \
    jq -r '.data.total_available_balance'

# 3. Instrument is tradable + get tick sizes
cdcx market instruments -o json | \
    jq '.data.data[] | select(.symbol=="BTC_USDT") |
        {symbol, price_tick_size, qty_tick_size, min_qty, max_qty, tradable}'

# 4. Current market context
cdcx market ticker BTC_USDT -o json | \
    jq '.data[0] | {last:.a, bid:.b, ask:.k, high:.h, low:.l}'
cdcx market book BTC_USDT --depth 10 -o json
```

## Dry-Run (free preview)

```
cdcx trade order BUY BTC_USDT 0.1 \
    --type LIMIT --price 50000 \
    --client-oid buy-btc-$(date +%s) \
    --dry-run -o json
```

`--dry-run` prints the signed request body without sending it. Inspect to confirm every field is correct.

## Place

```
cdcx trade order BUY BTC_USDT 0.1 \
    --type LIMIT --price 50000 \
    --time-in-force GOOD_TILL_CANCEL \
    --client-oid buy-btc-2026-04-17 \
    -o json
```

Response includes `order_id`. Store both `order_id` and your `client_oid` — either can be used to look up or cancel.

## Monitor

```
# List open orders for this instrument
cdcx trade open-orders BTC_USDT -o json

# Get full detail for one
cdcx trade order-detail <ORDER_ID> -o json
# or
cdcx trade order-detail --client-oid buy-btc-2026-04-17 -o json
```

## Amend (reprice)

```
cdcx trade amend \
    --order-id <ORDER_ID> \
    --new-price 51000 \
    --new-quantity 0.1 \
    -o json
```

Both `--new-price` and `--new-quantity` are required — re-submit the original value for the side you don't want to change.

## Cancel

```
cdcx trade cancel --order-id <ORDER_ID> -o json
# or
cdcx trade cancel --client-oid buy-btc-2026-04-17 -o json
```

## Patterns

### Laddered Entry (4 rungs)

```bash
INSTRUMENT=BTC_USDT
QTY_PER=0.025
for price in 49500 49250 49000 48750; do
    cdcx trade order BUY $INSTRUMENT $QTY_PER \
        --type LIMIT --price $price \
        --client-oid "ladder-$price" \
        -o json
done
```

### POST_ONLY (maker-only)

```
cdcx trade order BUY BTC_USDT 0.1 \
    --type LIMIT --price 50000 \
    --exec-inst POST_ONLY \
    -o json
```

POST_ONLY rejects the order if it would cross the book (and therefore would fill as taker).

## Common Errors

| Error | Meaning | Fix |
|-------|---------|-----|
| `INVALID_PRICE` | Price doesn't match `price_tick_size` | Round to nearest tick from `cdcx market instruments` |
| `INVALID_QUANTITY` | Quantity below `min_qty` or not a multiple of `qty_tick_size` | Adjust to a valid rung |
| `INSUFFICIENT_BALANCE` | Available < price × quantity (for BUY) | Reduce size or top up |
| `INVALID_TIME_IN_FORCE` | Unsupported TIF value | Use `GOOD_TILL_CANCEL` / `FILL_OR_KILL` / `IMMEDIATE_OR_CANCEL` |

## Notes

- Prices in the API are decimals — send them as strings with a decimal point (e.g. `"50000.0"` not `50000`). The CLI takes numeric forms and formats correctly
- `cdcx trade order --help` lists every supported flag including STP (self-trade prevention) and isolated-margin arguments
- For bracket orders (entry + SL + TP in one payload) use `cdcx advanced create-otoco` — see the `cdcx-advanced` skill
