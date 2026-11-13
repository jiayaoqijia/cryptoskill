---
name: train-serve-skew
domain: software-engineering/train-serve-skew
trigger: "Hunting the bug class where serving computes features differently than training."
anti_trigger: "Not for feature design, and not for data drift."
scope: "The bug class where serving computes features differently than training did."
status: seedling
---

# Train-serve skew

## Standard

Skew is a divergence between the feature the model learned and the feature it is being given. Training builds features from a batch pipeline over historical data; serving must produce the same features per request, in milliseconds, from live sources. The two implementations can drift silently — different null handling, different rounding, different normalisation statistics, different category defaults — and each divergence quietly corrupts every prediction made.

Skew is a distinct failure class from drift: the world is unchanged, the pipeline just lies differently at the two ends. A model can be correct and its serving path wrong, and metrics computed on the serving outputs will blame the model. The cures are structural: compute features once in shared code, log the features actually used at serving, and compare serving features against re-computed training features on the same inputs to detect divergence.

Primary sources: <https://developers.google.com/machine-learning/guides/rules-of-ml> and <https://ml-ops.org/>.

## Decision rules

- One feature implementation shared by training and serving; a second copy is the bug's habitat.
- Log the feature vector at serving, sampled, so skew is measurable rather than suspected.
- Compare serving-time features against re-computed features from the batch path on identical inputs.
- Pin normalisation statistics, vocabularies, and category defaults into the artefact, not re-derived.
- Verify in serving order: the per-request path is the one that must match, and any caching layer sits inside it.
- Treat a monitoring gap between training and serving feature distributions as an alarm, not a curiosity.

## Procedure

1. Trace each feature's two computations: batch and per-request.
2. Eliminate duplicate implementations; both paths call one library.
3. Sample serving feature vectors and log them with prediction identifiers.
4. Replay logged serving inputs through the batch path; diff the features.
5. Investigate any diff beyond tolerance; document the divergence and its cause.
6. Keep the skew detector running permanently — refactors and upgrades re-introduce skew.

## Anti-patterns

- A "small adaptation" of the training feature code for serving speed.
- Nulls mapped to zero in training but to the mean at serving.
- Category vocabularies rebuilt at serving, producing different indices.
- Detecting skew only after users complain about prediction quality.
- Comparing distributions of two pipelines run at different times and calling that a skew check.

## Done checklist

- [ ] One implementation traced and enforced for both paths.
- [ ] Serving features sampled and logged.
- [ ] Replay-and-diff harness runs on identical inputs.
- [ ] Statistics and vocabularies pinned in the artefact.
- [ ] Skew detector permanent and alarmed.
- [ ] Every diff beyond tolerance root-caused.

## Sources

- Google rules of ML, training/serving skew: <https://developers.google.com/machine-learning/guides/rules-of-ml>
- MLOps overview: <https://ml-ops.org/>
- Pipeline separation guidance: <https://developers.google.com/machine-learning/crash-course>
