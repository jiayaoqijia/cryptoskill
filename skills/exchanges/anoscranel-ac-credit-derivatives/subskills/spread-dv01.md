---
name: spread-dv01
domain: investing/spread-dv01
trigger: "Sizing a credit position by spread sensitivity rather than notional."
anti_trigger: "Not for predicting spreads, and not for borrower analysis."
scope: "Spread sensitivity, hedge ratios, and why notional matching misleads."
status: seedling
---

# Spread DV01

## Standard

Spread DV01 is the change in the value of a credit position for a one-basis-point move in spread. It is the credit analogue of a bond's DV01, and it is the only unit in which positions of different maturities and different names can be compared or hedged. Matching notional instead is the most common sizing error in credit, because a five-year contract and a one-year contract with the same notional carry very different sensitivities.

The sensitivity falls as maturity shortens and as the spread level rises, and it rises with the credit's riskiness at a given spread because the probability-weighted payoff is larger. Two positions with the same spread can therefore have materially different DV01s, and a hedge built on spread alone will drift as the position ages.

Primary sources: <https://www.isda.org/> and <https://www.federalreserve.gov/>.

## Decision rules

- Compute spread DV01 per position and per unit of notional.
- Size hedges by matching spread DV01, not notional.
- Record the maturity and spread level used in the calculation.
- Record how DV01 changes as the position ages towards maturity.
- Record the DV01 of each leg in a basis or index trade.
- Recompute the hedge ratio at stated intervals and at spread moves.

## Procedure

1. Compute the position's spread DV01 at the current spread and maturity.
2. Compute the hedging instrument's spread DV01.
3. Divide to get the hedge notional.
4. Record the maturity decay of the sensitivity.
5. Recompute at the review trigger.
6. Record the ratio and its basis.

## Anti-patterns

- Hedging credit exposure by matching notional.
- Ignoring that DV01 changes as the contract seasons.
- Using a single maturity's DV01 for a portfolio of maturities.
- Treating spread DV01 as constant across a large spread move.
- Comparing index and single-name risks on notional.

## Done checklist

- [ ] Spread DV01 computed per position.
- [ ] Hedge notional computed from DV01.
- [ ] Maturity and spread inputs recorded.
- [ ] Decay recorded.
- [ ] Recalculation trigger set.
- [ ] Ratio and basis recorded.

The sensitivity also depends on the assumed recovery, since a lower recovery raises the payout for a given event probability and therefore raises the DV01: a hedge computed on one recovery assumption and measured against another will appear to drift even when the spread has not moved.

## Sources

- Credit derivatives market standards: <https://www.isda.org/>
- Market and rate data: <https://www.federalreserve.gov/>
- Spread and rate series: <https://fred.stlouisfed.org/>
