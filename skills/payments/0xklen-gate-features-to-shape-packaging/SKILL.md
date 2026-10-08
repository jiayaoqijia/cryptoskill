---
name: gate-features-to-shape-packaging
description: Use when deciding which features sit behind which plan. Picks gates that segment buyers by willingness to pay without blocking activation, and prices the value metric that grows with use.
---

# Gate features to shape packaging

A gate is a pricing tool, not a feature flag. The right fence separates buyers who value a feature differently; the wrong one blocks the first ten minutes of use and taxes every customer.

## Procedure

1. Classify each feature by who cares: individual activation (single-user exports), team collaboration (shared workspaces), and governance (SSO, audit logs, role control).
2. Never gate activation. If a user cannot reach first value on the free or entry plan, the gates further up are never seen.
3. Anchor the value metric to what the customer's usage grows: seats, events, documents, or GB. Pick one and let tiers differ in its allowance.
4. Map governance features to the top tier, because willingness to pay for control scales with headcount, not with usage.
5. Quantify the gate: if 40% of accounts hit a gated limit monthly and 15% of those upgrade to lift it, the gate converts 15% of the hitting cohort, not 15% of all accounts.
6. Price the allowance so the natural growth path crosses a limit: a 1,000-event tier for a customer running 1,400 events is a 40% overage decision — an upgrade or a wall.
7. Measure the conversion the gate causes, not the gate's existence:

       ```
       python3 -c "from decimal import Decimal as D; print(D('0.15')/D('0.40'))"
       # 0.375 -> 15% of all accounts is 37.5% of the accounts that actually hit the limit
       ```

8. Keep allowances as integer counts and prices as integer minor units (`limit=1000`, `price_minor=4900`); a float threshold triggers the gate one event early or late at the boundary.
9. Avoid gating by arbitrary seat counts when usage is the real driver; it lets a heavy user pay the light-user price.
10. Review yearly. A gate everyone crosses is a feature, and a gate nobody crosses is dead weight on the pricing page.

## Pitfalls

- Gating an activation feature, so trial users never reach the value that would upgrade them.
- A limit so generous nobody hits it, which is not a gate but decoration.
- Mixing the value metric across tiers, so a customer cannot tell what they are buying.
- Counting a limit-hit as an upgrade without measuring whether it converted.
- Overage pricing so sharp it turns growth into an adversarial negotiation.
- Float thresholds that trip the gate at the wrong event count.

## Verification

    ```
    python3 -c "from decimal import Decimal as D; print(D('0.15')/D('0.40'))"
    # 0.375 -> upgrade rate on the cohort that hits the limit
    ```

Pass when each gate names its value metric and the conversion it causes on the hitting cohort. Report every gate, its metric, and the cohort conversion it produced.
