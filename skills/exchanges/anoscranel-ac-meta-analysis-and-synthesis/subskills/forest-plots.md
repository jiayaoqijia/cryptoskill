---
name: forest-plots
domain: research-operations/forest-plots
trigger: "Reading and building the forest plot as the review's evidence display."
anti_trigger: "Not for visual design in general, and not for the funnel plot."
scope: "What the plot displays, and what it is asked to prove it cannot."
status: seedling
---

# Forest plots

## Standard

A forest plot shows one row per study: the point estimate, its confidence interval, the study's weight, and usually the pooled estimate with its interval as a summary row. Its honesty is in the display of spread — the reader sees every interval, not just the average. The plot is an evidence display, and the display's purpose is to let the reader see disagreement that a single number would hide.

What the plot cannot do is prove homogeneity or significance by eyeball. Overlapping intervals do not imply no heterogeneity; non-overlapping intervals do not imply a real difference between those two studies without a formal test; and the summary diamond's width is a confidence statement about the mean, not about where individual effects lie. The plot supports these readings when the statistics are printed; it substitutes for none of them.

Primary sources: <https://training.cochrane.org/handbook/current/chapter-10> and <https://prisma-statement.org/>.

## Decision rules

- Display one row per study with estimate, interval, and weight.
- Carry the raw counts per arm for binary outcomes so a reader can recompute.
- Include the summary row clearly distinguished from study rows.
- Keep the scale identical across panels that will be compared.
- Sort by a pre-specified, non-result-based order, or keep input order; never sort to make a pattern visible.
- Include tau-squared or I-squared on the plot, not only in the text.

## Procedure

1. Assemble per-study estimates, intervals, and weights.
2. Choose the scale — ratio measures plot on the log scale; label accordingly.
3. Fix the sort order by a rule fixed before seeing results.
4. Draw study rows, then the summary diamond.
5. Annotate with the heterogeneity statistics and the model used.
6. Check that the visual and the printed statistics agree; if the plot looks homogeneous while Q says otherwise, find the error.

## Anti-patterns

- Sorting studies by effect size to manufacture a visible trend.
- Reading a diamond-only plot with no displayed study intervals.
- Comparing squares' sizes as if weight equalled quality.
- Plotting ratio measures on the raw scale while labelling them as ratios.
- Expecting the plot to settle heterogeneity.

## Done checklist

- [ ] Per-study rows with estimate, interval, weight.
- [ ] Counts carried for binary outcomes.
- [ ] Summary row distinct.
- [ ] Scale consistent and correctly labelled.
- [ ] Sort rule pre-specified.
- [ ] Heterogeneity and model printed on the plot.

## Sources

- Cochrane Handbook, presenting results: <https://training.cochrane.org/handbook/current/chapter-10>
- PRISMA statement: <https://prisma-statement.org/>
- Reporting guideline directory: <https://equator-network.org/>
