---
name: missed-run-semantics
domain: software-engineering/missed-run-semantics
trigger: "Deciding what a job does when its trigger time is missed."
anti_trigger: "Not for the lock preventing overlaps (that is overlap-and-singleton)."
scope: "What happens when a trigger time passes while the system is down or busy."
status: seedling
---

# Missed-run semantics

## Standard

When a scheduler misses a trigger — the process was down, the node was cordoned, the previous run still held the lock — the moment passes, and the question is what the system should do next. The options are few and consequential: run immediately late (catch up), run once at the next normal time (coalesce), skip entirely, or run every missed instance (replay). Each is right for a different job: a billing run wants catch-up, a digest wants coalesce, and a cache warmer is happy to skip.

The wrong choice is usually invisible until an outage. A job with replay semantics that catches up three days of missed runs after downtime can saturate its own dependencies; a job with skip semantics that was needed for compliance silently produced nothing for the gap. The semantics must be chosen per job, written in the schedule record, and known to whoever responds when the outage report arrives.

## Decision rules

- Classify each job by consequence of missing one instance: none, degraded, or material.
- Choose semantics per class — skip for none, coalesce for degraded, catch-up for material.
- Bound any catch-up explicitly: a replay window longer than one interval is a deliberate decision.
- Write the chosen semantics next to the job definition, not in a runbook nobody opens.
- After any downtime, enumerate jobs whose triggers passed and confirm each behaved as designed.
- Record the maximum lateness after which a catch-up is no longer meaningful.

## Procedure

1. List the jobs and their triggers from the schedule record.
2. Classify each by the consequence of one missed instance.
3. Assign the semantics per class.
4. Configure the scheduler's matching option and verify against its documentation.
5. Simulate one downtime window and confirm the behaviour of each job.
6. Record the semantics in the job's definition and in the schedule record.

## Anti-patterns

- Accepting the scheduler's default semantics without classifying the job.
- Replay semantics on a job whose downstream cannot absorb three runs.
- Skip semantics on a job whose output is consumed downstream as complete.
- Discovering the semantics during the first outage.
- No record of the decision, so the next engineer inherits a mystery.

## Done checklist

- [ ] Jobs classified by missed-instance consequence.
- [ ] Semantics assigned per job.
- [ ] Catch-up windows bounded where used.
- [ ] Scheduler configuration verified to match.
- [ ] Downtime simulation confirmed behaviour.
- [ ] Semantics recorded in the definition.

## Sources

- CronJob concurrency and miss policies: <https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/>
- Time and scheduling semantics: <https://www.rfc-editor.org/rfc/rfc3339>
- Failure policies in scheduled systems: <https://learn.microsoft.com/en-us/azure/well-architected/>
