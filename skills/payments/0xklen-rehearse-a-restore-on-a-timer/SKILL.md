---
name: rehearse-a-restore-on-a-timer
description: Use when a backup has never been restored. Runs a scheduled restore into an isolated target, measures RTO and data age, and records the result.
---

# Rehearse a Restore on a Timer

An untested backup is a guess. Run the restore on a schedule, into a throwaway target, and measure how long it actually took and how old the newest usable record is — those two numbers are your real RPO and RTO.

## Procedure

1. Pick a cadence matched to change rate: weekly for high-churn systems, monthly for slow ones; never "when we get to it".
2. Provision an isolated target — a scratch database, a temp bucket, a VM with no route to prod — so a bad restore cannot touch live data.
3. Restore the latest backup AND the oldest backup still inside retention; the old one proves deep retention works, the new one proves recency.
4. Time the whole path from cold: `time pg_restore -d scratch db.dump` or `time restic restore latest --target /mnt/scratch`.
5. Validate row counts and a checksum against the source at the same point in time: `SELECT count(*)`, `sha256sum` on an exported sample.
6. Query the restored copy for the newest row timestamp — that delta from now is the real RPO, which is often worse than the policy claims.
7. Record start, end, dataset size, record count, and observed RTO/RPO in a drill log; alert on the occasional drill, not on every backup job.
8. Delete the scratch target when done and confirm the delete to keep the drill cheap.
9. For a failed drill, open a ticket and fix the restore path before the next drill — a drill that fails silently is worse than none.

## Pitfalls

- Restoring onto the production host "just to check" and overwriting live data — always use an isolated target.
- Measuring RTO from a warm cache; the real number is from cold storage with no local blocks.
- Only restoring the newest backup, so a slow corruption that has been in every backup for a month goes unnoticed.
- Declaring success because the restore command exited 0, without comparing record counts or querying the data.
- Leaving the scratch target running, running up cost and cluttering the account with stale copies.
- Skipping the drill because "nothing changed" — drift in the backup tool or credentials breaks restores without a code change.
- Restoring the database but not the object store, so blobs are missing and the app 500s on first image load.

## Verification

    pg_restore -d scratch latest.dump && \
      psql -d scratch -c 'SELECT count(*), max(created_at) FROM events;'

Restore exits 0, the count matches the source snapshot, and the max timestamp gives an RPO within the stated window; the drill log names the measured RTO.

Report: "Restore drill <date>: <size> restored in <m>m <s>s (RTO), newest record <h>h old (RPO ≤ target). Logged at ops/restore-drills.log."
