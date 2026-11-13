---
name: catchup-and-backfill
domain: software-engineering/catchup-and-backfill
trigger: "Designing what runs when the schedule resumes after downtime."
anti_trigger: "Not for missed-run semantics per instance (that is missed-run-semantics)."
scope: "What runs after downtime: catch-up policy and bounded replay."
status: seedling
---

# Catch-up and backfill

## Standard

After an outage, a scheduled system faces a decision its trigger semantics only partly answer: how much of the gap to replay. Catch-up ranges from "run once with the current time and let the job self-correct", to "replay every missed period in order", to "run once per missed period but with fresh side effects only". The choice must bound both the load the replay generates and the meaning of the data it writes, because a replayed report row for a period that has already been aggregated can corrupt a summary.

Bounded replay is the discipline: a maximum number of periods to catch up, a decision for what happens beyond it, and a record written of which periods were replayed and which were declared lost. The record matters because downstream consumers of the data need to know the gap exists — missing data that nobody knows is missing produces quietly wrong conclusions for months.

## Decision rules

- Define the catch-up window per job: zero periods, one period, or all.
- Bound the replay by an explicit maximum, and define the behaviour beyond it.
- Replay in period order, oldest first, unless the job is explicitly order-independent.
- Record skipped periods in a place downstream consumers can query.
- Rate-limit the replay so catch-up does not reproduce the outage's load at 10x.
- Verify after catch-up that the state matches what a fully-up system would show.

## Procedure

1. Read the job's missed-run semantics to know the starting point.
2. Decide the catch-up window and the bound.
3. Implement ordered replay with the rate limit.
4. Add the skipped-period record for consumers.
5. Simulate a downtime and observe the replay.
6. Verify state against the expected fully-up result.

## Anti-patterns

- Full replay with no rate limit, turning recovery into a second outage.
- Replaying periods that have already been aggregated downstream.
- No record of skipped periods, so gaps are invisible to consumers.
- Newest-first replay for order-dependent data.
- Catch-up tested only on the happy path of a two-minute outage.

## Done checklist

- [ ] Catch-up window and bound chosen per job.
- [ ] Ordered replay implemented.
- [ ] Rate limit present.
- [ ] Skipped-period record written and queryable.
- [ ] Downtime simulation run.
- [ ] Post-catch-up state verified.

## Sources

- CronJob concurrency and suspend behaviour: <https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/>
- Backfill semantics in pipelines: <https://www.postgresql.org/docs/current/sql-insert.html>
- Well-architected recovery guidance: <https://learn.microsoft.com/en-us/azure/well-architected/>
