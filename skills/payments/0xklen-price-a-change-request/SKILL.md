---
name: price-a-change-request
description: Use when someone asks for an addition or alteration mid-task. Estimate its time, risk, and regression cost before agreeing, and return a price rather than a yes.
---

# Price a change request

"Sure, quick" is how a schedule dies. A change with no price has not been accepted, it has been absorbed, and the cost surfaces later as a missed date with no one to blame.

## Procedure

1. Restate the change as a deliverable with a definition of done.

2. Estimate three costs separately:
   - build time in half-days
   - risk of touching already-tested code (does it invalidate prior test runs?)
   - deferral cost, meaning what slips to pay for the change

3. Name what it displaces: adding X means Y does not ship by the date, so name Y.

4. Give the price in one line: `2 days; pushes the release to Thu; re-tests the sync path`.

5. Classify against the change-order threshold: small absorbs and logs, medium needs written agreement, large triggers a re-plan.

6. Log the priced change to `CHANGES.md` with the requester, the cost, and the decision.

7. If the change is declined, the price is the answer; do not do it anyway as a favour.

## Pitfalls

- Accepting "it's just a small thing" with no price, then watching it eat the buffer.

- Counting build time only and ignoring re-test, review, and rollback cost.

- Failing to name the displaced work, so the tradeoff stays invisible.

- Pricing so late the change is already built; price before you start.

- Absorbing a bug the change exposes as free extra work.

## Verification

```
    grep -E '^- \[ \] .*days' CHANGES.md   # each change carries a cost estimate
```

Report the change, its three costs, and the work it displaces before accepting.
