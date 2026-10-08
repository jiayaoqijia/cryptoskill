---
name: round-currency-with-the-correct-mode
description: Use when money arithmetic divides and a rounding rule must be chosen (half-up, half-even, floor, ceiling). Picks the mode the accounting standard or protocol requires and applies it once at the boundary.
---

# Round currency with the correct mode

Every division of money forces a rounding decision, and the default is not "whatever the language does." Choose the mode the ledger or protocol mandates, apply it in exactly one place, and never round intermediate steps.

## Procedure

1. Name the policy before coding: retail totals are usually **half-up**, EU tax and statistical aggregation often **half-even**, payouts to a party **floor**, charges **ceiling**.
2. Python: quantize with an explicit mode — `D("2.345").quantize(D("0.01"), rounding=ROUND_HALF_UP)` -> `2.35`; `ROUND_HALF_EVEN` -> `2.34`.
3. Java/Kotlin: `amount.setScale(2, RoundingMode.HALF_UP)`.
4. JS decimal.js: `new Decimal(x).toDecimalPlaces(2, Decimal.ROUND_HALF_UP)` — the default is half-up but set it explicitly.
5. SQL: Postgres `ROUND(x, 2)` on `NUMERIC` is half-up; MySQL `ROUND` on `DOUBLE` is unreliable, so keep the column `NUMERIC`.
6. Solidity: integer division truncates (floor for positives). To round up use `Math.ceilDiv` from OpenZeppelin; there is no half-up — implement it explicitly if the spec needs it.
7. Round **once**, at the boundary (display, posting, payout). Carry full precision through the computation: `round(round(a/b) * c)` differs from `round(a*c/b)`.
8. For each division, write down which party the chosen mode favours. Flooring a payout shortchanges the recipient by under one minor unit; flooring a charge undercharges. The safe mode follows the direction of the payment.
9. Test the boundaries: exact halves, `2.675` (not exactly representable), negatives, and 0.
10. Bake `quantize` into the money type's serializer so JSON output never emits more decimals than the currency allows.
11. Set the SQL column scale to the currency exponent so the database enforces the same rounding you chose in code.
12. Record the rounding policy in a docstring or config next to the money module; otherwise a new contributor picks the language default.

## Pitfalls

- `2.675` in binary is `2.674999...`, so half-up on the float yields `2.67`, not `2.68`. Use `Decimal("2.675")` from the string.
- Python's built-in `round()` is banker's rounding — `round(2.5) == 2` — surprising if you expected half-up.
- Rounding each line then summing compounds drift; round the total, not each row (unless a tax rule says otherwise — see `compute-line-vs-invoice-tax-rounding`).
- `Math.round(-0.5)` in JS is `-0` and rounds toward +inf, so it is not symmetric for negatives; use decimal.js.
- A mode difference between your invoice system and the payment gateway leaves a permanent 1-cent reconciliation break.
- Serializing with `json.dumps` on a `Decimal` raises or falls back to a float; use a custom encoder that emits the rounded string.

## Verification

    python3 -c "from decimal import Decimal as D, ROUND_HALF_UP, ROUND_HALF_EVEN; print(D('2.675').quantize(D('0.01'), ROUND_HALF_UP), D('2.5').quantize(D('1'), ROUND_HALF_EVEN))"
    # 2.68  2  (half-even on the exact half), not 2.67 / 3

Report the mode chosen, the policy that requires it, and the boundary cases it was tested against.
