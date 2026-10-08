---
name: tune-chunk-size-and-overlap
description: Use when chunk size is a guess and answers miss context that sits next door. Sweeps size and overlap against a labelled query set and picks the pair by measured retrieval score, not by feel.
---

# Tune Chunk Size and Overlap

Chunk size is a hyperparameter with a measurable optimum for your corpus and queries, and overlap is what stops an answer falling on a boundary. Neither should be a default copied from a blog post.

## Procedure

1. Freeze a labelled query set first (10-30 queries with their gold chunk ids) so every sweep is scored the same way.
2. Build a sweep grid: sizes `[128, 256, 512, 1024]` tokens, overlaps `[0, 0.1, 0.25, 0.5]` of size.
3. Render chunks for each cell to `runs/s{size}_o{overlap}/chunks.jsonl`, keeping document id and offsets.
4. Embed and index each cell into its own collection so runs never mix: `qdrant` collection `kb_s512_o128`.
5. Score each cell with recall@10 and MRR against the frozen set; write one row per cell to `runs/sweep.csv`.
6. Pick the cell with the best recall, breaking ties toward the smaller chunk (cheaper prompt, less dilution).
7. Raise overlap rather than size when the misses are boundary misses (the answer spans two adjacent sections).
8. Re-read the sweep: if a size wins only by a single query, it is noise — prefer the plateau, not the spike.
9. Fix the winner, re-index production once, and record the numbers in the ingest config.
10. Re-run the sweep only when the corpus type changes (docs to tickets, prose to code).

11. Hold the corpus and query set fixed during the sweep; a corpus edit mid-sweep invalidates every earlier cell.

## Pitfalls

- Tuning on the queries you built the eval from and reporting the in-sample best as real gain.
- Measuring only recall and ignoring that bigger chunks triple the tokens you paste into the prompt.
- Changing size and embedding model at once, so the score cannot be attributed to either.
- Leaving overlap at a round fraction of a size you also changed, mixing two variables.
- Assuming the best cell for prose holds for code, where boundaries are syntax, not paragraphs.
- Storing tuned values only in a notebook cell that nobody reruns.

- Running the sweep on one machine and serving under different memory limits, so the chosen size is unservable.
- Re-tuning on every ingest, so the chunker churns and citations stop resolving across versions.

## Verification

    sort -t, -k3 -rn runs/sweep.csv | head -3
    # passes when a single cell leads on recall@10 by more than the runner-up's standard error, and is written into config

Report to the user: the winning size and overlap, its recall@10 and MRR, the next-best cell, and the token cost per retrieved answer.
