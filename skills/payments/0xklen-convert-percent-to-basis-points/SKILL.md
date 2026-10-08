---
name: convert-percent-to-basis-points
description: Use when a rate arrives as a string or float percent ("2.9%", 0.029) and must drive money arithmetic. Converts to integer basis points (or ppm) once, at the boundary, and stores the integer.
---

# Convert percent to basis points

Percentages are the most common way a float sneaks into money code: `2.9%` becomes `0.029` becomes a float multiplier. Convert the rate to an integer basis-point (or parts-per-million) representation once, at the edge, and do all arithmetic in that integer.

## Procedure

1. Fix the scales: `1% = 100 bps = 10_000 ppm`, so `2.9% = 290 bps = 29_000 ppm`. bps covers two decimals of a percent, ppm covers four.
2. Pick the smallest denominator the rates need: a 0.075% fee needs ppm (`750`); a 2.9% fee fits in bps (`290`).
3. Parse the incoming string with exact decimal, then scale: `int((Decimal(s.rstrip('%')) * 100).to_integral_value())` turns `"2.9%"` into `290`.
4. Reject a rate that does not land on an integer at the chosen scale: `7.5 bps` is not representable in bps, so escalate to ppm (`750`) instead of silently truncating.
5. Store the integer `rate_bps` (or `rate_ppm`) in the schema; never a floating `rate` column.
6. Apply it as `mulDiv(amount, rate_bps, 10_000)` — the integer rate is the numerator.
7. Round-trip for display only: format `rate_bps / 100` after all arithmetic, never during it.
8. Put the denominator in the column name so `rate_bps` and `rate_ppm` cannot be confused (see `reject-currency-mismatch-before-arithmetic`).
9. Store the raw string the user typed next to the parsed bps for an audit trail of the rate's origin.
10. Define the rounding when a rate does not land on the scale: `2.005%` is 200.5 bps; choose truncate or round explicitly.
11. Keep a fee-schedule bps table in code with a test that pins each value.
12. Assert the field name carries the unit; a bare `rate` field is where fraction/percent confusion starts.

## Pitfalls

- `float("2.9") * 100` yields `289.99999999999997`; `round()` masks the symptom but the intermediate was wrong.
- A column named `rate` holding `0.029` for one row and `2.9` for another (fraction vs percent) shifts money by 100x on one row; name and document the unit.
- Storing `"2.9%"` as text and parsing at each use scatters the conversion; do it once at ingest.
- Choosing bps for a rate that needs three decimals truncates 0.001% fees to zero.
- Reading `"2,9%"` (comma decimal, EU) with `float` fails or misparses; parse locale-aware.
- A rate loaded from a config file as YAML gives `0.029` as a float; parse it with `Decimal(str(value))`, not `Decimal(value)`.

## Verification

    python3 -c "from decimal import Decimal as D; print(int(D('2.9')*100), int(D('0.075')*100*100))"   # 290, 750
    rg -n 'float\(.*%|parseFloat.*%|/ *100' rates.py   # expect no float percent handling

Report the denominator chosen, one parsed example, and the round-trip display value.
