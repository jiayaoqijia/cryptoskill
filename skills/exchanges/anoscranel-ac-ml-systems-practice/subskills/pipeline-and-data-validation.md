---
name: pipeline-and-data-validation
domain: software-engineering/pipeline-and-data-validation
trigger: "Validating data at the boundary before it enters training."
anti_trigger: "Not for feature maths, and not for dataset evaluation as research evidence."
scope: "Hygiene at the pipeline boundary: what enters training must be checked, not assumed."
status: seedling
---

# Pipeline and data validation

## Standard

Training data arrives through a pipeline, and every stage of that pipeline can corrupt silently: a half-written file, a schema change upstream, a join that duplicated rows, a timezone that shifted a timestamp by a day. Validation at the boundary means the pipeline asserts what it believes — counts, ranges, null rates, schema — and refuses or flags when the assertion breaks, instead of letting the model learn the corruption.

The validation that matters is the distributional kind, not just the structural. Schema checks catch the type that changed; they do not catch the column whose values quietly doubled when an upstream unit changed, or the category list that gained a token nobody told the features about. Both layers are required: structure first, then the distributional expectations with thresholds a human chose.

Primary sources: <https://ml-ops.org/> and <https://developers.google.com/machine-learning/guides/rules-of-ml>.

## Decision rules

- Validate at the boundary where data enters the pipeline, not at the trainer.
- Assert schema explicitly: types, required fields, enum membership.
- Assert distributional expectations with thresholds: row counts in a range, null rates under limits, numeric ranges, category cardinality.
- Quarantine failures rather than silently dropping rows; the dropped rows are usually the story.
- Record the validation version with the data version so a training run names its checks.
- Fail loudly in training pipelines; in serving, degrade by policy, never by crash mid-request.

## Procedure

1. List the structural invariants of each input source.
2. List distributional expectations per column with thresholds and a stated rationale.
3. Implement checks at the ingestion boundary; quarantine failed batches.
4. Route quarantines to a human path with the failing assertion named.
5. Record the check set version alongside each dataset version.
6. Revisit thresholds when legitimate distribution shifts arrive; revise, never delete.

## Anti-patterns

- Training on whatever the pipeline produced because last month it worked.
- Dropping failed rows silently; the model trains on the easy cases only.
- Asserting only schema; the unit change and the cardinality creep pass.
- Deleting a check that fires, rather than deciding whether the data or the check is wrong.
- Validating at the trainer, where the corruption has already been joined away.

## Done checklist

- [ ] Structural checks implemented at the boundary.
- [ ] Distributional expectations with named thresholds.
- [ ] Quarantine path with named failing assertion.
- [ ] Check set versioned with the data version.
- [ ] Trainer fails loudly; serving degrades by policy.
- [ ] Thresholds revised on legitimate shift, with dates.

## Sources

- MLOps practices overview: <https://ml-ops.org/>
- Google rules of ML, pipeline hygiene: <https://developers.google.com/machine-learning/guides/rules-of-ml>
- Inference and training separation: <https://developers.google.com/machine-learning/crash-course>
