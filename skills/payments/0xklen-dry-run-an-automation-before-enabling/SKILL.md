---
name: dry-run-an-automation-before-enabling
description: Use when enabling a new or changed automation that writes, deletes, or sends. Rehearses it in report-only mode against real input before it is allowed to act.
---

# Dry-run an automation before enabling

An automation's first run should not be its first test against production. Build a dry-run mode that computes exactly what the job would do and prints it, and run that against real input until the plan is boring and correct.

## Procedure

1. Give the job a `--dry-run` flag that runs every read, every query, and every decision, and prints the intended writes instead of performing them:
       ./reaper --dry-run --as-of 2026-10-07 | head -50
2. Make the dry-run share the real code path. A dry-run with its own logic tests nothing; the only difference must be the final write or send call.
3. Emit the plan as structured, countable output: `WOULD_DELETE table=events rows=4821 oldest=2024-01-02`. Counts, not prose.
4. Run the dry-run against production data (read-only) for at least one full cadence before enabling. A monthly job must show a month of realised input, not a hand-made sample.
5. Diff the plan against expectations: if you predicted about 5k deletions and it proposes 400k, stop; the predicate is wrong, not the data.
6. Add a cap to the report: `WOULD_DELETE ... (cap=10000, exceeded=true)` — if the real run would exceed the cap it should refuse, not truncate silently.
7. When enabling, keep the flag: wire the same plan to a `--report-only` schedule that still logs counts after go-live, so predicate drift shows up as an anomalous count.
8. For write jobs, dry-run against a clone or snapshot where possible, so the plan is verified against a real database with foreign keys and constraints.
9. Record the dry-run output (command, date, counts) in the change ticket; that is the evidence the automation was reviewed, not the diff of the script.
10. Only flip to live once the plan has been identical, or deliberately changed, across two runs.

## Pitfalls

- A dry-run that only skips the biggest write and still sends emails or mutates a watermark.
- Testing with a tiny sample that never exercises the predicate's edges (empty results, a timezone boundary).
- Enabling the job and watching the first live run as if it were a rehearsal.
- A dry-run that runs the same expensive query twice because the code path is duplicated.
- No cap in the plan, so a wrong predicate proposes deleting the whole table.
- Deleting the `--dry-run` flag after go-live, so you can never re-verify.

## Verification

    ./reaper --dry-run --as-of 2026-10-07 | awk '/^WOULD_DELETE/{r+=$3} END{print r" rows proposed"}'
    # compare against an independent count, e.g.
    psql -c "select count(*) from events where created_at < '2024-01-02'"   # matches within the cap

Report the dry-run command, the proposed counts, the cap, and the independent count you checked them against.
