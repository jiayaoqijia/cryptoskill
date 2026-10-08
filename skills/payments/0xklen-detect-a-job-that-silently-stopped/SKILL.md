---
name: detect-a-job-that-silently-stopped
description: Use when a scheduled or background job could stop running without erroring, long before anyone notices its output is missing. Adds a heartbeat and a freshness alarm.
---

# Detect a job that silently stopped

The dangerous failure is not a job that crashes loudly; it is a job that simply stops. The scheduler is fine, the process is gone, and nothing alerts because nothing errored. Detect absence, not just errors.

## Procedure

1. Pick the dead-man's-switch pattern: the job must prove it ran, and an external system alarms when the proof stops arriving.
2. Have the job write a heartbeat on every successful run to a known path or a monitoring endpoint:
       date -u +%s > /var/lib/jobs/nightly-reconcile.heartbeat
   or, for hosted monitors, `curl -fsS -m 5 https://hc-ping.com/<uuid>` at the end of a clean run.
3. Alarm on staleness, not on exit code: `now - heartbeat_mtime > 1.5 * period` means the job is late. A daily job alarms if the heartbeat is older than about 36h.
4. Send a failure ping to the same monitor on error paths (`curl https://hc-ping.com/<uuid>/fail`) so crashes and stops are distinguished.
5. Alert on the signal that matters: the missing output, not the missing process. For a reconciliation job, alert if `max(reconciled_at)` in the table lags the scheduler.
6. Cover the whole chain: a job that runs but produces zero rows is also stopped in effect. Heartbeat on rows processed, not just process exit.
7. Put the heartbeat write after the work commits, never before, so a job that dies mid-work does not look healthy.
8. Give the alarm an owner and a runbook — a staleness alarm with no action is noise.
9. Test the detector: disable the job in a staging environment and confirm the alarm fires within the expected window, not hours later.
10. For jobs behind a scheduler you cannot trust to report, derive the heartbeat from the side effect: query the destination's latest row timestamp and compare it to the schedule.

## Pitfalls

- Monitoring the scheduler ("cron is running") instead of the job's effect.
- A heartbeat written at job start, so a job that hangs after starting looks alive forever.
- Alerting only on non-zero exit, which never fires when the job is not launched at all.
- Setting the staleness threshold so tight that normal jitter pages someone nightly.
- A monitor with no owner, so the alarm goes to a channel nobody reads.
- Relying on the job to report its own absence — a dead job cannot.

## Verification

    # simulate the stop and confirm the alarm, then the freshness query agrees
    systemctl stop nightly-reconcile.timer
    psql -c "select now() - max(reconciled_at) as lag from reconciliations"   # grows past threshold
    # pass: the monitor fires within 1.5x the period and the owner is paged

Report the heartbeat mechanism, the staleness threshold, the alarm that fired in the test, and its owner.
