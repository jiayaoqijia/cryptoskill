---
name: average-and-spread-options
domain: investing/average-and-spread-options
trigger: "Using an average-price or spread option to match a physical exposure."
anti_trigger: "Not for pricing exotic options, and not for predicting prices."
scope: "Asian and average-price options, and options on processing spreads."
status: seedling
---

# Average and spread options

## Standard

An average-price option pays off against the average of the underlying over a period rather than against its price on one date. That structure matches how physical businesses actually transact: a refiner buys crude across a month, a producer sells grain across a harvest, and the average is the price that matters to them. Averaging also reduces the option's sensitivity to a single spike, which makes it cheaper than the equivalent European option on the same period.

Spread options pay off against the difference between two prices: a crack spread between crude and products, a crush spread between soybeans and meal and oil, or a location spread between two delivery points. They express a view on processing economics or logistics rather than on the level of either leg, and their risk is concentrated in the relationship, which can move for reasons neither leg explains.

Primary sources: <https://www.cmegroup.com/> and <https://www.eia.gov/>.

## Decision rules

- Record the averaging period, the observation frequency, and the price source.
- Record the effect of the averaging on the option's vega and gamma.
- Record the spread's two legs, the ratio, and the units.
- Record the historical range of the spread and its liquidity.
- Record the correlation assumption implicit in the spread's price.
- Record the execution plan for the leg that is harder to trade.

## Procedure

1. Define the average or spread precisely.
2. Record the observation schedule and source.
3. Record the effect of averaging on the greeks.
4. Record the spread's history and liquidity.
5. Record the correlation assumption.
6. Write the structure summary.

## Anti-patterns

- Pricing an average option like a European on the same date.
- Ignoring the observation frequency's effect on value.
- Trading a spread without checking the far leg's liquidity.
- Assuming the historical spread range is a bound.
- Using a spread to express a directional view.

## Done checklist

- [ ] Averaging or spread definition recorded.
- [ ] Observation schedule recorded.
- [ ] Greek effect of averaging recorded.
- [ ] Spread history and liquidity recorded.
- [ ] Correlation assumption recorded.
- [ ] Execution plan written.

The averaging also changes the hedge: a position that pays on an average is only partially sensitive to the spot price on any one day, so a delta hedge computed from the spot price will overstate the exposure and will need to be reduced as the observation window fills, which is a schedule the record should state.


## Sources

- Exchange spread and average-price contracts: <https://www.cmegroup.com/>
- Energy and product market data: <https://www.eia.gov/>
- Agricultural supply data: <https://www.usda.gov/>
