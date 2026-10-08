---
name: log-a-scheduled-run-outcome
description: Use when a job runs unattended and you cannot tell what it did. Emits one structured, greppable outcome line per run with counts and the run key.
---

# Log a scheduled run outcome

Unattended jobs need a per-run record that answers "did this run, what did it change, and how long did it take" without reading the whole log stream. Emit one structured line per run.

## Procedure

1. Emit exactly one outcome record when the job finishes, as a single-line JSON object, so it greps and parses:
       {"job":"nightly-reconcile","run":"2026-10-07","status":"ok","rows":4821,
        "duration_ms":63120,"started":"2026-10-07T03:00:01Z","finished":"2026-10-07T03:01:04Z"}
2. Include the run key so the line ties back to the idempotency guard and the status table.
3. Log counts that matter for correctness: rows read, rows written, rows skipped or duplicated. A zero-write day is often the bug.
4. Log at a single level (`INFO`) with a stable event name (`event=job_finish`) so you can build one query across all jobs.
5. On failure, emit the same fields plus `status="error"`, an error class, and the trace or correlation id — never a bare stack trace on its own line.
6. Put the log line on stdout so the scheduler's log collector picks it up; do not write to a per-job file nobody ships.
7. Never log secrets, tokens, or full PII payloads in the outcome; log identifiers, not contents.
8. Make the logger a shared helper so every job emits the same schema; a bespoke format breaks the cross-job query.
9. Keep verbose per-item logs at DEBUG and off by default, so the outcome line is not buried in thousands of peers.
10. Alert off the aggregate of these lines, not by parsing free text.
11. Verify by running the job and checking one parseable line comes out with the expected keys.

## Pitfalls

- Logging "done" with no counts, so a run that processed nothing looks identical to a healthy one.
- Multi-line stack traces that break line-based parsing and flood the stream.
- Logging the whole payload, including customer data.
- A different JSON key per job, so the cross-job dashboard needs a mapping per job.
- Logging at job start with no finish line, so a hung job looks like it completed.
- Writing the outcome to a file on the host that is lost on restart.

## Verification

    ./nightly-reconcile 2>&1 | grep -E '"event":"job_finish"' | jq -c '.status,.rows,.duration_ms'
    # pass: exactly one finish line, status ok, rows>0, duration_ms present

Report the outcome field list, the shared helper, and a sample line from a real run.
