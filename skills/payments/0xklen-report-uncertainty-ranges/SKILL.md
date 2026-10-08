---
name: report-uncertainty-ranges
description: Use when stating any estimate or measurement. Attaches an interval and the source of the uncertainty instead of a single false-precision number.
---

# Report Uncertainty Ranges

A point estimate without an interval tells the reader the number is exact when it is not. Quantify the range or say plainly that you cannot.

## Procedure

1. Name the uncertainty type: sampling (finite n), measurement (instrument/annotation error), model (assumption), or scenario (future path). They compose differently.
2. For sampling uncertainty, give 95% intervals. Bootstrap is the fallback for any statistic without a closed form:
   ```python
   import numpy as np
   rng = np.random.default_rng(0)
   boots = [np.median(rng.choice(x, x.size, replace=True)) for _ in range(10000)]
   lo, hi = np.percentile(boots, [2.5, 97.5])
   ```
3. For a proportion, use a Wilson interval, not the textbook normal one, when p is near 0 or 1 or n is small.
4. Propagate measurement error rather than ignoring it: for a product `f = a·b`, `σ_f/|f| = sqrt((σ_a/a)² + (σ_b/b)²)`.
5. Report intervals that describe the quantity you mean. A 95% CI is not "95% likely to contain the true value" under every interpretation — say which.
6. Do not shrink an interval to look decisive; do not widen it to cover a claim it cannot support. If the interval spans the decision threshold, say the data is inconclusive.
7. Round the interval to the precision of the estimate: `12.4% (95% CI 9.1–15.7)`, not `12.4312 ± 0.4937`.

```bash
python3 -c "from statsmodels.stats.proportion import proportion_confint; \
print(proportion_confint(37, 210, method='wilson'))"
```

## Pitfalls

- A CI on a biased estimator is precisely wrong; uncertainty about bias is separate and usually larger.
- The interval says nothing about systematic error you did not model — name it.
- Error bars that are ±1 SEM look 3.9× narrower than a 95% interval and mislead by convention.
- Combining intervals by adding half-widths is wrong for independent errors; combine variances.
- Too many significant figures implies precision the interval contradicts.

## Verification

    grep -cE '95%|CI|interval|±|\[[0-9.]+, ?[0-9.]+\]' estimates.md

Every headline number carries an interval or an explicit "no interval available: reason". Report: "Estimate 12.4% (95% CI 9.1–15.7, Wilson, n=210); model bias not quantified."
