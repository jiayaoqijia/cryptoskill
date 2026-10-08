---
name: make-a-scheduled-job-idempotent
description: Use when a job may run twice from retries, overlap, or a manual re-run and doing its work twice would corrupt data or double-charge. Makes each run safe to repeat.
---

# Make a scheduled job idempotent

Retries, overlapping runs, and re-runs after a crash all mean the same run can execute more than once. Design every job so running it twice produces the same state as running it once.

## Procedure

1. Name the unit of work precisely: a day, a tenant, a block range, an order id. The job's effect must be keyed to that unit, not to "whatever is new".
2. Derive a deterministic run key from the unit, e.g. `reconcile:2026-10-07` or `settle:order:8812`, and write it to a `job_runs` table with a unique constraint before doing the work:
       INSERT INTO job_runs(run_key, started_at) VALUES($1, now())
       ON CONFLICT (run_key) DO NOTHING RETURNING run_key;
   A returned row means you own the run; no row means someone already did it — exit 0.
3. Prefer upsert over insert. `INSERT ... ON CONFLICT (id) DO UPDATE` makes a re-run overwrite the same row instead of failing on a duplicate key.
4. Make the work a pure function of input state: read the source for the unit, compute, write the result. Do not depend on "the last run" for correctness; re-derive from the source.
5. Move external side effects (email, payment, webhook) behind the run key too, or record that they fired, so a replay does not send the same invoice twice.
6. For batch jobs, process per-unit and commit per-unit. A crash halfway leaves finished units committed; the next run skips them and finishes the rest.
7. Record progress, not just success: advance a `last_processed_at` watermark inside the same transaction as the data write.
8. Handle the "already in progress" case explicitly. If a second copy finds the run key open, it exits 0 quietly rather than erroring into the alert channel.
9. Test the property, don't assume it: run the job twice against the same fixture and diff the destination. The diff must be empty.
10. For destructive steps (delete, truncate, send), make them keyed and guarded; a re-run must find nothing left to do and say so.
11. Log the run key, the unit, and the row count on every run so a replay is auditable against the ledger.

## Pitfalls

- A job that does `DELETE ... WHERE date = yesterday` then re-inserts; a second run deletes its own output.
- Using "not yet processed" as the query predicate: the second run sees different rows, not the same ones.
- Sending notifications outside the transaction, so a retried run double-emails.
- Assuming the scheduler fires once — `concurrencyPolicy` may allow overlap.
- Committing everything at the end of a batch, so a mid-batch crash replays the whole batch.
- Guarding the run in memory (`const seen = new Set()`) which vanishes on restart.

## Verification

    # run the same unit twice and compare the destination
    ./job.sh --unit 2026-10-07 && ./job.sh --unit 2026-10-07
    psql -c "select count(*) from job_runs where run_key='reconcile:2026-10-07'"   # 1
    # pass: second run exits 0, job_runs has one row, destination checksum unchanged

Report the run key, the statement guarding it, and the empty diff from the double-run test.
