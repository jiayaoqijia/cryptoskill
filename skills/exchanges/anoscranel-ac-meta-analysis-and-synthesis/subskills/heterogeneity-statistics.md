---
name: heterogeneity-statistics
domain: research-operations/heterogeneity-statistics
trigger: "Measuring and reading variation before averaging over it."
anti_trigger: "Not for choosing the pooling model alone, and not for subgroup hunting."
scope: "Q, I-squared, tau, and reading spread before averaging it."
status: seedling
---

# Heterogeneity statistics

## Standard

Three statistics describe between-study variation, and they answer different questions. Cochran's Q tests the null hypothesis that all variation is within-study sampling noise; it is underpowered with few studies and overpowered with many, so a non-significant Q is absence of evidence, not evidence of absence. I-squared expresses the proportion of total variation that is between studies — a percentage of variation, not a magnitude, so thirty percent of a tiny tau and thirty percent of a large tau are both thirty percent. Tau itself is the between-studies standard deviation, the quantity the random-effects model actually uses.

The reading that matters combines them: how big is the spread in the effect units a reader understands, not whether a threshold was crossed. An I-squared of sixty percent with effects all in the same clinical direction is a different finding from forty percent where estimates straddle both harm and benefit. The magnitude and the direction pattern are read together, and the thresholds — low, moderate, high — are conventions for signalling, not calibrated boundaries.

Primary sources: <https://training.cochrane.org/handbook/current/chapter-10> and <https://handbook-5-1.cochrane.org/chapter_9>.

## Decision rules

- Report Q with its p-value, I-squared, and tau-squared — all three, with units clear.
- State the confidence interval around I-squared when studies are few; the point estimate alone is unstable.
- Use magnitude thresholds as signals only, never as decision rules in themselves.
- Judge whether estimates lie on the same side of no-effect as well as their spread.
- Pre-specify what heterogeneity will trigger if it appears: an investigation, a model change, or a decision not to pool.
- Record which measure drives any claim that variation is or is not present.

## Procedure

1. Compute Q, I-squared, tau-squared, and the I-squared confidence interval.
2. Read tau in the effect units of the measure.
3. Judge the pattern of directions across studies.
4. Compare against the protocol's pre-specified response to heterogeneity.
5. If explaining is claimed, go to meta-regression — never re-run pooling models until significance shifts.
6. Record all statistics and the reading; omission of negative Q findings is a reporting failure.

## Anti-patterns

- Declaring heterogeneity absent because Q is non-significant in five studies.
- Reading I-squared as a magnitude rather than a proportion.
- Dropping the largest study until Q quiets, then reporting the remainder.
- Using threshold crossing as an automatic model switch.
- Reporting I-squared without tau-squared when the measure's scale is what a reader needs.

## Done checklist

- [ ] Q, p, I-squared, tau-squared all reported.
- [ ] I-squared interval given for few-study cases.
- [ ] Tau read in effect units.
- [ ] Direction pattern judged alongside spread.
- [ ] Protocol's pre-specified response followed.
- [ ] All statistics recorded, including inconvenient ones.

## Sources

- Cochrane Handbook, heterogeneity chapter: <https://training.cochrane.org/handbook/current/chapter-10>
- Cochrane Handbook 5.1, heterogeneity statistics: <https://handbook-5-1.cochrane.org/chapter_9>
- Methods articles: <https://www.biomedcentral.com/methods>
