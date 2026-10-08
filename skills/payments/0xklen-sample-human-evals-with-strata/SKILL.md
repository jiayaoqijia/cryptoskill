---
name: sample-human-evals-with-strata
description: Use when you can only human-review a fraction of outputs. Draws a stratified random sample so the estimate generalises and the interval is reportable.
---

# Sample Human Evals with Strata

You cannot read every output, so the sample must be random and stratified or the reviewed score is a story about the convenient cases.

## Procedure

1. Define the population and strata (traffic source, language, length, or a prior model's score). Sample within each stratum.
2. Draw randomly within strata; a convenience sample from the top of a dashboard is not random.
3. Allocate n across strata either proportional to volume or equal for equal precision per stratum. State which.
4. Size each stratum for its own interval, not just the total. A 5% stratum at n=20 gives an unusable +/-22%.
5. Compute the weighted estimate back to the population if strata are equal-sized: `p_hat = sum(w_i * p_i)`, weights = population share.
6. Report the interval on the population estimate plus the per-stratum rates with counts.
7. Log the sampling frame and seed so the draw is reproducible and auditable.

```python
import pandas as pd
rng = 7
sample = df.groupby("stratum", group_keys=False).apply(
    lambda g: g.sample(n=min(len(g), 120), random_state=7))
```

## Pitfalls

- Reviewing only flagged or low-confidence outputs measures the hard tail, not the average — useful, but label it as such.
- Proportional allocation leaves rare strata at n=3; oversample them and reweight.
- Sampling without a fixed seed cannot be reproduced or re-audited after a challenge.
- Ignoring non-response: if raters skip hard items, the completed set is biased.
- Reporting a per-stratum rate from a handful of items as if it were precise.

## Verification

    python3 sample.py --frame traffic.parquet --strata language --n 400 --seed 7 | head   # reproducible draw

Report: "Stratified by language, n=400 (proportional, Japanese oversampled to 100); weighted pass 0.74 +/-0.04, Japanese stratum 0.61 (n=100, +/-0.10)."
