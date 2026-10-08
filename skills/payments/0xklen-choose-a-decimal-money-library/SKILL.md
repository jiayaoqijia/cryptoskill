---
name: choose-a-decimal-money-library
description: Use when a project must pick a numeric type for currency (Decimal vs bigint vs decimal.js vs NUMERIC). Chooses the representation that keeps money exact end to end.
---

# Choose a decimal money type

The right money representation depends on whether amounts are bounded. Bounded fiat and token balances fit in integers; unbounded or fractional-scaled values need an arbitrary-precision decimal. Decide once, at the schema, and hold it everywhere.

## Procedure

1. Classify each quantity: **bounded integer** (cents, wei, a count of sats) -> native integer; **exact decimal with a fixed scale** (an FX rate at 8 dp) -> decimal or scaled integer; **unbounded or irrational** (compounding interest) -> arbitrary-precision decimal with an explicit rounding context.
2. Python: use `decimal.Decimal` with an explicit context — `getcontext().prec = 34` — and `quantize` at the boundary. Never `float`.
3. JS/TS: use `decimal.js` or `big.js`; for chains, `ethers` `BigInt`. `Number` is IEEE-754 — inexact below 2^53 and unsafe above it.
4. Java/Kotlin: use `BigDecimal` with `setScale(scale, RoundingMode.HALF_EVEN)`; never `double`.
5. Go: use `math/big.Rat` or `shopspring/decimal`; never `float64`.
6. SQL: use `NUMERIC(p, s)` (Postgres/MySQL) with `s` = the currency scale; never `REAL`. SQLite stores integer minor units.
7. Freeze the choice in one module and re-export it (`from .money import Money, D`) so every caller shares the same type and context.
8. Encode the unit in the type: `struct Money { amount_minor: i64, currency: [u8;3] }`, so a currency-less decimal cannot enter the ledger.
9. Document the scale per quantity in the schema comment — an amount, a rate and a ratio have different scales and must not be mixed.
10. Benchmark the hot path before choosing arbitrary precision: `Decimal` is ~10-50x slower than int64 and that only matters if the loop runs millions of times.
11. Pin the library version in the lockfile; minor bumps in decimal libraries have flipped default rounding before.
12. Write a round-trip test: parse a string amount, run the operation, and assert the exact expected string comes back.

## Pitfalls

- `Decimal(float)` inherits the float's error: `Decimal(0.1)` is `0.1000000000000000055...`. Construct from a string: `Decimal("0.1")`.
- Python's default context precision (28) silently rounds products; a product of two 18-dp values loses digits without raising.
- `Decimal("1.0") == Decimal("1.00")` is True but the `quantize` results differ; compare after quantizing, not before.
- `big.js` and `decimal.js` default to half-up; if your policy is half-even, set it or totals disagree with the ledger.
- `float64` holds an integer exactly only up to 2^53; a wei-scale balance silently overflows past it.
- Two modules importing two different decimal libraries (say `decimal.js` and `bignumber.js`) produces silent comparison failures across the boundary.

## Verification

    python3 -c "from decimal import Decimal as D; print(D('0.1')*3 == D('0.3'))"   # True
    rg -n 'float|double|\bNumber\b' money.py ledger/ | grep -v test   # expect no money fields

Report the representation chosen per quantity class and the exact library/type pinned in the schema.
