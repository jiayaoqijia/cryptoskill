---
name: ac-query-and-index-design
description: "Designing indexes and the queries that use them: what an index costs on write and in space, the access paths a planner can choose, composite column order, covering and partial indexes, selectivity and statistics, and partition pruning. It explains access paths and their costs; it never recommends a database product and never promises a latency. Use when asking \"database index\", \"which columns to index\", \"composite index order\", \"covering index\", \"query plan\", \"why is this query slow\", \"full table scan\", \"index selectivity\", \"partition pruning\", \"explain plan\". Not for schema shape and migrations (ac-database-changes), not for application-level caching (ac-caching-and-invalidation), not for end-to-end latency work and profiling (ac-performance)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Query and index design

## Overview

An index is a second copy of some of a table's data, kept sorted, paid for on every write. That framing decides most index questions: the read it accelerates and the write it slows are both real, and the choice is a trade rather than an improvement. A table with eleven indexes is a table whose inserts cost eleven sorted writes.

The planner chooses between access paths using statistics about the data, and the choice can be wrong when the statistics are stale or when a predicate is written in a form the planner cannot use. This skill covers the paths available, how column order decides which predicates an index serves, what makes an index selective, and how partitioning interacts with pruning.

Primary sources: <https://www.postgresql.org/docs/> and <https://use-the-index-luke.com/>.

## When to use

- When a query is slow and the cause might be the access path.
- When adding, removing, or reordering an index.
- When a table's write cost is dominated by its index count.
- When partitioning is expected to reduce scanned data.

## When NOT to use

- For schema shape, keys, and normalisation (use ac-database-changes).
- For migrations that change the table while it is live (use ac-database-changes).
- For application-level latency and caching layers (use ac-caching-and-invalidation).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/index-cost-and-tradeoffs.md` | `software-engineering/index-cost-and-tradeoffs` | Write amplification, space, and what an index is actually buying. |
| `subskills/access-paths.md` | `software-engineering/access-paths` | Sequential scan, index scan, index-only, bitmap, and when each wins. |
| `subskills/composite-column-order.md` | `software-engineering/composite-column-order` | Why the leftmost column dominates, and how to order for the query set. |
| `subskills/selectivity-and-statistics.md` | `software-engineering/selectivity-and-statistics` | Cardinality, histograms, staleness, and the planner's mistakes. |
| `subskills/covering-and-partial-indexes.md` | `software-engineering/covering-and-partial-indexes` | Including columns to avoid a lookup, and indexing a subset of rows. |
| `subskills/partitioning-and-pruning.md` | `software-engineering/partitioning-and-pruning` | Partition keys, pruning, and the predicates that prevent it. |
| `subskills/query-record.md` | `software-engineering/query-record` | The written record: the query, its plan, the indexes, and the cost model. |

## Status and honest limits

Planner behaviour is product-specific and changes between versions, and this skill describes the general mechanism rather than any one optimizer's rules. Statistics go stale, and a plan that was optimal at one data volume is not optimal at another. Nothing here recommends a database, and an index added to fix one query can slow every write on the table, which is why the record states both sides.
