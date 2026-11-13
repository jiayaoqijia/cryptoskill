---
name: ac-analytical-data-modeling
description: "Designing data for questions rather than for transactions: fact and dimension tables, grain as the first decision, star and snowflake shapes, slowly changing dimensions and their types, aggregation and pre-summary trade-offs, columnar layout and sort order, metrics definition layers, and the written modeling record. It explains how analytical shape serves queries; it never recommends a warehouse product and never promises a query time. Use when asking \"star schema\", \"fact table\", \"dimension table\", \"grain\", \"slowly changing dimension\", \"SCD type 2\", \"snowflake schema\", \"OLAP\", \"metrics layer\", \"semantic layer\", \"columnar storage\", \"aggregate table\", \"why is this dashboard query slow\". Not for operational schema and migrations (ac-database-changes), not for reporting the numbers once defined (ac-dataviz), not for query and index tuning of the engine (ac-query-and-index-design)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Analytical data modeling

## Overview

Operational schema serves writes; analytical schema serves questions. The difference shows in every decision: a transactional model normalises to protect integrity under concurrent updates, while an analytical model denormalises around a grain — one row per event, per order line, per daily balance — and organises everything else to serve aggregation over that grain. Getting the grain wrong is the one mistake that cannot be fixed by indexing, because every number built on it inherits the ambiguity.

This skill covers the analytical craft: choosing grain, designing facts and dimensions, star versus snowflake, handling change over time in dimensions, pre-aggregation and its refresh cost, columnar layout and sort order, and the metrics definition layer that keeps a number meaning one thing. The engine's query tuning and the operational schema are other skills.

Primary sources: <https://www.kimballgroup.com/> and <https://martinfowler.com/>.

## When to use

- When designing a schema whose job is analysis and reporting.
- When a metric must mean the same thing in every report.
- When dimension data changes over time and history must stay truthful.
- When aggregate tables and pre-summaries are being considered.

## When NOT to use

- For operational schema design and migrations (use ac-database-changes).
- For presenting the numbers once defined (use ac-dataviz).
- For engine-level query and index tuning (use ac-query-and-index-design).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/grain-and-facts.md` | `software-engineering/grain-and-facts` | The one-row-per-what decision, and what belongs in a fact. |
| `subskills/dimensions.md` | `software-engineering/dimensions` | Descriptive context, keys, and the flat-vs-snowflaked choice. |
| `subskills/slowly-changing-dimensions.md` | `software-engineering/slowly-changing-dimensions` | Preserving history as descriptive data changes, types one to four. |
| `subskills/star-versus-snowflake.md` | `software-engineering/star-versus-snowflake` | Join depth versus update cost, and when normalising dimensions is worth it. |
| `subskills/aggregates-and-summaries.md` | `software-engineering/aggregates-and-summaries` | Pre-computed rolls, their refresh windows, and their drift risk. |
| `subskills/columnar-and-sort-design.md` | `software-engineering/columnar-and-sort-design` | How columnar layout, sort order, and partitioning serve analytical scans. |
| `subskills/metrics-definition-layer.md` | `software-engineering/metrics-definition-layer` | One definition per metric, and the drift that follows from many. |
| `subskills/modeling-record.md` | `software-engineering/modeling-record` | The written record: grain, dimensions, change policy, and metric ownership. |

## Status and honest limits

A model encodes the business definitions of its facts and dimensions, and those definitions are negotiated rather than discovered — one team's revenue is another's bookings. Nothing here recommends a warehouse product, and a model whose grain is unstated produces numbers that reconcile only by accident.
