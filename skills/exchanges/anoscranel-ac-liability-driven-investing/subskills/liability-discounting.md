---
name: liability-discounting
domain: investing/liability-discounting
trigger: "Choosing and reading the discount basis behind a liability value."
anti_trigger: "Not for actuarial advice, and not for predicting rates."
scope: "Discount curves, the choice of basis, and the sensitivity of the liability value."
status: seedling
---

# Liability discounting

## Standard

A liability is a stream of future payments, and its present value depends entirely on the rate used to discount it. Two bodies of practice dominate: discounting at a rate that reflects the yield on high-quality corporate bonds, which ties the liability to a market observable, and discounting at an expected-return assumption on assets, which ties the liability to the portfolio and makes the funding ratio less volatile by construction.

The choice is a policy decision with a consequence. Market-based discounting produces a liability that moves with rates and therefore a funding ratio that moves with markets, which is uncomfortable to report but honest. Asset-return-based discounting produces a smoother series that can hide a deterioration, because a fall in expected returns raises the liability and a rise lowers it in a way that partly offsets the asset effect.

Primary sources: <https://www.federalreserve.gov/> and <https://www.cfainstitute.org/>.

## Decision rules

- Record the discount basis and the source of the curve used.
- Record the term structure applied, not only the headline rate.
- Record the sensitivity of the liability value to a one-point change.
- Record whether the basis is market-observable or an assumption.
- Record the effect of a change in basis on the reported ratio.
- Where comparability matters, restate on a common basis before comparing.

## Procedure

1. Record the basis and the curve used.
2. Record the cash-flow projection behind the liability.
3. Compute the present value at the stated curve.
4. Compute the sensitivity to a parallel move.
5. Record the basis change's effect on the ratio.
6. Write the discounting summary with its basis named.

## Anti-patterns

- Comparing liability values computed on different bases.
- Using a single rate for a long-dated liability stream.
- Treating an asset-return assumption as a market observable.
- Ignoring the effect of a basis change on the reported funding ratio.
- Assuming the curve is stable across the liability's horizon.

## Done checklist

- [ ] Basis and curve recorded.
- [ ] Cash-flow projection recorded.
- [ ] Present value computed.
- [ ] Rate sensitivity computed.
- [ ] Basis-change effect recorded.
- [ ] Summary names the basis.

A practical check is to restate the ratio on the alternative basis before any comparison: if the ranking of two schemes reverses when the basis changes, the comparison was measuring accounting convention rather than funding, and that finding is worth more than the ranking itself.

## Sources

- Interest-rate and policy data: <https://www.federalreserve.gov/>
- Investment management standards: <https://www.cfainstitute.org/>
- Yield curve series: <https://fred.stlouisfed.org/>
