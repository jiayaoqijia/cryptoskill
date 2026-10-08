---
name: multiply-then-divide-with-widening
description: Use when money maths multiplies by a rate then divides (or the reverse). Orders multiply-before-divide and widens the intermediate so no precision or overflow is lost.
---

# Multiply then divide with widening

`amount * rate / divisor` is exact only if you multiply first and widen the intermediate. Dividing first truncates to zero; a narrow type overflows. Get the order and the width right or the arithmetic is quietly wrong.

## Procedure

1. Rewrite every expression to multiply before dividing: `(amount * rate) / divisor`, never `(amount / divisor) * rate`.
2. Treat `amount * rate` as the dangerous product — up to `10**exp` times larger than either operand. Check it fits before computing.
3. Use a widening multiply: Solidity `Math.mulDiv(amount, rate, divisor)` forms a 512-bit product then divides to 256-bit; in C use `__int128`; in Go `big.Int`; in Python plain `int` is arbitrary precision.
4. Choose the division rounding in the same call: `mulDiv(a, b, d, Rounding.Floor)`.
5. When the divisor is a power of ten, confirm the product keeps full precision — `mulDiv` does; a float `a * b * 1e-6` does not.
6. If a multiply and a divide by the same factor appear (`a * r / r`), cancel only if neither step rounds; a truncated integer round-trip is lossy.
7. For chained conversions keep the full-precision product through the chain and round once at the end, not per step.
8. Test with operands at the type boundary (int64 max, near uint256 max) to surface the overflow that normal-sized inputs hide.
9. Prefer a library `mulDiv` over a hand-rolled `a*b/d` so the widening and rounding are battle-tested.
10. Assert the divisor is non-zero before dividing; a zero rate denominator is a config bug that must fail loudly.
11. For a rate applied over time, accumulate in the widest unit and divide only at the accrual boundary.
12. Keep the intermediate product in the log so a disputed result can be recomputed exactly.

## Pitfalls

- Divide-first on small amounts truncates to zero: `(1 / 10_000) * 290 = 0` in integers, wiping out the fee.
- Storing a wide product back into a narrow variable: `uint128 p = a * b` overflows before the division can shrink it.
- A float product `amount * 1e-9` is inexact for money well below 2^53; use the integer denominator.
- Assuming `a * b / d == a * (b / d)` for truncated integers — false whenever `b % d != 0`.
- Forgetting that `mulDiv` defaults to Floor rounding, so every ceil case under-charges.
- A C `int` (32-bit) product of two large money values overflows with UB before you can widen; declare the intermediate as `__int128` or `int64`.

## Verification

    python3 -c "a=7; d=2; b=5; print('divide-first', (a//d)*b, 'multiply-first', (a*b)//d)"   # divide-first 15, multiply-first 17
    forge test --match-test .*[Mm]ul[Dd]iv -vv

Pass when the wide-order result equals the exact rational rounded once. Report the operands, the order used and the widening type.
