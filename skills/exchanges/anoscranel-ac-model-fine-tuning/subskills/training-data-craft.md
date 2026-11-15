---
name: training-data-craft
domain: software-engineering/training-data-craft
trigger: "Curating instruction or preference training data."
anti_trigger: "Not for running the training, and not for general dataset evaluation."
scope: "Instruction pairs and preference pairs, where quality makes or breaks the run."
status: seedling
---

# Training data craft

## Standard

The model learns the data, not the intention behind it. Instruction-tuning data is input-output pairs demonstrating the target behaviour; preference data is a prompt with a chosen and a rejected response demonstrating the direction. Both make or break the run before any gradient is computed: a thousand clean, diverse, verified pairs outperform ten thousand noisy ones, and the noise teaches the wrong thing.

Quality control is iterative and adversarial. Every pair is checked for correctness, consistency of format, and fidelity to what production traffic will actually look like; a training set whose inputs are stylistically unlike deployment inputs produces a model that performs on its test set and fails on real traffic. Contamination is checked both ways: training examples must not overlap with the evaluation sets, and the base model's training data must not have already memorised the evaluation set.

Primary sources: <https://huggingface.co/docs/datasets/index> and <https://huggingface.co/docs/trl/index>.


One further discipline outperforms volume: adversarial filtering of the curated set against a small set of hard negatives — pairs a weaker model gets wrong — sharpens the training signal more than doubling mediocre examples, and recording the hard-negative set alongside the dataset version preserves the sharpening for the next run.

## Decision rules

- Define the target behaviour precisely enough that an annotator can verify each pair against it.
- Audit every pair: correctness, format consistency, and dupes near-identical in meaning.
- Match the deployment distribution: inputs in training resemble inputs in production.
- Verify provenance and rights for the data's source before training on it.
- Check overfit-prone patterns: near-duplicates, template artefacts, single-source dominance.
- Set the train/eval split before curation ends; contamination is checked at the boundary.

## Procedure

1. Write the target behaviour as a verification guide for annotators.
2. Collect or generate pairs; record provenance per item.
3. Audit the set: correctness pass, format pass, deduplication.
4. Compare the input distribution with production traffic.
5. Carve the evaluation set first and quarantine it from all curation.
6. Version the dataset; every training run references a dataset version.

## Anti-patterns

- Bulk scraped pairs with no verification pass.
- Training inputs written by engineers; production inputs written by users.
- The evaluation examples leaking into training through dedup failures.
- Near-duplicate examples crowding out diversity.
- No dataset version, so runs cannot be compared.

## Done checklist

- [ ] Verification guide written.
- [ ] Provenance recorded per item.
- [ ] Correctness, format, and dedup passes done.
- [ ] Distribution compared with production traffic.
- [ ] Evaluation set quarantined before curation ended.
- [ ] Dataset versioned.

## Sources

- Datasets documentation: <https://huggingface.co/docs/datasets/index>
- TRL, trainer library for instruction and preference data: <https://huggingface.co/docs/trl/index>
- Wikipedia overview of the adaptation paradigm: <https://en.wikipedia.org/wiki/Fine-tuning_(deep_learning)>
