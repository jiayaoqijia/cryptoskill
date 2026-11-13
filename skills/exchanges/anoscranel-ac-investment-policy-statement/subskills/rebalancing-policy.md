---
name: rebalancing-policy
domain: investing/rebalancing-policy
trigger: "Deciding when and how the portfolio returns to its target weights."
anti_trigger: "Not for changing the targets, and not for trading around the bands."
scope: "Calendar versus threshold rebalancing, the bands, and the cost of each choice."
status: seedling
---

# Rebalancing policy

## Standard

Rebalancing is the mechanism that keeps the portfolio at its policy weights. There are two honest designs: calendar-based, which restores weights on a schedule regardless of drift, and threshold-based, which acts only when a holding leaves its band. Both are defensible; mixing them without a rule is not, because then every decision is discretionary and the policy stops constraining anything.

The cost side matters. Every rebalance incurs spreads, fees, and possibly taxes, so a threshold that fires constantly is a policy for transferring value to intermediaries. The band width should be wide enough that the expected benefit exceeds the cost, and the record should say what that estimate was based on.

Primary sources: <https://www.cfainstitute.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- One primary mechanism: calendar, threshold, or a stated hybrid with a fixed order of precedence.
- Bands are set wide enough to survive normal volatility without firing.
- Rebalancing uses cash flows first where possible, to avoid unnecessary transactions.
- Tax consequences are considered before the trade, and the policy states whether they can override a rebalance.
- The rebalancing rule is written before the first rebalance and is not revised during a drawdown.
- Every rebalance is recorded with the trigger, the trades, and the cost.

## Procedure

1. Choose the mechanism and write the precedence rule.
2. Set band widths with a stated rationale.
3. Define the cash-flow-first rule.
4. State the tax override policy, if any.
5. Record the rule in the policy statement.
6. Log each rebalance with trigger, trades, and cost.

## Anti-patterns

- Rebalancing whenever the owner feels uneasy.
- Bands so tight the portfolio trades constantly.
- Ignoring tax on the sale side.
- Changing the mechanism after it forces an uncomfortable trade.
- Rebalancing without recording the trigger.

## Done checklist

- [ ] Mechanism chosen and precedence stated.
- [ ] Band widths set with rationale.
- [ ] Cash-flow-first rule defined.
- [ ] Tax override policy stated.
- [ ] Rule entered in the policy statement.
- [ ] Rebalance log maintained with cost.

## Sources

- Investment-policy reference material: <https://www.cfainstitute.org/>
- Investor education on rebalancing: <https://www.investor.gov/introduction-investing>
- Regulatory context for trading costs and disclosure: <https://www.sec.gov/investor>

The cost of rebalancing is small per trade and large in aggregate, which is why the band width matters more than the mechanism. A rule that fires often enough to feel responsive is usually a rule that pays intermediaries for the comfort. Record the estimated cost of a typical rebalance when the rule is written, and compare it against the drift the bands are meant to contain; the comparison, not the preference, should set the width.

