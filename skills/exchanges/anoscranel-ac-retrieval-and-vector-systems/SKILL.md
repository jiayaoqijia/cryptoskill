---
name: ac-retrieval-and-vector-systems
description: "Building the retrieval layer behind search and grounded answers: chunking strategy and what it costs, embedding models and their dimensional and multilingual trade-offs, vector index types and the recall-latency curve, hybrid search and reranking, freshness and the stale index problem, relevance evaluation with golden sets, and the written retrieval record. It explains how the index is built and measured; it never recommends a vendor and never promises an accuracy. Use when asking \"vector database\", \"embedding model\", \"chunking strategy\", \"reranking\", \"hybrid search\", \"recall versus latency\", \"stale index\", \"retrieval quality\", \"why does search return nothing useful\", \"grounded answers\". Not for prompt design and RAG prompting (ac-prompt-engineer), not for evaluating a dataset's provenance (ac-alternative-data), not for batch pipeline scheduling (ac-market-data-collection)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Retrieval and vector systems

## Overview

Retrieval is a system with its own failure modes, and most of them are not model failures. A chunk that splits a sentence in half produces an embedding that means neither half; an index built last week returns last week's answer to today's question; a dense-only search misses the exact identifier that a keyword search would have found in one step. Each of those is a design decision, and each is measurable.

This skill covers that layer: how documents are split and why the split matters, what an embedding model's dimensions and training data decide, how index types trade recall against latency, where hybrid search and reranking add value, how freshness is maintained, and how relevance is evaluated against a fixed set rather than by impression. Prompting and evaluation of a model's output belong to another skill.

Primary sources: <https://nlp.stanford.edu/IR-book/> and <https://www.nist.gov/>.

## When to use

- When building or reviewing a retrieval index for search or grounded answers.
- When retrieval quality is poor and the cause is unknown.
- When index freshness or rebuild cost becomes a constraint.
- When choosing between dense, sparse, and hybrid retrieval.

## When NOT to use

- For prompt design and RAG prompt construction (use ac-prompt-engineer).
- For evaluating an external dataset's provenance and bias (use ac-alternative-data).
- For batch ingestion pipeline scheduling (use ac-market-data-collection).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/chunking-strategy.md` | `software-engineering/chunking-strategy` | Boundaries, overlap, and the size that matches the question being asked. |
| `subskills/embedding-models.md` | `software-engineering/embedding-models` | Dimensions, training domain, multilingual coverage, and re-embedding cost. |
| `subskills/vector-index-types.md` | `software-engineering/vector-index-types` | Flat, IVF, HNSW, and the recall-latency-memory trade each makes. |
| `subskills/hybrid-search-and-reranking.md` | `software-engineering/hybrid-search-and-reranking` | Sparse plus dense fusion, and the second stage that fixes ranking. |
| `subskills/freshness-and-rebuilds.md` | `software-engineering/freshness-and-rebuilds` | Incremental updates, tombstones, and the cost of a full re-embed. |
| `subskills/relevance-evaluation.md` | `software-engineering/relevance-evaluation` | Golden sets, recall at k, and measuring a change honestly. |
| `subskills/retrieval-record.md` | `software-engineering/retrieval-record` | The written record: chunking, model, index, freshness, and metrics. |

## Status and honest limits

Embedding models and vector indexes change quickly, and a specific product's behaviour may differ from the general trade-offs described here. Relevance metrics measure agreement with a labelled set, which is a proxy for usefulness rather than a measurement of it, and a golden set that was built from one team's judgement inherits that judgement. Nothing here recommends a vendor, and a retrieval system that has not been evaluated against a fixed set has not been evaluated at all.
