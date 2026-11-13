---
name: funding-ratio-and-surplus
domain: investing/funding-ratio-and-surplus
trigger: "Computing a funding ratio and measuring the risk around it."
anti_trigger: "Not for actuarial valuation, and not for recommending an allocation."
scope: "The ratio, its components, and surplus risk as the measure that matters."
status: seedling
---

# Funding ratio and surplus

## Standard

The funding ratio divides the value of assets by the value of liabilities. Both numbers move: assets with markets, liabilities with the discount rate and with changes in the assumptions behind them. A ratio that rises because rates fell is a real improvement in the funding position, even though the assets may have fallen in price, because the liabilities fell further.

Surplus risk is the volatility of the difference between assets and liabilities, and it is the quantity a liability-driven mandate exists to manage. Measuring it requires the two sides to be valued on the same basis and at the same frequency, which is why monthly asset values paired with an annually updated liability estimate produce a surplus series that is mostly an artefact of the update schedule.

Primary sources: <https://www.federalreserve.gov/> and <https://www.cfainstitute.org/>.

## Decision rules

- Record the asset value, the liability value, and the ratio with the same as-of date.
- Record the basis on which each side is valued.
- Record the sensitivity of the ratio to a change in the discount rate.
- Record surplus volatility as a series, not a single figure.
- Record the contributions made in the period separately from investment return.
- Where the liability is updated less often than the assets, record that.

## Procedure

1. Record assets, liabilities, and the ratio at a stated date.
2. Record the valuation basis for each side.
3. Compute the rate sensitivity of both sides.
4. Build the surplus series over a stated window.
5. Separate investment return from contributions.
6. Write the funding summary with its basis.

## Anti-patterns

- Comparing a funding ratio computed on two different bases.
- Treating a fall in asset value as a fall in funding without the liability side.
- Mixing monthly asset marks with annual liability estimates.
- Reading a single ratio as a trend.
- Ignoring contributions in a period of improvement.

## Done checklist

- [ ] Ratio computed with a common date.
- [ ] Bases recorded.
- [ ] Rate sensitivity computed.
- [ ] Surplus series built.
- [ ] Contributions separated.
- [ ] Summary states the basis.

A further discipline is to report the ratio alongside its sensitivity: a ratio of ninety percent that moves five points for a one-point rate change is a different object from one that moves one point, and the two can carry the same headline number while requiring entirely different governance attention.

## Sources

- Interest-rate and monetary data: <https://www.federalreserve.gov/>
- Investment management standards: <https://www.cfainstitute.org/>
- Rate series for discounting: <https://fred.stlouisfed.org/>
