---
name: trading-odds
description: Monte Carlo simulation for traders - estimate the odds a specific setup hits its target before its stop by block-bootstrapping the symbol's own price behaviour, and stress-test a strategy by resampling its trade R-multiples into thousands of equity paths to get realistic return ranges, drawdown percentiles, losing streaks and risk of ruin. Use when the user asks "what are the odds", "how likely is my target", "how bad can drawdowns get", "risk of ruin", or after a backtest or journal review.
license: MIT
metadata:
  author: reddygopalkrishna
  version: "0.2.0"
  pack: trading-skills
---

# Trade Odds (Monte Carlo) (`trading-odds`)

Two questions, two modes:

**1. Is this setup worth it?** (`setup`)
```bash
python3 scripts/mc.py setup AAPL --entry 195 --stop 188 --target 212 --horizon 20
python3 scripts/mc.py setup BTC-USD --entry 64000 --stop 61000 --target 70000 --interval 1h --period 1mo --horizon 48
```
Builds 10,000 future paths from 5-bar blocks of the last 250 bars (keeps gaps, ranges and short-term
momentum), checks stop before target inside each bar, and reports P(target first), P(stop first),
expected R and a verdict versus the breakeven win rate for that reward:risk.

**2. What can this system do to my account?** (`trades`)
```bash
python3 scripts/mc.py trades --csv trades.csv --risk-pct 1 --trades 100 --report mc.html   # from trading-backtest --trades-csv
python3 scripts/mc.py trades --journal --risk-pct 0.5                                     # your real trades
python3 scripts/mc.py trades --r "2.1,-1,-1,0.4,3,-1,-0.6,1.8,-1,2.5" --trades 200
```
Resamples R-multiples into 10,000 sequences: return and max-drawdown percentiles, P(loss),
P(drawdown >= 10/20/30%), risk of ruin, worst losing streaks.

## Interpreting

- Expected R < 0 -> the stop/target pair is poorly placed for how this instrument moves.
- Compare `prob_target_first` with `breakeven_win_rate` (1 / (1 + R:R)).
- Plan for the **95th percentile drawdown**, not the median. If that number would make the user quit,
  risk per trade is too high - use trading-size to find a level they can live with.
- Fewer than ~30 input trades makes the trade-mode output unstable; say so.
- Both modes assume the future resembles the sampled past. They are not forecasts.
