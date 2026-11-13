---
name: factor-construction
domain: investing/factor-construction
trigger: "Turning a characteristic into a tradeable factor definition."
anti_trigger: "Not for predicting returns, and not for fund selection."
scope: "Definitions, transformations, and the choices that change results."
status: seedling
---

# Factor construction

## Standard

Constructing a factor means making a series of choices, each of which changes the result: how the raw characteristic is measured, whether it is scaled by a denominator such as book value or earnings, how outliers are handled, how often the portfolio is rebalanced, and how weights are assigned within the sorted groups.

The choices are not neutral, and a result reported without them cannot be reproduced. A value factor defined on book-to-price behaves differently from one defined on earnings yield; a momentum factor measured over twelve months excluding the most recent behaves differently from one measured over six. The record states each choice so that a result can be attributed to a definition rather than to a general idea.

Primary sources: <https://www.nber.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the raw characteristic and the denominator used.
- Record the outlier treatment and its threshold.
- Record the rebalancing frequency and the holding period.
- Record the weighting within groups: equal, cap-weighted, or otherwise.
- Record the universe and any filters applied before ranking.
- Record each choice that was tested and rejected, since the alternatives matter.

## Procedure

1. Define the raw characteristic.
2. Choose the denominator and state why.
3. Set the outlier treatment.
4. Choose the rebalancing frequency.
5. Choose the weighting.
6. Record all choices, including rejected alternatives.

## Anti-patterns

- Reporting a result without the construction choices.
- Changing the definition after seeing the result.
- Using a denominator inconsistent with the characteristic.
- Ignoring the effect of rebalancing frequency on turnover.
- Treating equal and cap weighting as interchangeable.

## Done checklist

- [ ] Characteristic and denominator recorded.
- [ ] Outlier treatment recorded.
- [ ] Rebalancing frequency recorded.
- [ ] Weighting recorded.
- [ ] Universe and filters recorded.
- [ ] Rejected alternatives recorded.

A further choice is the treatment of the financial sector: leverage makes book value and earnings behave differently for banks, and whether they are excluded, treated separately, or included with an adjusted denominator changes both the factor's composition and its measured premium, which is why the exclusion is a construction decision rather than a data-cleaning detail.


The rebalancing choice also determines what the factor is exposed to between rebalances: a monthly schedule captures short-term reversals that an annual one ignores, and an annual schedule holds positions through a year of news that a quarterly one would have sold, so the frequency is a statement about which horizon the premium is believed to operate over.


## Sources

- Asset pricing and factor construction research: <https://www.nber.org/>
- Investor education on factor products: <https://www.investor.gov/introduction-investing>
- Market and fundamental data: <https://fred.stlouisfed.org/>
