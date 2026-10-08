---
name: compare-vector-and-keyword-retrieval
description: Use when deciding between embeddings and keyword search for a corpus. Runs both on the same labelled queries and picks per query class by measured recall, not by preference.
---

# Compare Vector and Keyword Retrieval

Embeddings and BM25 fail in opposite ways: vectors miss exact identifiers and rare tokens, keyword search misses paraphrase. Decide with a head-to-head measurement on your own queries, and expect the answer to be "both, for different classes".

## Procedure

1. Split the labelled queries into classes: exact-token (`error TS2345`, `ERC20`, a SKU) vs paraphrase ("how do I cancel").
2. Index once for BM25 (`rank_bm25` or `Tantivy`) and once for vectors on identical chunk sets, so only the scorer differs.
3. For each query run both retrievers at k=10 and record whether the gold chunk is present.
4. Tabulate recall per class, not overall: keyword usually wins exact-token, vectors win paraphrase.
5. Inspect keyword false-negatives: a paraphrase miss is expected; an exact-token miss means the tokenizer split your identifier (`TS-2345`) — fix the analyzer.
6. Inspect vector false-negatives: a rare identifier embedded into a generic region is the classic miss — a keyword path fixes it.
7. Note queries where both fail: the chunk likely does not exist, which no retriever can fix.
8. If classes split cleanly, adopt hybrid search (`build-hybrid-search-with-fusion`) instead of picking one loser.
9. Keep the per-class table as the regression baseline for any retriever change.
10. Report the decision as per-class recall, never as "vectors are better".

11. Re-run the comparison after any analyzer or model change; tokenizer edits move keyword recall without touching vectors.

## Pitfalls

- Comparing on aggregate recall so the exact-token failures hide inside the paraphrase wins.
- Using a different chunk set for each retriever, so the comparison tests the corpus, not the scorer.
- Judging BM25 with its default analyzer when your corpus is full of hyphenated ids.
- Declaring embeddings superior after testing only natural-language questions.
- Ignoring latency: a reranker or vector search that is 200 ms slower may not be worth 2 points of recall.

- Testing vectors with a query rewriter enabled and keyword without it, giving one side an unearned advantage.
- Concluding from a corpus whose identifiers are rare, then generalising to a corpus of prose questions.

## Verification

    python3 compare.py --queries q.jsonl --classes exact,paraphrase
    # passes when the table shows per-class recall for both retrievers and a stated routing decision

Report to the user: recall per class for each retriever, the worst query per retriever, and the adoption decision with its reasoning.
