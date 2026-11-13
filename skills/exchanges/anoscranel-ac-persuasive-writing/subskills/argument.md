---
name: argument
domain: writing/argument
trigger: "\"argue this\", \"how strong a claim can I make\", \"is this overstated\", \"handle the counter-argument\", \"should I hedge this\"."
anti_trigger: "Attaching the checkable source for each claim; persuasive structure across a whole document (subskills/persuasion.md)."
scope: "Claim-evidence-warrant, calibrated hedging, counter-argument"
status: "seedling"
---

# Argument

## Standard

- **Toulmin's model is the working grammar.** Grounds (the data), claim (the conclusion), warrant (the licence to infer), backing (why the warrant has authority), qualifier (how much reliance the claim carries), rebuttal (what defeats it).
 The grounds are the only element known; claim and warrant are asserted (<https://doi.org/10.1002/joom.1137>).
- **Qualifiers map to the inference form.** Deduction carries certainty, induction probability, abduction plausibility. These are properties of the reasoning, not of tone.
- **Overclaim is measured, and readers believe it.**
 Across 194,631 cross-sectional articles (1980–2024), 46% used causal language in title or abstract.
 The annual rate rose from 20% to about 60% by 2024.
 In an experiment (N = 1,105) readers took the causal framing as causal evidence (Isch et al., *Nature Human Behaviour* 2026, https://doi.org/10.1038/s41562-026-02553-x).
 Methodological labels (β = −0.4, 95% CI −0.56 to −0.19) reduced that reading. Associational wording (β = −0.3, CI −0.43 to −0.07) did the same.
- **Models amplify overstatement.** Five LLMs summarising these articles stripped hedges and added causal claims where the abstract had used associational wording. A caution prompt reduced but did not remove it.
- **Calibration runs in both directions.** Claim exactly as much as the design supports: no more (overclaim), no less (mush). The named mechanism is drift — the abstract hedges, the introduction is bolder, the conclusion reaches *causes*.

## Decision rules

1. Every claim carries grounds plus a warrant in the same paragraph or the adjacent one.
2. Causal verbs need a causal design. A cross-sectional result gets associational wording.
3. Set the qualifier from the design, not from how confident the writer feels.
4. Name the strongest counter-argument and answer it. An unaddressed best objection reads as evasion.
5. Run the drift check: claim strength must not rise from abstract to conclusion.
6. Where a claim is contested, present both readings and the reason for preferring one.
7. Kill hedging that survives into a conclusion resting on solid grounds.

## Procedure

1. Build a claim ledger, one row per claim: claim, grounds, warrant, qualifier, rebuttal.
2. Classify the inference form for each row (deductive, inductive, abductive).
3. Set the qualifier word to match the form. Prefer plain wording: "shows", "is consistent with", "suggests".
4. Replace every causal verb whose row lacks a causal design.
5. Write the rebuttal for the three load-bearing claims: best counter-evidence, then the reply.
6. Read the ledger alone. Any row whose claim exceeds its grounds is cut or weakened.
7. Re-read the document checking claim strength at each mention. Equalise drift.

## Anti-patterns

- Correlation written with a causal verb.
- A warrant left implicit and therefore unexaminable.
- Hedges so heavy the section says nothing.
- The counter-argument answered with a one-line dismissal.
- Claim strength rising as the document progresses.

## Done checklist

- [ ] Claim ledger complete: grounds, warrant, qualifier, rebuttal.
- [ ] Causal verbs match causal designs.
- [ ] Qualifiers match the inference form.
- [ ] Three load-bearing claims have stated rebuttals.
- [ ] Drift check run from abstract to conclusion.
- [ ] Contested claims show both readings.

## Sources

- <https://doi.org/10.1002/joom.1137>
- https://doi.org/10.1038/s41562-026-02553-x · https://arxiv.org/abs/2109.14776
