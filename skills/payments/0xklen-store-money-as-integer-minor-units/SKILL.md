---
name: store-money-as-integer-minor-units
description: Use when storing or computing currency amounts in code (prices, balances, invoice totals). Represents money as an integer count of the smallest unit and bans binary floating point for it.
---

# Store money as integer minor units

Binary floating point cannot represent 0.10 exactly, so `0.1 + 0.2 != 0.3` and cents evaporate across thousands of operations. Store an integer count of the currency's smallest unit — the minor unit — and never a `float`.

## Procedure

1. Fix the minor unit per currency and record its exponent in one table: `CURRENCY_EXPONENT = {"USD": 2, "JPY": 0, "KWD": 3, "BTC": 8, "ETH": 18}`.
2. Store the amount as a signed integer `amount_minor` plus an ISO-4217 `currency` column. `$12.34` -> `1234 USD`; `-0.05` -> `-5 USD`.
3. Never let a float into a money field. Hunt for existing ones: `rg -n '\b(float|double|REAL|FLOAT|DOUBLE)\b' --type sql src/`.
4. In a language with a decimal type, use it for parsing and display only; persist and transmit integers. `int(Decimal("12.34") * 100)` -> `1234`.
5. In SQL use `BIGINT` or `NUMERIC(20,0)`, never `FLOAT`/`DOUBLE PRECISION`/SQLite `REAL`. SQLite has no decimal type: store `INTEGER` minor units and convert at the edge.
6. Do arithmetic in integers. Addition, subtraction and multiplication by an integer are exact; division needs a rounding decision — see `round-currency-with-the-correct-mode`.
7. Convert to human units only at the input/output boundary, dividing by `10 ** exponent` there and nowhere else.
8. Check magnitude against int64 max (~9.22e18): at 2 decimals that is 9.2e16 dollars, safe; wei-scale balances at 18 decimals fit but `wei * wei` does not — widen or use bigint.
9. Assert the invariant on the way in: `assert isinstance(amount_minor, int) and not isinstance(amount_minor, bool)`.
10. Reject a currency-less amount at the boundary: a `Money` without a code is just a number, and numbers get summed across currencies by accident.
11. Add a database CHECK that the currency is a known ISO code (`CHECK (currency IN ('USD','EUR','JPY'))`) so a typo'd code cannot enter the ledger.

## Pitfalls

- JSON has only a double for numbers: `{"amount": 12.34}` is a float in every parser. Send minor units as an integer (`{"amount_minor": 1234}`) or a string (`{"amount": "12.34"}`), never a JSON float for money.
- A JavaScript `Number` is a float and only exact to 2^53; use `BigInt` or a decimal library for minor units past ~9e15.
- CSV and Excel round-trips silently float-ify integers; export minor units or a text-formatted column.
- Mixing a minor-unit integer with a float rate in one expression reintroduces the float: `amount_minor * 0.0725` is a float. Use a rational or basis-point integer.
- A `SUM` over a float column looks fine at small scale and drifts at millions of rows.
- A column simply called `amount` invites a float; name it `amount_minor` so the unit is undeniable.
- Storing `amount_minor` as `TEXT` "to be safe" reintroduces string sorting and comparison bugs; keep it numeric.

## Verification

    python3 -c "from decimal import Decimal as D; assert D('0.1')+D('0.2')==D('0.3'); print('decimal ok')"
    rg -n '\b(FLOAT|DOUBLE|float|double|REAL)\b' src/ db/   # expect no hits on money columns

Pass when no money field is typed float and the schema shows integer minor units. Report the exponent table and the grep result.
