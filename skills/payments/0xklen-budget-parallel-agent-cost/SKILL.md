---
name: budget-parallel-agent-cost
description: Use when running many children in parallel under token, time, or money limits. Allocates per-child budgets and enforces a wave ceiling so parallelism cannot overspend unnoticed.
---

# Budget Parallel Agent Cost

N children cost roughly N times one, and failures inflate the bill. Set a per-child budget and a wave ceiling, then stop the wave before it breaches either.

## Procedure

1. Estimate unit cost from history: tokens (or seconds or dollars) for one child of this shape — say 40k tokens.
2. Multiply by the roster size and add a retry allowance (say +30%) to get the wave estimate.
3. Compare the wave estimate to the hard ceiling the requester set; if it exceeds it, split into waves or reduce scope before launching.
4. Give each child a per-child cap in its brief: "stop after ~50k tokens or 10 minutes and report partial."
5. Meter live: append each child's usage to `notes/cost.jsonl` as `{child, tokens, seconds}` at completion.
6. Sum the running total each poll; if it passes 80% of the ceiling, stop launching new children in this wave.
7. Account for retries: a child that fails twice costs 3×; count them in the total, not just the successes.
8. Track cost-per-verified-result, not cost-per-launch; a cheap child that fails all checks is the expensive one.
9. When the ceiling hits, freeze results, report the partial wave, and ask before spending more.
10. Record the final total against the estimate in `notes/cost.jsonl` under a `wave_total` line for future estimates.

## Pitfalls

- Budgeting per child but not per wave, so twenty small overspends sum past the ceiling before anyone notices.
- Ignoring retries in the accounting, so the true spend is two to three times the estimate.
- Metering only successful children, hiding spend burned by failures.
- Setting a ceiling with no live check, discovering the breach only after the wave ends.
- Treating tokens as free and counting only wall time, when the provider bills tokens.

## Verification

```bash
jq -s '{total:(map(.tokens)|add), runs:length}' notes/cost.jsonl
# passes when total <= the wave ceiling and runs == roster size (+ declared retries)
```

Report to the user: the estimated and actual wave cost, the 80% checkpoint result, and whether the wave stayed under budget.
