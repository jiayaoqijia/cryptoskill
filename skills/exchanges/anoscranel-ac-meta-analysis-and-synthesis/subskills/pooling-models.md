---
name: pooling-models
domain: research-operations/pooling-models
trigger: "Choosing between fixed and random effects, and knowing what each claims."
anti_trigger: "Not for heterogeneity diagnostics, and not for the conduct layer."
scope: "Inverse-variance weighting, fixed versus random effects, tau-squared."
status: seedling
---

# Pooling models

## Standard

Fixed-effect pooling weights each study by the inverse of its variance and answers: what is the best estimate of the single underlying effect? That single underlying effect is an assumption, not a finding. Random-effects pooling adds a between-studies variance component — tau-squared — and answers a different question: what is the mean of the distribution of effects across studies? The two models can produce similar numbers with different meanings, and the meaning is what a reader uses.

The honest handling is decision-first. If the studies plausibly estimate one effect — same population, same implementation — the fixed model expresses that belief. If they plausibly differ — different settings, different intensity — random effects expresses that, and the pooled estimate becomes an average across a spread that itself matters. Choosing random effects because heterogeneity appeared, then reporting only the mean and not the spread, hides the very thing the model was chosen to admit.

Primary sources: <https://training.cochrane.org/handbook/current/chapter-10> and <https://handbook-5-1.cochrane.org/chapter_9>.

## Decision rules

- Choose the model from the protocol's substantive belief about variation, not from the data.
- With random effects, report tau-squared and the prediction interval, not just the pooled mean.
- State which question the pooled estimate answers: one true effect, or a mean of varying effects.
- Record the tau-squared estimator used; results can move with it in few-study cases.
- Prefer the Knapp-Hartung or similar adjustment for the confidence interval in small numbers of studies.
- Pre-specify which model is primary; the other is a sensitivity analysis, not a shopping option.

## Procedure

1. State the substantive belief: one effect or a distribution of effects.
2. Select the primary model in the protocol.
3. Run the primary model and record its estimate and interval.
4. Run the other model as the pre-specified sensitivity analysis.
5. With random effects, extract tau-squared and compute the prediction interval.
6. Report both, labelled by the question each answers.

## Anti-patterns

- Switching to random effects because the result became non-significant under fixed.
- Reporting a random-effects mean without tau-squared or the prediction interval.
- Treating inverse-variance weights as study quality; they are mostly precision.
- Letting heterogeneity statistics choose the model after the fact.
- Presenting the more favourable model as the finding.

## Done checklist

- [ ] Substantive belief stated in the protocol.
- [ ] Primary model pre-specified.
- [ ] Other model run as sensitivity.
- [ ] Tau-squared reported with the estimator name.
- [ ] Prediction interval computed under random effects.
- [ ] Each estimate labelled with the question it answers.

## Sources

- Cochrane Handbook, fixed versus random: <https://training.cochrane.org/handbook/current/chapter-10>
- Cochrane Handbook 5.1, pooling methods: <https://handbook-5-1.cochrane.org/chapter_9>
- Methodology resources: <https://www.biomedcentral.com/methods>
