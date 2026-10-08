---
name: set-an-alert-noise-budget
description: Use when alerts fire so often the on-call starts ignoring them. Sets a countable noise budget per rotation and treats every alert over budget as a defect to fix.
---

# Set an alert noise budget

Alert fatigue is a measurable condition: when pages outnumber actions, responders start skimming. Give each rotation a budget of interruptions and treat the excess as a bug, not a fact of life.

## Procedure

1. Measure the baseline before setting a target: export page counts per rotation per week from your paging tool for the last month.
2. Set a budget. A common starting point is at most 2 pages per on-call shift for a mature service; anything above is a queue of work.
3. Track the actioned ratio: of pages fired, how many led to a human action? Below roughly 50% actioned, the noisiest rules are the problem.
4. Rank rules by page count and fix from the top: add `for:` durations, raise thresholds, or demote the rule to a ticket or dashboard.
5. Distinguish flapping from real: a rule that fires and clears repeatedly in minutes needs a duration condition or deduplication, not a louder page.
6. Remove duplicate coverage: the same failure paged by the app and again by the monitor is one incident reported twice.
7. Review the budget weekly with the raw numbers and keep a chart; "we feel paged less" is not evidence.
8. When a new alert is added, it inherits the budget: either retire an old rule or account for the new one in the count.
9. Route non-actionable informational alerts to a digest so they stop competing for the interrupt.
10. Treat each over-budget rule as a ticket with an owner and a deadline, so the budget actually ratchets down.

## Pitfalls

- Raising thresholds until nothing pages, which hides real outages.
- Setting a budget and never measuring against it.
- Counting only distinct incidents and ignoring the repeated flapping pages.
- Adding alerts during an incident ("we should watch this") with no pruning later.
- Blaming the responders for "not reading" instead of the rules that over-fire.
- A digest so noisy it becomes the new ignored channel.

## Verification

    # pages per shift for the last two weeks, and the actioned ratio
    pd analytics pages --since 14d --by rotation | awk '{print $1, $2}'
    # pass: pages/shift at or under budget and actioned ratio above 50%

Report the budget, the measured pages per shift, the actioned ratio, and the top rules by count with their fixes.
