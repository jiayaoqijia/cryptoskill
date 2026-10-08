---
name: enforce-retention-with-lifecycle-rules
description: Use when data accumulates without a deletion policy. Encodes per-class retention as automated expiry rules and proves objects actually age out.
---

# Enforce Retention with Lifecycle Rules

Retention decided in a meeting is not retention enforced by the system. Put an expiry rule on every data class and verify objects disappear on schedule; undocumented indefinite retention is a liability and a cost.

## Procedure

1. Inventory data classes and their required retention: audit logs 400 days, request payloads 30 days, backups 90 days, user uploads until account closure.
2. Confirm no rule exceeds a legal or contractual maximum (GDPR storage limitation, sector rules) and none is shorter than a business need.
3. Encode expiry as data-plane rules, not cron scripts, wherever the platform supports them:
   `aws s3api put-bucket-lifecycle-configuration --bucket acme --lifecycle-configuration file://lc.json`.
4. For object stores, chain transitions and expiries: Standard → IA at 30d → Glacier at 90d → expire at 400d.
5. For databases, add TTL or partitioning: `ALTER TABLE events SET (ttl_expire_after = '90 days');` or `pq_create_retention_policy`.
6. For logs, set the index/ILM policy retention and a delete phase rather than a size cap alone.
7. Keep a short soft-delete window (7-30 days) before hard delete, but make the hard delete real.
8. Verify by sampling age: `aws s3api list-objects-v2 --bucket acme --query 'Contents[?LastModified<`...`]'` should be empty.
9. Log deletions with counts to prove the rule ran, and alert if a class stops shrinking for two cycles.

## Pitfalls

- Writing a retention policy in docs but never attaching it to the bucket, so data lives forever.
- Setting a lifecycle expiry on a versioned bucket without an `NoncurrentVersionExpiration`, so old versions accumulate.
- Deleting active data with an over-broad prefix; a rule scoped to the bucket root will expire things you meant to keep.
- A "soft delete" flag nothing ever purges, so the row count never actually drops.
- Retaining personal data past its purpose because deletion was never a task, turning a policy gap into a compliance finding.
- Expiring logs you still need to satisfy a legal hold — check for holds before adding a delete phase.
- Assuming the provider applies lifecycle asynchronously and immediately; expiry can lag hours, so do not rely on it for security-critical deletion.

## Verification

    aws s3api get-bucket-lifecycle-configuration --bucket acme
    aws s3api list-objects-v2 --bucket acme \
      --query 'Contents[?LastModified<=`2025-01-01`].Key' --output text  # expect empty

Every class has an attached rule, the rule is within the contractual bound, and no object older than its retention still exists.

Report: "Attached lifecycle rules to <N> classes; sampled <M> objects, oldest now <d>d (target <t>d) — no object exceeds its retention."
