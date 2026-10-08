---
name: prove-a-storage-failover-with-a-read
description: Use when a standby or replica must take over. Proves failover by serving a real read from the promoted target, not by checking replication status or a health flag.
---

# Prove a Storage Failover with a Read

Promotion scripts report success; only an actual read from the promoted target proves it can serve. Failover is verified by reading a known key from the new primary, confirming the write path, and then deciding on the old primary.

## Procedure

1. Before failover, record the exact expected state: a known key and its value, the last committed transaction id, and the replication lag.
2. Stop writes to the primary (fence it) so the two cannot diverge — an unfenced old primary accepts writes and creates split-brain.
3. Promote the standby: `pg_ctl promote -D /var/lib/postgresql/data` or `SELECT pg_promote();`; for a cluster, the orchestrator's promote path.
4. Verify with a read, not a status flag: `psql -h newprimary -c "SELECT pg_is_in_recovery();"` must return `f` (not a standby).
5. Read the known key from the new primary and compare to the recorded value — this is the proof the data survived.
6. Re-point clients (DNS/service endpoint/VIP) and verify a write round-trips: insert a canary row and read it back.
7. Confirm the old primary is fenced or demoted to standby before it is ever allowed to accept traffic again.
8. Record RTO (time from fence to first successful read) and RPO (the newest record present) and update the runbook.
9. Fail the drill if any read served stale or missing data, even if the promotion command exited 0.

## Pitfalls

- Declaring failover done because `pg_ctl promote` returned success, without reading data back.
- Promoting without fencing the old primary; both accept writes and the data diverges with no clean winner.
- Reading from a client still cached to the old endpoint, so the "successful read" came from the wrong host.
- A read-only standby that was promoted but has a `default_transaction_read_only = on` override, so writes silently fail.
- DNS TTLs too long, so clients keep hitting the dead primary for minutes after promotion and the RTO is understated.
- Forgetting downstream consumers (cache, search index, analytics) still pointed at the old primary.
- Promoting a replica with high lag and losing the un-replicated tail, then reporting RPO as if it were zero.

## Verification

    psql -h newprimary -c "SELECT pg_is_in_recovery();"          # expect f
    psql -h newprimary -c "SELECT * FROM canary WHERE id=1;"     # expect the recorded value
    psql -h newprimary -c "INSERT INTO canary(id) VALUES (99) RETURNING id;"  # write succeeds

The promoted target returns `f` for recovery, serves the recorded key without loss, and accepts a new write; RTO/RPO are logged and within target.

Report: "Failover drill: promoted <replica> in <s>s (RTO); known key intact (RPO <n>s lag); write canary round-trip OK; old primary fenced."
