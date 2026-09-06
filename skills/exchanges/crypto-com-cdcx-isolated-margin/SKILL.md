---
name: cdcx-isolated-margin
description: Trade instruments that require isolated margin (e.g. RWA/equity perpetuals like SPYUSD-PERP). Covers the create-order flag, funding transfers, leverage adjustment, and the TUI M toggle.
---

# Isolated Margin

## When to Use

Some instruments — notably equity/RWA perpetuals such as `SPYUSD-PERP` and `NVDAUSD-PERP` — cannot be traded on the default cross-margin account. Attempting to do so returns:

```json
{
  "code": 623,
  "message": "INSTRUMENT_MUST_USE_ISOLATED_MARGIN"
}
```

Isolated margin puts the position in its own margin bucket with its own leverage. Losses are capped at the isolated balance; a wipeout on one position cannot cascade into cross-margin balances on other instruments.

Use isolated margin when:
- The exchange requires it (error `623`).
- You want per-position risk isolation (e.g. high-leverage directional bet).
- You want a distinct leverage setting on one instrument without changing your cross-account config.

Do **not** use isolated margin for:
- Spot pairs (`CCY_PAIR`) — not applicable.
- Crypto perpetuals where you want shared collateral across positions.

## One Position Per Instrument

The exchange enforces **one isolated position per instrument per account**. You cannot open two separate isolated buckets on `SPYUSD-PERP` — the second order must reference the first position's `isolation_id` so the exchange knows whether you're adding to, trimming, or reversing it.

To top up or trim an open isolated position:

1. Look up its `isolation_id` via `cdcx account positions -o json` (or the `user.positions` WS channel).
2. Include `--isolation-id <ID>` on the next `cdcx trade order` call.

Omitting `--isolation-id` on a second order returns:

```json
{
  "code": 617,
  "message": "DUPLICATED_INSTRUMENT_ORDER_FOR_ISOLATED_MARGIN"
}
```

## TUI Workflow

Open the place-order modal (`t` on the Market tab) and use the **Margin** row:

```
Inst:   SPYUSD-PERP
Side:   [BUY]   SELL
Type:   [LIMIT] MARKET
Margin: [ISOLATED]  CROSS    (M to toggle)
Price:  710.25
Qty:    0.001
```

- `←/→` or `Space` while on the Margin row, or **`M` from anywhere in the modal** (except free-text fields), flips `ISOLATED ↔ CROSS`.
- Isolated margin is **pre-selected automatically** for instruments whose `inst_type` requires it (e.g. equity perpetuals).
- On success, the toast reads `Order placed (isolated margin)` so the mode is unambiguous.
- The TUI subscribes to `user.positions` at startup (when authenticated) so `isolation_id` for any open isolated position is cached and **auto-attached** to your next order on the same instrument. You do not need to supply it manually in the TUI.

### Handling Rejection

The modal **stays open** on any exchange rejection, showing the code and message so you can decide how to recover.

**Error 623 — `INSTRUMENT_MUST_USE_ISOLATED_MARGIN`**

```
[623] INSTRUMENT_MUST_USE_ISOLATED_MARGIN  (press M then R to retry with isolated margin)

R/Enter:retry  M:toggle margin  E:edit  Esc:cancel
```

Press `M` → `R` to resubmit the exact same payload with `exec_inst: ["ISOLATED_MARGIN"]`. No re-typing.

**Error 617 — `DUPLICATED_INSTRUMENT_ORDER_FOR_ISOLATED_MARGIN`**

You already have an isolated position on this instrument. If the TUI has cached the `isolation_id` (which it will have from the `user.positions` stream), the hint reads:

```
[617] DUPLICATED_INSTRUMENT_ORDER_FOR_ISOLATED_MARGIN  (R to retry — will attach your open isolation_id)
```

Press `R` and the retry includes the correct `isolation_id` automatically.

If the cache is empty (e.g. WS hadn't pushed the position yet), the TUI triggers a REST `private/get-positions` refresh in the background and shows:

```
[617] DUPLICATED_INSTRUMENT_ORDER_FOR_ISOLATED_MARGIN  (waiting on positions stream; check `cdcx account positions` then R)
```

Give it a moment then press `R` — the cache will be populated by then.

## Closing Positions (TUI)

On the **Positions** tab, select a row and press `x` to open the close-position modal. Two choices:

- **MARKET** — immediate fill at the best available price. Fast but exposes you to slippage, especially on thin books.
- **LIMIT** — pre-filled with the current mark price; edit to your desired exit level. Safer on illiquid instruments, but may not fill if the market moves away.

The workflow:

- Automatically flips the side (LONG → SELL, SHORT → BUY).
- Uses the **exact** quantity from the positions snapshot, preserving `qty_tick_size` precision — avoids leaving dust.
- Attaches `REDUCE_ONLY` so the order cannot accidentally flip your position.
- For isolated positions, attaches `exec_inst: [ISOLATED_MARGIN, REDUCE_ONLY]` and the correct `isolation_id` automatically.

If the exchange rejects the close (e.g. error 617 before the WS has pushed the `isolation_id`), the modal stays open with a retry hint. Press `R` once the positions snapshot has refreshed.

## CLI Workflow

### Place an order on isolated margin

```bash
cdcx trade order BUY SPYUSD-PERP 0.001 \
    --type LIMIT --price 710.25 \
    --exec-inst ISOLATED_MARGIN \
    -o json
```

`--exec-inst` is repeatable if you need to combine flags:

```bash
cdcx trade order BUY SPYUSD-PERP 0.001 \
    --type LIMIT --price 710.25 \
    --exec-inst ISOLATED_MARGIN \
    --exec-inst POST_ONLY \
    -o json
```

Optional tuning:

```bash
    --isolated-margin-amount 200   # USD to lock into the position's margin bucket
    --isolation-id <ID>            # Target an existing isolated position
    --leverage 5                   # Per-position max leverage
```

If you omit `--isolation-id`, the exchange creates a new isolated position. The response includes the `isolation_id` — store it if you plan to top up margin or change leverage later.

### Fund an isolated position

Move USD from your cross account into the isolated position's margin bucket:

```bash
cdcx margin transfer \
    --direction IN \
    --amount 100 \
    <ISOLATION_ID>
```

Withdraw unused margin back out:

```bash
cdcx margin transfer \
    --direction OUT \
    --amount 50 \
    <ISOLATION_ID>
```

Always dry-run first when moving funds:

```bash
cdcx margin transfer --direction IN --amount 100 <ISOLATION_ID> --dry-run
```

### Adjust leverage

```bash
cdcx margin leverage --leverage 5 <ISOLATION_ID>
```

Lower leverage reduces liquidation risk at the cost of more locked margin. Higher leverage is the inverse.

## Complete Flow Example

Open an isolated long on `SPYUSD-PERP` at 5x with $200 margin:

```bash
# 1. Preflight: confirm instrument is tradable
cdcx market instruments -o json | \
    jq '.data.data[] | select(.symbol=="SPYUSD-PERP")'

# 2. Check current price
cdcx market ticker SPYUSD-PERP -o json

# 3. Dry-run the order
cdcx trade order BUY SPYUSD-PERP 0.1 \
    --type LIMIT --price 710.00 \
    --exec-inst ISOLATED_MARGIN \
    --isolated-margin-amount 200 \
    --leverage 5 \
    --client-oid spy-long-$(date +%s) \
    --dry-run -o json

# 4. Place for real; capture the isolation_id
ORDER=$(cdcx trade order BUY SPYUSD-PERP 0.1 \
    --type LIMIT --price 710.00 \
    --exec-inst ISOLATED_MARGIN \
    --isolated-margin-amount 200 \
    --leverage 5 \
    -o json)
ISOLATION_ID=$(echo "$ORDER" | jq -r '.data.isolation_id')

# 5. Later: top up another $100 if price moves against us
cdcx margin transfer --direction IN --amount 100 "$ISOLATION_ID"

# 6. Change leverage mid-position
cdcx margin leverage --leverage 3 "$ISOLATION_ID"
```

## Common Errors

| Code | Meaning | Fix |
|------|---------|-----|
| `623` / `INSTRUMENT_MUST_USE_ISOLATED_MARGIN` | Instrument requires isolated margin | Add `--exec-inst ISOLATED_MARGIN` |
| `617` / `DUPLICATED_INSTRUMENT_ORDER_FOR_ISOLATED_MARGIN` | You already have an isolated position on this instrument | Fetch its `isolation_id` from `cdcx account positions` and pass `--isolation-id <ID>` to add/trim it |
| `INSUFFICIENT_BALANCE` | Not enough free USD to lock as margin | Reduce `--isolated-margin-amount` or top up the cross account |
| `INVALID_LEVERAGE` | Leverage outside instrument's allowed range | Check instrument metadata for `max_leverage` |
| `ISOLATION_NOT_FOUND` | `--isolation-id` doesn't match an open position | Omit it to create a new position, or list positions to find the right ID |

## Notes

- Isolated-margin positions appear under `cdcx account positions` alongside cross-margin positions, but have a distinct `isolation_id`.
- Closing an isolated position does **not** auto-return the margin to your cross account — use `cdcx margin transfer --direction OUT` to reclaim it.
- The TUI auto-default is conservative: it only pre-selects isolated for `inst_type` values known to require it (`EQUITY_PERP` / `EQUITY_PERPETUAL`). For any other instrument it defaults to cross, which you can flip with `M`.
- For bracket orders on isolated-margin instruments, pass `--exec-inst ISOLATED_MARGIN` to `cdcx advanced create-otoco` the same way.
