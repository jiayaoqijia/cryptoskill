---
name: separate-milestone-from-deadline
description: Use when a date is being treated as both a progress marker and a hard cutoff. Tags each date as milestone or deadline so a slip triggers re-planning, not panic, and a deadline triggers a scope cut.
---

# Separate milestone from deadline

A milestone is a projection you can move; a deadline is a constraint that moves you. Blur them and every slip reads as an emergency, and the only lever left is optimism. Label each date and attach the response that fits it.

## Procedure

1. In `notes/plan.md`, tag every date. Use an explicit field so it is machine-checkable:

       - [ ] M2 2026-03-14 milestone   # projection, can move
       - [ ] launch 2026-04-01 deadline  # constraint, cannot move

2. Define the response per tag before the slip happens: a **milestone** that misses triggers a re-plan and a new date; a **deadline** that is at risk triggers a scope cut until it fits.
3. Never let a milestone drift into a deadline by being repeated. If a date has been quoted to customers or a contract, it is a deadline — re-tag it and write down what that means.
4. Keep at most one or two true deadlines in a plan. More than that means the plan is over-constrained and something else has to give.
5. Count them so the split stays honest:

       grep -c 'deadline' notes/plan.md
       grep -c 'milestone' notes/plan.md

6. When a milestone moves, the plan's end date moves with it unless a buffer absorbs it. Say which.
7. When a deadline is fixed, re-derive scope from the date backwards — do not assert both will hold.

## Pitfalls

- Calling everything a deadline, which makes every projection a crisis and destroys the plan's credibility.
- Repeatedly re-dating a milestone while telling stakeholders it is unchanged.
- A deadline with no scope lever attached, so the only way to "make it" is unpaid overtime or hidden risk.
- Forgetting that an external commitment (contract, marketing date, dependency) silently converts a milestone into a deadline.
- Reporting milestone status to people who heard a deadline, so a forecast slip is received as a broken promise.

## Verification

    grep -c 'deadline' notes/plan.md; grep -c 'milestone' notes/plan.md
    # passes when every date carries a tag and deadlines are the minority of dates

Report each date with its tag, the response rule for each, and the count of true deadlines in the plan.
