---
name: expose-job-failures-in-one-place
description: Use when failed jobs are scattered across email, logs, and dashboards so nobody has a single view. Builds one surface listing every automation's last run and status.
---

# Expose job failures in one place

Failures that live in the wrong inbox are failures nobody acts on. Put every scheduled and background job's last known status on one page, so "what is broken right now" is one glance, not a search.

## Procedure

1. Choose the single surface: a dashboard panel, a status page, or a table in the operations DB. One, not three.
2. Have each job write a row on every run to a shared table:
       CREATE TABLE job_status(
         job text PRIMARY KEY, last_started timestamptz,
         last_finished timestamptz, status text, rows_affected bigint,
         detail text, runbook text);
3. Make every job report through the same helper so the row shape is identical — a per-job bespoke format defeats the single view.
4. Derive the status from evidence: `status='ok'` means the run finished and produced the expected shape, not merely that it exited 0.
5. Show three columns at minimum: last finished (age), status, and rows affected. Compare age to the schedule to catch silent stops.
6. Sort by "most broken first": stale and failing at the top, healthy at the bottom, so the page answers "what needs me" immediately.
7. Include the owning team and the runbook link per row.
8. Do not require a human to open N tools: pull external jobs (cron on other hosts, cloud schedulers, CI crons) into the same table via their APIs.
9. Alarm from the aggregate ("more than 0 jobs failing for 10m") so a job with no heartbeat monitor is still caught.
10. Keep history: prune only rows older than your retention window, so a weekly failing job is visible on Monday from Saturday's rows.
11. Test the surface by forcing a job to fail and confirming the row and the alarm both update.

## Pitfalls

- Failure alerts split across three channels, so each team sees only its own and nobody sees the whole.
- Storing only success/failure with no timestamp, so a job that has not run for a week looks fine.
- A dashboard that requires a query per job and is too slow to trust.
- Per-job log formats, so the aggregate view needs a different parser per job.
- Reporting exit code 0 for a run that did nothing (zero rows) — the dangerous silent success.
- A status page that is read-only and unauthenticated, leaking internal service names.

## Verification

    psql -c "select job, now()-last_finished as age, status, rows_affected
             from job_status order by (status<>'ok') desc, age desc limit 20"
    # pass: every known job appears, the failing and stale ones sort first

Report the surface URL, the jobs it covers, and the query behind it.
