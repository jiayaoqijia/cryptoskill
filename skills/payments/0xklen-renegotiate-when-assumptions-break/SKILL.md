---
name: renegotiate-when-assumptions-break
description: Use when a premise the plan rested on turns out false, such as data being larger or an API being gone. Re-open the agreement explicitly instead of quietly absorbing the delta.
---

# Renegotiate when assumptions break

An estimate is a promise conditional on its assumptions. When a premise fails, the promise is void, and the honest move is to re-open it, not to grind through extra work and hope nobody notices the date drift.

## Procedure

1. Detect the break: a measured fact (row count, response size, a missing endpoint) contradicts a recorded assumption.

2. Quantify the delta in the units that matter: twice as big, 400 ms slower, three extra days.

3. Do not absorb it silently. The moment you quietly do more, the agreement is void and the estimate becomes a lie.

4. Re-open the agreement on the same three axes, scope, quality, and time, plus the new fact.

5. Present the cheapest re-plan that still reaches the goal, and the cost of keeping the original scope fixed.

6. Get fresh confirmation in writing (a recap with an objection deadline) before continuing on the new basis.

7. Version the scope document and keep the old version, so the change stays auditable.

## Pitfalls

- Grinding through the extra work to "not bother anyone", hiding a schedule break until it is unrecoverable.

- Re-negotiating on a call and never writing the new terms down.

- Presenting the new facts without a recommended re-plan, pushing the analysis uphill.

- Treating one broken assumption as licence to change everything.

- Re-negotiating so often that confidence in any plan collapses.

## Verification

```
    grep -n 'assumption' SCOPE.md   # the broken assumption and its re-plan are recorded
```

Report the broken assumption, the measured delta, and the re-plan you recommend.
