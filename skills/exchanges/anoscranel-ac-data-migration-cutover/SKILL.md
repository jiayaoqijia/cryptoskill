---
name: ac-data-migration-cutover
description: "Moving a live system onto new data or a new backend: dual writes and the divergence window, shadow traffic and comparison, backfill ordering before the switch, cutover triggers and rollback, migration windows and freeze periods, straggler and reconciliation, and the written migration record. It explains how to move data and traffic without losing either; it never recommends a tool and never promises a downtime figure. Use when asking \"dual write\", \"shadow traffic\", \"data migration cutover\", \"backfill then switch\", \"rollback plan\", \"migration window\", \"straggler rows\", \"reconciliation after migration\", \"dark launch data\", \"zero downtime migration\". Not for schema migrations within an existing store (ac-database-changes), not for deployment rollouts of code (ac-ci-and-release), not for analytical backfills and reproducibility (ac-market-data-collection)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Data migration cutover

## Overview

A cutover moves a live system onto different data or a different backend, and the difficulty is not the copy — it is keeping the copy truthful while the source keeps changing. Every technique in this skill exists to answer one question: at the moment traffic switches, is the new store a faithful continuation of the old one, and what happens to the writes that arrive between, before, and after?

The approaches trade complexity against downtime. A big-bang copy with an outage is simple and stops the world. A dual-write phase with backfill and a switch is complex and stops nothing, but introduces a divergence window in which the two stores disagree. Between them sits shadow traffic: real reads answered by the new store in silence, compared against the old, cutover only when the comparison is quiet. The choice must be explicit because each carries a different failure, not merely a different cost.

Primary sources: <https://martinfowler.com/> and <https://www.postgresql.org/docs/>.

## When to use

- When moving data to a new store, schema, or sharding arrangement.
- When splitting, merging, or re-keying a dataset that is still serving writes.
- When choosing between outage, dual write, and shadow-verify styles of migration.

## When NOT to use

- For schema evolution within one existing store (use ac-database-changes).
- For code rollout and rollback strategy (use ac-ci-and-release).
- For research-data backfills and reproducibility (use ac-market-data-collection).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/cutover-strategies.md` | `software-engineering/cutover-strategies` | Big bang, dual write, and shadow-verify; what each risks. |
| `subskills/dual-writes.md` | `software-engineering/dual-writes` | Writing both stores at once, and how they silently diverge. |
| `subskills/shadow-and-verification.md` | `software-engineering/shadow-and-verification` | Serving the new store silently and comparing results before trusting it. |
| `subskills/backfill-ordering.md` | `software-engineering/backfill-ordering` | Copying the old data so the backfill finishes ahead of the switch. |
| `subskills/switch-and-rollback.md` | `software-engineering/switch-and-rollback` | The cutover trigger, the reverse path, and what rollback restores. |
| `subskills/straggler-and-reconciliation.md` | `software-engineering/straggler-and-reconciliation` | Rows written late, counted after, and reconciled into truth. |
| `subskills/migration-record.md` | `software-engineering/migration-record` | The written record: strategy, phases, triggers, and the numbers compared. |

## Status and honest limits

Migrations fail in the divergence between two live systems, and that divergence is discovered, not deduced — the verification and reconciliation passes are the only measurement that matters. Nothing here recommends a tool, and a cutover plan whose rollback has never been executed is a plan that assumes the old system will hold still while the new one is being repaired, which is the assumption the plan exists to avoid.
