---
name: choose-cron-vs-event-trigger
description: Use when wiring up when an automation runs. Picks schedule-based or event-based triggering from freshness needs, idempotency, and failure cost rather than habit.
---

# Choose cron or event trigger

A cron schedule and an event subscription are not interchangeable. Pick the one that matches how fresh the work must be and how expensive a missed or duplicated run is.

## Procedure

1. State the freshness requirement first: "within 5 minutes of a change" (event) versus "once a day is fine" (schedule). The number decides the trigger; the trigger does not decide the number.
2. Choose event-driven when latency matters and the source emits a reliable signal — a webhook, a queue message, an object-created notification, or a filtered `eth_getLogs` sweep.
3. Choose cron when the work is a sweep of state that has no single event: nightly reconciliation, weekly report, expiring leases, batch cleanup.
4. Model the failure modes before committing. An event can be lost (webhook 500, subscriber down), so a periodic reconciliation sweep is still needed. A schedule cannot be "lost" but can be missed while the host is down, so overlap windows are needed.
5. For cron, decide cadence from the work's tolerance, not from the smallest unit cron allows. Hourly is not a virtue; a job that could run daily and runs every minute burns cost.
6. For events, design for at-least-once: every handler must be idempotent, because most brokers redeliver.
7. Prefer the source's native retry and dead-letter over hand-rolled retry loops. A webhook endpoint that returns 200 for work it queued, then processes from the queue, survives a restart.
8. When a schedule drives a fan-out, stagger the runs (`0 3 * * *` per shard, offset by shard index) so the batch does not stampede the database at one instant.
9. Add a reconciliation sweep behind any event stream: once a day, compare source count to processed count and re-run gaps. Events handle freshness; the sweep guarantees completeness.
10. Record the trigger choice and its freshness number in the job header so a later reader does not swap them.
11. In Kubernetes, set `concurrencyPolicy: Forbid` to prevent overlap when a run outlasts its period, and set `startingDeadlineSeconds` so a missed run does not queue forever.
12. For long-running event consumers, store the cursor or offset so a restart resumes rather than replays from the beginning.

## Pitfalls

- Polling every minute for something that changes weekly, because a schedule is easy to add.
- Event-only design with no sweep, so a lost webhook silently means a record never processed.
- A cron expression copied from a blog that fires at 00:00 UTC — peak load for every other job on the same host.
- `concurrencyPolicy: Allow` on a job that occasionally runs longer than its period, so two copies fight over the same rows.
- Treating a schedule as exactly-once: the host reboots, the run is skipped, and nothing notices without a heartbeat check.
- Overlapping schedules that all fire on the hour, turning a quiet database into a load spike.

## Verification

    kubectl get cronjob nightly-reconcile -o jsonpath='{.spec.schedule} {.spec.concurrencyPolicy}{"\n"}'
    # confirm the schedule, the overlap policy, and that startingDeadlineSeconds is set

Report the freshness requirement, the chosen trigger, and the failure-mode mitigation for the trigger you rejected.
