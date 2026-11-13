---
name: ac-meta-analysis-and-synthesis
description: "Pooling study results statistically rather than narratively: choosing the effect measure, inverse-variance weighting and the fixed-effect estimate, random effects and what tau-squared means, the heterogeneity statistics and how to read them, forest plots, small-study effects and the funnel plot's limits, subgroups and meta-regression, network meta-analysis and transitivity, and the written synthesis record. It explains the arithmetic and the assumptions of pooling; it never certifies a conclusion. Use when asking \"meta-analysis\", \"forest plot\", \"funnel plot\", \"fixed versus random effects\", \"I-squared\", \"tau squared\", \"odds ratio pooled\", \"meta-regression\", \"network meta-analysis\", \"indirect comparison\", \"leave one out\", \"trim and fill\", \"risk of bias sensitivity\". Not for the review's conduct machinery (ac-systematic-review-conduct), not for narrative synthesis without pooling (ac-deep-researcher), not for writing the report (ac-academic-writing)."
license: MIT
metadata:
  domain: research-operations
status: seedling
---

# Meta-analysis and synthesis

## Overview

A meta-analysis is an arithmetic performed on estimates, and its honesty lives in the assumptions rather than the computation. Pooling asks: are these studies measuring the same thing in the same way, and is the spread between them what sampling noise would produce? When the answer to the second question is no, the pooled number is an average of disagreements, and reporting it without the disagreement is the field's most common failure.

This skill covers the statistical half of synthesis: the effect measures and their choices, the two pooling models and what each assumes about between-study spread, the statistics that measure that spread, the plots that display it, the bias investigations and their limits, the moderator analyses that can be believed or abused, and the network extension that turns direct comparisons into an assumption about indirect ones. The conduct of the review that produced the studies is a separate skill; the narrative synthesis of evidence that cannot be pooled is another.

Primary sources: <https://training.cochrane.org/handbook/current/chapter-10> and <https://handbook-5-1.cochrane.org/chapter_9>.

## When to use

- When pooling study estimates into a combined effect.
- When heterogeneity appears and must be measured, explained, or respected.
- When small-study bias or selective reporting is suspected.
- When comparing multiple interventions through indirect evidence.

## When NOT to use

- For search, screening, and the review's conduct machinery (use ac-systematic-review-conduct).
- For narrative synthesis of unpoolable evidence (use ac-deep-researcher).
- For writing the review as a document (use ac-academic-writing).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/effect-measures.md` | `research-operations/effect-measures` | Ratio, difference, and standardised measures, and when each distorts. |
| `subskills/pooling-models.md` | `research-operations/pooling-models` | Inverse-variance weighting, fixed versus random effects, tau-squared. |
| `subskills/heterogeneity-statistics.md` | `research-operations/heterogeneity-statistics` | Q, I-squared, tau, and reading spread before averaging it. |
| `subskills/forest-plots.md` | `research-operations/forest-plots` | What the plot displays, and what it is asked to prove it cannot. |
| `subskills/small-study-effects.md` | `research-operations/small-study-effects` | Funnel asymmetry, trim-and-fill, Egger's test, and their honest limits. |
| `subskills/subgroups-and-meta-regression.md` | `research-operations/subgroups-and-meta-regression` | Moderator analysis done as pre-specified test, not story. |
| `subskills/network-meta-analysis.md` | `research-operations/network-meta-analysis` | Indirect comparison, transitivity, and incoherence checking. |
| `subskills/certainty-and-sensitivity.md` | `research-operations/certainty-and-sensitivity` | GRADE ratings and the sensitivity analyses that test the finding. |
| `subskills/synthesis-record.md` | `research-operations/synthesis-record` | The written record: model, assumptions, tests run, and all of them re-run. |

## Status and honest limits

Every pooling model is a claim about where variation comes from, and the data cannot fully verify the claim; the fixed-effect assumption of one true effect is unfalsifiable from the studies alone. Small-study tests are underpowered at few studies and confounded by genuine heterogeneity. Nothing here decides whether an intervention works — it states what the pooled estimate is, how certain the evidence behind it is, and which assumptions the certainty rests on. A meta-analysis of biased studies is precise about the wrong number.
