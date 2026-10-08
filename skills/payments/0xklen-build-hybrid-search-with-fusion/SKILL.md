---
name: build-hybrid-search-with-fusion
description: Use when keyword and vector retrieval each miss a different half of the queries. Runs both and fuses the ranked lists with reciprocal rank fusion so exact tokens and paraphrase both surface.
---

# Build Hybrid Search with Fusion

Neither a vector index nor BM25 alone clears both exact identifiers and paraphrase. Run both and fuse their rankings with reciprocal rank fusion (RRF), which needs no score calibration between the two scorers.

## Procedure

1. Retrieve k=50 candidates from each retriever independently: BM25 over the chunk text, vectors over the embeddings.
2. Fuse with RRF: `score(d) = sum over retrievers of 1 / (60 + rank_of_d)`, where rank is 1-based.
3. Implement the constant 60 as the standard RRF k; it damps the weight of deep ranks so neither list dominates.
4. Deduplicate by chunk id before fusing — the same chunk from both lists must score once, not twice.
5. Sort by fused score, take top-n (n = 10-20) into the reranker or straight into the prompt.
6. Weight the lists only if one retriever is clearly weaker per class; keep the weights in config, not code.
7. Do not normalise raw cosine and BM25 scores to fuse them; the scales are unrelated and RRF deliberately avoids it.
8. Measure with recall@10 against the labelled set and compare against each retriever alone.
9. If RRF wins by less than the eval's noise floor, ship the single retriever and save the second index's cost.
10. Keep both indexes built from the same chunk set and rebuilt together, or the fusion joins mismatched ids.

11. Log the fused list and both source lists per query so a bad result can be traced to one retriever.

## Pitfalls

- Fusing a vector list of 10 with a keyword list of 500, so the keyword tail dominates every fused rank.
- Adding the two scores after min-max normalising them, which lets one retriever's outlier set the scale.
- Double-counting a chunk that appears in both lists, inflating its fused score above a genuine top hit.
- Rebuilding only one index after an ingest, so fusion returns ids that exist in one store and not the other.
- Treating RRF's 60 as a tunable knob and overfitting it to a 12-query eval.

- Fusing lists produced by different queries because the rewrite ran twice with different outputs.
- Applying the reranker before fusion, so the two retriever ranks no longer reflect their own scales.

## Verification

    python3 fuse.py --bm25 bm25.json --vec vec.json --k 60 | head -20
    grep -c . fused_top10.txt
    # passes when dedup by chunk id holds and recall@10 beats the better single retriever

Report to the user: recall@10 for BM25, vectors, and fused; the fused top-5 ids; and whether the second index earned its cost.
