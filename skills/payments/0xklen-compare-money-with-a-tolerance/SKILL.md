---
name: compare-money-with-a-tolerance
description: Use when code tests money values for equality or a threshold. Never compares floats with ==; compares exact amounts or allows a stated tolerance in minor units.
---

# Compare money with a tolerance

`0.1 + 0.2 == 0.3` is False in floating point, so a naive `==` on money rejects valid payments and accepts invalid ones. Compare exact values, and where a tolerance is unavoidable (an external system's float), define it explicitly in minor units.

## Procedure

1. If both sides are integer minor units or exact decimals, compare exactly — `==` for integers, `Decimal.compare` for decimals — no tolerance is needed.
2. In SQL compare on the integer/minor column: `WHERE amount_minor = 1234`, not `WHERE amount = 12.34`. On `NUMERIC` `=` is exact; on `DOUBLE` it is not.
3. When a value truly arrives as a float (a third-party API), convert it to minor units and compare with an absolute tolerance: `abs(got - want) <= tolerance_minor`.
4. Set the tolerance from the source's precision, not by feel: a feed reporting 2 dp has an inherent ±0.5 minor-unit error, so `tolerance = 1` minor unit — document the reasoning.
5. Never use a relative tolerance (`abs(a-b)/a < 1e-9`) for money: meaningless for a $0.01 charge, and it hides real cents on a huge balance.
6. For a threshold, compare on the integer form: `amount_minor >= threshold_minor`, not `amount >= 9.99` on a float.
7. When a tolerance is used, alert on a non-zero residual that is inside it — repeated near-misses signal a systematic 1-cent bug, not noise.
8. Keep a regression test with the classic case so the guard is not removed.
9. Wrap the comparison in a named function (`money_equal(a, b)`) so the tolerance lives in one place, not as scattered literals.
10. Log both operands and the difference whenever a within-tolerance comparison fires, so the trend is visible.
11. For a 0-decimal currency the only valid tolerance is 0; special-case it rather than reusing the 2-dp default.
12. Never compare money by formatted string equality; formatting is a presentation choice, not a value.

## Pitfalls

- `abs(a - b) < 1e-9` rejects a legitimate `0.30` vs `0.30000000000000004` one way and passes nonsense another.
- Comparing a rounded display value (a 2-dp string) to an unrounded source creates spurious mismatches.
- A relative tolerance hides a missing cent on a large total (`1e-6 * 1e9` allows a $1000 discrepancy).
- `Decimal("12.30") == Decimal("12.3")` is True but the `str()` differs; compare numerically, never as strings.
- A tolerance applied to a 0-decimal currency (JPY) permits ±1 yen where ±0 is required.
- `math.isclose` defaults to a relative tolerance and is the wrong tool for money; if you use it, pass `rel_tol=0` and an absolute `abs_tol` in minor units.

## Verification

    python3 -c "print(0.1+0.2==0.3, abs((0.1+0.2)-0.3) < 1e-9)"   # False True -> why exact money matters
    python3 -c "from decimal import Decimal as D; print(D('0.1')+D('0.2')==D('0.3'))"   # True

Report whether the comparison is exact or tolerance-based, and the tolerance's justification in minor units.
