---
name: ac-database-engine-internals
description: "The storage engine under the query interface: how a B-tree pages and splits, how an LSM tree layers and compacts, the write-ahead log and what it makes durable, buffer pools and eviction, page layout and slot directories, tombstones and deletion in structures that do not overwrite, checkpointing and recovery, and the written engine record. It explains how an engine's structures decide its read-write trade-offs; it never recommends an engine and never promises a throughput. Use when asking \"b-tree\", \"LSM tree\", \"write ahead log\", \"buffer pool\", \"page layout\", \"tombstone\", \"compaction\", \"why are my writes getting slower\", \"read amplification\", \"write amplification\", \"space amplification\", \"storage engine\", \"why does deleting not reclaim space\". Not for index selection and query plans (ac-query-and-index-design), not for transaction isolation and anomalies (ac-transaction-isolation), not for analytical columnar layout (ac-analytical-data-modeling)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Database engine internals

## Overview

A database's behaviour is decided less by its query language than by its storage engine. A B-tree rewrites pages in place, which makes point reads cheap and writes proportional to the tree; an LSM tree appends and merges, which makes writes fast and reads pay for the layers the merge has not yet folded. Both keep a log so a crash does not lose an acknowledged write, and both hold pages in memory governed by an eviction policy that decides which reads are fast.

The three amplifications — read, write, and space — are the currency of every design choice in this layer, and a tuning question almost always resolves into trading one for another. This skill covers the structures and their consequences so that a slow-write or fast-fill diagnosis begins at the mechanism rather than at the vendor.

Primary sources: <https://postgresql.org/docs/current/> and <https://dev.mysql.com/doc/>.

## When to use

- When diagnosing writes that slow over time, deletes that do not reclaim space, or reads whose cost grows with system age.
- When choosing between a B-tree and an LSM workload shape, or reasoning about compaction.
- When reasoning about durability: what the log guarantees and what a checkpoint does.
- When explaining amplification terms in a design conversation or an incident.

## When NOT to use

- For choosing indexes and reading query plans (use ac-query-and-index-design).
- For isolation levels, anomalies, and locking (use ac-transaction-isolation).
- For analytical columnar and sort design (use ac-analytical-data-modeling).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/write-ahead-logging.md` | `software-engineering/write-ahead-logging` | Log-before-overwrite, group commit, checkpoints, and recovery replay. |
| `subskills/btrees-and-pages.md` | `software-engineering/btrees-and-pages` | The in-place update tree, its splits, and its page model. |
| `subskills/lsm-trees.md` | `software-engineering/lsm-trees` | Append-only layers, memtables, and the merge that keeps depth bounded. |
| `subskills/buffer-pools.md` | `software-engineering/buffer-pools` | What stays in memory, what gets evicted, and the fix-up cost of a miss. |
| `subskills/tombstones.md` | `software-engineering/tombstones` | Deletion as a write, and the reclamation it defers. |
| `subskills/compaction-tuning.md` | `software-engineering/compaction-tuning` | When merges run, what they cost, and whose latency they borrow. |
| `subskills/amp-analysis.md` | `software-engineering/amp-analysis` | Read, write, and space amplification as the engine's design currency. |
| `subskills/engine-record.md` | `software-engineering/engine-record` | The written record of structures, config, and amplification for a workload. |

## Status and honest limits

Engine internals differ between implementations, and the same term can cover different mechanics: one engine's compaction is another's vacuum, and page sizes are configuration, not constants. The invariants here — log before overwrite, append before merge, amplify one dimension to save another — hold across engines, but a diagnosis made from a term should be verified against the implementation's own documentation before being acted on.
