---
name: securities-backed-lending
domain: investing/securities-backed-lending
trigger: "Comparing a securities-backed loan with a margin account."
anti_trigger: "Not for arranging a loan, and not for legal or tax advice."
scope: "LTV ratios, covenants, and the difference between a margin account and a loan against assets."
status: seedling
---

# Securities-backed lending

## Standard

A securities-backed loan is a loan secured on a portfolio, usually with a fixed advance ratio, a stated interest rate, and covenants. It differs from a margin account in three ways that matter: the lender sets an LTV rather than a maintenance margin, the loan may be non-recourse or recourse, and the covenants can require action long before a margin call would.

The covenant structure is where the risk hides. A loan-to-value covenant is a threshold on the ratio, not on the portfolio's value, so a fall in the collateral and a draw on the facility can both trigger it. A cure right may allow the borrower to post more collateral or repay a portion, and the absence of a cure right converts a temporary shortfall into a forced sale or an acceleration.

Primary sources: <https://www.federalreserve.gov/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the LTV, the collateral eligibility, and the valuation method.
- Record whether the loan is recourse or non-recourse.
- Record every covenant with its threshold, its testing frequency, and its cure right.
- Record the draw mechanics and whether the facility is revolving.
- Record the consequences of a breach: cure, partial repayment, or acceleration.
- Where a covenant has no cure, record the sale that would follow.

## Procedure

1. Read the facility agreement and extract the LTV and eligibility terms.
2. Record the covenants with thresholds and testing dates.
3. Record the cure rights and their limits.
4. Identify the collateral valued and the valuation source.
5. Model a collateral fall to the covenant threshold.
6. Write the structure summary with the breach path.

## Anti-patterns

- Treating an LTV as equivalent to a maintenance margin.
- Missing a covenant that is tested more often than the LTV.
- Assuming a cure right exists.
- Ignoring recourse status for the borrower's wider balance sheet.
- Accepting the lender's valuation of illiquid collateral at face value.

## Done checklist

- [ ] LTV and eligibility recorded.
- [ ] Recourse status recorded.
- [ ] Every covenant with threshold and cure recorded.
- [ ] Draw mechanics recorded.
- [ ] Breach consequences recorded.
- [ ] Model of the breach path written.

A comparison of facilities should include what happens at maturity: a revolving line and a term loan behave differently when the market is closed for refinancing, and a facility that must be rolled in a crisis is a stronger commitment than its rate suggests.

## Sources

- Securities credit and lending context: <https://www.federalreserve.gov/>
- Investor education on borrowing against assets: <https://www.investor.gov/introduction-investing>
- Regulatory material on collateral and margin: <https://www.finra.org/>
