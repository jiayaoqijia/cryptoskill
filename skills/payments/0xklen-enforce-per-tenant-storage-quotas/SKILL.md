---
name: enforce-per-tenant-storage-quotas
description: Use when one tenant can fill a shared store. Sets per-tenant quotas and alarms on a shared table, bucket, or filesystem so a single tenant cannot starve the rest.
---

# Enforce Per-Tenant Storage Quotas

In a multi-tenant store, one tenant's runaway upload or log flood consumes the shared volume and fails every other tenant. Enforce a quota per tenant, alarm before it is hit, and make the rejection graceful rather than a full-disk outage.

## Procedure

1. Define the shared resource: one S3 prefix per tenant, a shared Postgres table with a `tenant_id`, or a filesystem with per-tenant directories.
2. Pick the enforcement point nearest the write: database row limits checked in the app, per-bucket/per-prefix metrics, or filesystem project quotas.
3. For filesystems, set project quotas: `xfs_quota -x -c 'project -s -p /data/tenant_a 1001'` then `limit bhard=100g`.
4. For object stores, alert on per-prefix bytes (`aws cloudwatch get-metric-statistics` with a prefix dimension) and enforce at the app layer, since S3 has no hard quota.
5. For tables, add a periodic job that counts per-tenant bytes and rejects writes past the cap, or use row-level storage accounting where available.
6. Alert at 80% of quota, not at 100%, so the tenant has time to clean up or upgrade.
7. Fail the write with a clear error (`QuotaExceeded: tenant_a at 100/100 GB`), not a generic disk-full that the tenant cannot diagnose.
8. Provide a real deletion path so a tenant can get under quota: a purge endpoint with a receipt, wired to `purge-expired-records-with-a-receipt`.
9. Test by writing to a tenant's limit in a scratch environment and confirming only that tenant is affected.

## Pitfalls

- Enforcing quota only in the UI so an API write bypasses it and still fills the shared volume.
- A soft quota with no hard limit, so a single large upload exceeds it before the next check runs.
- Counting only object counts and not bytes, letting one tenant store a few enormous objects under the count cap.
- Alerting at 100%, by which point other tenants are already failing.
- Rejecting all writes for the tenant including its deletes, so it cannot recover below the quota.
- No per-tenant metric, so the last writer to the shared disk gets blamed instead of the actual over-user.
- Copying a quota across tenants with very different sizes, blocking a legitimate large tenant while a small one wastes its allocation.

## Verification

    xfs_quota -x -c 'report -h -p' /data                    # per-project usage vs limit
    aws cloudwatch get-metric-statistics --namespace AWS/S3 \
      --metric-name BucketSizeBytes --dimensions Name=BucketName,Value=acme
# expect: every tenant < 80% of its quota; over-quota write returns QuotaExceeded

Each tenant has a metered usage below its cap, the 80% alarm exists per tenant, and an over-cap write fails for that tenant only.

Report: "Set quotas on <n> tenants (<g> GB each); usage max <p>% of cap; over-quota write returns QuotaExceeded and does not affect other tenants."
