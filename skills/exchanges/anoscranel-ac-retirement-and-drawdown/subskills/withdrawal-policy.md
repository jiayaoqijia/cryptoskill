---
name: withdrawal-policy
domain: investing/withdrawal-policy
trigger: "Writing the spending rule that governs withdrawals."
anti_trigger: "Not for computing a safe rate, and not for tax advice."
scope: "Fixed real versus dynamic withdrawals, guardrails, and the written spending rule."
status: seedling
---

# Withdrawal policy

## Standard

A withdrawal policy is the spending half of the investment policy statement. It specifies how much is taken, when, from where, and under what conditions the amount changes. The two families are fixed real withdrawals — the same inflation-adjusted amount each year — and dynamic rules that adjust spending with portfolio value or market conditions.

Fixed real is simple and exposes the portfolio to sequence risk; dynamic rules reduce that risk at the cost of variable spending. The honest policy states which family it uses, the rules inside it, and the bounds: a floor below which spending will not fall, and a ceiling above which it will not rise, so the plan remains a plan rather than a reaction.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://www.irs.gov/>.

## Decision rules

- The policy states the withdrawal basis: fixed real amount, or a percentage of portfolio value.
- A dynamic rule names its trigger, its adjustment size, and its frequency.
- Spending floors and ceilings are stated, because an unbounded rule is not a policy.
- Withdrawals are scheduled, not discretionary; the schedule is recorded.
- The rule is written before the first withdrawal and revised only at a review.
- Changes to the rule are versioned with dates and reasons.

## Procedure

1. Choose the basis and record the reasoning.
2. If dynamic, write the trigger, adjustment, and frequency.
3. Set the floor and ceiling in real terms.
4. Set the withdrawal schedule and the account order.
5. Test the policy against a poor-first-decade scenario.
6. Record it as part of the drawdown policy.

## Anti-patterns

- Taking withdrawals whenever needed with no rule.
- A dynamic rule with no floor, which permits spending to collapse.
- Revising the rule during a bad month.
- Mixing fixed and dynamic without a stated precedence.
- Leaving the schedule informal.

## Done checklist

- [ ] Withdrawal basis chosen and justified.
- [ ] Dynamic rule parameters written where applicable.
- [ ] Floor and ceiling set in real terms.
- [ ] Schedule and account order recorded.
- [ ] Policy stress-tested.
- [ ] Policy recorded and versioned.

## Sources

- Investor education on retirement withdrawals: <https://www.investor.gov/introduction-investing>
- Tax context for withdrawal sequencing: <https://www.irs.gov/>
- Inflation data for real-terms rules: <https://fred.stlouisfed.org/>

The floor and ceiling are what make a dynamic rule usable: without them, a mechanical adjustment can prescribe spending that the household will not follow, and a rule that is not followed is worse than no rule because it hides the actual behaviour. Set bounds that the household can live with, then let the rule work inside them.
