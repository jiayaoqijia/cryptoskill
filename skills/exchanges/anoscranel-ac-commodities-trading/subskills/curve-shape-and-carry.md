---
name: curve-shape-and-carry
domain: investing/curve-shape-and-carry
trigger: "Reading the futures curve and what it costs or pays to hold a position."
anti_trigger: "Not for forecasting the spot price, and not for asset allocation."
scope: "Contango, backwardation, roll yield, and what holding a position pays or costs."
status: seedling
---

# Curve shape and carry

## Standard

The curve is the set of prices for successive delivery months, and its shape is a return component that exists independently of the spot price. When later months trade higher than nearby ones the market is in contango, and a long position held by rolling from month to month pays the difference; when later months trade lower the market is in backwardation, and the roll earns. That roll yield can dominate the spot move over a holding period of months.

Reading the curve means separating its components. The slope reflects the cost of storage plus financing, less the convenience of holding the physical good, plus expectations. Those components are observable together but not separately, so the honest record states the slope, computes the implied roll yield at the current prices, and identifies which of the components is plausibly driving it rather than asserting one.

Primary sources: <https://www.cmegroup.com/> and <https://www.eia.gov/>.

## Decision rules

- Record the prices for at least the front three contract months.
- Compute the annualised roll yield from the slope, and state the calculation.
- Record whether the curve is in contango or backwardation and by how much.
- Record the implied storage and financing cost and compare with the observed physical market.
- Record what a roll would realise if the curve stayed unchanged.
- Record the curve's history where available, since its shape is regime-dependent.

## Procedure

1. Collect settle prices for the front three months.
2. Compute the spread between months and annualise it.
3. Classify the shape and record the magnitude.
4. Compare the implied carry with the published storage and rate data.
5. Compute the roll outcome under an unchanged curve.
6. Record the analysis with its date and the curve used.

## Anti-patterns

- Reading the spot price and ignoring the curve.
- Treating contango as a forecast of falling prices.
- Computing roll yield without annualising or stating the convention.
- Comparing curves across commodities with different storage economics.
- Assuming today's shape persists through the holding period.

## Done checklist

- [ ] Front three months priced and recorded.
- [ ] Roll yield computed and annualised.
- [ ] Shape classified with magnitude.
- [ ] Implied carry compared with observed costs.
- [ ] Roll outcome under unchanged curve computed.
- [ ] Analysis dated.

## Sources

- Exchange settlement prices and curve data: <https://www.cmegroup.com/>
- Energy and inventory statistics: <https://www.eia.gov/>
- Regulatory market data: <https://www.cftc.gov/>
