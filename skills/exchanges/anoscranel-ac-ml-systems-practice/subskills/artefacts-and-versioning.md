---
name: artefacts-and-versioning
domain: software-engineering/artefacts-and-versioning
trigger: "Versioning models, features, and data so every prediction is reproducible."
anti_trigger: "Not for choosing a model format, and not for registry product selection."
scope: "Versioning models, features, and data so any prediction is reproducible."
status: seedling
---

# Artefacts and versioning

## Standard

A deployed model is three versioned things or it is nothing: the trained artefact, the feature computation it expects, and the data it was trained on. When a prediction is questioned, the only honest answer names all three versions; if the data that trained the artefact is unnamed, the model cannot be reproduced, only re-approximated by whatever the pipeline produces today.

Versioning the artefact alone is the common half-measure. Models depend on their feature definitions — column names, scaling statistics, vocabulary lists — and each is as load-bearing as weights. A trained artefact without the training-data snapshot cannot be diffed against its successor: the two models differ in unknowns, and "improved" is a guess.

Primary sources: <https://ml-ops.org/> and <https://scikit-learn.org/stable/model_persistence.html>.

## Decision rules

- Assign a version to every model artefact, feature set, and training dataset at creation.
- Record the lineage triple together: artefact version + feature-set version + dataset version.
- Persist encoders, scalers, and vocabularies as part of the artefact, not as ambient state.
- Tag every prediction with the artefact and feature-set version that produced it.
- Make rollback mechanical: storing the predecessor should be enough to restore it.
- Record evaluation results at promotion time, tied to the lineage triple of the promoted artefact.

## Procedure

1. Give each training input a dataset version, immutable once used.
2. Version the feature definitions alongside their outputs.
3. Store artefact + encoders + scalers + vocabularies as one bundle with one identifier.
4. Log the lineage triple with each training run and with each prediction.
5. Keep promoted predecessors available for rollback, with their records.
6. Diff successor against predecessor on the same test data before promotion.

## Anti-patterns

- Versioning the model file with no record of its training data.
- Encoders and scalers applied at serving from memory, reimplemented by hand.
- Naming artefacts by date alone, with no change description.
- Overwriting "v2" because v1 had a bug, where v1 was already serving.
- Comparing new and old models on different data and calling it an improvement.

## Done checklist

- [ ] Dataset, feature-set, and artefact versions recorded at training.
- [ ] Bundle includes encoders, scalers, vocabularies.
- [ ] Predictions tagged with the versions that produced them.
- [ ] Predecessors retained for rollback.
- [ ] Evaluation recorded with the lineage triple.
- [ ] Successor diffed on identical data.

## Sources

- MLOps versioning practice overview: <https://ml-ops.org/>
- Model persistence and bundling: <https://scikit-learn.org/stable/model_persistence.html>
- Google rules of ML: <https://developers.google.com/machine-learning/guides/rules-of-ml>
