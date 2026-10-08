---
name: aggregate-before-you-round
description: Use when summing many money rows that each carry a rounded value. Sums the unrounded amounts first and rounds the total once, avoiding per-row rounding drift.
---

# Aggregate before you round

Rounding each line and then adding bakes in up to half a minor unit of error per row; a 100k-row report can be off by hundreds of units. Sum the exact amounts, then round the aggregate a single time.

## Procedure

1. Establish whether the stored values are already rounded (integer cents) or hold sub-minor precision (a rate, a pro-rated fee). Only the latter drift when summed.
2. Sum in the widest exact type available: `sum(amount_minor for ...)` in Python is exact integers; `SUM(x)` over `NUMERIC` in SQL is exact.
3. Round the total once at the end: `round(total, 2)` after summation, never inside it.
4. If the source rows are already integer minor units, the sum is exact and needs no re-rounding — do not double-round it.
5. For a weighted sum (`sum of amount * rate`), compute each product in exact decimals, sum, then round once; never round each product.
6. Watch the SQL trap: `SELECT SUM(ROUND(x, 2))` rounds per row; `ROUND(SUM(x), 2)` is the aggregate-first form. They differ.
7. When a legal rule requires per-line rounded values (per-line tax), the total is the sum of rounded lines and you reconcile to *that*, not to the unrounded total.
8. State in the report which figure you produced: a sum-then-round or a sum-of-rounded-lines.
9. For running balances keep one integer accumulator rather than a list of rounded deltas.
10. Stream large sums in integer chunks; the accumulator stays exact and memory stays bounded.
11. When two systems report totals, compare integer minor-unit sums, not formatted strings (see `compare-money-with-a-tolerance`).
12. Document whether a report figure is net of fees before someone stacks another fee column on top of it.

## Pitfalls

- `SELECT SUM(ROUND(...))` vs `ROUND(SUM(...))` differ by cents on large tables; pick the one the business rule means.
- Pandas `.round(2).sum()` rounds per row while `df['x'].sum().round(2)` sums first — the two are easy to swap and hard to notice.
- Excel's `SUM` of cells displayed at 2 dp adds the underlying full-precision values, so the shown total disagrees with hand-adding the visible numbers.
- A float column summed across millions of rows accumulates representation error; even a sum-first float sum is wrong.
- Re-rounding an already-integer total is harmless but signals the source scale was not understood.
- `np.sum` over a float32 array of amounts can differ from the int64 sum; keep money arrays as integers.

## Verification

    python3 -c "from decimal import Decimal as D; rows=[D('0.005')]*10; print(sum(rows), sum(round(r,2) for r in rows))"
    # 0.050 vs 0.00 -> aggregate-first keeps the half-cent that per-row rounding destroys

Report whether the figure is sum-then-round or a sum of rounded lines, and show the two SQL variants compared.
