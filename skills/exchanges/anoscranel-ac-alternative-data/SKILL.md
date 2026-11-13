---
name: ac-alternative-data
description: "Evaluating non-traditional datasets before they are used in a decision: provenance and vendor claims, point-in-time integrity and backfill leakage, survivorship and restatement in vendor history, coverage and representativeness, signal decay as a dataset becomes popular, licensing and permitted use, and the written data-vendor record. It evaluates datasets as evidence; it never recommends a strategy or predicts a return. Use when asking \"alternative data\", \"data vendor\", \"point-in-time\", \"backfill bias\", \"is this dataset any good\", \"signal decay\", \"panel data\", \"satellite data\", \"web scraping data\". Not for building the pipeline (ac-market-data-collection), not for testing a strategy on it (ac-backtest-integrity), not for prompt or model design (ac-prompt-engineer)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Alternative data

## Overview

Alternative data is any dataset that is not a standard market or financial-statement series: card transactions, satellite imagery, app usage, shipping records, job postings, web traffic. Its attraction is that it may contain information before it reaches prices; its difficulty is that establishing whether it does requires work that the vendor's marketing does not do.

This skill is about that work. The questions are unglamorous and decisive: where did the data come from, is the history point-in-time or reconstructed, does the coverage represent the universe being modelled, and what happens to the signal once the dataset is widely sold. A dataset that fails the provenance and point-in-time tests cannot be rescued by a good backtest, because the backtest will be measuring the reconstruction rather than the data.

Primary sources: <https://www.sec.gov/investor> and <https://www.nber.org/>.

## When to use

- When a new dataset is being considered for a decision process.
- When a vendor's historical performance claim is being evaluated.
- When a signal's decay after publication is being assessed.
- When licensing terms restrict how a dataset may be used or shared.

## When NOT to use

- For building the ingestion and storage pipeline (use ac-market-data-collection).
- For judging whether a strategy built on it is real (use ac-backtest-integrity).
- For prompt, model, or agent design (use ac-prompt-engineer).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/provenance-and-vendor-claims.md` | `investing/provenance-and-vendor-claims` | Where the data came from, and how to test a vendor's assertions. |
| `subskills/point-in-time-integrity.md` | `investing/point-in-time-integrity` | Backfill, restatement, and the difference between history and reconstruction. |
| `subskills/coverage-and-representativeness.md` | `investing/coverage-and-representativeness` | Who is in the panel, who is missing, and what that does to inference. |
| `subskills/signal-decay.md` | `investing/signal-decay` | What happens to an edge once the dataset is widely sold. |
| `subskills/licensing-and-permitted-use.md` | `investing/licensing-and-permitted-use` | Terms, redistribution, derived data, and the compliance constraint. |
| `subskills/data-cost-and-build.md` | `investing/data-cost-and-build` | Buy versus build, total cost, and the maintenance burden. |
| `subskills/data-vendor-record.md` | `investing/data-vendor-record` | The written record: source, tests passed, limits, and review dates. |

## Status and honest limits

Vendors are commercial counterparties, and their documentation is marketing as well as description; claims should be tested rather than accepted. The most common failures are invisible in a backtest because they flatter it: reconstructed history, coverage that matches the current index rather than the historical one, and survivorship in the panel. Nothing here certifies a dataset, and a dataset that has not been tested for point-in-time integrity has not been evaluated at all.
