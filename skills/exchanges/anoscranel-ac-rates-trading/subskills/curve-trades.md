---
name: curve-trades
domain: investing/curve-trades
trigger: "Structuring a trade on the shape of the curve rather than its level."
anti_trigger: "Not for forecasting the curve, and not for duration policy."
scope: "Steepener, flattener, and butterfly structures with DV01-neutral weights."
status: seedling
---

# Curve trades

## Standard

A curve trade takes a position in one maturity against another, so that a parallel move in yields affects both legs similarly and the profit comes from the change in the spread. The standard structures are the steepener, which profits when the long end rises relative to the short end, the flattener, which profits from the reverse, and the butterfly, which takes a position in a belly maturity against both wings.

The construction detail that decides whether the trade is what it claims to be is the weighting. A spread trade between two contracts with different DV01s must be weighted so that the position is neutral to a parallel shift; otherwise the trade is partly a duration bet. The record states the weights, the DV01 of each leg, and the spread level at entry with its range.

Primary sources: <https://www.cmegroup.com/> and <https://www.federalreserve.gov/>.

## Decision rules

- State the spread being traded, its two or three legs, and its unit of measurement.
- Weight the legs by DV01 so the structure is neutral to a parallel move.
- Record the spread level at entry and its historical range.
- Record the carry of the structure, which differs between steepeners and flatteners.
- Record what a change in the CTD would do to the weights.
- Record the stop in spread terms, not in price terms per leg.

## Procedure

1. Define the spread and its legs.
2. Compute each leg's DV01 and the weights.
3. Record the spread level and its range over a stated window.
4. Compute the carry of the structure.
5. Check the CTD sensitivity of the weights.
6. Record the trade with its weights, level, and carry.

## Anti-patterns

- Trading equal contract counts across maturities with different DV01s.
- Quoting a spread in price points rather than in yield or basis points.
- Ignoring the carry difference between the two structures.
- Assuming the weights stay correct as the curve moves.
- Setting stops in per-leg prices, which the hedge obscures.

## Done checklist

- [ ] Spread and legs defined.
- [ ] DV01 weights computed.
- [ ] Level and range recorded.
- [ ] Carry computed.
- [ ] CTD sensitivity checked.
- [ ] Stop recorded in spread terms.

A further check is to express the trade's risk in the same units as its thesis: a view stated in basis points should have a stop in basis points, a target in basis points, and a carry estimate in basis points per month, so that the three can be compared without converting anything.

## Sources

- Futures contract and DV01 data: <https://www.cmegroup.com/>
- Treasury yield curve data: <https://www.federalreserve.gov/>
- Yield series for spread history: <https://fred.stlouisfed.org/>
