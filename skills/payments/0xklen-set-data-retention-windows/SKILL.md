---
name: set-data-retention-windows
description: Use when data classes have no defined lifetime or rely on a policy document nobody enforces. Assign each class a window with a mechanism that actually deletes.
---

# Set data retention windows

Data kept past its purpose is undeclared risk. This skill assigns each data class a retention window backed by a mechanism that enforces it, not a paragraph in a policy.

## Procedure

1. Group data into classes by purpose and legal minimum: auth logs 90d, invoices 7 years for tax, raw analytics 30d, session tokens 24h.

2. Record the windows machine-readably in `retention.yaml`:
   ```yaml
   invoice:      {window_days: 2555, basis: legal_obligation, action: archive_then_delete}
   analytics_raw: {window_days: 30,  basis: legitimate_interest, action: delete}
   session:      {window_days: 1,   basis: contract, action: ttl}
   ```

3. Separate active from archive and define when a row leaves active storage, for example `closed_at + 30d`.

4. Pick an enforcement mechanism per class: scheduled delete job, partition drop, TTL index, or object lifecycle rule.

5. For object stores use native lifecycle, not cron: `aws s3api put-bucket-lifecycle-configuration --bucket b --lifecycle-configuration file://life.json` with `Expiration.Days`.

6. For Postgres prefer declarative partitioning plus `DROP TABLE` of the oldest partition over row-by-row `DELETE`, which bloats and cannot be proven complete.

7. Set retention longer than dependencies: never delete a user row still referenced by an open invoice. Order child deletions first or use an explicit `ON DELETE` behaviour you have tested.

8. Add monitoring that the oldest row cannot exceed its window:
   `select 'analytics_raw', max(now()-created_at) from analytics_raw union all select 'auth_logs', max(now()-created_at) from auth_logs`

9. Run a quarterly audit comparing the policy windows in `retention.yaml` to the actual maximum ages.

## Pitfalls

- Deletion jobs that fail silently leave rows forever; alert on rows-deleted = 0 when the window should have fired.
- A legal hold overrides retention; a litigation or investigation flag must pause deletion for the specific rows.
- Backups outlive the window and need their own schedule; see verify-deletion-in-backups-and-snapshots.
- A "daily" job at 00:00 UTC deletes a day early or late for some tenants; anchor on the stored timestamp, not the wall clock.
- Cascading deletes can remove too much; confirm FK behaviour on a copy before enabling the constraint in production.

## Verification

    psql "$DATABASE_URL" -c "select 'analytics_raw' k, max(now()-created_at) age from analytics_raw union all select 'auth_logs', max(now()-created_at) from auth_logs"

Every age must be under its configured window; report any class exceeding it as a live retention failure.
