---
name: allocation-in-drawdown
domain: investing/allocation-in-drawdown
trigger: "Setting asset allocation when the portfolio is funding spending."
anti_trigger: "Not for predicting returns, and not for product selection."
scope: "How allocation changes when spending is funded from the portfolio, and the limits of bucket approaches."
status: seedling
---

# Allocation in drawdown

## Standard

Allocation during drawdown answers a different question from allocation during accumulation: not how much risk to take for growth, but how much of the portfolio must be safe for near-term spending and how much can stay exposed for later. The answer is driven by the reserve requirement and the horizon that remains, not by a target return.

Bucket approaches formalise this: a spending bucket of safe assets, a medium bucket, and a growth bucket. The idea is sound — match the asset to when the money is needed — but the implementation often drifts, because the buckets are refilled from the growth side after good years and not after bad ones, which reintroduces the sequence risk the structure was meant to reduce.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://fred.stlouisfed.org/>.

## Decision rules

- Allocation derives from the reserve requirement: years of spending covered by safe assets.
- The reserve is sized in years, not in a percentage chosen by convention.
- Bucket refill rules are written, including the rule for bad years.
- The growth allocation is stated with its horizon and its tolerable drawdown.
- Rebalancing in drawdown prefers refilling from cash flows over selling growth assets at a loss.
- Allocation changes are policy changes, versioned.

## Procedure

1. Compute years of spending to be held in safe assets.
2. Choose the instruments for the reserve and record the reasoning.
3. Write the bucket refill rules for good and bad years.
4. Set the growth allocation with the tolerable drawdown stated.
5. Test the structure against a poor-first-decade scenario.
6. Record the allocation and the rules in the drawdown policy.

## Anti-patterns

- Choosing an allocation from a rule of thumb rather than the reserve requirement.
- Buckets with no refill rule.
- Refilling only after good years.
- Selling growth assets to refill the bucket in a drawdown.
- Treating the bucket structure as removing risk.

## Done checklist

- [ ] Reserve computed in years of spending.
- [ ] Reserve instruments chosen and recorded.
- [ ] Refill rules written for both directions.
- [ ] Growth allocation and tolerable drawdown stated.
- [ ] Structure stress-tested.
- [ ] Allocation recorded in policy.

## Sources

- Investor education on asset allocation in retirement: <https://www.investor.gov/introduction-investing>
- Return and inflation data: <https://fred.stlouisfed.org/>
- Tax context for asset location: <https://www.irs.gov/>

The reserve's size is the policy's most consequential number, and it is also the one most often chosen by feel. Sizing it in years of spending, and writing why that number, makes the trade-off explicit: every year of reserve is a year of possible poor returns absorbed, bought with the return the reserve does not earn.
