---
name: pre-register-an-ab-test-analysis
description: Use when launching or reading an A/B test. Freezes the primary metric, MDE, alpha, sample size, and stop rule before any data is seen.
---

# Pre-Register an A/B Test Analysis

If the analysis is chosen after the data arrives, the p-value is a story about your search, not the treatment. Freeze the plan first.

## Procedure

1. State one primary metric and its exact definition (numerator and denominator) before launch.
2. Set the decision rule in business units, not p-values: the minimum effect worth shipping (MDE).
3. Compute the required sample per arm from alpha, power, baseline rate, and MDE:
   ```python
   from statsmodels.stats.power import NormalIndPower
   from statsmodels.stats.proportion import proportion_effectsize
   es = proportion_effectsize(0.10, 0.11)            # base 10% -> 11%
   n = NormalIndPower().solve_power(es, power=0.8, alpha=0.05, ratio=1)
   print(int(n) + 1)                                  # per arm, two-sided
   ```
4. Fix alpha at 0.05 two-sided and power at 0.8, and name the segmentation family (which slices count as confirmatory).
5. Declare the stop rule: a fixed horizon at n per arm, or a sequential test with an alpha-spending function — never "look daily and stop when significant".
6. Commit the plan with a timestamp before the first impression; the commit hash is the evidence of ordering.
7. After the test, run exactly the registered primary analysis and report everything else as exploratory.

## Pitfalls

- Peeking at a fixed-horizon test and stopping on the first significant day roughly doubles the false-positive rate.
- Switching the primary metric after launch (HARKing) turns a null into a headline.
- A test powered for a 1-point lift cannot detect the 2-point drop that matters; MDE is a two-sided contract.
- Running until p crosses 0.05 and stopping is a stopping rule chosen by the outcome.
- Pre-registering in a document nobody versions is not a commitment; use the same repo as the experiment config.

## Verification

    git log -1 --format='%H %cI' -- experiments/exp_1234.yaml   # commit time must precede the experiment start

Report: "Plan frozen 2026-09-01 (commit 4f2c9e1), before the 09-03 launch: primary = 7-day purchase conversion, MDE +1.0pt, n=14,900/arm, alpha 0.05 two-sided, fixed horizon."
