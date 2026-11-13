---
name: stress-liquidity
domain: investing/stress-liquidity
trigger: "Testing the liquidity answer under stress conditions."
anti_trigger: "Not for predicting a crisis, and not for scenario design in general."
scope: "Volume that vanishes, correlations that converge, and the changed answer."
status: seedling
---

# Stress liquidity

## Standard

The liquidity measured in calm conditions is not the liquidity available in stress. Three things change together: volume falls as dealers withdraw, spreads widen as the remaining liquidity is repriced, and correlations across assets rise so that the holdings that normally provide a choice of what to sell all become the same sale.

A stress test of liquidity therefore re-runs the days-to-liquidate calculation with reduced volume and a lower participation rate, and it assumes that the assets intended to be sold last are also the ones whose market has thinned most. The output is a revised ladder, not a probability: the point is to know what the answer becomes, not to forecast when.

Primary sources: <https://www.bis.org/> and <https://www.finra.org/>.

## Decision rules

- Record the stress volume assumption per asset class and its basis.
- Re-run days to liquidate with the stressed volume and a lower participation rate.
- Assume correlations converge and record which holdings then compete.
- Record the revised ladder and the bucket that becomes short.
- Record the historical episode used as the reference, if any.
- Record what the portfolio would have to do differently in the stress case.

## Procedure

1. Choose a stress reference and record it.
2. Apply stressed volume and participation.
3. Recompute the ladder.
4. Identify the bucket shortfall.
5. Record the actions the stress case would require.
6. Write the comparison of calm and stress ladders.

## Anti-patterns

- Applying a uniform volume reduction across all assets.
- Assuming the diversification of liquidity survives the stress.
- Using a stress episode that did not affect the assets held.
- Treating the stress ladder as a forecast rather than a test.
- Skipping the stress case because the calm case is comfortable.

## Done checklist

- [ ] Stress reference recorded.
- [ ] Stressed volume and participation applied.
- [ ] Ladder recomputed.
- [ ] Shortfall identified.
- [ ] Required actions recorded.
- [ ] Both ladders compared.

The test is also worth running at the level of a single requirement rather than the whole portfolio: a specific dated obligation can be tested against the stressed ladder to see which bucket fails first, and that answer is more actionable than a portfolio-wide figure because it names the asset that would have to be sold.


## Sources

- Financial stability and liquidity analysis: <https://www.bis.org/>
- Market stress and volatility data: <https://fred.stlouisfed.org/>
- Trading and market structure guidance: <https://www.finra.org/>
