---
name: measure-inter-annotator-agreement
description: Use when several humans label the same eval items. Measures agreement before treating any label set as a target the model is scored against.
---

# Measure Inter-Annotator Agreement

If the humans cannot agree, no model can match them and your "ground truth" is noise. Measure agreement before the labels grade anything.

## Procedure

1. Have >=2 annotators label an overlapping set (>=30 items, >=10% of the total). Overlap is required; disjoint labelling cannot be checked.
2. Compute a chance-corrected statistic, never raw percent: Cohen's kappa for two raters, Fleiss' kappa or Krippendorff's alpha for more.
   ```python
   import krippendorff
   a = krippendorff.alpha(reliability_data=ratings, level_of_measurement="ordinal")
   ```
3. Interpret: alpha >= 0.8 near-agreement, 0.67–0.8 tentative, < 0.67 the rubric is ambiguous — fix it before scaling.
4. Read the disagreement, not just the number. Pull the items raters split on; they are either genuinely ambiguous or a rubric gap.
5. Fix the source: tighten the rubric, add examples for the split cases, and re-measure on a fresh overlap.
6. Only adjudicate to a gold label after agreement clears the bar — adjudicating noisy labels entrenches the noise.
7. Record alpha alongside any reported model score; a 0.6-alpha target means the model's ceiling is near the humans' agreement.

```bash
python3 agree.py --labels labels.csv --metric krippendorff-alpha --level ordinal
```

## Pitfalls

- Raw percent agreement inflates when one class dominates; use a chance-corrected metric.
- Three raters with only two overlapping produces no usable estimate.
- Averaging conflicting labels into a fraction hides a rubric that cannot be applied consistently.
- Reporting alpha without n or the metric name is uninterpretable.
- Treating low alpha as annotator laziness when it usually means an under-specified rubric.

## Verification

    python3 agree.py --labels labels.csv --metric krippendorff-alpha   # prints alpha and per-item disagreement

Report: "alpha=0.64 on 90 overlap items (3 raters) — below the 0.67 bar; rubric rewritten for the 12 split items, re-measured alpha=0.79 before scoring."
