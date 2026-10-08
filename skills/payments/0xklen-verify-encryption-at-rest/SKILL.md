---
name: verify-encryption-at-rest
description: Use when a store is claimed to be encrypted at rest and you need proof, not a console default. Check the resource setting, the key source, and the backups separately.
---

# Verify encryption at rest

"Encrypted at rest" is a claim to prove, not a checkbox to tick. This skill verifies the actual storage layer encrypts and that keys live separately from the data.

## Procedure

1. Identify every store holding personal data: primary DB, replicas, object storage, search index, message queue, backups, and worker local disks.

2. For managed services confirm at the resource, not the console default:
   `aws s3api get-bucket-encryption --bucket b` and `aws rds describe-db-instances --query 'DBInstances[].StorageEncrypted'`

3. For self-hosted, check the storage layer: `cryptsetup status <dev>` shows the LUKS mapping, or confirm the cloud disk encryption flag on the volume.

4. Confirm the key is separate from the data: KMS/HSM-managed, not an app-embedded key. `aws kms describe-key --key-id <id>` must show the customer-managed key where policy requires one, not the provider default.

5. Verify backups independently. An unencrypted snapshot of an encrypted disk can exist:
   `aws rds describe-db-snapshots --query 'DBSnapshots[].{id:DBInstanceIdentifier,Encrypted:Encrypted}'`

6. Give the search index and cache their own check or treat them as ephemeral. Redis with persistence and Elasticsearch snapshots need encryption too.

7. Test one restore of an encrypted backup: data must be readable only with the correct KMS grant. A backup that restores without a key is not encrypted.

8. Record rotation: `aws kms get-key-rotation-status --key-id <id>` should show enabled with a period of 365 days or less.

9. Flag any store relying only on a provider default with no documented key policy.

## Pitfalls

- Encrypting the disk does not encrypt a `pg_dump` written to an unencrypted bucket; check the dump scripts.
- App-level column encryption with the key in the same DB config gives little against DB compromise on its own.
- Elasticsearch snapshots and Kafka topics are the usual blind spots.
- A KMS key scheduled for deletion makes the data permanently unreadable; guard it with a deletion-protection policy.
- Replica and read-copy encryption settings are independent of the primary's; check each copy.

## Verification

    aws rds describe-db-instances --query 'DBInstances[].[DBInstanceIdentifier,StorageEncrypted,KmsKeyId]' --output table

Report per-store encryption status, the key source for each, and any store resting on an unverified default.
