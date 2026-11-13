---
name: ac-time-series-storage
description: "Storing and serving numeric measurements over time: the time series data model and its labels, the write path and out-of-order arrival, compaction and downsampling, retention as a per-series policy, the query path from range selectors to aggregation, cardinality as the design constraint that decides everything else, and the written storage record. It explains how time series storage behaves and how to keep it healthy; it never recommends a database product and never promises a query time. Use when asking \"time series database\", \"metric cardinality\", \"labels versus tags\", \"timestamped samples\", \"downsampling\", \"rollup\", \"retention policy\", \"out of order samples\", \"histogram bucket\", \"PromQL\", \"capacity for metrics\", \"why is my TSDB slow\", \"sample interval\". Not for SLO definition and alerting semantics (ac-reliability), not for event and log pipelines (ac-data-pipeline-orchestration), not for financial market data collection (ac-market-data-collection)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Time-series storage

## Overview

A time series is a named measurement sampled over time, and a time-series database is engineered around the patterns that produce: writes are append-mostly and arrive continuously, queries read dense windows rather than single rows, and the storage engine works by chunking, compressing, and gradually compacting the data so that recent samples are cheap to write and old samples are cheap to keep. The design constraint that dominates everything — capacity, query speed, feasibility — is cardinality: the number of distinct label combinations, because that is the number of series the system tracks.

The failure mode of a time-series deployment is almost never the engine; it is a label set that grew. A metric with an id label turns per-object into per-series, and one unbounded label multiplies the series count until ingest slows, queries time out, and the retention job starves. This skill covers the model, the write and query paths, the compaction and retention mechanics, and above all the design discipline over labels that decides whether the system stays healthy.

Primary sources: <https://prometheus.io/docs/introduction/overview/> and <https://en.wikipedia.org/wiki/Time_series_database>.

## When to use

- Designing a metrics schema and its labels for a service or platform.
- Diagnosing TSDB capacity, ingest, or query-performance problems.
- Setting retention, downsampling, and rollup policies.
- Evaluating the storage consequences of an observability design.

## When NOT to use

- For SLO targets, error budgets, and alert routing semantics (use ac-reliability).
- For batch event and log pipeline orchestration (use ac-data-pipeline-orchestration).
- For market data collection pipelines in finance (use ac-market-data-collection).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/the-series-model.md` | `software-engineering/the-series-model` | Series, samples, labels, and what cardinality means. |
| `subskills/write-path.md` | `software-engineering/write-path` | Ingest, scrape intervals, timestamp assignment, and out-of-order arrival. |
| `subskills/schema-and-indexing.md` | `software-engineering/schema-and-indexing` | The label index, matching, and cardinality as the design constraint. |
| `subskills/chunking-and-compaction.md` | `software-engineering/chunking-and-compaction` | Head chunks, compression, block compaction, and the cost curve. |
| `subskills/downsampling-and-retention.md` | `software-engineering/downsampling-and-retention` | Rollups, value-selection semantics, and retention as a policy. |
| `subskills/query-path.md` | `software-engineering/query-path` | Range selectors, aggregation, and the scrape-interval floor. |
| `subskills/tsdb-record.md` | `software-engineering/tsdb-record` | The written record: series inventory, capacity, and policy state. |

## Status and honest limits

Time-series engines differ in exact mechanics; this skill covers the shared design space rather than any single engine's internals, and names no products as recommendations. The honest absolute is that no amount of tuning rescues a schema whose cardinality was decided in application code, because the label set is decided before the database ever sees the sample. Nothing here promises a query time; the measurable outcomes are stored in the record with their dates.
