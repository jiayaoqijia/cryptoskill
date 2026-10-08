---
name: route-reads-to-a-replica-not-your-own-write
description: Use when read traffic saturates the primary — route read-only queries to a replica but send read-your-write reads to the primary and treat replication lag as a first-class metric.
---

# Route reads to a replica, read-your-write to the primary

Replicas scale reads cheaply, but they lag. Sending a read that must observe the caller's own write to a replica returns stale data. Route read-only work off the primary, and everything correctness-sensitive back onto it.

## Procedure

1. Identify genuinely read-only queries: no `INSERT/UPDATE/DELETE`, no `SELECT ... FOR UPDATE`, no advisory locks, no read-then-write cycles.
2. Give the app two sessions — `writer` and `reader` — and make the choice explicit on the read path rather than transparent:
```python
def get_orders(user_id):
    return reader.execute("SELECT ...")        # safe: no read-your-write
def create_order(...):
    return writer.execute("INSERT ... RETURNING *")   # return the written row directly
```
3. For read-your-write, either return the written row from the write (`RETURNING`) or pin the session to the primary for a short window after a write.
4. Watch replication lag per replica and gate reads on it:
```sql
SELECT now() - pg_last_xact_replay_timestamp() AS lag;   -- run ON THE REPLICA
```
   Fall back to the primary when lag exceeds a threshold (e.g. 5s); a stale read at that point is a correctness bug.
5. Use a monotonic token for exactness: take the primary's `pg_current_wal_lsn()` at write time and only read from a replica that has replayed past it.
6. Send long analytical reads to a replica to keep the primary's cache and connections for OLTP.
7. Alert on lag, not just replica liveness — a live replica hours behind is worse than none because it silently serves stale data.

## Pitfalls

- Transparent replica routing that sends a post-write read to a lagging replica — the "I saved it but it's not there" bug.
- Reading `pg_last_xact_replay_timestamp()` on the primary, where it is null.
- A read-modify-write cycle split across replica read and primary write, where the stale read clobbers.
- Failover that promotes a lagging replica and immediately takes traffic before it catches up.
- Assuming the replica is read-only; a misconfigured connection string bypasses the app's intent.
- Load-balancing interactive reads across replicas with the same query, so latency varies with which replica answers.

## Verification

    psql -h replica -c "SELECT now() - pg_last_xact_replay_timestamp() AS lag;"
    psql -c "SELECT pg_current_wal_lsn();"
    # pass: lag below the routing threshold, and read-your-write reads land on the primary

Report the read/write routing rule, the lag threshold that forces a primary read, and the measured lag distribution.
