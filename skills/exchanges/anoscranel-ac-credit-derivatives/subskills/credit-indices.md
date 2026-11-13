---
name: credit-indices
domain: investing/credit-indices
trigger: "Trading a credit index and understanding its composition and roll."
anti_trigger: "Not for predicting defaults, and not for borrower analysis."
scope: "Index composition, the roll, and the difference between index and single-name risk."
status: seedling
---

# Credit indices

## Standard

A credit index is a basket of single-name protection with rules for inclusion, weighting, and periodic replacement. Trading the index gives diversified credit exposure with one instrument and one spread, which is why indices are the most liquid part of the credit derivatives market and the tool most often used to hedge a book quickly.

The index differs from its components in two ways that matter. Its spread is an average, so it can be stable while individual names move sharply; and it rolls on a schedule, with a new series issued and the old one ageing into reduced liquidity. A position held across a roll must decide whether to migrate to the new series, and the cost of that decision is a real part of the position's economics.

Primary sources: <https://www.isda.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the index, the series, the maturity, and the number of constituents.
- Record the weighting method and the largest constituents.
- Record the spread and the skew between the index and its riskiest names.
- Record the roll schedule and the liquidity of the old series after the roll.
- Record the basis between the index and a basket of its components where it is traded.
- Record whether the position's purpose is hedging or expressing a view on the average.

## Procedure

1. Record the index, series, and maturity traded.
2. Record composition, weights, and concentration.
3. Record the index spread and its comparison with components.
4. Note the roll dates and plan the migration decision.
5. Record the index-to-components basis if applicable.
6. Write the position summary with its purpose.

## Anti-patterns

- Treating index protection as diversified when a few names dominate.
- Holding the old series past the roll without a liquidity assessment.
- Comparing index spreads across series as if they were the same basket.
- Assuming the index hedges idiosyncratic risk in a concentrated book.
- Ignoring the basis to the component basket.

## Done checklist

- [ ] Index, series, maturity recorded.
- [ ] Composition and concentration recorded.
- [ ] Spread and component comparison recorded.
- [ ] Roll dates recorded.
- [ ] Basis recorded where applicable.
- [ ] Purpose of the position stated.

The index's liquidity is also its weakness for hedging: because it is easy to trade, it is the instrument most used to reduce risk quickly, which means its spread can widen for reasons that have nothing to do with any constituent's credit and everything to do with how many holders are hedging at once.

## Sources

- Index documentation and market standards: <https://www.isda.org/>
- Regulatory market context: <https://www.federalreserve.gov/>
- Credit spread series: <https://fred.stlouisfed.org/>
