---
name: features-and-leakage
domain: software-engineering/features-and-leakage
trigger: "Engineering features without smuggling the answer or the future into training."
anti_trigger: "Not for model architecture, and not for dataset provenance."
scope: "Building features that do not smuggle the answer or the future into training."
status: seedling
---

# Features and leakage

## Standard

A leak is any information in training that will not be available at prediction time: the label itself, a field derived from the label, an aggregate computed over a window that includes the future, or a proxy column that encodes the outcome. Leaks make offline evaluation glow and production disappoint, because the evaluation measured recall of the hidden field rather than the learned signal.

The tests are temporal and procedural. Temporal: every feature at time T must be computable from data that existed before T — no window, fill, or aggregate that reaches across the split boundary into the validation period. Procedural: every feature must be implemented once, in the pipeline both training and serving call, so there is no second implementation whose small drift is itself a leak of a different kind.

Primary sources: <https://developers.google.com/machine-learning/guides/rules-of-ml> and <https://en.wikipedia.org/wiki/Training,_validation,_and_test_data_sets>.

## Decision rules

- For each feature, state what real-world data it uses and when that data exists relative to prediction time.
- Lags and windows must be computed on event time, never ingestion order.
- Reject any feature whose provenance traces to the label, including rank, index, or ID fields that correlate by construction.
- Compute features in the one shared implementation; forbid divergent training-only and serving-only copies.
- Re-derive aggregates after every split change; a shift in the boundary silently redraws every window.
- For any suspiciously strong feature, attempt to explain the mechanism; unexplainable strength is a leak until proven otherwise.

## Procedure

1. Write each feature's origin sentence: source, event time, derivation.
2. Check each origin for label provenance and future-visibility.
3. Verify windows and lags against the split boundary.
4. Confirm single-implementation by tracing the pipeline and the serving path to the same code.
5. Investigate the top features by importance for unexplainable strength.
6. Record the leak audit with the feature set version.

## Anti-patterns

- Features derived from the outcome: days-since-label, post-outcome aggregates, completion flags.
- Aggregates whose window closes after the split boundary.
- Duplicated feature code paths that drift between training and serving.
- Keeping a magic feature because it lifts the offline metric.
- Assuming IDs and free-text keys are inert; they often encode the outcome.

## Done checklist

- [ ] Origin sentence written per feature.
- [ ] Label provenance excluded per feature.
- [ ] Windows verified against event time and the split.
- [ ] Single implementation confirmed.
- [ ] Strong features investigated for mechanism.
- [ ] Leak audit recorded with the feature version.

## Sources

- Google rules of ML: <https://developers.google.com/machine-learning/guides/rules-of-ml>
- Training, validation, and test data sets: <https://en.wikipedia.org/wiki/Training,_validation,_and_test_data_sets>
- MLOps practice overview: <https://ml-ops.org/>
