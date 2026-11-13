---
name: splits-and-evaluation
domain: software-engineering/splits-and-evaluation
trigger: "Splitting data so the evaluation predicts production behaviour."
anti_trigger: "Not for tuning the model, and not for statistical review pooling."
scope: "Splitting data so the evaluation predicts production, not the past."
status: seedling
---

# Splits and evaluation

## Standard

The split architecture is the experiment's honesty, and the wrong split does not produce a wrong number — it produces a right number about the wrong question. Random splits where records share identity leak across the boundary: two rows from one user in train and validation let the model recognise the person, not the pattern. Time splits where training data sits after validation data answer a time-travel question.

The default answer for temporal data is a chronological split: train on the earlier period, validate on the next, test on the latest, and freeze the test set so it is opened once. For grouped data, split by group — user, account, device — so no identity appears on both sides. Layered evaluation adds a serving-realism check: evaluate the way the model will be used, including latency and the features that will actually be present, not the idealised form of the same computations.

Primary sources: <https://en.wikipedia.org/wiki/Training,_validation,_and_test_data_sets> and <https://scikit-learn.org/stable/modules/cross_validation.html>.

## Decision rules

- Choose split type from the data's structure: temporal for time series, grouped by identity, random only for truly independent records.
- Never mix identities across train and validation; group boundaries are hard boundaries.
- For temporal data, train strictly before validation, validation before test.
- Freeze the test set and open it once; a reopened test set is a second validation set.
- Pick metrics before results: the metric is chosen for the decision it feeds, thresholds included.
- Evaluate streaming or batch serving the way it will run, not on idealised inputs.

## Procedure

1. Classify the data: temporal, grouped, or independent.
2. Construct the split with hard boundaries — time or group, applied before any feature derivation.
3. Verify no overlap: IDs and timestamps on one side only.
4. Pre-register the metric, its threshold, and the decision it feeds.
5. Fit on train, tune on validation, and finish before touching test.
6. Open test once; report and stop; a second look is a new experiment needing a new set.

## Anti-patterns

- Random shuffling of time-correlated rows, then wondering why offline is golden and live is poor.
- A test set that has been used for model selection; its score is now a fit statistic.
- Splitting before deduplication, letting the same person argue on both sides.
- Metric chosen after seeing scores, picking the most favourable one.
- Tuning hyperparameters directly against the test set.

## Done checklist

- [ ] Split type matches data structure.
- [ ] Hard boundaries verified — no ID or time overlap.
- [ ] Test set frozen and opened once.
- [ ] Metric and threshold pre-registered.
- [ ] Evaluation matches serving conditions, including latency and feature presence.
- [ ] Every additional evaluation named as a new experiment.

## Sources

- Train, validation, and test sets: <https://en.wikipedia.org/wiki/Training,_validation,_and_test_data_sets>
- Cross-validation pitfalls and grouping: <https://scikit-learn.org/stable/modules/cross_validation.html>
- Google rules of ML on metrics: <https://developers.google.com/machine-learning/guides/rules-of-ml>
