---
name: yield-selling-and-its-tail
domain: crypto-trading/yield-selling-and-its-tail
trigger: "Evaluating selling covered calls or cash-secured puts for yield."
anti_trigger: "Not for recommending a strategy, and not for predicting prices."
scope: "Covered calls and cash-secured puts sold for yield, and the loss they concentrate."
status: seedling
---

# Yield selling and its tail

## Standard

Selling covered calls and cash-secured puts is the most common retail option activity in crypto, and it is usually described by its premium rather than by its payoff. A covered call caps the upside of a held position in exchange for a premium; a cash-secured put obliges the seller to buy the coin at the strike if it falls, in exchange for a premium. Both are short volatility, and both concentrate losses in exactly the scenario the seller is least prepared for.

The arithmetic that matters is the annualised premium against the loss the structure accepts. A strategy earning a percent a month while accepting a forty percent drawdown is not comparable to a bond, and the comparison only becomes visible when the premium is annualised and the maximum loss is written beside it. The tail is not hypothetical in a market that has produced multi-day moves of that size.

Primary sources: <https://www.cftc.gov/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the structure, the strike, the expiry, and the premium.
- Compute the annualised premium on the collateral committed.
- Record the maximum loss in currency, and the move that produces it.
- Record the break-even price and the distance to it.
- Record the assignment consequence: the coin position acquired or delivered.
- Record the correlation between the strategy's losses and the rest of the portfolio.

## Procedure

1. Record the structure and terms.
2. Compute the annualised premium.
3. Compute the maximum loss and the move required.
4. Record the break-even and its distance.
5. Record the assignment outcome.
6. Write the comparison against the risk accepted.

## Anti-patterns

- Quoting the premium as a yield without the loss.
- Comparing a short-volatility strategy with a cash return.
- Ignoring the assignment's effect on concentration.
- Assuming the premium compensates for a gap.
- Sizing so that the tail loss exceeds the portfolio's tolerance.

## Done checklist

- [ ] Structure and terms recorded.
- [ ] Annualised premium computed.
- [ ] Maximum loss and move recorded.
- [ ] Break-even recorded.
- [ ] Assignment outcome recorded.
- [ ] Correlation with the portfolio recorded.

The comparison that keeps the strategy honest is against the drawdown it would have suffered in the worst week of the asset's own history: if that drawdown would have consumed the premiums of a year, the strategy is a leveraged position on the asset's calm rather than an income stream, and the record should say so before the position is opened rather than after.


## Sources

- Regulatory guidance on crypto products: <https://www.cftc.gov/>
- Investor education on options strategies: <https://www.investor.gov/introduction-investing>
- Market volatility data: <https://fred.stlouisfed.org/>
