---
name: set-a-ship-threshold-with-a-margin
description: Use when deciding whether a model or prompt change ships. Gates on the lower confidence bound of the metric against a pre-set threshold, not the point estimate.
---

# Set a Ship Threshold with a Margin

Shipping on the point estimate ships noise. Decide on the lower bound of the interval, and only when it clears the threshold you set before the run.

## Procedure

1. Write the gate as a rule with a number: "ship if the 95% lower bound of accuracy >= 0.80 AND no slice < 0.70".
2. Compute the lower bound, not the mean: `lo = p - 1.96*sqrt(p*(1-p)/n)`.
   ```python
   import math
   def lower(p, n): return p - 1.96 * math.sqrt(p * (1 - p) / n)
   print(round(lower(0.83, 800), 3))   # 0.805
   ```
3. Gate on the same metric you optimised, measured on the frozen test set. A dev-set gate is not a gate.
4. Add the regression guard: no metric may drop more than X below the previous release. Ship = pass gate AND no regression.
5. Make the gate block automatically in CI so a merge cannot bypass it:
   ```bash
   python3 eval.py --gate config/gauntlet.yaml || { echo "gate failed"; exit 1; }
   ```
6. Record which gate version applied; moving the bar after a near-miss is the foul this blocks.
7. If the gate fails, the decision is "no ship" — not "ship and watch". Watching is for feature flags, not a failed quality bar.

```yaml
gate:
  metric: accuracy
  lower_bound_min: 0.80
  slices:
    max_drop_vs_last_release: 0.03
```

## Pitfalls

- Gating on the mean lets a lucky run through; the bound is the whole point.
- A threshold chosen after seeing the result is not a threshold.
- One aggregate gate hides a slice going to zero — pair it with the no-slice rule.
- Ignoring n: the same 0.83 is "ship" at n=8000 and "inconclusive" at n=50.
- Letting a human override a failed gate with no written reason turns the gate into a suggestion.

## Verification

    python3 eval.py --gate config/gauntlet.yaml; echo "exit=$?"   # exit 0 = passed

Report: "Gate: accuracy lower bound 0.805 >= 0.80, worst slice 0.72 >= 0.70, no regression > 3% — PASS, shipped under gate v3."
