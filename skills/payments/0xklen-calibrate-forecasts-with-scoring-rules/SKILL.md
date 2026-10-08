---
name: calibrate-forecasts-with-scoring-rules
description: Use when making or reviewing probabilistic predictions. Scores them against outcomes with proper rules and checks calibration, not just a hit rate.
---

# Calibrate Forecasts With Scoring Rules

A forecaster who says "90% likely" should be right about 90% of the time across many such calls. Accuracy at a threshold hides whether the probabilities are honest; proper scoring rules do not.

## Procedure

1. Publish the probability, not just a direction: "0.7", not "likely". A non-probabilistic call cannot be scored.
2. Score with a proper rule. Brier score for binary outcomes:
   ```python
   brier = sum((p - o)**2 for p, o in zip(probs, outcomes)) / len(outcomes)  # 0 best, 0.25 = coin flip
   ```
   Log loss for the sharper penalty on confident errors: `-mean(o*log(p) + (1-o)*log(1-p))`.
3. Check calibration, not only the score. Bin forecasts (0–0.1, …, 0.9–1) and plot mean predicted vs observed frequency; points on the diagonal are calibrated.
4. Compare to a base rate. Always-beats-nothing baselines: predict the historical frequency, or the majority class. Beat the baseline or say you did not.
5. For continuous/interval forecasts, score with the interval and the coverage: a 90% interval should contain the outcome ~90% of the time.
6. Score in advance and keep an immutable log (`forecasts.csv`: date, id, p, resolution_date); scoring invented after the fact is not calibration.
7. Report reliability (calibration), resolution (ability to separate), and the reliability diagram together.

```python
import numpy as np
probs, outs = np.array(probs), np.array(outs)
print("Brier", np.mean((probs - outs)**2), "base-rate Brier", np.mean((outs.mean() - outs)**2))
```

## Pitfalls

- Hit rate rewards overconfidence; a 60%-right forecaster who always says "99%" scores worse on Brier than a cautious one.
- Small n makes calibration noise dominate; below ~100 scored forecasts treat the diagram as suggestive only.
- Scoring only the times you were confident is selection on the forecast, not the outcome.
- Base rates drift; a model calibrated on 2019 frequencies can be miscalibrated on 2024 regimes.
- Refusing to forecast with a small edge is itself a forecast of "no edge" — record and score it.

## Verification

    python3 score.py --log forecasts.csv

Report: "412 scored forecasts, Brier 0.14 vs 0.21 base rate; reliability diagram within ±0.07 over all bins."
