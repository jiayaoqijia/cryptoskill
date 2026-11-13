<!--
  Imported from: https://github.com/saksham10arora-dotcom/quant-skills
  Source Path: skills/backtest-review/SKILL.md
  Curated for awesome-quant-skills
-->

---
name: backtest-review
description: Review a trading strategy or backtest for look-ahead bias, overfitting, and statistical validity. Use when the user shares backtest code, equity curves, Sharpe ratios, or asks whether a trading signal is real.
---

# Backtest Review

Review any strategy artifact in this order. Do not skip steps; most fatal flaws live in step 2.

## 1. Inventory before judging

Identify: universe, rebalance frequency, signal definition, execution assumptions, cost model, in-sample vs out-of-sample split, number of variants tried. If any of these are unstated, ask before analyzing.

## 2. Look-ahead sweep (kills most strategies)

Check every data access for information that would not exist at decision time:
- Full-sample normalization (z-scores, min-max) computed across the whole history
- Signals using close prices of day t to trade day t
- Fundamentals joined without point-in-time availability dates
- Survivorship: universe built from today's index membership
- Targets shifted the wrong direction (`df.shift(-1)` used as feature instead of label)

Report each finding with file and line references.

## 3. Multiple testing honesty

Ask: how many total variants were tried before this one? Apply these rules of thumb:
- Under ~5 trials: judge the raw statistics
- 5-50 trials: require out-of-sample confirmation on data never touched during iteration
- 50+: demand explicit deflation analysis (deflated Sharpe ratio, Bailey & Lopez de Prado); a Sharpe under 1 is presumptively noise at this search scale

## 4. Distribution sanity

Compute and report: skewness, kurtosis, max drawdown, longest drawdown duration, lag-1 autocorrelation of returns.
- |autocorrelation| significant at sqrt(n) > 2 → suspect smoothed marks or stale fills
- Kurtosis > 6 → warn that Sharpe understates tail risk
- Win rate > 65% with positive skew on daily bars → check for hidden short-vol exposure

## 5. Verdict format

Deliver exactly:
```
VERDICT: REAL / UNPROVEN / LIKELY ARTIFACT
Fatal issues: [list or none]
Statistics: [Sharpe, PSR-style confidence note, DD]
Next test: [single highest-value next action]
```

Be direct. A kind lie about a strategy costs more than a harsh truth.
