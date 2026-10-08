---
name: flip-to-read-only-under-stress
description: Use when a saturated primary or exhausted write path risks data loss or corruption — switches the system to read-only rather than accepting writes it cannot durably commit.
---

# Flip to read-only under stress

When the write path is the thing failing — replication lag climbing, disk nearly full, the primary flapping — continuing to accept writes is how a recoverable slowdown becomes data loss. Flip to read-only, serve the reads you can, and preserve the write intent for later if the contract allows.

## Procedure

1. Define the signal that means "writes are unsafe": replication lag above N seconds, free disk below 5%, WAL/redo growth beyond the disk's headroom, primary failover in progress, or write-error rate above a threshold. It must be a measurement, not "things feel slow".

2. Flip at the *database* layer as the hard backstop and at the app layer for a clean message. Postgres:
       ALTER DATABASE app SET default_transaction_read_only = on;   -- applies to new sessions
   App middleware then returns `503` with `Retry-After` for non-idempotent verbs, and serves GETs normally.

3. Serve reads from where they are safe: replicas if lag allows, otherwise an application cache. Do *not* read from a primary mid-failover; a stale read beats an error but a read from a flapping node beats neither:
       if replica_lag_seconds > 30 { serve_from_cache() } else { route_to_replica() }

4. Decide write-intent policy *before* flipping: either reject (client must retry) or queue durably (accept and replay). Queuing requires an idempotent replay path and a dedupe key; without those, a queued write replayed twice is the corruption you fled.

5. Target read-only at the operations that are actually unsafe. A read-only mode that blocks a lock-contended batch insert but also blocks login (which writes a session row) turns a write incident into a full outage. Exempt the minimum necessary critical writes explicitly.

6. Announce on the status page and in the API body why writes are refused, so clients do not interpret `503` as a bug and retry aggressively the moment you flip back.

7. Flip back only after the trigger has been clear for 2× its window and a write smoke test passes against a canary. Then ramp writes: one internal client, then a percentage, watching lag.

## Pitfalls

- Enabling read-only but leaving an async consumer or cron writing directly with a privileged role that bypasses `default_transaction_read_only`.
- Blocking session/login writes along with the risky ones, locking users out and multiplying support load during the incident.
- Queuing writes in memory that are lost when the process restarts — "we'll replay them later" needs the queue to survive the restart.
- Flipping back the instant lag briefly dips, then re-tripping and oscillating, which is worse for clients than a steady read-only.

## Verification

    # trigger read-only and confirm writes are refused while reads serve
    psql "$DB" -c "SHOW default_transaction_read_only;"     # on
    curl -s -o /dev/null -w '%{http_code}\n' -X POST localhost:8080/items -d '{}'  # 503 + Retry-After
    curl -s -o /dev/null -w '%{http_code}\n' localhost:8080/items                  # 200
    psql "$DB" -c "SELECT count(*) FROM sessions WHERE created_at > now() - interval '1 min';"  # login still works

Report: the trigger metric and threshold, the layer the flip lives at, proof writes are refused and reads serve, and the write-intent policy (reject vs durable queue) with its dedupe key.
