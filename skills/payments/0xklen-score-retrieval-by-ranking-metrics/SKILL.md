---
name: score-retrieval-by-ranking-metrics
description: Use when a single recall number hides whether the good chunk ranks first or tenth. Computes recall@k, MRR and nDCG against labelled queries so ranking quality, not just presence, is measured.
---

# Score Retrieval by Ranking Metrics

"Did the right chunk come back" is half the question; "where did it rank" decides whether it survives the top-k cut and reaches the prompt. Rank metrics make that visible.

## Procedure

1. Freeze the labelled set as `evals/retrieval.jsonl`: one object per query with `q` and `gold_ids` (ranks matter, so order them best-first).
2. Record the raw ranked ids your retriever returns for each query, at k=10 or deeper.
3. Compute recall@k = (queries with at least one gold id in top k) / queries.
4. Compute MRR = mean of `1 / rank_of_first_gold`; a gold at rank 1 scores 1.0, rank 4 scores 0.25.
5. Compute nDCG@k with graded gains when a query has several gold chunks; binary gains are fine when it has one.
6. Report all three at the k you actually serve; recall@10 is irrelevant if you cut to top-3.
7. Slice the report by query class — the mean hides a class at 0.2 dragged up by another at 0.9.
8. Read MRR for failures that recall hides: gold present but ranked 9th, so a tighter k loses it.
9. Keep every metric run appended to `evals/history.jsonl` with a git hash, so a regression is attributable.
10. Set the ship bar before the change: e.g. recall@5 >= 0.80 and MRR >= 0.60 on the frozen set.

11. Bootstrap a confidence interval over queries; report a gain only when the interval excludes zero.

## Pitfalls

- Reporting only recall@10 and serving top-3, so the metric measures a system you do not run.
- Averaging metrics across queries of wildly different difficulty without showing the spread.
- Letting gold ids be a set, so MRR's "first gold" is undefined and the number becomes arbitrary.
- Re-labelling gold chunks after seeing what the retriever returned — that is fitting the answer.
- Comparing an nDCG computed at k=10 with a baseline computed at k=5.
- Treating a 0.02 improvement as real when the eval has 15 queries and no confidence interval.

- Computing statistics on 10 queries and treating a 3-point move as a regression.
- Letting different queries contribute different numbers of gold ids, so nDCG is dominated by the multi-gold ones.

## Verification

    python3 metrics.py --preds runs/current.jsonl --gold evals/retrieval.jsonl --k 5
    # passes when recall@5, MRR and nDCG@5 are all printed, per class, against the frozen set

Report to the user: recall@k, MRR and nDCG@k at the served k, split by query class, with the worst class named.
