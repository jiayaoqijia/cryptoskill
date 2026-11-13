---
name: metrics-and-reading
domain: prompt-engineering/eval-metrics-and-reading
trigger: "Choosing aggregate metrics and reading them without fooling yourself."
anti_trigger: "Not for judge calibration, and not for scoring tiers."
scope: "Pass-at-k, aggregate scores, and honest reading."
status: seedling
---

# Metrics and reading

## Standard

An aggregate metric is a compression of a suite into one number, and every compression loses the structure that would qualify it. Pass-at-`n` — the probability that at least one of `n` samples passes a case — rewards models that are right occasionally while a single-sample pass rate rewards consistent correctness, and the two rank models differently. A mean score over weighted constructs hides which construct lost ground; an improvement can be a large gain on a cheap construct masking a regression on the one the decision cares about. The metric should be chosen for the decision, and the reading should always come with the breakdown.

The second discipline is scope honesty. Percentages computed over suites with different contents, or `n` values, or scoring tiers are not comparable; a "five-point gain" that reflects a different case set, or a longer sampling budget, is an artefact of the change in measurement, not of the models. Statistical honesty completes it: small suites produce noisy rankings, and a few points of difference on a hundred cases is usually within noise — reporting the comparison without the noise band invites a confident choice among indistinguishable options.

Primary sources: <https://arxiv.org/abs/2306.05685> and <https://github.com/EleutherAI/lm-evaluation-harness>.

## Decision rules

- Choose the metric from the decision: consistency favours single-sample rates, coverage favours pass-at-k.
- Report the per-construct breakdown beside every aggregate.
- Never compare scores across suites with different cases, samplings, or scoring tiers.
- Report the number of cases and a noise or interval estimate with every comparison.
- State what `n` means in pass-at-k, and keep it fixed within a comparison.
- Prefer reading distributions on borderline constructs, not only their means.

## Procedure

1. List the candidate aggregates for the suite's shape.
2. Select the primary metric and keep it fixed across the whole comparison.
3. Compute per-construct breakdowns and the primary aggregate for every model.
4. Estimate noise by resampling cases or by binomial intervals on pass rates.
5. Mark comparisons within the noise band as ties in the written record.
6. Attach `n`, case count, and suite version to every reported number.

## Anti-patterns

- Comparing pass-at-one against pass-at-ten as though one number.
- A headline aggregate whose gain hides the decision construct's regression.
- A cross-suite "gain" that reflects a changed measurement, not a changed model.
- Ranking on differences inside the noise band.
- Quoting metrics without case count or suite version.

## Done checklist

- [ ] Primary metric fixed per comparison.
- [ ] Per-construct breakdowns reported.
- [ ] No cross-suite comparisons.
- [ ] Noise band estimated and stated.
- [ ] Ties marked within noise.
- [ ] `n`, case count, suite version attached.

## Sources

- Pass-at-k metrics and evaluation survey: <https://arxiv.org/abs/2306.05685>
- Harness metric practice: <https://github.com/EleutherAI/lm-evaluation-harness>
- Claude evaluation guidance: <https://docs.anthropic.com/en/docs/about-claude/evaluate>
