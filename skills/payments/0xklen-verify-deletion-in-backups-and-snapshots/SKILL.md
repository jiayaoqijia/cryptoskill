---
name: verify-deletion-in-backups-and-snapshots
description: Use when an erasure or retention policy stops at the live database and backups still hold the data. Bound the residue window and prove the expiry and restore paths.
---

# Verify deletion in backups and snapshots

Erasure that stops at the live database leaves the person in every backup. This skill bounds the residue and proves the expiry path works.

## Procedure

1. Enumerate the backup classes: automated DB snapshots, logical dumps, object-store versioning, WAL archive, read replicas, and third-party SaaS backups.

2. Record retention per class so the maximum residue window is known:
   `aws rds describe-db-snapshots --query 'DBSnapshots[].{id:DBInstanceIdentifier,created:SnapshotCreateTime}'`

3. Decide the policy: either rewrite backups, which is rarely justified, or accept bounded residue with a documented maximum age.

4. For versioned object stores, delete all versions, not just the current object; a delete marker leaves prior versions behind:
   `aws s3api list-object-versions --bucket b --prefix "key/"`

5. Turn on expiry so residue self-heals: a lifecycle rule that deletes noncurrent versions after N days.

6. If a backup is restored, the restore runbook must re-apply pending deletions before the data is used; test this path.

7. For the WAL archive, note that point-in-time restore can resurrect deleted rows within the recover window; cap that window explicitly.

8. Write the residue statement into the erasure record: "the subject's data remains in backups until <date> and is never restored into active use".

9. Test the full path once: create a subject, back up, delete, restore to a sandbox, and confirm the runbook removes them.

## Pitfalls

- Object-store versioning keeps every overwritten `PUT`; deleting the key does not delete the versions.
- A restore drill that skips re-applying deletions silently reintroduces the data.
- Third-party SaaS keeps its own backup beyond your window; get their retention in writing.
- Snapshot retention longer than the erasure policy implies is a common contradiction; reconcile the two.
- Encrypted backups whose key is deleted are unrecoverable and safe; this is a legitimate residue strategy, not a failure.

## Verification

    aws s3api list-object-versions --bucket b --prefix "$KEY" --query 'length(Versions || `[]`)'   # expect 0 after purge

Report the backup classes, the maximum residue date, and whether the restore path re-applies pending deletions.
