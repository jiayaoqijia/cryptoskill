---
name: push-back-on-an-unrealistic-constraint
description: Use when a hard constraint such as "no downtime" or "must be free" conflicts with the work. Test whether it is real, and if so, price what honouring it actually costs.
---

# Push back on an unrealistic constraint

Constraints arrive as absolutes and turn out to be preferences. Before redesigning around one, find what it protects; sometimes the true limit is narrower than its wording, and sometimes it is real and expensive.

## Procedure

1. Separate the constraint from the preference. Is it a legal, contractual, or physical limit, or a wish ("ideally no downtime")?

2. Ask what the constraint protects. "No downtime" often means "no lost revenue during business hours", which still leaves a 02:00 maintenance window.

3. Quantify the cost of honouring it literally: dual-write, blue-green deploy, or a rewrite, in days and risk.

4. Offer the cheapest way to respect the true limit rather than the literal wording.

5. When the constraint is real and the cost is high, present the bill: this is what "same day" costs in risk and rework.

6. Let the owner decide with the number in front of them; your job is to price, not to overrule.

7. Record the constraint and its true source, so it is not re-litigated from scratch next project.

## Pitfalls

- Accepting "no downtime" and building an over-engineered path when an 02:00 window was fine.

- Dismissing the constraint as silly without asking what it protects.

- Quoting a cost from memory instead of measuring deploy time or dual-write overhead.

- Winning the argument and losing the relationship by being adversarial about it.

- Treating every constraint as negotiable when some are genuinely fixed and must be designed around.

## Verification

```
    grep -nE 'cost:|risk:' constraint.md   # the literal cost of the constraint is numbered
```

Report whether the constraint is real, the source that makes it real, and the cost of honouring it.
