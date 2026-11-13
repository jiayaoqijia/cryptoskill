---
name: ac-transaction-isolation
description: "Understanding what a database transaction actually guarantees: the isolation levels from read uncommitted to serializable and the anomalies each permits, MVCC and snapshot reads, lost updates and both optimistic and pessimistic resolution, explicit locking and lock ordering deadlocks inside the engine, savepoints and nested work, long transactions and their costs, and the written isolation record. It explains what isolation a query runs under; it never recommends a database product and never promises a result free of anomalies without the level to match. Use when asking \"isolation level\", \"read committed\", \"repeatable read\", \"serializable\", \"MVCC\", \"snapshot isolation\", \"lost update\", \"optimistic locking\", \"SELECT FOR UPDATE\", \"deadlock retry\", \"long transaction\", \"write skew\". Not for schema shape and migrations (ac-database-changes), not for distributed consensus across nodes (ac-distributed-state-and-replication), not for queue and workflow delivery semantics (ac-durable-execution)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Transaction isolation

## Overview

A transaction's isolation level decides which of another transaction's effects it can see, and the levels are best understood as a list of permitted anomalies: dirty reads, non-repeatable reads, phantoms, and write skew each disappear at some level and are permitted below it. The upward options trade strictness for concurrency, and the engineering work is matching the level to what the code actually assumes — because most code is written as if it were serialised and run at something weaker.

This skill covers the levels and their anomalies, multiversion concurrency control and what a snapshot read really freezes, lost updates and the two locking philosophies that prevent them, explicit row locking and the deadlock shapes it creates inside a single database, partial rollback with savepoints, and the cost profile of long-running transactions. Distributed consensus across nodes is a different skill.

Primary sources: <https://www.postgresql.org/docs/current/transaction-iso.html> and <https://jepsen.io/consistency>.

## When to use

- When choosing or verifying an isolation level for a unit of work.
- When concurrent updates may lose each other and must not.
- When deadlocks arise from explicit locking inside one database.
- When a batch or reporting query holds locks or snapshots for minutes.

## When NOT to use

- For schema shape, migrations, and backfills (use ac-database-changes).
- For replication quorums and split-brain across nodes (use ac-distributed-state-and-replication).
- For message and workflow delivery guarantees (use ac-durable-execution).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/levels-and-anomalies.md` | `software-engineering/levels-and-anomalies` | The isolation levels, the anomaly each permits, and the one it removes. |
| `subskills/mvcc-and-snapshots.md` | `software-engineering/mvcc-and-snapshots` | Multiversion reads, snapshot freezes, and what writers see of each other. |
| `subskills/lost-updates.md` | `software-engineering/lost-updates` | The lost update anomaly and optimistic versus pessimistic prevention. |
| `subskills/explicit-locking.md` | `software-engineering/explicit-locking` | Row locks, lock ordering, and the deadlock the engine reports back. |
| `subskills/savepoints-and-partial-rollback.md` | `software-engineering/savepoints-and-partial-rollback` | Nested work inside one transaction and recovering part of it. |
| `subskills/long-transactions.md` | `software-engineering/long-transactions` | Lock hold time, vacuum and snapshot age, and batching the work. |
| `subskills/isolation-record.md` | `software-engineering/isolation-record` | The written record: level, assumptions, locks, and retry policy. |

## Status and honest limits

Isolation behaviour is engine-specific: the same level name can mean different things in different products, and the SQL standard's own definitions famously permit more anomalies under repeatable read than engines implement. This skill teaches the questions and the anomalies; the engine's own documentation is the authority on its answers, and the record should name both. Nothing here recommends a database, and a retry-on-conflict loop without a jittered backoff is a stampede waiting for its trigger.
