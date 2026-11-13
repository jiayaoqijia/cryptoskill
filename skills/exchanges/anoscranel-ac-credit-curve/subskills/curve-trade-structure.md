---
name: curve-trade-structure
domain: investing/curve-trade-structure
trigger: "Structuring a credit curve steepener or flattener."
anti_trigger: "Not for predicting spreads, and not for default modelling."
scope: "Steepener and flattener structures with spread DV01 weights."
status: seedling
---

# Curve trade structure

## Standard

A credit curve trade takes opposite positions at two maturities on the same issuer, weighted so that a parallel move in spreads produces no profit or loss. The weights come from spread DV01: the position at each maturity is sized so that its sensitivity to a one-basis-point parallel move is equal and opposite to the other leg's.

The structure's risk is then concentrated in the slope rather than the level. That concentration is the point, and it is also a constraint: a curve trade can lose money while the issuer's credit improves, if the spread between the two maturities narrows in the wrong direction. The record should state the weights, the DV01 used, and the slope change required to break even.

Primary sources: <https://www.isda.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the two maturities and the issuer, with the same documentation version.
- Compute spread DV01 per leg and derive the weights.
- Record the resulting spread-slope exposure and the level neutrality.
- Record the roll and carry of the combined structure, which differs from either leg.
- Record the slope change required to break even, in basis points.
- Record liquidity at each leg separately, since the trade is sized to the harder one.

## Procedure

1. Record the legs and the documentation.
2. Compute DV01 per leg and the weights.
3. Verify level neutrality.
4. Compute combined roll and carry.
5. Derive the break-even slope change.
6. Record the trade with its weights and liquidity.

## Anti-patterns

- Weighting by notional rather than by spread DV01.
- Trading legs with different documentation versions.
- Sizing to the liquid leg and assuming the other fills.
- Ignoring the combined roll and carry.
- Describing the trade as level-neutral without verifying it.

## Done checklist

- [ ] Legs and documentation recorded.
- [ ] DV01 and weights computed.
- [ ] Level neutrality verified.
- [ ] Combined roll and carry computed.
- [ ] Break-even slope derived.
- [ ] Liquidity recorded per leg.

The documentation point deserves particular weight in credit, because two trades with the same issuer but different documentation versions are not the same instrument, and a curve trade built across versions carries a basis that has nothing to do with the slope being targeted.


The weighting check is worth performing twice, once on notional and once on DV01, because the two produce very different sizes and the difference is the amount of level risk that remains in the trade.


## Sources

- Credit derivatives conventions: <https://www.isda.org/>
- Market and rate data: <https://www.federalreserve.gov/>
- Spread series for slope history: <https://fred.stlouisfed.org/>
