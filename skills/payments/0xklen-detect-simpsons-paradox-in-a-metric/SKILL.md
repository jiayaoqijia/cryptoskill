---
name: detect-simpsons-paradox-in-a-metric
description: Use when an aggregate moves one way while its parts move the other. Checks for Simpson's paradox before trusting a pooled rate.
---

# Detect Simpson's Paradox in a Metric

A pooled rate can fall while every subgroup rises, or rise while every subgroup falls, when the mix of groups changes. The aggregate is a weighted average and the weights are doing the talking.

## Procedure

1. Compute the metric pooled, then per strata for the obvious confounders: platform, channel, geography, account tier.
2. Compare the two tables and look for a sign flip between pooled and per-stratum.
3. Check whether the mix of strata changed between periods — that shift is the usual cause.
4. Recompute by fixing the mix: standardise to a common weight vector and compare like for like:
   ```python
   grp = df.groupby(['segment','period'])['converted'].agg(['sum','count'])
   rate = grp['sum']/grp['count']
   w = df[df.period=='prior'].groupby('segment').size(); w = w/w.sum()
   print((rate.unstack('period') * w).sum())   # mix-adjusted rate per period
   ```
5. Report both the pooled and the mix-adjusted number, with the stratum breakdown, whenever they disagree.
6. Take the unweighted mean of stratum rates only for diagnostics — never present it as the overall rate.

## Pitfalls

- A pooled ratio (sum over sum) is not the mean of ratios; averaging per-day rates distorts the total.
- Mobile users quadrupling in share can drag a conversion rate down even as mobile and desktop both improve.
- Small strata with extreme rates swing the unweighted mean; weight by volume.
- Confounders are not only categorical — a continuous variable like account age can hide the same reversal.
- Simpson's paradox is a warning about a lurking variable, not a licence to pick the subgroup with the nicer story.

## Verification

    python3 - <<'PY'
import pandas as pd
d = pd.read_csv('conv.csv')
pooled = d.groupby('period').apply(lambda g: g['conv'].sum()/g['n'].sum())
byseg = d.groupby(['segment','period']).apply(lambda g: g['conv'].sum()/g['n'].sum()).unstack()
print(pooled.to_string()); print(byseg.to_string())
PY

Report: "Pooled conversion fell 1.1pt while every segment rose; the mix shifted 60% toward low-converting mobile. Mix-adjusted change is +0.4pt — the fall was composition, not performance."
