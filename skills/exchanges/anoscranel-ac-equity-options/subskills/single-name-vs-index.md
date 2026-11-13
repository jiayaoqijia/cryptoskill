---
name: single-name-vs-index
domain: investing/single-name-vs-index
trigger: "Choosing between a single-name option and an index option."
anti_trigger: "Not for predicting prices, and not for generic option theory."
scope: "Two contract families with different settlement, liquidity, and risk."
status: seedling
---

# Single-name versus index options

## Standard

Single-name options and index options are different instruments that share a vocabulary. A single-name contract is American, physically settled into shares, and exposed to one company's news, dividends, and borrow. An index contract is usually European, cash-settled, and exposed to a weighted average of many companies, which makes its volatility a function of correlation as much as of the components' own volatility.

The practical differences follow. Liquidity concentrates in index options for large notional hedging, and in a handful of mega-cap names for single-name trading; a mid-cap option may quote but not trade at size. Settlement matters too: a cash-settled index option pays a difference and never delivers shares, while a single-name option exercised delivers a stock position with everything that follows.

Primary sources: <https://www.cboe.com/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the contract family, its exercise style, and its settlement method.
- Record the underlying's liquidity and, for a single name, its borrow status.
- Record the dividend schedule where the option is American.
- Record the index's concentration, since a few names can dominate its volatility.
- Record whether the position's purpose is hedging a portfolio or expressing a single-name view.
- Where the position crosses families, record the correlation exposure it creates.

## Procedure

1. Identify the contract and its specification.
2. Record exercise style and settlement.
3. Record liquidity, borrow, and dividends.
4. Record index concentration where applicable.
5. State the purpose and the exposure the family choice creates.
6. Write the summary with the specification reference.

## Anti-patterns

- Treating an index option as a diversified version of a single-name option.
- Ignoring the dividend schedule on an American single-name call.
- Assuming index concentration does not affect volatility.
- Comparing implied volatilities across families as if they measured the same thing.
- Overlooking physical settlement on exercise.

## Done checklist

- [ ] Contract family and specification recorded.
- [ ] Exercise and settlement recorded.
- [ ] Liquidity, borrow, dividends recorded.
- [ ] Index concentration noted.
- [ ] Purpose recorded.
- [ ] Cross-family exposure recorded.

A further distinction is the information content of the two: a single-name option's implied volatility reflects one company's event calendar, while an index's reflects the market's expectation of the aggregate, so a comparison between them is a comparison of two different questions rather than of two prices for the same risk.


## Sources

- Exchange option specifications and product data: <https://www.cboe.com/>
- Regulatory context for listed options: <https://www.sec.gov/investor>
- Investor education on options: <https://www.investor.gov/introduction-investing>
