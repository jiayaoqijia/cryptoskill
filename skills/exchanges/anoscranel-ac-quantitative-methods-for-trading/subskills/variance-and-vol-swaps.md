---
name: variance-and-vol-swaps
domain: crypto-trading/variance-and-vol-swaps
trigger: "Pricing or reading a variance or volatility swap."
anti_trigger: "Not for predicting volatility, and not for options execution."
scope: "Payoff mechanics, convexity, and the volatility risk premium."
status: seedling
---

# Variance and vol swaps

## Standard

A variance swap pays the difference between realized variance over a period and a fixed strike, with no delta to manage. A volatility swap pays the same comparison on volatility — the square root — and the root makes its payoff concave in variance: gains per variance point shrink as realized variance rises, while losses per variance point grow as it falls. Jensen's inequality follows directly, which is why the fair volatility strike sits below the square root of the variance strike, the gap being the concavity the market charges for.

The strike on either instrument is not the same as the at-the-money implied volatility, because the payoff's convexity means the market charges for more than the level. The variance strike sits near a weighted average of implied across strikes with the weights that the replication demands, which is why the strike reads as a composite and why comparing it to a single at-the-money implied misprices the trade. The difference between the realized variance that arrives and the strike paid for is the volatility risk premium, and it is a premium for a reason.

Primary sources: <https://www.cboe.com/> and <https://www.isda.org/>.

## Decision rules

- Record the contract type: variance or volatility, and the curvature it implies: the variance payoff is convex in the underlying's moves, the volatility payoff concave in variance.
- Record the strike, the convention (annualised, percentage), and the notional units.
- Record how realized variance is computed and from which prices.
- Record the strike's relation to the implied surface, not to one point.
- Record the tail exposure of a variance payoff: large moves dominate quadratically.
- Record the settlement date and the disruption provisions.

## Procedure

1. Identify the contract type and its payoff formula.
2. Record strike, conventions, and notional units.
3. Record the realized-variance calculation in full.
4. Compare the strike to the surface it came from.
5. Compute the payoff under a jump and under a quiet period.
6. Record settlement terms in the trade file.

## Anti-patterns

- Comparing the strike to a single at-the-money implied.
- Treating volatility and variance quotes as interchangeable.
- Ignoring the quadratic payoff's sensitivity to a single large move.
- Reading the strike as expected realized rather than the market's asking price.
- Overlooking the calculation convention, which differs between contracts.

## Done checklist

- [ ] Contract type and payoff recorded.
- [ ] Conventions and units recorded.
- [ ] Realized calculation recorded.
- [ ] Strike's surface origin recorded.
- [ ] Jump and quiet payoffs computed.
- [ ] Settlement terms recorded.

## Sources

- Volatility derivative markets and data: <https://www.cboe.com/>
- Derivative documentation standards: <https://www.isda.org/>
- Volatility series for context: <https://fred.stlouisfed.org/>
