---
name: compute-basis-point-fees-in-integers
description: Use when applying a percentage fee to an amount (platform fee, spread, interest rate). Works in basis points as integers and avoids float percentages entirely.
---

# Compute basis-point fees in integers

A fee is `amount * bps / 10_000` in integer arithmetic. A percentage as a float (`amount * 2.9 / 100`) reintroduces binary error; basis points keep the rate exact and the rounding explicit.

## Procedure

1. Convert every rate to basis points: 1% = 100 bps, 2.9% = 290 bps, 0.15% = 15 bps. Store the integer `fee_bps`, not the string `"2.9%"`.
2. Compute `fee = mulDiv(amount, fee_bps, 10_000)` where `mulDiv` widens before dividing (Solidity `Math.mulDiv`, exact Python int, JS `BigInt`). Multiply first, divide last.
3. Decide the fee's rounding direction and pass it to `mulDiv`: floor favours the payer, ceil favours the collector. Never round the rate.
4. Validate the result: `0 <= fee <= amount`. A fee exceeding the principal means a bad rate or an overflow.
5. Recompute the net as `net = amount - fee`. Do not also compute `amount * (10_000 - bps) / 10_000`; the two paths can round differently — pick one and stay consistent.
6. For stacked fees on the same base, sum the bps first (`total_bps = a_bps + b_bps`) and multiply once. Only multiply sequentially if each fee applies to the running remainder.
7. If a rate needs more than two decimals of a percent (`0.075%`), it is not an integer in bps — move to parts-per-million (`750 ppm`) rather than truncating.
8. Log the amount, `fee_bps`, fee and rounding direction so the arithmetic is auditable.
9. Derive the payout from the same rounded `fee` value, or the two components can sum to a minor unit more than the gross.
10. Express the denominator as a `BPS = 10_000` constant so no literal `10000` drifts between call sites.
11. For a fee on a tax-inclusive amount, confirm whether the base is gross or net; both look plausible and they differ.
12. Property test: for random amounts, `net + fee == amount` under every rounding mode you support.

## Pitfalls

- `amount * 0.029` is a float; at $1e6 the product is off by fractions of a cent that compound across rows.
- Dividing before multiplying truncates small amounts to nothing; integer `(amount / 10_000) * bps` loses the fee on every small charge.
- A "percent" field stored as `2.9` and multiplied as `amount * 2.9 / 100` is a float even when `amount` is an integer.
- Negative amounts (refunds) round differently per language — floor on a negative fee rounds toward minus infinity in some, toward zero in others. Define it.
- `amount * bps` where both are near int64 max wraps; widen to 128-bit or use `mulDiv`.
- A fee table stored as JSON with string rates (`"2.9"`) parsed per call re-introduces the float at parse time; store integers.

## Verification

    python3 -c "a=1_000_000; bps=290; assert a*bps//10_000 == 29_000; print('ok')"
    rg -n '\* *[0-9]+\.[0-9]|/ *100\b' fee.py   # expect no float percent literals

Pass when the fee is exact for a round amount and the source shows no float rate. Report amount, bps, fee and the rounding mode.
