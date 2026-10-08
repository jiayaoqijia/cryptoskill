---
name: rerank-candidates-before-generation
description: Use when retrieval returns the right chunk but ranked below weaker matches. Adds a cross-encoder reranker over the candidate list and cuts to the top-k that actually enters the prompt.
---

# Rerank Candidates Before Generation

First-stage retrieval is fast and coarse; a cross-encoder scores query and chunk together and is far more accurate, but too slow for the whole corpus. Retrieve wide, rerank narrow, then prompt with few.

## Procedure

1. Retrieve wide: 50-100 candidates from hybrid or vector search, cheaply.
2. Score each candidate with a cross-encoder (`cross-encoder/ms-marco-MiniLM-L-6-v2` via `sentence-transformers`) or a hosted reranker.
3. Sort by rerank score, not by the retrieval score; the retrieval score only decided who got ranked.
4. Cut to the top-k the prompt can afford — usually 3-8 chunks; more context is often worse, not better.
5. Set a rerank-score floor and drop candidates below it so an off-topic query returns few, or zero, chunks.
6. Keep the truncated list ordered so the most relevant chunk is first; models weight early context more.
7. Measure the delta: recall@10 stays the same by construction, but nDCG@5 and answer faithfulness should rise.
8. Cache rerank scores per (query, chunk) pair within a session; repeated questions are common.
9. Batch the cross-encoder — scoring 60 chunks one at a time is minutes, batched it is milliseconds.
10. Re-evaluate the top-k once when the reranker changes; the old k was tuned to the old ordering.

11. Fall back to the fused ordering when the reranker times out, so a slow model degrades instead of failing.

## Pitfalls

- Reranking with a bi-encoder, which is the first-stage scorer again and adds nothing but latency.
- Passing all 100 reranked chunks into the prompt and calling the win a reranker win.
- Reranking on the GPU and serving on CPU, so production latency is a surprise.
- Forgetting the query used at rerank time differs from the one embedded (rewriting one, not the other).
- Dropping the score floor so a nonsense query still yields five confident-looking chunks.

- Reranking only the top-10 candidates, which cannot fix a gold chunk the first stage ranked 30th.
- Changing the candidate count and the top-k together, so the nDCG delta cannot be attributed.

## Verification

    python3 eval.py --retriever vec --rerank --k 5
    # passes when nDCG@5 rises versus the un-reranked baseline and p95 latency stays inside budget

Report to the user: candidate count, top-k kept, nDCG@5 before and after, and the added p95 latency.
