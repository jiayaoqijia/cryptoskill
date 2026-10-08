---
name: measure-novelty-and-primacy-effects
description: Use when an A/B result might decay or grow over time. Plots treatment effect by exposure age before extrapolating the launch-week lift.
---

# Measure Novelty and Primacy Effects

Treatment effects are not constant: a redesign often spikes on novelty then decays, and a disruptive change can look bad until users adapt. A single pooled number hides both shapes.

## Procedure

1. Bucket the analysis by `days_since_exposure` (or weeks) and plot the treatment effect per bucket with its interval.
2. Read the shape: novelty = effect high early, decaying toward a smaller steady state; primacy = effect low early, rising later.
3. Extrapolate from the steady state, not the peak. The launch-week lift overstates the durable effect when the curve is decaying.
4. Run the test through at least one full business cycle (a weekly cycle plus the tail of monthly behaviour) before reading a level.
5. Separate the effect from the ramp: if traffic was ramped in over days, exposure age and calendar time are confounded.
6. Check whether the metric's own seasonality coincides with the test window; a holiday inside the run fakes decay.
7. Report both the `peak` and the `settled` effect, and the date the curve flattened.

## Pitfalls

- Calling a win on day 3 of a decay curve commits the novelty trap; a two-week hold often halves it.
- A change to a rarely-visited surface has a long, slow primacy period and looks null for weeks.
- Restarting the test after a bug fix mixes two exposure ages; split the analysis at the fix.
- Aggregating all days equally gives the peak day too much weight when traffic is front-loaded.
- A decaying curve that flattens below the relevance bar is a loss even if the peak was significant.

## Verification

    python3 - <<'PY'
import pandas as pd
d = pd.read_csv('by_day.csv')
d['effect'] = d['treat']/d['n_t'] - d['ctrl']/d['n_c']   # per-day lift
print(d[['day','effect']].tail(10).to_string())
print("peak", round(d['effect'].head(3).mean(),4), "settled", round(d['effect'].tail(7).mean(),4))
PY

Report: "Effect peaks +2.1pt in week 1 and settles at +0.6pt by week 4; extrapolate from the settled value, not the peak, and re-check at week 8 before a full rollout."
