---
name: measure-whether-a-memory-helped
description: Use when deciding if a stored memory or skill earns its place. Compares task outcomes with and without the entry instead of assuming storage is good.
---

# Measure Whether a Memory Helped

A stored fact costs a reader's attention every time it is loaded. Whether it earns that cost is measurable: run the task with the entry and without it, and compare.

## Procedure

1. Name the entry and the task it is supposed to help.
2. Record the task baseline: time, tool calls, and correctness without the entry.
3. Run the same task with the entry present and note the same three numbers.
4. Count reads: how many times the entry was actually loaded or grepped during the task.
5. Compare like with like — a fast wrong run is not an improvement; correctness gates the comparison.
6. A useful entry cuts tool calls or errors; an entry that is never read cannot be helping.
7. If it never helped across several tasks, demote it: move from durable memory to archive or scratch.
8. If it helped, keep it and pin it (`pin: true`) so future pruning does not evict a load-bearing entry.
9. Check the negative case: an entry that misled you once and helped once is net-zero — investigate the mislead.
10. Re-check after the fact goes stale: an entry can help today and mislead after the system changes.

## Pitfalls

- Assuming a stored fact helps because it exists, without ever measuring the task with and without it.
- Counting load success as value, when the entry was loaded and unused.
- Comparing a fast run that was wrong against a slower correct run and calling it a win.
- Measuring once and treating an old fact as permanently useful after the source changed.
- Discarding a rarely-used entry that is load-bearing for a rare, high-cost task.

- Measuring on one task and generalising the result to all of them.
- Recording the "with" number and inferring the "without" instead of running it.
- Demoting an entry while a task that needs it is still open.

## Verification

    grep -c "reads\|calls\|errors" notes/memory-value.md
    # passes when the entry has a with/without comparison and a read count, not just "seems useful"

Report to the user: the entry, the with/without numbers, the read count, and whether it was kept, pinned, or demoted.
