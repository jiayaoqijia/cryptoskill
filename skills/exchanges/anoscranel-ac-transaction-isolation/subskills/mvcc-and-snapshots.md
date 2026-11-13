---
name: mvcc-and-snapshots
domain: software-engineering/mvcc-and-snapshots
trigger: "Understanding what a snapshot read freezes and what it does not."
anti_trigger: "Not for replication topology, and not for choosing an isolation level."
scope: "Multiversion reads, snapshot freezes, and what writers see of each other."
status: seedling
---

# MVCC and snapshots

## Standard

Under multiversion concurrency control, a row's old version survives alongside its new one, and a reader operates on a consistent snapshot — the database as of the moment the transaction started, with every writer's in-flight changes invisible. Readers do not block writers and writers do not block readers, which is the mechanism behind fast concurrent reads at the cost of storing multiple versions and clearing them later.

What a snapshot freezes is reads, not writes. Two snapshot transactions can both read a stale value and both write based on it; the first writer wins and the second fails its check — serializable aborts it, while weaker levels can commit it as an anomaly. The snapshot is a camera, and the recording in the record should say plainly that a camera does not prevent the people in the photo from moving.

Primary sources: <https://www.postgresql.org/docs/current/mvcc.html> and <https://jepsen.io/consistency>.

## Decision rules

- Record which statements take a snapshot and when the snapshot is taken.
- State whether a transaction's snapshot is fixed at start or moves per statement.
- Record the write-conflict check the engine applies between concurrent writers.
- Note that long snapshots delay version cleanup, and by how much.
- Never describe a snapshot read as a lock on the data it read.
- Name write skew as the snapshot's own failure: two transactions check the same stable snapshot, each decide safely on their own, and the combination breaks a rule neither saw broken.
- Record what a snapshot does not contain: other transactions' uncommitted and later work.

## Procedure

1. Determine the engine's snapshot acquisition point per isolation level.
2. Record whether the snapshot advances with each statement.
3. Test two concurrent snapshot readers both writing the same row.
4. Observe which one the engine rejects and which level allows both.
5. Measure version-age growth with a deliberately long snapshot.
6. Record snapshot semantics and the conflict behaviour.

## Anti-patterns

- Assuming a repeatable read blocks concurrent writers.
- Holding a snapshot open for a report while writes continue, then vacuum stalls.
- Treating snapshot age as harmless background noise.
- Describing MVCC as "locking that never blocks", which is only half true.
- No test of the concurrent-writers case at the chosen level.

## Done checklist

- [ ] Snapshot acquisition point recorded.
- [ ] Fixed versus per-statement snapshot stated.
- [ ] Write-conflict behaviour tested.
- [ ] Version-age cost measured.
- [ ] Snapshot limits stated plainly.
- [ ] Findings recorded.

## Sources

- Multiversion concurrency control, from the engine: <https://www.postgresql.org/docs/current/mvcc.html>
- Consistency-model anomaly taxonomy: <https://jepsen.io/consistency>
- Isolation levels that build on snapshots: <https://www.postgresql.org/docs/current/transaction-iso.html>
