---
name: scoring-and-judges
domain: prompt-engineering/scoring-and-judges
trigger: "Choosing scoring tiers from deterministic checks to humans."
anti_trigger: "Not for case design, and not for evaluation-metric selection."
scope: "Deterministic checks first, judges second, humans for the residue."
status: seedling
---

# Scoring and judges

## Standard

Scoring is a hierarchy, and each tier measures with different error. Deterministic checks — exact match, test passes, schema validity, stated constraints — are reproducible and cheap, and they should take every case that they can honestly score. Model judges handle the open-ended residue, at the price of the judge's own biases: position in a pair, verbosity preference, and self-family preference all move a judge's grades, and an uncalibrated judge quietly imports its preferences into the model ranking. Humans sit at the top of cost and trustworthiness, grading the residue the judges cannot hold.

A judge is usable only after calibration: its grades on a blind gold set are compared against trusted human grades, its systematic biases measured by swapping order and length variants, and its verdicts kept advisory — calibration numbers travel with the judge, so a later reader knows what the grades are worth. The determinism-first ordering is what keeps evaluation affordable: every case promoted from human to judge, and from judge to deterministic check, cuts the recurring cost of running the suite while leaving a stated measurement trail where the softer tiers only approximated.

Primary sources: <https://arxiv.org/abs/2306.05685> and <https://docs.anthropic.com/en/docs/about-claude/evaluate>.

## Decision rules

- Score every case at the lowest tier that can honestly grade it.
- Calibrate model judges against a blind human gold set before trusting them.
- Measure judge position and verbosity bias by order-swapping and length-matching.
- Keep judge verdicts advisory on adopt-decisions; humans decide where the construct is subjective.
- Record the calibration numbers beside the judge's grades.
- Re-calibrate when the judge model or the graded construct changes.

## Procedure

1. Classify each case as deterministically checkable, judge-gradable, or human-only.
2. Write the deterministic check first wherever it exists.
3. Assemble a blind gold set for each judge-graded construct.
4. Grade the gold set with humans; run the judge on it and compute agreement.
5. Run the order- and length-swap tests; record the bias magnitudes.
6. Publish the tier map — which case is scored where — alongside every suite result.

## Anti-patterns

- A judge grading cases a schema check could have scored.
- Trusting a same-family judge without calibration.
- Grades presented without the judge's bias measurements.
- Promoting a judge's subjective verdict to a decision.
- Recalibrating only when results look odd.

## Done checklist

- [ ] Tier map recorded per case.
- [ ] Deterministic checks written first.
- [ ] Gold set assembled and blind-graded by humans.
- [ ] Judge agreement computed.
- [ ] Order- and length-swap biases measured.
- [ ] Calibration numbers accompany every reported grade.

## Sources

- Bias and calibration survey: <https://arxiv.org/abs/2306.05685>
- Claude evaluation guidance: <https://docs.anthropic.com/en/docs/about-claude/evaluate>
- Human-eval style schema checking: <https://github.com/openai/human-eval>
