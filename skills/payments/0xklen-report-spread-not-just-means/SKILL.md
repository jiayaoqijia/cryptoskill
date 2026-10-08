---
name: report-spread-not-just-means
description: Use when summarising any measured quantity. Reports the distribution — spread, n, and outliers — instead of a lone mean.
---

# Report Spread, Not Just Means

A mean with no spread hides the two things that change decisions: how variable the data is and how many points it rests on. Always ship the spread.

## Procedure

1. Report n first. A mean over 4 points and a mean over 40,000 are different claims.
2. Choose the spread that matches the shape: symmetric → standard deviation; skewed or heavy-tailed → median with IQR; bounded/count → give min, max, quartiles.
3. Print the actual distribution before summarising: `python3 -c "import pandas as pd; s=pd.read_csv('data.csv')['x']; print(s.describe(pct=[.05,.25,.5,.75,.95]))"`.
4. Look for multimodality. A bimodal set has a mean that no unit attains — plot the histogram and say so.
5. Report extreme values by count and effect, not by deletion. "3 records >100× the median" beats silently dropping them.
6. For a change over time, give the difference with its interval, not two bare means: `Δ = -2.1 (95% CI -3.4 to -0.8)`.
7. Round to the precision the data supports; do not print 6 decimals from 3 sig-fig inputs.

```python
import pandas as pd
s = pd.read_csv('data.csv')['latency_ms']
print("n", s.size, "median", s.median(), "IQR", s.quantile(.75)-s.quantile(.25),
      "p95", s.quantile(.95), "max", s.max())
```

## Pitfalls

- SD is meaningless for skewed data — for income or latency report median and IQR.
- A "mean of 4.2" on a 1–5 Likert scale is not a point on a ruler; report the modal band.
- Mixing units or cohorts inflates variance; check the distribution is from one population before pooling.
- Outliers carried by a one-digit keying error are not signal — inspect before trimming.
- Two groups with equal means can have opposite variances; the decision often lives in the spread.

## Verification

    grep -cE 'median|IQR|p95|std|range' summary.md

Every reported average is accompanied by n and a spread measure. Report: "Median 210 ms, IQR 180–260 (n=8,412); mean alone would hide a 9-second p99 tail."
