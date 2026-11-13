---
name: buyback-offset-arithmetic
domain: investing/buyback-offset-arithmetic
trigger: "Working out how much buyback is needed to hold the share count flat."
anti_trigger: "Not for evaluating the buyback as capital allocation, and not for tax advice."
scope: "How much repurchase is needed to hold the count flat."
status: seedling
---

# Buyback offset arithmetic

## Standard

A buyback offsets dilution when the shares repurchased equal the shares newly issued. The arithmetic is a ratio rather than a judgment: if a company issues two percent of its count each year through compensation, it must repurchase two percent to stand still, and any shortfall is net dilution that reduces each holder's claim.

The comparison that makes this legible is between the cash spent on the buyback and the expense recognised for the compensation. If the two are close, the company is effectively paying cash for the shares it gives employees, and the compensation is a cash cost routed through the equity market. If the buyback is smaller, the difference is being funded by the holders through dilution, which is a transfer that no line in the income statement records.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record shares issued for compensation over the period.
- Record shares repurchased over the same period.
- Compute the net change and express it as a percentage of the opening count.
- Compute the buyback spend and compare it with the compensation expense.
- Record the average repurchase price and compare it with the average grant price.
- Record whether the buyback was debt-funded, which adds a second cost.

## Procedure

1. Record the opening and closing counts.
2. Record shares issued and repurchased separately.
3. Compute net dilution as a percentage.
4. Compare buyback spend with compensation expense.
5. Compare repurchase price with grant price.
6. Write the finding with the net position stated.

## Anti-patterns

- Describing a buyback as a return of capital when it only offsets issuance.
- Ignoring the price at which shares are repurchased relative to the price at which they are granted.
- Measuring dilution from the diluted count alone, which hides the movement.
- Overlooking debt-funded repurchases, which add interest cost.
- Assuming a buyback reduces the count when the net change is positive.

## Done checklist

- [ ] Opening and closing counts recorded.
- [ ] Issuance and repurchase recorded separately.
- [ ] Net dilution computed as a percentage.
- [ ] Buyback spend compared with expense.
- [ ] Repurchase and grant prices compared.
- [ ] Funding source recorded.

The offset also has a timing problem: grants vest on a calendar while repurchases happen when the company chooses, so a year of heavy vesting can be offset by a repurchase in the following period, and a single-year comparison can mislead either way. The record should state whether the offset is measured on the same period or on a rolling basis.


## Sources

- Share count and repurchase disclosure: <https://www.sec.gov/investor>
- Investor education on buybacks and dilution: <https://www.investor.gov/introduction-investing>
- Market data for price comparison: <https://fred.stlouisfed.org/>
