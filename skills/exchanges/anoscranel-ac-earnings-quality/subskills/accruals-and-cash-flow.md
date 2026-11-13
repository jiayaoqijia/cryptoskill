---
name: accruals-and-cash-flow
domain: investing/accruals-and-cash-flow
trigger: "Comparing reported earnings with operating cash flow."
anti_trigger: "Not for accusing a company, and not for the investment case."
scope: "Earnings versus operating cash flow, and what the gap's direction means."
status: seedling
---

# Accruals and cash flow

## Standard

Accrual accounting records revenue when it is earned and expenses when they are incurred, which means reported profit includes amounts that have not yet become cash. The difference between profit and operating cash flow is the accrual balance, and its behaviour over time is one of the most durable signals available: accruals that grow faster than revenue imply that the earnings are increasingly made of estimates rather than receipts.

The direction matters more than the level. A single year of high accruals can follow a large contract or a seasonal build; a persistent pattern in which profit runs ahead of cash across several periods is harder to explain, and it often precedes either a write-down or a period of weak reported growth as the accruals reverse. The record compares the gap with revenue growth over the same window.

Primary sources: <https://www.sec.gov/edgar/search/> and <https://www.sec.gov/investor>.

## Decision rules

- Record net income and operating cash flow for each period in the window.
- Compute the accrual gap and express it as a percentage of revenue and of assets.
- Record the direction of the gap and its trend across at least three periods.
- Record the components driving the gap: receivables, inventory, payables, and provisions.
- Record any explanation the company gives, with the filing reference.
- Where the gap reverses, record the period and what reversed.

## Procedure

1. Pull the cash flow statement and the income statement for the window.
2. Compute the accrual gap per period.
3. Decompose the gap into its balance-sheet drivers.
4. Compare with revenue growth.
5. Record the company's explanation.
6. Write the questions the trend raises.

## Anti-patterns

- Comparing one quarter's profit with one quarter's cash flow.
- Treating a seasonal working-capital build as a quality signal.
- Ignoring the reversal period.
- Reading a single year's gap as a pattern.
- Concluding misconduct from a gap the filings explain.

## Done checklist

- [ ] Profit and cash flow recorded per period.
- [ ] Gap computed as a ratio.
- [ ] Drivers decomposed.
- [ ] Trend across three periods recorded.
- [ ] Company explanation referenced.
- [ ] Questions written.

A useful comparison is against the company's own history rather than against a peer: the level of accruals differs by business model, and a retailer carrying inventory will always look different from a software company recognising subscription revenue, so the question the data can answer is whether this company's gap has widened relative to its own past.


## Sources

- Company filings and full-text search: <https://www.sec.gov/edgar/search/>
- Disclosure framework: <https://www.sec.gov/investor>
- Investor education on financial statements: <https://www.investor.gov/introduction-investing>
