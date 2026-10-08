---
name: idempotent-operations
description: Use when a step may run more than once through retries, re-entry, resume, or a scheduled job. Makes the step safe to repeat so a second run cannot double its effect.
---

# Idempotent Operations

Anything that can run twice will run twice — through a retry, a resumed handoff, or a cron overlap. Design each step so the second run changes nothing the first did not already do.

## Procedure

1. For each mutating step, ask: what happens if this runs twice with the same input? If the answer is "duplicates" or "double-charges", make it idempotent.
2. Filesystem: use `mkdir -p`, `install -D`, and write-then-rename (`mv tmp final`) so partial runs do not leave half-written files. Guard with a sentinel: `[ -f .done ] || (work && touch .done)`.
3. Databases: prefer upsert/set-semantics over append:
   `INSERT INTO runs (id, val) VALUES ($1,$2) ON CONFLICT (id) DO UPDATE SET val=EXCLUDED.val;`
   For apply-once effects, key on a natural id and `SELECT 1 FROM ... WHERE id=$1` before acting.
4. Shell: avoid `>>` for logs that must not duplicate; truncate-then-write (`>`), or key the append by attempt id so the ledger stays one row per attempt.
5. API calls that create resources: send an idempotency key (`Idempotency-Key: <uuid>` on Stripe/HTTP write APIs) or a deterministic request id so a retry returns the first result, not a second object.
6. Concurrency: take a lock before mutating shared state: `flock -n /tmp/job.lock -c '...'` or a DB advisory lock, so two runners do not interleave.
7. For batch jobs, make each item's processing independent and recorded: after each item, append its id to `data/done.txt`; on resume, skip ids already listed.
8. Verify by running the step twice deliberately in a scratch target and diffing the state; it must be identical.
9. Choose the natural key that makes repeats collapse: a content hash, a stable id from the source, or an idempotency uuid generated once.
10. Make the side effect a check-then-act inside a transaction or lock so two runners cannot both pass the check.
11. Test idempotency against the real retry path (run, kill mid-way, run again), not only a clean double-run.

## Pitfalls

- A counter incremented in the write path, so a retry double-counts.
- `>>` appending a startup line every time a service is retried, inflating a metrics file.
- An upsert keyed on a value that legitimately changes, silently overwriting good rows.
- A lockfile left behind by a crashed run, then blocking every later run forever.
- Assuming a third-party POST is idempotent when it has no idempotency-key support.
- Generating a fresh idempotency key on each retry, which defeats the dedupe the API offers.
- A "done" marker written before the work, so a crash leaves the item marked complete but unprocessed.

## Verification

    # Run the step twice against a scratch target, then diff
    cp -a scratch scratch.probe && ./step.sh scratch && ./step.sh scratch.probe && diff -r scratch scratch.probe
    # passes when diff prints nothing

Report to the user: which steps are idempotent, the guard used (upsert, sentinel, lock, key), and the double-run diff result.
