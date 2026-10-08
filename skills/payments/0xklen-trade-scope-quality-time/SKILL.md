---
name: trade-scope-quality-time
description: Use when a fixed deadline meets a fixed scope and something must give. Present the three-way tradeoff as concrete cuts with their cost, and let the decider choose.
---

# Trade scope, quality and time

Scope, quality, and time are three constraints with only two degrees of freedom. A request that fixes all three has not removed the tradeoff; it has just hidden who pays for it.

## Procedure

1. State the three axes plainly: scope (deliverables), quality (defect rate, perf, coverage), and time (the date).

2. Fix the two the requester has genuinely fixed, usually the date, and test whether the third is truly fixed or merely assumed.

3. Produce two or three concrete options, each a named cut with its consequence:
   - ship all scope, date slips 3 days
   - ship cut A and B by the date, C as a fast follow
   - ship everything on the date at 70% test coverage

4. Attach a number to every consequence: days slipped, defect risk, rework cost.

5. Recommend one option and give the reason, then let the owner decide.

6. Record the chosen option so a later complaint points at a decision, not at you.

7. Never absorb all three by working nights; that trades the person for the schedule and hides the real constraint.

## Pitfalls

- Promising all three fixed by working harder, so nobody learns the schedule was wrong.

- Offering "we'll try" instead of a named cut with a price.

- Cutting quality silently by skipping tests instead of offering it as a visible option.

- Presenting options the decider cannot choose between: all bad, no default.

- Treating a deadline as fixed when it was only ever a preference.

## Verification

```
    grep -E '^(scope|quality|time):' TRADEOFF.md   # each axis named with its consequence
```

Report the two fixed axes, the cut you recommend, and each option's cost in days or risk.
