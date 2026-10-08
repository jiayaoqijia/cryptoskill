---
name: choose-durability-by-loss-window
description: Use when setting replication, fsync, or ack policy for a store. Picks the durability tier from the acceptable loss window and failover time, not from defaults.
---

# Choose Durability by Loss Window

Durability is not a boolean, it is a number: how much acknowledged data may one failure destroy, and how long until the store serves reads again. Set fsync, replication and ack policy to hit that number and no higher — extra durability is paid for in latency and cost.

## Procedure

1. State the loss window in seconds of writes and the maximum acceptable failover time. "One acknowledged order may not be lost" is a different tier than "a minute of metrics may vanish".
2. Map the window to a mechanism: fsync-per-write (0 loss, ~ms latency), group commit (bounded loss, batched), async replication (RPO = lag), WAL on a separate volume.
3. Set the write-ack tier explicitly. Postgres: `synchronous_commit = on` (0 loss) vs `off` (up to `wal_writer_delay` = 200ms). Kafka: `acks=all` + `min.insync.replicas=2`. Redis: `appendfsync everysec` vs `always`.
4. Confirm the replica count meets the failed-node tolerance: replication factor 3 survives one node; factor 2 with `min.insync.replicas=1` silently risks loss.
5. Put the WAL/journal on a separate physical device from the data files so a disk failure does not take both.
6. Measure the latency cost of the tier under load — the sync path is where p99 lives: `pgbench -c32 -T60` with `synchronous_commit=on`.
7. Write the RPO/RTO into the runbook; if the business wants a smaller window, name the latency and cost it will add.
8. Re-check when the storage class changes (e.g. moving to network-attached EBS changes fsync latency by 10x).

## Pitfalls

- Leaving `synchronous_commit=off` because it was faster in a benchmark, then losing 200ms of acknowledged writes in a power cut.
- `min.insync.replicas=1` with `acks=all` — the ack is meaningless when a single in-sync replica can vanish with the leader.
- fsync on a filesystem or hypervisor that lies (older ext4 `data=writeback`, some network filesystems); verify with a crash test, not the docs.
- Treating replication lag as an operational metric only; it is the actual RPO and belongs in the durability budget.
- Assuming a cloud SSD volume is durable per-write; durability is a property of the ack path, not the disk spec sheet.
- Ignoring that a synchronous replica in another region adds round-trip latency to every commit, not just failures.
- Choosing the durable tier globally when only the payment table needs it, paying the latency cost on every logging write.

## Verification

    # postgres: acknowledged writes survive an unclean restart
    SHOW synchronous_commit; SHOW synchronous_standby_names;
    # kafka: no message lost with a broker down
    kafka-topics.sh --describe --topic orders | grep -E 'ReplicationFactor|min.insync'

`SHOW synchronous_commit` returns `on`, or the async tier is documented with its measured loss window; a kill -9 test loses no acknowledged record.

Report: "Durability tier: synchronous_commit=on, RF=3/minISR=2 → RPO 0, RTO <60s; measured p99 commit <x>ms under 2x peak."
