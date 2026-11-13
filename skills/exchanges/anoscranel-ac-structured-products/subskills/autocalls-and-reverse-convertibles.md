---
name: autocalls-and-reverse-convertibles
domain: investing/autocalls-and-reverse-convertibles
trigger: "Reading an autocallable or reverse convertible and the conditions attached."
anti_trigger: "Not for recommending a product, and not for predicting the underlying."
scope: "Early redemption triggers, coupon conditions, and the short-volatility profile they create."
status: seedling
---

# Autocalls and reverse convertibles

## Standard

An autocallable redeems early when the underlying is at or above a trigger on an observation date, paying a coupon for the period and returning principal. A reverse convertible pays a higher coupon and delivers shares, or a cash amount based on them, if the underlying finishes below a strike. Both are short-volatility structures: the investor collects a premium for accepting a truncated upside or a converted downside.

Naming the structure as short volatility explains its behaviour. In calm, rising markets the autocall triggers early and the investor is returned to cash, often at the moment when reinvesting is least attractive. In a fall, the reverse convertible converts exactly when the shares are falling, and the autocall's protection may fail at the barrier. The profile is the same one that makes option selling attractive on average and damaging in the tail.

Primary sources: <https://www.sec.gov/investor> and <https://www.esma.europa.eu/>.

## Decision rules

- Record the observation dates, the trigger levels, and the coupon conditions in full.
- Record what happens when the barrier is breached: conversion, cash settlement, or loss of coupon.
- State the short-volatility character explicitly and the maximum loss that follows from it.
- Compute the coupon as a rate over the actual expected life, not the maximum term.
- Compare with the alternative of holding the underlying plus a listed option structure.
- Record the issuer's early-redemption right where it exists.

## Procedure

1. Extract the observation schedule and trigger levels.
2. Record the coupon conditions and any memory feature.
3. Identify the barrier and the consequence of breaching it.
4. Compute the annualised coupon under an early-redemption scenario and a full-term scenario.
5. Compare with a listed-equivalent structure.
6. Record the structure and its tail loss.

## Anti-patterns

- Quoting the coupon as an annual yield without the expected life.
- Assuming the autocall triggers a fair reinvestment opportunity.
- Ignoring the barrier because the trigger is far away.
- Treating a reverse convertible's coupon as income without the conversion risk.
- Comparing coupons across notes with different barriers.

## Done checklist

- [ ] Observation schedule and triggers recorded.
- [ ] Coupon conditions and memory feature noted.
- [ ] Barrier consequence recorded.
- [ ] Annualised coupon computed for two scenarios.
- [ ] Listed-equivalent comparison made.
- [ ] Tail loss stated.

## Sources

- Structured note disclosure context: <https://www.sec.gov/investor>
- European regulatory material on structured retail products: <https://www.esma.europa.eu/>
- Retail product guidance: <https://www.finra.org/>
