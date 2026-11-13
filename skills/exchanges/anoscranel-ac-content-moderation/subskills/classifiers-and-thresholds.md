---
name: classifiers-and-thresholds
domain: software-engineering/classifiers-and-thresholds
trigger: "Setting automated pre-screening with known error trade-offs."
anti_trigger: "Not for building the model itself, and not reviewer queue design."
scope: "Pre-screening models as precision-recall decisions."
status: seedling
---

# Classifiers and thresholds

## Standard

A moderation classifier pre-screens content so humans review only what machines cannot decide. Its output is a score against a category, and the threshold that converts score into action is a policy decision expressed as an error trade-off: a lower threshold catches more violations and removes more legitimate content; a higher threshold protects legitimate content and lets more violations through. Both error rates are measured, published internally, and chosen deliberately — never defaulted.

The threshold is set per category and per action tier. High-severity categories can justify low thresholds with near-immediate action and human backfill; low-severity categories warrant conservative thresholds because removal mistakes carry user-trust costs and violations only queue delay. The operating point is recorded with its measured precision and recall, and any change to it is an experiment with before-and-after numbers.

Primary sources: <https://en.wikipedia.org/wiki/Precision_and_recall> and <https://en.wikipedia.org/wiki/False_positives_and_false_negatives>.

## Decision rules

- Record per category: score meaning, threshold, resulting precision and recall.
- Threshold changes are experiments with measured before-and-after error rates.
- Every automated action names its trigger: which classifier, which threshold.
- Automated removal requires a confidence tier and an appeals path; passive queueing does not.
- Classify on the content itself; reviewer outcomes feed calibration, not silent thresholds.
- Model updates re-derive threshold calibration; a new model without recalibration is a defect.

## Procedure

1. List the categories the classifier serves and their action tiers.
2. Choose an initial threshold per category from a validation set with known labels.
3. Measure precision and recall on a held-out, human-labelled sample.
4. Wire automated actions only for the confidence and severity tier justified.
5. Record the operating point in the moderation record.
6. Re-calibrate on model updates and review quarterly against appeal outcomes.

## Anti-patterns

- Thresholds copied from defaults without measured error rates.
- Treating a classifier score as a probability it was never calibrated to be.
- Automated removal with no appeals path.
- Publishing recall goals while concealing over-removal rates.
- Changing model and threshold at once, so neither effect is attributable.

## Done checklist

- [ ] Score meaning documented per classifier.
- [ ] Threshold per category with measured precision and recall.
- [ ] Automated actions justified by tier.
- [ ] Appeals path for automated actions.
- [ ] Operating point recorded.
- [ ] Recalibration scheduled and wired to model updates.

A second operating-point rule prevents the common silent failure: model updates often shift score distributions, so a threshold carried across versions changes its meaning without anyone deciding it should. Recalibration on update is therefore a hard gate, not a reminder, and the moderation record shows each threshold beside the model version it was calibrated against.

## Sources

- Precision and recall: <https://en.wikipedia.org/wiki/Precision_and_recall>
- Error types: <https://en.wikipedia.org/wiki/False_positives_and_false_negatives>
- Content moderation overview: <https://en.wikipedia.org/wiki/Content_moderation>
