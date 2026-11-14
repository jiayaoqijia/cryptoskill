---
name: trading-chart
description: Technical analysis of any stock, ETF, index, forex pair or crypto - trend stage, moving averages, RSI, MACD, ADX, ATR, Bollinger squeeze, Supertrend, volume/OBV, 52-week range, support and resistance levels, and daily vs weekly agreement, rolled into a -100..+100 bias score with reasons. Use when the user asks "what does the chart say", "is X bullish", "analyze X", for support/resistance, indicator values, or wants to test a rule such as price above its 200-day average on a symbol.
license: MIT
metadata:
  author: reddygopalkrishna
  version: "0.2.0"
  pack: trading-skills
---

# Technical Analysis (`trading-chart`)

Deterministic indicator math (no guessing numbers) plus a transparent scoring model.

```bash
python3 scripts/analyze.py AAPL                       # daily + weekly read, markdown
python3 scripts/analyze.py INFY.NS --period 5y --json # full JSON
python3 scripts/analyze.py BTC-USD --interval 1h --period 3mo --no-mtf
python3 scripts/analyze.py AAPL --eval "close > sma(200) and rsi(14) < 40"
python3 scripts/analyze.py --csv my_bars.csv --symbol XYZ
```

Use `--period 2y` or more for daily bars so the 200-SMA and stage analysis are valid.

## What you get

- **Bias + score** (-100..+100) with every point explained (`reasons`). >= +60 strong bullish,
  +25 bullish, -25..+25 neutral, <= -25 bearish.
- **Stage** (Weinstein): 1 basing, 2 advancing, 3 topping, 4 declining.
- **Trend:** SMA20/50/200, EMA21, ADX/DI, Supertrend, trend-template count (x/7).
- **Momentum:** RSI14, MACD, rate of change (1w..12m).
- **Volatility:** ATR and ATR%, Bollinger width and its percentile (<= 10th = squeeze).
- **Volume:** relative volume vs 50-day, OBV direction.
- **Levels:** clustered swing-pivot support/resistance with touches and distance.
- **Higher timeframe:** weekly read; when daily and weekly disagree, say so and suggest smaller size.

## How to present

Lead with the one-line verdict, then the 3-5 readings that matter most for the user's question,
then the levels. Quote numbers exactly as printed. Mention the data source and date.
Never present the score as a forecast or a buy/sell instruction - it summarizes conditions.

## Rule language

`--eval` accepts the same rule language as trading-scanner and trading-backtest
(see `../trading-scanner/references/rule-language.md`), e.g.
`cross_above(ema(20), ema(50))`, `close >= 0.97 * highest(high, 252)`, `bb_width(20) < 5`.

## Related skills

trading-patterns (setups), trading-market (index context), trading-plan (turn a view into entry/stop/target).
