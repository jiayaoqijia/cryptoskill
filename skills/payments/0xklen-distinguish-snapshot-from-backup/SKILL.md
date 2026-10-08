---
name: distinguish-snapshot-from-backup
description: Use when a storage plan treats snapshots as a backup. Separates point-in-time copies from restorable, off-array backups and closes the gap before an incident.
---

# Distinguish Snapshot from Backup

A snapshot is a fast pointer to blocks on the same device; a backup is an independent copy you can restore from after that device is gone. Conflating them means a single disk or zone failure destroys "both copies".

## Procedure

1. Audit every copy you call a backup and label it: same volume? same array? same account? same region? Any "yes" is a snapshot, not a backup.
2. State the failure each copy is meant to survive: block corruption, disk death, array loss, ransomware (needs immutability), accidental delete (needs retention), region loss (needs offsite).
3. For every failure with no independent copy, add one. Minimum viable backup is: offbox, off-account, offline or immutable.
4. Keep snapshots for their real job — fast rollback of hours-old mistakes and clone-and-test — with a short retention (typically 24-72h).
5. Keep backups for disaster recovery with a retention that matches the business requirement, verified by restore.
6. Make backups immutable or air-gapped: S3 Object Lock in compliance mode, an offline tape, or a pull-only repo the source cannot delete. A backup the source can `rm` is erased by the same attacker.
7. Encrypt backups with a key held separately from the source, so a compromised source account cannot read them.
8. Document, per dataset, the RPO (snapshot age) and RTO (restore time), and confirm they match the business requirement.

## Pitfalls

- Snapshots on the same physical array: a controller or power failure takes the live data and every "backup" at once.
- Ransomware that encrypts the live volume and then the mounted snapshot target, because both were writable from the host.
- Using a filesystem snapshot of a running database as a backup; the on-disk state is crash-consistent, not app-consistent, and may not replay.
- Assuming a managed provider's automatic snapshot is offsite; often it lives in the same region and account.
- Never testing the restore, so the "backup" is a hypothesis, not a proven fallback.
- Retaining snapshots indefinitely until they silently fill the array and block writes.
- Encrypting backups with the same key in the same secret store as production, so one leak compromises both.

## Verification

    aws s3api get-object-lock-configuration --bucket acme-backups
    aws s3api list-objects-v2 --bucket acme-backups --query 'Contents[].Key' --max-items 5

Every dataset has at least one copy in a different account/region, locked or air-gapped, and the drill in `rehearse-a-restore-on-a-timer` restores from it.

Report: "Audited N copies: X are snapshots on the source array, Y are independent backups; Y copies are immutable and offsite, RPO <n>h / RTO <n>h."
