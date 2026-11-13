---
name: ac-distributed-state-and-replication
description: "Keeping copies of data consistent when there is more than one copy: replication topologies and what each promises, read replicas and their staleness, leader election and split-brain prevention, quorum reads and writes and the arithmetic of their overlap, vector clocks and conflict detection, CRDTs and conflict-free merges, read-your-writes and session guarantees, and the written replication record. It explains the guarantees a replicated store can and cannot give; it never recommends a database product and never promises a consistency level. Use when asking \"read replica\", \"replication lag\", \"split brain\", \"leader election\", \"quorum\", \"vector clock\", \"CRDT\", \"read your writes\", \"eventual consistency\", \"write conflict\", \"why did my write disappear\", \"stale read\". Not for cache correctness and TTL choices (ac-caching-and-invalidation), not for schema migrations and backfills (ac-database-changes), not for event delivery between services (ac-event-driven-architecture)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Distributed state and replication

## Overview

Replication is keeping more than one copy of the same data, and every replication decision is a trade between consistency, availability, and latency — pick two at the replica level and the third degrades. The skill is knowing which guarantee your application actually needs, because the strongest one is the most expensive, and most applications do not need it for most operations.

This skill covers the mechanics: primary-replica versus multi-leader versus quorum topologies, the staleness a read replica carries and how to bound it, how leaders are elected and how split brain is prevented (or fails to be), the quorum arithmetic that makes reads and writes overlap, vector clocks and version vectors as conflict detectors, CRDTs as merges that cannot conflict, and the session guarantees that give a user their own writes back. Caching correctness is a different skill; so are migrations and event delivery.

Primary sources: <https://jepsen.io/> and <https://martinfowler.com/>.

## When to use

- When choosing or configuring a replication topology for a data store.
- When a read must see a recent write and the data is replicated.
- When more than one writer can accept writes for the same key.
- When a failover plan has to state what happens during and after.

## When NOT to use

- For cache keys, TTL choices, and invalidation design (use ac-caching-and-invalidation).
- For schema changes, migration runners, and backfills (use ac-database-changes).
- For event delivery between services and consumer lag (use ac-event-driven-architecture).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/replication-topologies.md` | `software-engineering/replication-topologies` | Primary-replica, multi-leader, and leaderless; what each can promise. |
| `subskills/read-replicas-and-staleness.md` | `software-engineering/read-replicas-and-staleness` | Replica lag, its causes, and bounding how far behind a read can be. |
| `subskills/leader-election-and-split-brain.md` | `software-engineering/leader-election-and-split-brain` | Choosing a leader, fencing old ones, and the failure that is two. |
| `subskills/quorum-arithmetic.md` | `software-engineering/quorum-arithmetic` | Read and write quorums, the overlap that makes them intersect, and the arithmetic of staleness. |
| `subskills/vector-clocks-and-conflicts.md` | `software-engineering/vector-clocks-and-conflicts` | Detecting concurrent writes and what the detection costs. |
| `subskills/crdts-and-merge.md` | `software-engineering/crdts-and-merge` | Data types whose merges cannot conflict, and their limits. |
| `subskills/session-guarantees.md` | `software-engineering/session-guarantees` | Monotonic reads, read-your-writes, and routing a session to the right replica. |
| `subskills/replication-record.md` | `software-engineering/replication-record` | The written record: topology, guarantees chosen, failover plan, and measured lag. |

## Status and honest limits

Consistency guarantees are enforced by the store's implementation, not by intent, and implementations fail their own documentation — consistency under partitions and failures is an empirical property, verified by testing, not read off a feature list. Nothing here recommends a product, and a topology choice made without stating which operations need which guarantee is a choice made blind.
