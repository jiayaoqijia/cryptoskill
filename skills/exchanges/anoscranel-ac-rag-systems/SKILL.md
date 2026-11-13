---
name: ac-rag-systems
description: 'Building the whole retrieval-augmented answering loop as one system: the query transform stage before retrieval, multi-hop decomposition when one query cannot reach the answer, chunk-level citation so every claim traces to a source, grounding verification that catches unsupported answers, refusal behaviour when the corpus is silent, and the written RAG record. It explains how the loop components compose; it never recommends an embedding model and never promises an accuracy. Use when asking "RAG", "retrieval augmented generation", "query rewriting", "multi-hop retrieval", "citation extraction", "grounding check", "hallucination guard", "answer verification", "corpus is silent", "RAG evaluation", "RAG pipeline design". Not for vector index and hybrid search mechanics (ac-retrieval-and-vector-systems), not for the grounding prompt itself (ac-prompt-engineer), not for model evaluation suites (ac-model-evaluation).'
license: MIT
metadata:
  domain: prompt-engineering
status: seedling
---

# RAG systems

## Overview

Retrieval-augmented generation answers questions from a corpus rather than from a model's parameters alone: retrieve passages, generate an answer over them, and cite where each claim came from. The original formulation in the research literature pairs a retriever with a generator; the production system built on it is a loop with more stages than that pair suggests — the query as asked is rarely the query as searched, the retrieval as returned is rarely everything the answer needs, and the answer as generated is not always the answer as supported.

This skill owns the composition: the stages between the user's question and a citable, verified answer. The index mechanics — chunking, embedding choice, hybrid search, reranking — belong to ac-retrieval-and-vector-systems; the prompt that instructs the model to answer only from retrieved text belongs to ac-prompt-engineer. What this skill adds is what neither of those owns: transforming the query before it reaches the index, decomposing questions that need more than one retrieval, binding every generated claim to a retrieved passage, verifying the answer after generation, and refusing cleanly when the corpus does not contain the answer.

Primary sources: <https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview> and <https://arxiv.org/abs/2005.11401>.

## When to use

- When designing or debugging an end-to-end retrieval-augmented answering system.
- When answers must cite their sources and the citations must be trustworthy.
- When questions arrive in forms the index cannot serve directly.
- When the system must refuse rather than confabulate when the corpus is silent.

## When NOT to use

- For chunking, embedding choice, hybrid search, and reranking mechanics (use ac-retrieval-and-vector-systems).
- For the grounded-answer prompt itself (use ac-prompt-engineer).
- For model evaluation suites and benchmark design (use ac-model-evaluation).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/query-transforms.md` | `prompt-engineering/query-transforms` | Rewriting the question into what the index should be asked. |
| `subskills/multi-hop-decomposition.md` | `prompt-engineering/multi-hop-decomposition` | Splitting questions whose answer needs more than one retrieval. |
| `subskills/citation-binding.md` | `prompt-engineering/citation-binding` | Binding each generated claim to the passage that supports it. |
| `subskills/grounding-verification.md` | `prompt-engineering/grounding-verification` | Checking the answer against retrieved text after generation. |
| `subskills/refusal-behaviour.md` | `prompt-engineering/refusal-behaviour` | Answering honestly when the corpus does not contain the answer. |
| `subskills/loop-composition.md` | `prompt-engineering/loop-composition` | Ordering the stages and choosing what each may depend on. |
| `subskills/rag-record.md` | `prompt-engineering/rag-record` | The written record: stage design, failure taxonomy, measured failures. |

## Status and honest limits

A RAG system inherits the corpus's gaps and the retriever's blind spots; verification catches unsupported claims but cannot make a silent corpus speak. Every stage added in the name of quality adds latency and a new failure mode, and the record exists so the trade is deliberate. Nothing here recommends an embedding model, a vector store, or a framework, and retrieval quality itself — recall, ranking, reranking judgment — is owned by the retrieval skill, not this one.
