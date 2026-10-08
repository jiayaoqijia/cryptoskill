---
name: detect-sample-ratio-mismatch
description: Use when an A/B test's randomisation may be broken. Tests the observed arm split against the intended ratio before reading any treatment metric.
---

# Detect Sample Ratio Mismatch

If the split is not the ratio you designed, the randomisation or the logging is broken and every downstream metric is suspect. SRM is the first check, always.

## Procedure

1. Count units (users, not events) per arm in the assignment log, not in the outcome table where filtering can differ by arm.
2. Test observed against intended with chi-square; treat p below 0.001 as failure and report the observed ratio:
   ```python
   from scipy.stats import chisquare
   obs = [49_120, 50_880]; exp = [50_000, 50_000]
   chi2, p = chisquare(obs, exp)
   print(f"ratio {obs[0]/sum(obs):.4f}, chi2={chi2:.1f}, p={p:.2e}")
   ```
3. A ratio near 0.4965 with large n can still be a real SRM; use the test, not a by-eye tolerance band.
4. If SRM is present, stop. Check the assignment hash, the fallback when the experiment service times out, and any redirect or capping logic that drops an arm.
5. Look for asymmetric filtering: bot removal, ad-blocker drop, or an SDK that errors only in one variant.
6. Re-run the assignment in a sandbox on a replay of traffic and compare; a stable SRM points to the sampler, an intermittent one to the logger.

## Pitfalls

- Checking the ratio in the analysed (post-filter) table hides drop-out that is arm-dependent.
- Weighted or ramp-up experiments (10% then 50%) produce a moving ratio; measure inside a fixed window.
- Counting events instead of users exaggerates the arm whose users have more sessions.
- A p-value between 0.001 and 0.05 is worth a look but is not an automatic halt; a deliberate threshold avoids noise-driven restarts.
- Excluding SRM because "the result still looks plausible" is how broken experiments ship.

## Verification

    python3 -c "from scipy.stats import chisquare; print(chisquare([49120,50880]).pvalue)"
    # p < 0.001 -> halt the analysis and investigate the sampler

Report: "SRM check: 49,120 / 50,880 (ratio 0.4912), chi2=61.8, p=4e-15 — halt. Randomisation is asymmetric; metrics suppressed until the assignment path is fixed."
