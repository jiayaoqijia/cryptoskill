---
name: index-options-and-tranches
domain: investing/index-options-and-tranches
trigger: "Trading options on a credit index or a tranche of one."
anti_trigger: "Not for predicting defaults, and not for credit analysis."
scope: "Options on credit indices, and the correlation that tranches carry."
status: seedling
---

# Index options and tranches

## Standard

An option on a credit index gives the right to buy or sell protection on the index at a stated spread. Because the index is a basket, its spread reflects both the average credit quality and the correlation between the names: when correlation is high, defaults cluster and the tail of the loss distribution is fatter, which changes the price of protection at different points of that distribution.

Tranches slice the loss distribution: an equity tranche absorbs the first losses, a senior tranche absorbs only the last, and their prices reveal the market's view of correlation separately from its view of the average spread. That decomposition is why tranches exist and why their liquidity is concentrated in a few standard points.

Primary sources: <https://www.isda.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the index, series, maturity, and the tranche attachment and detachment points.
- Record the spread and the correlation implied by the tranche's price.
- Record the liquidity at the specific tranche point, which is narrower than the index's.
- Record the effect of a series roll on the exposure.
- Record the correlation scenario under which the position loses.
- Record the documentation for the tranche, which differs from the index.

## Procedure

1. Record the index and tranche terms.
2. Record the spread and the implied correlation.
3. Assess liquidity at the tranche point.
4. Record the roll effect.
5. Compute the loss under a correlation move.
6. Write the summary with its correlation assumption.

## Anti-patterns

- Treating a tranche as a diversified version of the index.
- Ignoring the correlation exposure embedded in the tranche.
- Assuming index liquidity applies to the tranche.
- Comparing tranche prices across different attachment points.
- Overlooking the documentation difference.

## Done checklist

- [ ] Index and tranche terms recorded.
- [ ] Spread and implied correlation recorded.
- [ ] Tranche liquidity recorded.
- [ ] Roll effect recorded.
- [ ] Correlation loss scenario computed.
- [ ] Documentation recorded.

The tranche's liquidity is also structurally different: the equity tranche absorbs early losses and trades as the market's view of default correlation among the weakest names, while the senior tranche trades as a view of the tail, and the two can move in opposite directions on the same news. A position described as a tranche trade should record which point of the distribution it sits on, because that is what the price is actually about.

## Sources

- Index and tranche documentation: <https://www.isda.org/>
- Regulatory market context: <https://www.federalreserve.gov/>
- Credit spread series: <https://fred.stlouisfed.org/>
