<!--
  Imported from: https://github.com/saksham10arora-dotcom/quant-skills
  Source Path: skills/stats-test-picker/SKILL.md
  Curated for awesome-quant-skills
-->

---
name: stats-test-picker
description: Choose the correct statistical test for a comparison, with assumption checks and effect sizes. Use when the user asks which test to use, mentions t-tests, ANOVA, chi-square, A/B test analysis, or wants p-values for a comparison.
---

# Stats Test Picker

Never name a test before answering these three questions:
1. What is the outcome type? (continuous / binary / count / ordinal / time-to-event)
2. How many groups or variables, and are they independent or paired?
3. What is the actual question: difference, association, equivalence, or non-inferiority?

## Decision path

**Comparing means of 2 independent groups (continuous outcome):**
- n < ~50 per group or visible skew: Mann-Whitney U
- Else Welch's t-test (default over Student's; unequal variances are the norm)
- Report: difference in means with CI, not just p

**Paired/repeated measures:** Wilcoxon signed-rank if differences are skewed; paired t otherwise

**3+ groups:** Kruskal-Wallis or one-way ANOVA; follow up with pairwise tests corrected via Holm, never raw

**Binary outcome, 2 groups:**
- Check expected cell counts; all >= 5: two-proportion z or chi-square without Yates
- Small cells: Fisher exact
- Large n and interested in direction with CI: report risk difference and ratio, not just chi-square

**Count outcomes:** Poisson/negative binomial regression if covariates exist; else compare rates

**Time-to-event:** log-rank test + hazard ratio with CI. Never compare mean survival times directly under censoring.

## Assumption checks that actually matter

- Normality: do not Shapiro-test into paralysis. With n >= 50 per group prefer rank tests only for heavy skew (>1.5) or visible bimodality
- Independence is NOT testable from the data: ask how it was collected. Clustered sampling requires mixed models, period
- Equal variances: Welch sidesteps it; use it by default

## Mandatory output format

Every test answer must include:
```
TEST: <name>
ASSUMPTIONS CHECKED: [what was verified and result]
EFFECT SIZE: <difference/ratio/CI>   <- never omit
P-VALUE: x.xxx
ONE-LINE INTERPRETATION: in plain language, no jargon
POWER NOTE: if n < 30/group, state detectable effect size at 80% power
```

Refuse to give bare p-values. If the user insists on a test that violates its assumptions, say what breaks and propose the alternative once; do not argue twice.
