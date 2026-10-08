---
name: quantify-estimate-error-bars
description: Use when giving a number that is an estimate. State the low and high range, the basis, and the dominant uncertainty instead of a single falsely precise figure.
---

# Quantify estimate error bars

A lone number ("about 3 days") reads as a measurement. This skill attaches a range and its basis so a reader can plan against the downside, not just the midpoint.

## Procedure

1. Identify the estimate's basis and say which: a past measurement, a formula, or a guess.

2. Give three points, not one: low, expected, high. If you cannot name a plausible low and high, the estimate is a guess — label it as such.

3. For a formula, propagate the input ranges. A job costing `n * per_item` with `n = 500 ± 50` and `per_item = 2s ± 0.5s` yields `(450*1.5)` to `(550*2.5)` seconds, roughly 11-23 minutes.

4. Name the dominant uncertainty by which input moves the answer most; that is where extra effort pays off.

5. State what new information would narrow the range and how long gathering it costs.

6. Report leading with the range: "12-21 min (expected 17), driven mostly by item count".

7. If the estimate feeds a decision with a deadline, note explicitly whether the high end still fits.

## Pitfalls

- Precision implies accuracy; "17.3 minutes" from a guess is a lie told by formatting.
- A range only helps if the high end is honest; anchoring both ends near the midpoint hides risk.
- Correlated inputs widen the range: if n and per_item both rise, the errors add, not cancel.
- Recycling an old estimate without rechecking its assumptions makes it stale by default.
- Quoting the expected value without the range invites the reader to treat it as a promise.

## Verification

    python3 -c "n,dn,t,dt=500,50,2,0.5; print((n-dn)*(t-dt), (n+dn)*(t+dt))"

Report the range, the expected value, and the largest contributing uncertainty, all three.
