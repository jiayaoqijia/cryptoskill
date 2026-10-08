---
name: audit-a-benchmark-for-saturation
description: Use when a benchmark is nearly maxed out or nearly floored. Tests whether it still discriminates between systems or only ranks noise.
---

# Audit a Benchmark for Saturation

A benchmark at 99% cannot tell two good systems apart — the differences are rounding. Check discrimination before you quote a rank off it.

## Procedure

1. Look at the score distribution across systems, not one score. If the top ten span 1 point, the benchmark is saturated for that tier.
2. Compute per-item discrimination: items almost everyone gets right (p>0.95) add no signal. Report the fraction of items in the useful band (0.3<p<0.9).
3. Compute a split-half reliability: split items in half, rank systems on each half, and correlate the rankings. Low rank-correlation means the leaderboard order is noise.
   ```python
   from scipy.stats import spearmanr
   rho, _ = spearmanr(rank_half_a, rank_half_b); print("rank reliability", round(rho, 3))
   ```
4. Check floor effects the same way; a benchmark everyone fails at 5% is equally undiscriminating.
5. Compare the top systems' CIs. If they overlap, the rank is not supported, saturated or not.
6. Prefer a harder variant or a held-out fresh set if you need to separate near-tied systems.
7. State the saturation explicitly: "MMLU-tier saturated for frontier models; use a fresh set for ranking."

```python
band = sum(0.3 < p < 0.9 for p in item_accuracies) / len(item_accuracies)
```

## Pitfalls

- Quoting a 0.5-point lead as a rank when every leaderboard CI overlaps.
- Saturation applies per tier; a benchmark at 60% for small models still discriminates there.
- Adding harder items fixes saturation only if they are valid; flawed hard items add noise, not signal.
- Assuming a new benchmark is unsaturated — check its item difficulty band too.
- Rank reliability across halves is the honest test; a single full-set ranking hides instability.

## Verification

    python3 bench.py --scores leaderboard.csv --split-half-rank   # prints rank reliability rho

Report: "Top-10 span 0.8 points, split-half rank reliability rho=0.31 — the order is noise; benchmark saturated, use the fresh set to separate them."
