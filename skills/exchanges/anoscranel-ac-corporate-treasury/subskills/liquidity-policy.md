---
name: liquidity-policy
domain: investing/liquidity-policy
trigger: "Judging whether a company's cash buffer is adequate for its business."
anti_trigger: "Not for the investment case, and not for credit scoring."
scope: "The cash buffer, its size relative to the business, and what it may be invested in."
status: seedling
---

# Liquidity policy

## Standard

A cash buffer exists to fund the business through a period when its cash flows are interrupted, so its size is a function of the business's volatility rather than of a target multiple. A company with contracted recurring revenue needs less than one with seasonal working capital and lumpy capital expenditure, and a comparison that ignores the difference produces a buffer that looks conservative in one case and inadequate in the other.

What the buffer may be invested in is a second decision, and the constraint is preservation rather than return. A policy that permits only deposits and short-dated government paper is preserving the buffer; one that permits longer-dated or lower-rated instruments is taking a return that the treasury does not need and cannot afford to lose, because the buffer's purpose is to be available precisely when other assets are not.

Primary sources: <https://www.sec.gov/investor> and <https://www.federalreserve.gov/>.

## Decision rules

- Record the cash and equivalents balance and its change over several periods.
- Record the buffer as months of operating expense and as a percentage of debt due within a year.
- Record the seasonal and cyclical swing in operating cash flow.
- Record the permitted instruments and their maximum maturity.
- Record the weighted average maturity of the invested buffer.
- Record the committed undrawn facilities, which are liquidity that does not sit on the balance sheet.

## Procedure

1. Record the cash balance and its trend.
2. Compute the buffer in months of operating expense.
3. Compute it against near-term debt maturities.
4. Record the seasonal swing in cash flow.
5. Record the permitted instruments and maturities.
6. Record undrawn committed facilities and write the total liquidity position.

## Anti-patterns

- Judging a buffer by a fixed multiple without the business's volatility.
- Counting an undrawn facility as equivalent to cash without checking its conditions.
- Ignoring the buffer's investment policy, which determines whether it is available.
- Comparing buffers across industries with different working capital cycles.
- Treating a revolver that depends on covenant compliance as unconditional liquidity.

## Done checklist

- [ ] Buffer recorded in months of expense.
- [ ] Buffer compared with near-term maturities.
- [ ] Seasonal swing recorded.
- [ ] Permitted instruments and maturities recorded.
- [ ] Undrawn facilities recorded with conditions.
- [ ] Total liquidity position written.

## Sources

- Corporate liquidity disclosure: <https://www.sec.gov/investor>
- Money market and rate data: <https://www.federalreserve.gov/>
- Investor education on liquidity: <https://www.investor.gov/introduction-investing>
