---
name: overlap-and-singleton
domain: software-engineering/overlap-and-singleton
trigger: "Preventing or handling two runs of the same job at once."
anti_trigger: "Not for the job body's own tolerance (that is idempotent-job-bodies)."
scope: "The lock that keeps one run at a time, and what happens when it is held."
status: seedling
---

# Overlap and singleton

## Standard

When a job's interval is shorter than its worst-case duration, two runs want to be alive at once. Almost always that is a bug: the second run sees the first one's partial state, both write the same destinations, and the failure looks like corruption rather than scheduling. The standard control is a singleton lock — the run acquires a hold on a shared identifier before starting work, and the second run finds it taken.

The design question is what the second run does when the lock is held, and the same three answers apply as to missed triggers: skip this instance and record it, wait for the lock and run late, or fail loudly. Waiting is usually wrong because it stacks delay behind delay; skipping with a log is right for most work; failing loudly is right when the overlap itself signals something broken changed in the job's timing.

## Decision rules

- Record each job's worst-case duration and compare with its interval.
- Require a singleton lock for any job whose duration can exceed its interval.
- Decide the lock-held behaviour — skip, wait, or fail — per job and record it.
- Give every lock a time-bound lease so a crashed holder cannot block runs forever.
- Free the lock in a block that runs even on failure; a leaked lock is a self-inflicted outage.
- Alert when the held count exceeds a threshold, not merely when runs occur.

## Procedure

1. Identify jobs whose duration can approach or exceed their interval.
2. Add or verify a singleton lock keyed on the job identifier.
3. Choose and implement the lock-held behaviour.
4. Add a lease with a timeout to the lock.
5. Verify the lock frees on both success and failure paths.
6. Test by launching a second instance while one runs.

## Anti-patterns

- Assuming the interval guarantees separation because "the job only takes a minute".
- An unleased lock that survives a crashed holder.
- Freeing the lock only on success.
- Waiting for the lock indefinitely, stacking lateness.
- No record of skipped instances while the lock was held.

## Done checklist

- [ ] At-risk jobs identified.
- [ ] Singleton lock present per at-risk job.
- [ ] Lock-held behaviour chosen and recorded.
- [ ] Lease timeout present.
- [ ] Lock freed on failure paths.
- [ ] Overlap scenario tested.

## Sources

- Singleton execution patterns: <https://learn.microsoft.com/en-us/azure/architecture/>
- Distributed locks and their limits: <https://martinfowler.com/articles/patterns-of-distributed-systems/>
- Kubernetes CronJob concurrency policies: <https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/>
