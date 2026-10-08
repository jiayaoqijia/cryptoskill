---
name: prove-a-backup-is-readable
description: Use when a backup job reports success but the archive was never opened. Verifies integrity and reads back real records so "green" means recoverable, not just written.
---

# Prove a Backup Is Readable

A backup job exiting 0 means it wrote bytes, not that the bytes are a usable copy. Every backup must pass an integrity check and a content readback; until it does, "success" is an unverified claim.

## Procedure

1. After each run, verify the archive's own integrity check: `restic check --read-data-subset=5%`, `borg check --verify-data`, `pg_verifybackup backupdir`, `tar -tzf backup.tar.gz >/dev/null`.
2. Confirm the backup tool recorded a checksum and compare it: `sha256sum db.dump` against the manifest written at creation.
3. Read back real content, not just the index: restore one table/object and count rows/bytes; `tar -Ozf backup.tar.gz path/to/file | wc -c`.
4. Check the backup's internal consistency: `sqlite3 backup.db 'PRAGMA integrity_check;'`, `mongod --dbpath backup --repair --dryRun` where available.
5. Verify the tail: a truncated stream often restores everything except the newest records — check the newest key/row exists.
6. Confirm the backup contains what the manifest claims: file/list counts match `find data -type f | wc -l`.
7. Fail the pipeline, not just log, if any check fails — an unverified backup should page like an outage.
8. Run a full-content verification weekly; a subset read (`5%`) each night keeps cost bounded between full checks.

## Pitfalls

- Trusting exit code 0 from `mysqldump` that actually wrote a partial dump after the disk filled.
- Verifying the local staging copy but not the uploaded object; a truncated multipart upload can pass locally and be short in the bucket.
- Only listing the archive (`tar -tzf`) which reads headers but not data blocks — corruption inside files goes unseen.
- Compressed-and-encrypted backups where a single flipped bit breaks everything after it; verify data, not just the header.
- Assuming a database backup is consistent because the file opened; a crashed dump may restore a torn page.
- Skipping verification on the largest dataset "because it takes too long", leaving the most critical copy unproven.
- Restoring to verify but never comparing counts, so a backup missing a whole partition still "restores".

## Verification

    restic check --read-data-subset=10% && \
      restic restore latest --target /tmp/verify --include /data/events && \
      find /tmp/verify/data/events -type f | wc -l

The integrity check passes, the sample restore succeeds, and the restored record count matches the source manifest.

Report: "Verified <backup-id>: integrity ok, restored <n> records/sample, checksum matches manifest — backup is recoverable as of <ts>."
