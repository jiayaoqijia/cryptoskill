# PRE-REGISTRATION — selection hunt v2
Written 2026-09-11 ~03:00 UTC, **before running anything**. Committed before results exist.

## Why re-open at all
spike-hunt4/5/6/7/8 all tested ONE hypothesis with different stepping: score on trailing
fee-yield + IL over a 15d formation window, hold the top quintile 15d. Five failures of
one idea is not five failures of the hypothesis space. Re-running that scorer a sixth time
would be re-deriving a proven zero, which is forbidden.

What was NEVER tested:
- **Avoidance instead of selection.** Predicting which pools will be BAD, not which will be best.
  The spike-hunt7 attribution already showed bottom-decile loses on all 5 venues — an
  avoidance screen was observed in passing and never tested as a strategy on its own.
- **Persistence of HONESTY rather than of return.** We predict realized return. We never asked
  whether `trustLabel` itself persists — i.e. does a pool whose advertised APR tracked reality
  last window keep doing so next window? That is the question our own product already answers
  retrospectively, and it is a different target variable.
- Stability//dispersion features (fee-yield variance, TVL churn) rather than level features.

## The bar — fixed now, not after seeing results
Identical to the original so results are comparable and I cannot soften it:
- (a) median edge across windows **>= +0.5pp**
- (b) edge positive in **>= 60%** of windows
- (c) pooled random-selection control **p < 0.05**
A large mean with a negative median FAILS (one lucky window carrying it).

## Mandatory guards
1. **Three cutoffs.** Every headline reported at >= 3 formation/holdout lengths. If the winner
   changes across them there is no finding, there is a parameter. (`gate-cannot-audit-its-estimator`)
2. **Decoy.** A deliberately meaningless feature (hash of pool address -> pseudo-random score) is
   scored alongside every real candidate at matched window count. If the decoy also "passes",
   the instrument is measuring noise and the whole run is void.
3. **Cost charged** at 0.1% round-trip on every pick, as before.
4. Adjacent windows share market regime -> not fully independent. Ships as a caveat, never hidden.

## Commitment
If nothing clears the bar, the answer shipped to Jiggy and to judges is "we tested a second,
broader hypothesis space and it also failed" — NOT a softened/hedged/"directional" ranking.
A number that works sometimes, labelled as if it works always, is the exact defect this
project exists to expose. Publishing the second failure is a better submission artifact than
publishing a weak signal.
