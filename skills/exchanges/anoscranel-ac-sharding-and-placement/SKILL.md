---
name: ac-sharding-and-placement
description: "Deciding where data lives when one machine cannot hold it: the shard key and why load follows it, hash partitioning and even spread, consistent hashing and minimal movement, range partitioning and its locality trade, hot keys and skew no hash fixes, rebalancing and movement cost, directory services versus computed placement, and the written record. It explains how a key decides a location and what it costs; it never recommends a database and never promises even load. Use when asking \"shard key\", \"consistent hashing\", \"hash ring\", \"virtual node\", \"hot key\", \"partition skew\", \"resharding\", \"data placement\", \"hot partition\", \"shard rebalance\", \"directory service\". Not for replication and consistency of the copies (ac-distributed-state-and-replication), not for analytical partition pruning inside one engine (ac-query-and-index-design), not for multitenancy and tenant isolation (ac-multitenancy-and-isolation)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Sharding and placement

## Overview

Sharding answers a placement question: given a key, which node holds the data? The answer determines how load distributes, how much data moves when the cluster changes, and which access patterns are cheap. A hash of the key spreads writes evenly but answers range questions badly; a range of keys answers range scans well but concentrates load where the keys do; consistent hashing exists because naive modulo placement moves almost everything when the cluster size changes.

Placement is downstream of the query pattern, not the other way around. The record for any sharded system therefore starts from the access patterns the system must serve, states the key that serves them, and then measures what the key choice actually produced — because skew is an empirical fact about traffic, and no hashing scheme legislates it away.

Primary sources: <https://en.wikipedia.org/wiki/Consistent_hashing> and <https://martinfowler.com/articles/patterns-of-distributed-systems/>.

## When to use

- Choosing or evaluating a shard key for a dataset that outgrew one node.
- Reading a consistent-hash ring, virtual nodes, or rendezvous placement.
- Diagnosing hot keys and partition skew.
- Planning a rebalance and its movement cost.

## When NOT to use

- For replicating the copies once placement is decided (use ac-distributed-state-and-replication).
- For engine-internal partition pruning of a query (use ac-query-and-index-design).
- For tenant-level isolation and quota enforcement (use ac-multitenancy-and-isolation).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/shard-key-choice.md` | `software-engineering/shard-key-choice` | The key as the load balancer, and the analysis that precedes choosing it. |
| `subskills/hash-partitioning.md` | `software-engineering/hash-partitioning` | Modulo and hash placement: even spread, no order, and the rehash cost. |
| `subskills/consistent-hashing.md` | `software-engineering/consistent-hashing` | Rings, virtual nodes, rendezvous hashing, and movement proportional to change. |
| `subskills/range-partitioning.md` | `software-engineering/range-partitioning` | Ordered splits that serve range scans and concentrate hotspot risk. |
| `subskills/hot-keys-and-skew.md` | `software-engineering/hot-keys-and-skew` | Measuring skew, the celebrity-key problem, and mitigation that does not fragment the data. |
| `subskills/rebalancing.md` | `software-engineering/rebalancing` | Movement cost, split-by-key, directory re-pointing, and doing it live. |
| `subskills/directory-services.md` | `software-engineering/directory-services` | Computed placement versus a lookup layer, and the trade each makes. |
| `subskills/placement-record.md` | `software-engineering/placement-record` | The written record of key, scheme, measured skew, and rebalance history. |

## Status and honest limits

Placement decisions are falsifiable by traffic, and traffic changes. A key that balances today's workload can skew under tomorrow's largest tenant, and mitigation choices made under pressure have long half-lives. Nothing here recommends a partitioning scheme in the abstract; the honest output of this skill is a measured load distribution plus a rehearsed rebalance path, because the rebalance is the part that is always underestimated until it runs.
