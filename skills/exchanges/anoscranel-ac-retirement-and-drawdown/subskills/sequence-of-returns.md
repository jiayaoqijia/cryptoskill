---
name: sequence-of-returns
domain: investing/sequence-of-returns
trigger: "Managing the risk that poor returns arrive early in drawdown."
anti_trigger: "Not for forecasting returns, and not for allocation policy."
scope: "Why the order of returns matters when money is leaving the portfolio, and how the risk is managed."
status: seedling
---

# Sequence of returns

## Standard

When money is leaving a portfolio, the order of returns matters in a way it does not while saving. A large fall early in drawdown sells shares at low prices to fund spending, leaving fewer shares to participate in the recovery; the same average return applied in a different order produces a different ending balance, and sometimes a different lifetime.

The risk is managed by structure rather than by prediction. Spending from assets that are not exposed to the fall — cash reserves, short-duration bonds — buys time for the equity portion to recover. A dynamic withdrawal rule that trims spending after a poor year reduces the amount sold at low prices. Neither removes the risk; both change which failure mode dominates.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://fred.stlouisfed.org/>.

## Decision rules

- The record states the sequence risk explicitly: early poor returns are the binding scenario.
- Spending is funded first from assets not exposed to the fall, where the reserve exists.
- The reserve size is stated in months or years of spending, with its opportunity cost.
- A dynamic rule specifies the trigger and the size of the spending adjustment before it is needed.
- Simulations test a poor first decade, not just a poor average.
- The policy distinguishes a temporary fall from a permanent shortfall.

## Procedure

1. Record the reserve size in months of spending and its composition.
2. Model a poor-first-decade scenario and record the portfolio path.
3. Write the trigger that would move the portfolio into the reserve.
4. Specify the spending adjustment rule and its size.
5. Test the rule against the stress scenario.
6. Record the policy with its assumptions.

## Anti-patterns

- Planning on average returns without an early-fall case.
- Holding a reserve without stating its opportunity cost.
- Writing a dynamic rule that can be waived in the moment.
- Treating a poor first year as evidence of a permanent shortfall.
- Assuming the reserve removes the risk rather than shifting it.

## Done checklist

- [ ] Sequence risk stated in the record.
- [ ] Reserve sized and composed.
- [ ] Poor-first-decade scenario modelled and recorded.
- [ ] Trigger and adjustment rule written.
- [ ] Rule tested against the stress case.
- [ ] Policy recorded with assumptions.

## Sources

- Investor education on withdrawal planning: <https://www.investor.gov/introduction-investing>
- Inflation and return data: <https://fred.stlouisfed.org/>
- Tax context for withdrawals: <https://www.irs.gov/>
