---
name: watch-replication-lag-as-a-durability-gap
description: Use when reads or failover depend on a replica. Measures replication lag continuously and treats it as the real RPO, alerting before a failover loses acknowledged data.
---

# Watch Replication Lag as a Durability Gap

The promise "we have a replica" means nothing until you know the lag. Lag in seconds is the data a failover can lose; unmonitored lag turns a failover into silent data loss. Track it as a first-class durability metric.

## Procedure

1. Measure lag from the replica's perspective, not the primary's — the primary often cannot see a replica that stopped applying.
2. Postgres: `SELECT now() - pg_last_xact_replay_timestamp() AS lag;` on the standby; use `pg_last_wal_receive_lsn()` vs `replay_lsn` for byte lag.
3. MySQL: `SHOW REPLICA STATUS\G` → `Seconds_Behind_Source` (and check `Replica_IO_Running`/`SQL_Running` are both `Yes`).
4. Redis/Kafka: consumer-group lag `kafka-consumer-groups.sh --describe --group x` or `redis-cli info replication` `master_link_down_since_seconds`.
5. Export lag as a metric and alert on both bounds: warn at 5s, page at 60s, and page immediately on `null` lag (the standby lost connection).
6. Alert when lag is trending up over an hour even if the instant value is low — a slow replica catches up only after the write burst ends.
7. Tie the alert to the failover runbook: if lag exceeds the RPO window at failover time, the runbook must say to check before promoting.
8. Test the metric by pausing replication (`SELECT pg_wal_replay_pause();`) and confirming the alert fires within the expected delay.

## Pitfalls

- Measuring lag on the primary, which reports 0 when the replica has silently stopped — the classic blind spot.
- Alerting on `Seconds_Behind_Source` only; it can read 0 while the replica is stuck on a conflicting transaction and not applying.
- Ignoring byte lag: a standby replaying a steady state can show 0 seconds yet be gigabytes behind after a bulk load.
- A single async replica as the only copy, then promoting it during a primary outage and losing the un-replicated tail.
- Cascading lag: a replica-of-a-replica inherits the parent's lag and hides it from the primary's monitoring.
- Not accounting for lag during failover time itself; promotion freezes writes and widening the loss window further.
- Muting the lag alert during a known batch job and forgetting to unmute, so the next real stall goes unnoticed.

## Verification

    psql -h standby -c "SELECT now() - pg_last_xact_replay_timestamp() AS lag;"
    # alert test
    psql -h primary -c "SELECT pg_wal_replay_pause();"  # on standby; lag should climb and page

Lag is exported, an induced stall raises the alert within the configured delay, and the failover runbook checks lag against the RPO before promoting.

Report: "Replication lag metric on <N> replicas (warn 5s/page 60s); induced stall alerted in <x>s; current max lag <y>s vs RPO <z>s."
