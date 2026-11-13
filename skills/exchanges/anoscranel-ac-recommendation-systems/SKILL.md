---
name: ac-recommendation-systems
description: "Building systems that rank items for users: implicit versus explicit feedback, candidate generation and its recall, cold start for new users and items, learning-to-rank with the loss chosen for the decision, position and feedback bias corrected counterfactually, ranking metrics from precision to NDCG, final filtering for diversity and fatigue, exploration, and the recommender record. It explains how recommenders are built and evaluated; it never promises engagement gains. Use when asking \"recommendation system\", \"collaborative filtering\", \"implicit feedback\", \"candidate generation\", \"cold start\", \"learning to rank\", \"position bias\", \"NDCG\", \"diversify recommendations\", \"why do recommendations all look the same\". Not for vector retrieval mechanics (ac-retrieval-and-vector-systems), not for online experiment measurement (ac-online-experiments), not for feed-level data pipelines (ac-data-pipeline-orchestration)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Recommendation systems

## Overview

A recommender ranks items for a user, and the difficulty is that the system only ever sees the results of its own past rankings. Every click is contingent on what was shown, in which order, and what was never given a chance — so the raw interaction log is not data about preference; it is data about the ranking the system already served. Everything in the craft follows from that one uncomfortable fact.

The second defining fact is the two-stage shape. Ranking millions of items for every user, every time, is computationally unreachable, so real systems generate a candidate set cheaply from a union of signals — collaborative neighbourhoods, content similarity, popularity, co-occurrence — and then apply an expensive learned model to score only those candidates. The final ranking is then filtered for business rules, diversity, and fatigue before display. Each stage has its own failure mode, and a recommender that only optimizes the scorer is optimizing the middle of three problems.

Primary sources: <https://en.wikipedia.org/wiki/Recommender_system> and <https://en.wikipedia.org/wiki/Collaborative_filtering>.

## When to use

- When building a system that ranks items, feeds, or matches for users.
- When choosing between collaborative, content-based, and hybrid signals.
- When designing evaluation or offline metrics for ranking quality.
- When recommendation quality degrades, narrows, or loops.

## When NOT to use

- For vector index and retrieval mechanics (use ac-retrieval-and-vector-systems).
- For A/B experiment design and peeking discipline (use ac-online-experiments).
- For backfill and ingestion pipelines (use ac-data-pipeline-orchestration).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/feedback-signals.md` | `software-engineering/feedback-signals` | Implicit and explicit data, and what each honestly measures. |
| `subskills/candidate-generation.md` | `software-engineering/candidate-generation` | Cheap recall sources whose union is the judge of coverage. |
| `subskills/cold-start.md` | `software-engineering/cold-start` | The bootstrap sequence for new users and new items. |
| `subskills/learning-to-rank.md` | `software-engineering/learning-to-rank` | The scorer, its features, and its loss tied to the decision. |
| `subskills/bias-and-correction.md` | `software-engineering/bias-and-correction` | Position, popularity, and feedback loops; counterfactual remedies. |
| `subskills/offline-metrics.md` | `software-engineering/offline-metrics` | Precision and NDCG as arithmetic; what offline wins do and do not promise. |
| `subskills/filtering-and-diversity.md` | `software-engineering/filtering-and-diversity` | Final ranking: coverage, repetition, and fatigue as explicit rules. |
| `subskills/exploration-and-coverage.md` | `software-engineering/exploration-and-coverage` | Exploration as part of design, not an accident of randomness. |
| `subskills/recommender-record.md` | `software-engineering/recommender-record` | The record: signals, stages, rules, and their reasons, kept current. |

## Status and honest limits

Offline metrics are proxies; the interaction log is biased by what was already shown; offline wins at the proxy may or may not carry to the product — measurement belongs to the experiment skill, and the interface between them is a hypothesis. Relevance itself is not a fixed target; a recommender that is genuinely useful for one user in one context may be noise in another, and the record's job is to keep that gap visible rather than smoothed away.
