---
name: place-buffer-on-the-critical-chain
description: Use when padding every task has bloated a schedule without making it safer. Moves slack out of the individual tasks and into one visible reserve at the end that protects the delivery date.
---

# Place buffer on the critical chain

Per-task padding is consumed silently — work expands to fill it — and when one task overruns it eats its own cushion and the next task's too. Pull the slack out of the tasks, aggregate it, and put it where it protects the date, not the task.

## Procedure

1. Estimate each task at its credible 50% duration, no per-task padding.
2. Find the longest chain through the dependencies; that chain sets the earliest finish.
3. Sum the safety you removed. If each of 8 tasks dropped 20% of a 5-day estimate, the pool is roughly `8 * 5 * 0.2 = 8 days`.
4. Shrink that pool, because aggregated risk partly cancels. A common cut is 50% of the summed safety:

       python3 -c "tasks=8; pct=0.2; sized=5; pool=tasks*sized*pct; print('pool',pool,'project buffer',round(pool*0.5,1))"
       pool 8.0 project buffer 4.0

5. Attach the project buffer after the last critical-chain task, not distributed across tasks.
6. On the non-critical chains add a smaller feeding buffer where they join the critical chain, sized the same way.
7. Track consumption: if the buffer is, say, 4 days and 2 are gone with half the chain done, the schedule is behind — act then, not at the end.

## Pitfalls

- Leaving the per-task pads in place and adding a project buffer on top, which double-counts risk and inflates the date without buying safety.
- Cutting the aggregated pool too aggressively so it no longer covers the 80% case.
- Hiding the buffer inside a task, which puts it back where it gets silently consumed.
- Ignoring feeding chains, so a late non-critical task drains the project buffer from the side.
- Watching the buffer but never acting on a threshold, which turns the signal into a report nobody uses.
- Sizing the project buffer from a single past project rather than the chain's own spread.

## Verification

    python3 -c "pool=8*5*0.2; print('consumed_frac should be < elapsed_frac')  # 0.8 pool, buffer 4d"
    # passes when buffer consumed / buffer size stays below chain complete / chain length

Report the unbuffered chain end, the aggregated buffer size, and the current buffer-consumption percentage with the threshold you set.
