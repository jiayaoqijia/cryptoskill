---
name: keep-embedding-model-consistency
description: Use when query and document vectors may come from different models or versions. Pins the embedding model and dimension, and refuses to search an index built by a different one.
---

# Keep Embedding Model Consistency

Vectors from different models occupy different spaces; a query embedded with model B against an index built with model A returns noise that looks like results. The model, its version, and the vector dimension are one identity.

## Procedure

1. Pin the model by name and revision: `sentence-transformers/all-MiniLM-L6-v2@e8f8c211` — "all-MiniLM" alone is not a pin.
2. Record `model_id`, `dimension`, and `normalised` (true/false) in the index metadata at build time.
3. At query time, read the index metadata and assert the query encoder matches; abort if it does not.
4. Store the same three fields in the embedding cache key, so a model change does not reuse stale vectors.
5. When upgrading the model, re-embed the whole corpus — a partial upgrade is a two-space index.
6. Keep the old index serving until the new one is fully built and eval-passed, then switch atomically.
7. Enforce the dimension at the store level: a collection built for 384 dims rejects a 768-dim vector.
8. Normalise once, consistently; if you store L2-normalised vectors, the query must be normalised the same way.
9. Re-run retrieval metrics after any model change; a fresh model is a new system, not a patch.
10. Garbage-collect the old collection only after the eval and a rollback window pass.

11. Assert the dimension at insert time as well as at query time, so a mismatched write is rejected early.

## Pitfalls

- Upgrading the query encoder first, so every query is in the new space and every document in the old.
- Trusting a "same" model name that the upstream silently retrained, shifting the space under you.
- Mixing normalised and unnormalised vectors, so cosine similarity becomes meaningless.
- Reusing the embedding cache across a model change because the key was the text hash alone.
- Running half a corpus upgrade and serving a hybrid index where half the chunks never match a query.

- Two teams pinning the same model name at different revisions, building incompatible indexes.
- A hosted embedding endpoint that upgrades its model under a stable name without notice.

## Verification

    python3 check_model.py --index index/ --expect all-MiniLM-L6-v2@e8f8c211:384:true
    # passes when the index metadata matches the query encoder exactly and all vectors share one dimension

Report to the user: model id, dimension and normalisation of the index and the encoder, and the match or abort decision.
