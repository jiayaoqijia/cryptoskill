---
name: enable-versioning-to-undo-deletes
description: Use when a stray delete or overwrite has no recovery path. Turns on object versioning with a noncurrent-expiry so overwrites are reversible without unbounded growth.
---

# Enable Versioning to Undo Deletes

Without versioning, an overwrite or `rm` is permanent and a bad deploy that rewrites every object is unrecoverable. Versioning keeps prior versions so a delete becomes a soft, reversible event — provided you cap how long noncurrent versions live.

## Procedure

1. Turn versioning on before you need it: `aws s3api put-bucket-versioning --bucket acme --versioning-configuration Status=Enabled`.
2. Immediately add a `NoncurrentVersionExpiration` rule so old versions do not accumulate forever:
   `{"NoncurrentVersionExpiration":{"NoncurrentDays":30}}`.
3. For databases and filesystems, use the native equivalent: WAL + PITR for Postgres (`recovery_target_time`), ZFS/Btrfs snapshots for files.
4. Understand that a delete writes a delete-marker; the data is still there and recoverable by removing the marker:
   `aws s3api delete-object --bucket acme --key path --version-id <delete-marker-id>`.
5. Recover a specific version: `aws s3api list-object-versions --bucket acme --prefix path` then `get-object --version-id`.
6. Add MFA-delete or a bucket policy denying `DeleteObjectVersion` outside a break-glass role, so a compromise or script cannot purge history.
7. Test the recovery: delete a test object, confirm the current listing hides it, restore the prior version, confirm content matches.
8. Re-baseline storage cost after enabling; versioning multiplies stored bytes by the change rate within the retention window.

## Pitfalls

- Enabling versioning with no noncurrent expiry, so storage grows without bound and the cost alarm fires months later.
- Believing versioning protects against a malicious actor who has `s3:DeleteObjectVersion` — it does not; lock the permission.
- A lifecycle rule that deletes noncurrent versions after 1 day, which is too short to catch a slow-failing deploy's overwrites.
- Confusing a delete-marker with the absence of the object; `list-objects` hides it but `list-object-versions` still shows the data.
- Assuming versioning replicates to a bucket-replication target automatically; the target's versioning must be enabled too.
- Enabling versioning on a bucket with a huge existing object count and no plan for the first-month cost of retained versions.
- Forgetting that versioning changes ETag semantics and some SDK "overwrite" calls now leave the old bytes billed.

## Verification

    aws s3api get-bucket-versioning --bucket acme           # Status: Enabled
    aws s3api list-object-versions --bucket acme --prefix test/key \
      --query 'Versions[].VersionId' --output text | wc -w  # >1 after edits

Versioning is Enabled, a prior version is retrievable by `--version-id`, and a `NoncurrentVersionExpiration` rule bounds retention.

Report: "Versioning enabled on <bucket> with 30d noncurrent expiry; recovered test/key version <id>; delete now reversible within 30 days."
