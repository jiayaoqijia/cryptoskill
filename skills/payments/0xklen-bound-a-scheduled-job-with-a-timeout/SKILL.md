---
name: bound-a-scheduled-job-with-a-timeout
description: Use when an unattended job can hang and block the next run or hold a lock. Caps per-run and per-step time so a stuck job dies and alerts instead of stalling forever.
---

# Bound a scheduled job with a timeout

A job with no deadline is a job that can hang until someone notices it stopped producing. Every unattended job needs a wall-clock budget and a killed-and-alerted outcome when it exceeds it.

## Procedure

1. Set the wall-clock budget from observed runtime: measure the p99 of the last 30 runs and set the cap at roughly 2-3x that, not at "the period".
2. Enforce it at the outermost layer so the whole process dies:
       timeout --signal=TERM --kill-after=30s 900 ./nightly-reconcile
   or in Kubernetes `activeDeadlineSeconds: 900` on the CronJob.
3. Set a timeout on every network call inside the job too, so a single hung RPC does not consume the whole budget:
       curl --max-time 10 --connect-timeout 3 ...
   Libraries default to infinite waits; pass the timeout explicitly.
4. Set the DB statement timeout so a locked query cannot hold the run:
       SET statement_timeout = '30s';
5. Make the job release locks and cursors on TERM; register a handler so a killed run does not leave a stale advisory lock.
6. Distinguish "timed out" from "failed": exit with a distinct code (e.g. 124) and log `status="timeout"` so the alert says which.
7. Choose the budget below the schedule period, so a timed-out run never overlaps the next (combined with `concurrencyPolicy: Forbid`).
8. Re-check the budget after data grows; a cap set a year ago may now cut off legitimate runs.
9. Do not let a timeout silently retry forever: a timed-out run should alert or back off, not loop.
10. For multi-step jobs, set a per-step budget and sum a little headroom; one slow step should not eat the others' time.

## Pitfalls

- A `timeout` that kills the process but leaves a DB transaction open, holding locks for the next run.
- Budget equal to the period, so a slow run overlaps the next and two copies fight.
- Infinite default timeouts on the HTTP client inside an otherwise "bounded" job.
- Retrying the whole job on timeout, doubling the load that caused the slowness.
- Setting the budget once and never revisiting as the dataset grows.
- Killing with SIGKILL immediately, so cleanup handlers never run.

## Verification

    /usr/bin/time -v timeout 900 ./nightly-reconcile; echo "exit=$?"
    # pass: normal runs finish well under the cap; a simulated hang exits 124 within the budget

Report the wall-clock budget, the per-call timeouts, the exit code for timeout, and the p99 runtime it was derived from.
