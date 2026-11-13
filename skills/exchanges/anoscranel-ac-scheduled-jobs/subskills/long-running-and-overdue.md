---
name: long-running-and-overdue
domain: software-engineering/long-running-and-overdue
trigger: "Handling jobs whose duration approaches or exceeds their interval."
anti_trigger: "Not for the lock mechanics (that is overlap-and-singleton)."
scope: "Jobs that outlive their interval, and the queue of missed triggers behind them."
status: seedling
---

# Long-running and overdue

## Standard

A job whose worst-case duration crosses its interval has stopped being a job and become a pipeline problem: instances want to overlap, each trigger missed while the previous run held the lock stacks behind it, and latency compounds — if skipped, the work falls behind reality; if queued, the queue itself can grow without bound and must have its own cap.

The design responses are the interval change, the split, or the acceptance. Raising the interval matches the job to its real duration but accepts coarser data. Splitting the job into per-partition workers turns one long run into many short ones, at the cost of a coordinator. Accepting overlap semantics is only viable for genuinely idempotent work — a warmer whose late run causes no harm — and must be written down as a decision, not an oversight.

## Decision rules

- Measure the job's duration distribution, not just its typical time; the tail decides.
- Record the headroom between worst-case duration and interval; below one interval-width is a signal.
- Choose the response per job: raise the interval, split the work, or accept the overlap.
- If queueing missed triggers, give the queue a bound and define what happens at the bound.
- Alert on overdue state — a run older than its own interval — not only on failure.
- Track caught-up versus falling-behind if catch-up is used.

## Procedure

1. Collect the duration distribution from run history.
2. Compare worst-case duration with the interval.
3. Select the response per job and record it.
4. Implement the change — interval, split, or semantics.
5. Add or verify the overdue alerting.
6. Re-measure after a week of runs and record the new distribution.

## Anti-patterns

- Sizing the interval from the average duration.
- An unbounded backlog of missed triggers that "will catch up" and never does.
- Silent accumulation when the scheduler skips quietly.
- Overlap acceptance without a written decision.
- Alerting only on errors, so a chronically overdue job stays unnoticed.

## Done checklist

- [ ] Duration distribution recorded.
- [ ] Response chosen per job.
- [ ] Queue bound present where triggers queue.
- [ ] Overdue alerting live.
- [ ] Falling-behind tracking in place.
- [ ] Post-change distribution re-measured.

One further distinction keeps the diagnosis honest: a job that is slow because it does more work than it did last quarter is a different problem from one that is slow because its dependencies are, and the duration distribution cannot separate them on its own — the fix for the first is a design change, for the second a look downstream, and the record should say which the evidence supports.

## Sources

- CronJob history and retries: <https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/>
- Queue depth and backlog patterns: <https://learn.microsoft.com/en-us/azure/architecture/>
- Latency and scheduling analysis: <https://sre.google/sre-book/monitoring-distributed-systems/>
