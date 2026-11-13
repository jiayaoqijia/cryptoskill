---
name: commodity-vol-skew
domain: investing/commodity-vol-skew
trigger: "Reading the skew in a commodity option market."
anti_trigger: "Not for forecasting volatility, and not for option theory."
scope: "Supply-driven skew, and why the wings are priced where they are."
status: seedling
---

# Commodity volatility skew

## Standard

Commodity skew is shaped by physical scarcity. When a market is tight, the risk of a spike is real and the calls that pay in a spike are expensive; when a market is oversupplied, the risk is a collapse and the puts carry the premium. That is why the skew in energy and agricultural markets can be far wider than in equities, and why its direction can flip as inventories change.

The practical consequence is that a single at-the-money volatility describes very little. A market can have modest at-the-money vol and an extremely expensive tail, which is exactly the state that precedes a squeeze, and a position sized on the at-the-money number alone will be under-hedged for the risk that actually exists. The record should state the wing prices with the at-the-money level.

Primary sources: <https://www.cmegroup.com/> and <https://www.eia.gov/>.

## Decision rules

- Record at-the-money volatility and the wing volatilities at stated deltas.
- Record the direction of the skew and the inventory level that explains it.
- Record the cost of the tail: the price of an out-of-the-money option relative to its historical cheapness.
- Record any structural reason for an extreme wing, such as storage constraints.
- Record how the skew has changed with the last inventory report.
- Where the wing is illiquid, record the quote's uncertainty.

## Procedure

1. Collect at-the-money and wing options at a stated expiry.
2. Compute the skew and its direction.
3. Compare with inventory data.
4. Record the historical percentile of the wing price.
5. Note structural constraints that could justify it.
6. Write the skew summary with its data source.

## Anti-patterns

- Describing a commodity option market by its at-the-money volatility alone.
- Assuming equity-like skew.
- Buying tails because they are "cheap" without the inventory context.
- Comparing skew across commodities with different storage economics.
- Ignoring a wide market in the wing quote.

## Done checklist

- [ ] ATM and wing volatilities recorded.
- [ ] Skew direction recorded.
- [ ] Inventory context recorded.
- [ ] Wing percentile recorded.
- [ ] Structural constraints noted.
- [ ] Quote uncertainty recorded.

The comparison that matters is between the wing's price and the physical constraint that would have to be breached for it to pay: when storage is full and the curve is steep, the tail can be expensive and still cheap relative to the loss it covers, and the record should make that comparison rather than judge the price on its own.


## Sources

- Exchange option data: <https://www.cmegroup.com/>
- Energy inventory statistics: <https://www.eia.gov/>
- Regulatory market data: <https://www.cftc.gov/>
