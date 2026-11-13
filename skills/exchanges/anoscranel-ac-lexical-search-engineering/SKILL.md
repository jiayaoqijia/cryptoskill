---
name: ac-lexical-search-engineering
description: "Building token-based search: the analysis chain that turns text into indexable terms, the inverted index as the structure every term-based system shares, query construction from boolean to ranking clauses, field weighting and per-field analyzers, typo tolerance and fuzzy matching with their cost, facets and aggregations that must not scan the corpus, autocomplete and suggest built on prefix structures, and the written search record. It explains how term-based search behaves and is tuned; it never recommends a search product. Use when asking \"text analysis\", \"analyzer chain\", \"inverted index\", \"BM25\", \"query construction\", \"field boost\", \"fuzzy matching cost\", \"facets and aggregation\", \"autocomplete suggest\", \"why does search not find exact matches\". Not for vector and embedding retrieval (ac-retrieval-and-vector-systems), not for database index internals (ac-database-engine-internals), not for ranking systems over users and items (ac-recommendation-systems)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Lexical search engineering

## Overview

Term-based search rests on one structure — the inverted index, mapping terms to the documents containing them — and one transformation: the analysis chain that decides what counts as a term. Almost every search behaviour users notice, from exact-match misses to plural mismatches, from autocomplete speed to facet counts, traces back to those two decisions. The craft is making the analysis chain a deliberate, recorded choice rather than a library default, and building the structures each feature actually needs rather than scanning the corpus at query time.

The boundary with vector retrieval is clean: embeddings match meaning and miss exact strings; lexical matches terms and misses paraphrase. Most real systems run both, but their engineering is separate — the hybrid combination is owned by the retrieval skill. This skill owns the token side: an analyzer is chosen per field at index time, queries are analyzed too, and the same text must produce the same terms on both sides or search silently fails to find its own documents.

Primary sources: <https://elastic.co/guide/en/elasticsearch/reference/current/analysis.html> and <https://lucene.apache.org/core/corenews.html>.

## When to use

- When building or tuning term-based search over any corpus.
- When exact matches fail, plurals split, or queries and documents analyze differently.
- When designing facets, autocomplete, or type-ahead suggestions.
- When choosing per-field analyzers and field weighting.

## When NOT to use

- For vector, embedding, and hybrid retrieval (use ac-retrieval-and-vector-systems).
- For database page structures and storage engines (use ac-database-engine-internals).
- For recommending items to users by preference (use ac-recommendation-systems).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/analysis-chain.md` | `software-engineering/analysis-chain` | Tokenizers, normalization, stemming, and the analyzer per field. |
| `subskills/inverted-index.md` | `software-engineering/inverted-index` | The structure: postings, skipping, compression, and what it costs. |
| `subskills/query-construction.md` | `software-engineering/query-construction` | Boolean clauses, phrase and span queries, and how analysis rewrites queries. |
| `subskills/scoring-and-bm25.md` | `software-engineering/scoring-and-bm25` | Term frequency, inverse document frequency, field length, and the knobs. |
| `subskills/fuzzy-and-typos.md` | `software-engineering/fuzzy-and-typos` | Edit distance matching, its indexing cost, and cheaper alternatives. |
| `subskills/facets-and-aggregations.md` | `software-engineering/facets-and-aggregations` | Structured counts without corpus scans, and doc values as the design. |
| `subskills/autocomplete-and-suggest.md` | `software-engineering/autocomplete-and-suggest` | Prefix structures, completion suggesters, and type-ahead latency budgets. |
| `subskills/search-record.md` | `software-engineering/search-record` | The record: analyzers, schemas, query rewrites, and tuned mappings. |

## Status and honest limits

Relevance tuning is empirical and corpus-specific: the same analyzer decision helps one catalogue and hurts another, and no offline number settles it without user queries. The skill records the decisions and their reasons so tuning is repeatable; it promises no ranking figure. Search product internals differ and change, so the leaves hold to the shared physics — analysis, posting lists, scoring — that every term-based system shares.
