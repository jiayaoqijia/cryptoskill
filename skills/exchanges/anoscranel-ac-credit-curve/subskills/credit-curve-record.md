---
name: credit-curve-record
domain: investing/credit-curve-record
trigger: "Writing the record of a credit curve position and its assumptions."
anti_trigger: "Not for recommending a credit, and not for default prediction."
scope: "The written record: points, shape, roll assumption, and weights."
status: seedling
---

# Credit curve record

## Standard

The credit curve record states the points used, the shape at entry, the roll and carry assumed, the weights of any curve position, and the break-even slope change. It is written so that a later review can separate a result earned from the curve staying stable from one earned from the slope moving as intended.

The record also carries the liquidity constraint, because a curve trade is sized to the leg that is hardest to trade and that leg determines both the maximum size and the exit cost. Stating it beside the weights makes the position's practical limit visible at entry rather than at the point of unwinding.

Primary sources: <https://www.isda.org/> and <https://osf.io/prereg/>.

## Decision rules

- The record states the quoted points and maturities, and marks interpolated segments.
- The shape is described in one sentence with the slope values.
- Roll and carry are recorded with the assumption that the curve's shape is fixed.
- The weights are recorded with the DV01 used per leg.
- The break-even slope change is recorded in basis points.
- Liquidity per leg and the resulting maximum size are recorded.

## Procedure

1. Record the points and the shape.
2. Record roll and carry with the assumption.
3. Record weights and DV01.
4. Record the break-even slope.
5. Record liquidity and maximum size.
6. Review at each roll period and on any curve move.

## Anti-patterns

- Recording a shape without the points behind it.
- Omitting the fixed-shape assumption from the roll estimate.
- Recording weights without the DV01 that produced them.
- No liquidity constraint, so the position is sized beyond the harder leg.
- Reviewing only the profit and loss rather than the slope.

## Done checklist

- [ ] Points and shape recorded.
- [ ] Roll and carry recorded with assumption.
- [ ] Weights and DV01 recorded.
- [ ] Break-even slope recorded.
- [ ] Liquidity and maximum size recorded.
- [ ] Review cadence set.

A final field worth adding is the review date tied to the roll: a curve position's economics change as it ages along the curve, so a record reviewed only on calendar dates can describe a position whose roll assumption has already expired.


The record should also state which maturity the position will roll toward, because that target determines the roll arithmetic and changes as the position ages, so a record without it cannot be checked against the market later.


## Sources

- Credit market conventions: <https://www.isda.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Market and spread data: <https://www.federalreserve.gov/>
