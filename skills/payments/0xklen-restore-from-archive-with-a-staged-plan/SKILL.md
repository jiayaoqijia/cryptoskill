---
name: restore-from-archive-with-a-staged-plan
description: Use when recovering data from a cold archive tier. Stages the retrieval, estimates cost and delay, restores to an isolated path, and verifies before copying into production.
---

# Restore from Archive with a Staged Plan

Archive retrieval is slow, sometimes billable, and occasionally one-way. Plan the restore as a staged job: request, wait, verify in isolation, then promote — never restore straight over production from a cold tier.

## Procedure

1. Identify exactly what to restore and its checksum/size from the manifest, before issuing the retrieve.
2. Choose the retrieval tier and know the tradeoff: Glacier Standard (3-5h), Bulk (5-12h) / Expedited (1-5min, costly), Deep Archive (12-48h).
3. Estimate the cost: per-request fee plus per-GB retrieval plus the temporary restored-copy storage for the restore window.
4. Issue the staged restore with a bounded window so the temporary copy does not linger:
   `aws s3api restore-object --bucket acme --key archive/db.tar --restore-request '{"Days":7,"GlacierJobParameters":{"Tier":"Standard"}}'`.
5. Poll for completion rather than assuming: `aws s3api head-object --bucket acme --key archive/db.tar --query 'Restore'`.
6. Restore into an isolated path (scratch bucket, temp VM), not over the live dataset.
7. Verify the restored bytes: `sha256sum -c db.tar.sha256`, then open the archive and count records against the manifest.
8. Only after verification, promote by copying into the live path; keep the original archive object untouched.
9. Write down the whole path's elapsed time as the real archive RTO for the runbook.

## Pitfalls

- Expecting the restore to be instantly available and blocking a recovery on a 12-hour Deep Archive job that no one scheduled early.
- Expedited retrieval on a large object, which has size limits and higher per-GB cost, or fails outright above the threshold.
- Restoring over the live object before verifying, destroying the current copy if the archive is corrupt.
- Forgetting the temporary restored copy expires after `Days`, and being surprised when re-reading later fails.
- No manifest/checksum, so the restored archive cannot be proven good until the data is already in use.
- Retrieving the whole archive to recover one file; the request cost scales with the whole object.
- Restoring the data but not the schema/config needed to read it, so the bytes are back but unusable.

## Verification

    aws s3api head-object --bucket acme --key archive/db.tar --query 'Restore'  # "ongoing-request=\"false\""
    sha256sum -c db.tar.sha256   # expect OK before promoting to prod

The retrieval completes within the expected tier window, the checksum matches the manifest, and record counts match before any copy reaches production.

Report: "Restored <key> from <tier> in <h>h (RTO); checksum OK, <n> records match; cost ~$<x>; promoted to <path> after verification."
