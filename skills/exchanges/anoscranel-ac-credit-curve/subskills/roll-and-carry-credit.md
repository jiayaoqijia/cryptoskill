---
name: roll-and-carry-credit
domain: investing/roll-and-carry-credit
trigger: "Estimating the return on a credit position if the curve stays put."
anti_trigger: "Not for predicting spread moves, and not for default modelling."
scope: "Roll-down, carry, and the return from an unchanged curve."
status: seedling
---

# Roll and carry in credit

## Standard

Roll-down is the gain or loss from a position ageing along the curve. A ten-year spread held for a year becomes a nine-year spread, and if the curve slopes upward, the nine-year point carries a tighter spread than the ten-year, so the position gains as it rolls down. Carry is the premium income net of financing over the same period.

Together they give the return on an unchanged curve, which is the baseline against which a spread move is measured. A position with positive roll and carry earns while waiting, and one with negative roll and carry requires the curve to move in its favour just to break even. The record should state this break-even, because it converts a view into a hurdle.

Primary sources: <https://www.isda.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the spread at the current maturity and at the maturity it will roll to.
- Compute the roll-down as the spread change along the curve over the holding period.
- Record the coupon or premium income and the financing cost.
- Compute the unchanged-curve return and express it as an annualised figure.
- Record the break-even spread move implied by the roll and carry.
- Record the assumption that the curve's shape stays fixed, which roll depends on.

## Procedure

1. Record the current spread and the roll target.
2. Compute roll-down over the period.
3. Compute carry net of financing.
4. Sum to the unchanged-curve return.
5. Derive the break-even move.
6. Write the estimate with its assumption.

## Anti-patterns

- Treating carry as free income without the financing.
- Computing roll-down from a curve that has already moved.
- Assuming the curve's shape is fixed over a long holding period.
- Ignoring the funding cost of the position.
- Quoting a return without the unchanged-curve assumption.

## Done checklist

- [ ] Current and roll-target spreads recorded.
- [ ] Roll-down computed.
- [ ] Carry computed net of financing.
- [ ] Total return computed and annualised.
- [ ] Break-even move derived.
- [ ] Assumption stated.

The break-even is also the cleanest way to compare two curve positions: a trade with positive roll and carry has a cushion, and one with negative roll requires a forecast, so the two are different kinds of commitment regardless of how similar their slopes appear.


## Sources

- Credit market conventions and data: <https://www.isda.org/>
- Rates and financing data: <https://www.federalreserve.gov/>
- Short-rate series: <https://fred.stlouisfed.org/>
