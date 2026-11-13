---
name: offline-metrics
domain: software-engineering/offline-metrics
trigger: "Measuring ranking quality without users, and knowing what that promises."
anti_trigger: "Not for online experiment design, and not for feature engineering."
scope: "Precision and NDCG as arithmetic; what offline wins do and do not promise."
status: seedling
---

# Offline metrics

## Standard

Offline ranking metrics compare a ranked list against a held-out ground truth, and each encodes a belief about what ranking behaviour matters. Precision at K rewards getting relevant items into the first K positions. Recall at K rewards coverage of the relevant set. Mean reciprocal rank cares only about the first hit. NDCG at K weighs each relevant item by the inverse of its position, rewarding putting the best items first, and tolerating an excellent lower-ranked item less. Choosing the metric is choosing the failure you care about; computing several without choosing is how systems optimize an aggregate that nobody wanted.

The offline metric's honest claim: it measures the model against a frozen past. The held-out set is what a sample of users did in a period already served, under a ranking already run — so offline improvement says the new ranking better agrees with that past than the old one did. It is a fast, cheap, measurable proxy; it is not a forecast, and it is weakest exactly when the change is largest, because the biggest changes alter the conditions that produced the evaluation set.

Primary sources: <https://en.wikipedia.org/wiki/Recommender_system> and <https://en.wikipedia.org/wiki/Precision_and_recall>.

## Decision rules

- Name the primary metric per surface and decision type; the others are diagnostics.
- The held-out set is defined by a time split, frozen by a cut date, never sampled randomly from a pool.
- NDCG's graded-relevance definition is written down; the gain formula and the ideal-list construction are choices, not defaults.
- Every metric report carries the set size, window, and model versions compared.
- Offline win with online loss is a discrepancy finding, recorded with a hypothesis; an implicit online-only validation loop never overrides offline again.
- Per-segment breakdowns accompany every headline; an aggregate win on a thousand-item head can hide a loss everywhere else.

## Procedure

1. Time-split the interactions; freeze the held-out window; record the cut.
2. Define relevancy truthfully: implicit signal as truth or graded by interaction depth; write the gain mapping.
3. Compute the metric set per surface on the frozen split; record sizes and windows.
4. Compare candidate models with the primary metric; carry cut metrics as diagnostics.
5. Review per-segment, especially the tail segments the aggregate hides.
6. Log discrepancies with online outcomes; each is a note on the metric, not on the experiment.

## Anti-patterns

- Random sampled holdouts in a time-ordered domain; the future is never randomly mixed.
- Averaging NDCG across surfaces with different list lengths without noting the incomparability.
- Reporting one aggregate number with no cut breakdowns; the narrow win disguised as general improvement.
- Choosing the metric after seeing which one the new model wins.
- Treating an offline regression as dispositive when the online experiment disagreed.

## Done checklist

- [ ] Primary metric named and its rationale recorded.
- [ ] Held-out set time-split and frozen.
- [ ] Gain formula and ideal list defined for NDCG.
- [ ] Sizes, windows, versions in every report.
- [ ] Per-segment breakdowns accompany headlines.
- [ ] Online discrepancies logged with hypotheses.

## Sources

- Recommender overview: <https://en.wikipedia.org/wiki/Recommender_system>
- Precision and recall: <https://en.wikipedia.org/wiki/Precision_and_recall>
- Learning to rank: <https://en.wikipedia.org/wiki/Learning_to_rank>
