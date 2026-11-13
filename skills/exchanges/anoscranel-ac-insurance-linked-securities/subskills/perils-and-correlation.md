---
name: perils-and-correlation
domain: investing/perils-and-correlation
trigger: "Working out how much of one peril a portfolio is actually carrying."
anti_trigger: "Not for predicting events, and not for catastrophe modelling."
scope: "Peril definitions, secondary perils, and the correlation a portfolio carries."
status: seedling
---

# Perils and correlation

## Standard

Catastrophe bonds name a peril, and the definition decides what counts. A US hurricane bond may cover wind only, wind and storm surge, or a broader set; a wildfire bond may define the event by acreage burned or by insured loss. Two bonds on the same named peril can therefore respond differently to the same physical event, and the record should state the peril definition rather than the label.

Correlation is the second consideration and the one that turns a diversifying allocation into a concentrated one. Bonds across different regions and perils are less correlated than bonds on the same peril in the same region, but the correlation is not zero: a single season can produce events in several basins, and a reinsurance market dislocation affects every structure at once. A book of ten cat bonds on one peril is one position, not ten.

Primary sources: <https://www.artemis.bm/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the peril definition and what the trigger responds to.
- Record the region and the geographic granularity of the coverage.
- Record secondary perils covered or excluded.
- Record the correlation with other positions in the book by peril and region.
- Record the aggregate expected loss by peril, not only by position.
- Record the market-wide exposure: whether a dislocation would affect all positions at once.

## Procedure

1. Record the peril definition per position.
2. Record region and granularity.
3. Record secondary perils and exclusions.
4. Aggregate expected loss by peril and region.
5. Identify the largest single-peril concentration.
6. Write the correlation summary with the concentration named.

## Anti-patterns

- Treating ten bonds on one peril as ten positions.
- Using the peril label rather than the definition.
- Ignoring secondary peril exclusions.
- Aggregating by issuer or sponsor rather than by peril.
- Assuming regional diversification holds within a single season.

## Done checklist

- [ ] Peril definitions recorded.
- [ ] Regions recorded.
- [ ] Secondary perils recorded.
- [ ] Aggregate by peril computed.
- [ ] Largest concentration named.
- [ ] Market-wide exposure recorded.

The practical consequence for sizing is that the aggregate expected loss by peril is the number to budget against, not the sum of individual expected losses: a book whose positions each carry a small expected loss can carry a large one in aggregate when they respond to the same season, and the difference between those two numbers is the concentration the portfolio did not intend.

## Sources

- ILS market and peril data: <https://www.artemis.bm/>
- Securities disclosure context: <https://www.sec.gov/investor>
- Research on catastrophic risk: <https://www.nber.org/>
