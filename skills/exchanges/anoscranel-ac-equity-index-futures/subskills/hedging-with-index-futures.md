---
name: hedging-with-index-futures
domain: investing/hedging-with-index-futures
trigger: "Hedging a portfolio with index futures and measuring the residual."
anti_trigger: "Not for predicting the index, and not for portfolio policy."
scope: "Beta, contract count, and tracking error between a portfolio and the index."
status: seedling
---

# Hedging with index futures

## Standard

Hedging a portfolio with index futures means selling contracts whose notional exposure offsets the portfolio's market exposure. The number of contracts is the portfolio value times its beta, divided by the contract's notional, and the beta is the estimate that carries the uncertainty: a hedge built on a historical beta is a hedge against the past relationship, not against the next one.

The residual is what the hedge leaves behind. A portfolio of large-cap technology stocks hedged with a broad index future retains the spread between technology and the index, which can be larger than the market exposure the hedge removed. The record states the hedge ratio, the beta estimate and its window, and the residual exposure the hedge does not address, because a hedge that is measured only by its contract count is a hedge of unknown quality.

Primary sources: <https://www.cmegroup.com/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the portfolio value, its beta, the beta's estimation window, and the index used.
- Compute the contract count from beta times value divided by contract notional.
- Record the residual exposures the hedge does not remove: sector, factor, and single-name concentration.
- Record the margin required and the cash or collateral that must be posted.
- Record the roll and cost assumptions over the intended hedge horizon.
- Record the conditions that would end the hedge.

## Procedure

1. Estimate the portfolio's beta to the chosen index over a stated window.
2. Compute the contract count and round to a tradeable number.
3. Record the residual exposures by sector and factor.
4. Record the margin and collateral requirement.
5. Record the roll plan and expected cost.
6. Write the hedge record with its triggers.

## Anti-patterns

- Hedging by notional rather than by beta.
- Using a beta estimated over a period that excludes stress.
- Ignoring the residual sector exposure.
- Forgetting the margin and collateral the hedge requires.
- Leaving a hedge in place after the condition that justified it ended.

## Done checklist

- [ ] Beta, window, and index recorded.
- [ ] Contract count computed.
- [ ] Residual exposures recorded.
- [ ] Margin and collateral recorded.
- [ ] Roll plan and cost recorded.
- [ ] Exit conditions written.

A further point is that the hedge's cost is not only the roll and the margin: selling futures forgoes the dividends the cash portfolio continues to receive only if the hedge is implemented through the future's basis, which already nets them out, so the two effects should not be counted twice in the comparison.


## Sources

- Index futures contract data: <https://www.cmegroup.com/>
- Investor education on hedging: <https://www.investor.gov/introduction-investing>
- Market factor and volatility data: <https://fred.stlouisfed.org/>
