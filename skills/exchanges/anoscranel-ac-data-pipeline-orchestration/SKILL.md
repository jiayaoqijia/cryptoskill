---
name: ac-data-pipeline-orchestration
description: "Running batch data pipelines as a platform rather than as scripts: the DAG as the dependency contract, idempotent reruns and backfills, late-arriving data and upserts, partition strategy as the pipeline's physical index, freshness monitoring and SLAs, lineage and pipeline observability, and the written pipeline record. It explains how batch pipelines are scheduled, rerun, and kept observable; it never recommends an orchestrator and never promises a freshness figure. Use when asking \"data pipeline orchestration\", \"DAG scheduling\", \"backfill\", \"idempotent pipeline\", \"late arriving data\", \"partition strategy\", \"data freshness SLA\", \"pipeline lineage\", \"rerun failed tasks only\", \"upsert pattern\". Not for market-data collection specifically (ac-market-data-collection), not for the data contract at a boundary (ac-data-contracts), not for unbounded stream processing (ac-stream-processing)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Data pipeline orchestration

## Overview

A batch pipeline is a graph of transformations over data that arrives, changes, and sometimes arrives late. Scripts chained with cron break the moment a run fails halfway and someone must decide what to rerun without re-corrupting what already succeeded. Orchestration is the discipline that makes reruns safe: tasks are declared as a graph with explicit dependencies, each task is idempotent over a stated input partition, and the platform tracks which partitions of which tasks are complete.

The craft lives in the semantics, not the tool: idempotency over what key, backfill over what window, upsert keyed how, freshness measured against what reference. Get those right and any scheduler works; get them wrong and no scheduler saves the data.

Primary sources: <https://airflow.apache.org/docs/> and <https://docs.getdbt.com/>.

## When to use

- Designing or operating batch data pipelines with multiple dependent stages.
- Making reruns and backfills safe after partial failures.
- Choosing partitioning and upsert keys for correctness on late data.
- Setting and monitoring freshness for downstream consumers.

## When NOT to use

- For financial market-data collection specifics (use ac-market-data-collection).
- For the contract a dataset offers its consumers (use ac-data-contracts).
- For unbounded stream processing and watermarks (use ac-stream-processing).
- For single time-triggered job semantics (use ac-scheduled-jobs).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/dag-dependencies.md` | `software-engineering/dag-dependencies` | Declaring the graph, sensors versus polling, and what the DAG must not know. |
| `subskills/idempotency-and-reruns.md` | `software-engineering/idempotency-and-reruns` | Idempotent tasks keyed on input partition; rerun failed tasks only. |
| `subskills/backfills.md` | `software-engineering/backfills` | Rerunning history safely: window declaration, catch-up control, resource shaping. |
| `subskills/late-data-and-upserts.md` | `software-engineering/late-data-and-upserts` | Late-arriving records and the merge/upsert keys that keep them correct. |
| `subskills/partitioning-strategy.md` | `software-engineering/partitioning-strategy` | Partition keys as the pipeline's physical index for pruning and reruns. |
| `subskills/freshness-and-sla.md` | `software-engineering/freshness-and-sla` | Freshness measured against a reference, monitored, and honestly reported. |
| `subskills/lineage-and-observability.md` | `software-engineering/lineage-and-observability` | Column-level lineage, run metadata, and finding what a failure touched. |
| `subskills/pipeline-record.md` | `software-engineering/pipeline-record` | The written record: DAG, keys, SLAs, failure paths, backfill history. |

## Status and honest limits

Orchestration platforms change; the semantics — idempotency, backfill windows, partition keys, freshness references — are stable and are what this skill owns. Nothing here recommends a scheduler or promises zero-data-loss: a pipeline is only as correct as its keys, and a mis-keyed upsert fails silently while every task shows green. The record leaf exists because a pipeline's behavior under failure is only knowable from what was written down when it was designed.
