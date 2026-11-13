---
name: storage-and-convenience-yield
domain: investing/storage-and-convenience-yield
trigger: "Explaining why a commodity curve is shaped the way it is."
anti_trigger: "Not for forecasting prices, and not for portfolio allocation."
scope: "Physical stocks, storage cost, convenience yield, and why the curve can invert."
status: seedling
---

# Storage and convenience yield

## Standard

The cost of carrying a physical commodity is storage plus insurance plus financing, and in a market with ample stocks the futures curve should rise by roughly that cost across the delivery months. When the curve rises by less, or falls, the difference is the convenience yield: the value of having the physical good available now rather than later, which rises when stocks are scarce.

That relationship explains the shapes a trader sees. Backwardation is not primarily a bullish forecast; it is a market telling you that holders value the spot good more than the promise of it later, which usually means inventories are tight. Contango is not a bearish forecast either; it is the price of storage being paid by whoever holds the later-dated contract, which is why physical holders can earn it and financial holders pay it.

Primary sources: <https://www.eia.gov/> and <https://www.cftc.gov/>.

## Decision rules

- Record the physical stock level and its five-year range where the data exist.
- Record the storage and financing cost estimate and its source.
- Compute the implied convenience yield from the curve and the cost of carry.
- Record whether the curve shape is consistent with the inventory level.
- Record who in the market is paying the carry: a hedger, an index holder, or a speculator.
- Where inventory data are unavailable, record that and lower the confidence.

## Procedure

1. Collect the inventory series for the commodity and its location.
2. Estimate storage and financing costs.
3. Compute the implied convenience yield across the front months.
4. Compare the shape with inventory and with the seasonal pattern.
5. Identify the likely holder of the other side of the carry.
6. Record the analysis with its data sources and dates.

## Anti-patterns

- Reading contango as a bearish forecast.
- Ignoring inventories and treating the curve as pure expectation.
- Using storage costs from a different location or grade.
- Assuming convenience yield is constant across the year.
- Presenting an implied yield without its calculation.

## Done checklist

- [ ] Inventory level recorded with its range.
- [ ] Storage and financing estimated with sources.
- [ ] Implied convenience yield computed.
- [ ] Shape checked against inventory.
- [ ] Counterparty to the carry identified where possible.
- [ ] Confidence recorded.

## Sources

- Energy inventory and production statistics: <https://www.eia.gov/>
- Regulatory market and positioning data: <https://www.cftc.gov/>
- Exchange curve data: <https://www.cmegroup.com/>
