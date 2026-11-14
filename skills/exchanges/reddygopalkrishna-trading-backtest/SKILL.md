---
name: trading-backtest
description: Backtest trading strategies written as simple rules on one or many symbols in any market - next-bar-open execution with no look-ahead, commissions and slippage, ATR/percent/rule-based stops, R or percent targets, trailing stops, time exits, risk-based position sizing, max concurrent positions with ranking, benchmark comparison, in-sample vs out-of-sample split and a self-contained HTML report. Use when the user asks "does this strategy work", "backtest X", "test a moving-average crossover", "what if I bought when RSI was below 30", or wants to validate an idea before trading it.
license: MIT
metadata:
  author: reddygopalkrishna
  version: "0.2.0"
  pack: trading-skills
---

# Backtester (`trading-backtest`)

Test the idea on history before risking money. Honest defaults: costs on, no look-ahead, caveats printed.

```bash
python3 scripts/backtest.py --spec assets/strategies/rsi2-pullback.json --universe AAPL,MSFT,NVDA,AMZN,GOOGL \
    --oos-start 2021-01-01 --report rsi2.html
python3 scripts/backtest.py SPY --entry "cross_above(sma(50), sma(200))" --exit "cross_below(sma(50), sma(200))" \
    --stop none --start 2005-01-01 --report golden_cross.html
python3 scripts/backtest.py --spec my.json --universe list.txt --set n=20 --set mult=3
python3 scripts/backtest.py --spec my.json --csv-dir ./data --universe A,B,C --trades-csv trades.csv --json
```

Example strategies: `assets/strategies/*.json` (RSI-2 pullback, Donchian breakout, golden cross,
VCP-style breakout, Bollinger mean reversion, Supertrend trend-follow).

## Workflow

1. Write the idea as rules - see [strategy-spec.md](references/strategy-spec.md) and the rule language
   in `../trading-scanner/references/rule-language.md`. Validate rules with `screen.py --check`.
2. Use 10+ years (`--period 10y` default, or `--start`) and several symbols, not one hand-picked chart.
3. Always set `--oos-start` (e.g. the last 30% of the period) and compare in- vs out-of-sample.
4. Generate `--report` and send the HTML to the user.
5. Feed the trade R-multiples to **trading-odds** to see realistic drawdown ranges.
6. Try 2-3 nearby parameter values with `--set`. If results collapse when a parameter moves slightly,
   the edge is not robust - say so.

## Presenting results

Lead with: return vs benchmark, max drawdown vs benchmark, number of trades, avg R, and the
out-of-sample verdict. Always include the printed caveats. Never describe backtest returns as
expected future returns, and never recommend live trading on fewer than ~100 trades of evidence.
