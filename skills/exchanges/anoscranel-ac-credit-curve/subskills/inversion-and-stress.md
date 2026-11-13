---
name: inversion-and-stress
domain: investing/inversion-and-stress
trigger: "Explaining an inverted credit curve and what it implies for a position."
anti_trigger: "Not for predicting a default, and not for legal analysis."
scope: "Why an inverted credit curve appears, and what it implies."
status: seedling
---

# Inversion and stress

## Standard

An inverted credit curve means spreads at short maturities exceed those at long maturities, which is the market saying that near-term risk is larger than long-term risk. That happens when participants consider a default or a restructuring plausible within a defined window: the short-dated protection becomes the constrained instrument, and its spread can widen far beyond the long end.

The shape is informative but not predictive. An inverted curve can persist while the issuer refinances and the risk passes, or it can precede an event. What it does reliably is change the economics of a position: a short-dated long loses more on a widening than a long-dated one, and a curve trade that assumes a normal upward slope will behave differently from its historical pattern.

Primary sources: <https://www.isda.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the short and long spreads and the inversion's magnitude.
- Record when the inversion began and whether it has deepened.
- Record the maturities affected, which indicates the market's expected window.
- Record the difference between the issuer's curve and its peers' curves.
- Record the effect on roll and carry, which changes sign in an inversion.
- Record what would normalize the curve, as an observable condition.

## Procedure

1. Record the spreads at the short and long maturities.
2. Measure the inversion and its history.
3. Identify the affected maturities.
4. Compare with peers.
5. Recompute roll and carry under the inverted shape.
6. Record the normalization condition.

## Anti-patterns

- Reading an inversion as a default forecast.
- Assuming the historical upward slope for roll calculations.
- Comparing an inverted curve with peers whose curves are normal.
- Ignoring the maturity range that the inversion covers.
- Treating a persistent inversion as necessarily resolved by an event.

## Done checklist

- [ ] Short and long spreads recorded.
- [ ] Inversion magnitude and history recorded.
- [ ] Affected maturities identified.
- [ ] Peers compared.
- [ ] Roll and carry recomputed.
- [ ] Normalization condition recorded.

The affected maturities are the most informative part of the observation: an inversion confined to the shortest points suggests a specific near-term event, while one extending through the intermediate maturities suggests a broader reappraisal of the issuer's prospects across several years.


The normalization condition is the field that makes the position reviewable: a curve that flattens back above zero at the short point is observable and dated, which is more useful than a judgement that conditions have improved.


## Sources

- Credit market data and conventions: <https://www.isda.org/>
- Market and rate context: <https://www.federalreserve.gov/>
- Spread series: <https://fred.stlouisfed.org/>
