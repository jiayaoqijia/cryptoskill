---
name: calibrate-a-retrieval-score-cutoff
description: Use when a fixed similarity threshold lets nonsense queries return confident chunks. Chooses the cutoff from labelled score distributions instead of a guessed constant.
---

# Calibrate a Retrieval Score Cutoff

A threshold like 0.7 means nothing without knowing the score distribution of good and bad matches for your model and corpus. Calibrate it from labels so the cutoff separates answers from noise.

## Procedure

1. Collect scores for the gold chunks (top gold score per query) and for the top non-gold chunk per query, on the labelled set.
2. Plot or tabulate both distributions as histograms; the cutoff lives in the overlapping valley, not at a round number.
3. Choose the cutoff to trade precision against coverage for the use case: support bots favour recall, compliance answers favour precision.
4. Set two thresholds where useful: below `T_low` abstain, between the two answer with a hedge, above `T_high` answer plainly.
5. Validate: at the chosen value, measure how many answerable queries fall below the cutoff (lost recall) and how many off-corpus queries score above it (false confidence).
6. Recalibrate after any embedding-model change (`keep-embedding-model-consistency`) — the score scale shifts.
7. Keep the threshold in config next to the model id, so the two move together.
8. Apply the cutoff to the reranker score when you have one, since it is better calibrated than raw cosine.
9. Log the top score for every served query so the distribution keeps re-estimating from live traffic.
10. Re-check the cutoff quarterly; drift in the corpus moves the distributions.

11. Version the cutoff with the index so a rollback restores the matching threshold.

## Pitfalls

- Copying "0.7 cosine" from a tutorial for a model whose scores cluster at 0.4.
- Using one threshold for both the retrieval score and the reranker score, which are different scales.
- Calibrating on the eval queries and then reporting the same queries as the validation.
- Setting the cutoff so high that the corpus's own correct answers fall below it.
- Forgetting that cosine and inner-product scores are not comparable after a normalisation change.
- Treating the threshold as universal across tenants whose corpora have different score spreads.

- A threshold tuned on one tenant's corpus and applied to every tenant with a different score spread.
- Recalibrating on a query set that includes the very off-corpus probes used to validate the cutoff.

## Verification

    python3 calibrate.py --scores evals/scores.jsonl --gold evals/retrieval.jsonl
    # passes when the chosen cutoff keeps off-corpus queries below it and loses <5% of answerable golds

Report to the user: the chosen cutoff(s), the score ranges of gold vs non-gold, and the lost recall and false-confidence rates at that value.
