---
name: trading-start
description: Start here for anything trading - routes a goal (find trades, read news and results, track insiders, analyse a chart, time an entry, plan, size, backtest, place orders, set alerts, review performance) to the right trading-skills, runs the end-to-end idea-to-trade workflow, and produces a daily trading brief combining market regime, risk status, open positions versus stops, a watchlist screen and live chart patterns, designed for scheduled pre-market and end-of-day runs. Use when the user asks "how do I use these trading skills", "what should I do today", for a morning or daily brief, a trading routine, or automation of their trading workflow.
license: MIT
metadata:
  author: reddygopalkrishna
  version: "0.2.0"
  pack: trading-skills
---

# Trading Start (`trading-start`)

The front door to the trading-skills pack.

## Route the request

| user wants | skill |
|---|---|
| first-time setup, risk limits, connect broker | trading-setup |
| prices, history, CSV export | trading-data |
| "what does the chart say", levels, indicators | trading-chart |
| setups: VCP, breakout, flag, cup & handle | trading-patterns |
| "how's the market", exposure | trading-market |
| find / filter / scan stocks | trading-scanner |
| entry, stop, target, size for an idea | trading-plan |
| sizing math, Kelly, lots, leverage | trading-size |
| "can I take this trade", risk dashboard | trading-risk |
| test a strategy on history | trading-backtest |
| odds of a setup, drawdown ranges | trading-odds |
| option chain, Greeks, implied volatility, PCR, max pain, option strategy payoff | trading-fno |
| log / annotate trades | trading-journal |
| "how am I doing", weekly review | trading-review |
| buy, sell, cancel, positions, kill switch | trading-broker |
| "any news on X", why is it moving, morning briefing | trading-news |
| results, margins, EPS, "how was the quarter" | trading-earnings |
| Pelosi / Congress trades, insider buying, bulk/block deals | trading-insiders |
| "tell me when to get in", opening-range breakout, intraday trigger | trading-entry |
| "alert me when", watch my stop, market open/close | trading-alerts |

If setup has never been run (`~/.trading-skills/config.json` missing), start with trading-setup.

## Daily brief

```bash
python3 scripts/brief.py --watchlist assets/watchlists/us-mega-caps.txt
python3 scripts/brief.py --watchlist ~/my_list.txt --preset breakout-volume --patterns vcp,breakout --report brief.html
python3 scripts/brief.py --index ^GSPC ^NDX --json
```

Sections: regime per index, risk status (open risk, today's P&L, streak, kill switch), open
positions with open R and distance to stop (flags "near stop" / "STOP HIT?"), screen matches,
live patterns >= `--min-score`. Presets: trend-template, breakout-volume, oversold-in-uptrend,
near-52w-high, squeeze (or `--rule`).

## Workflows

See [workflows.md](references/workflows.md): first-time setup, idea -> trade, strategy research,
daily routine, automation, risk-off day.

## Principles to uphold in every conversation

1. **Risk first.** Every trade has a stop and a size before it has a reason to exist.
2. **Process over prediction.** Indicators and simulations describe the past; say so.
3. **Human in the loop for money.** Orders go preview -> explicit user confirmation -> submit.
4. **Paper before live.** Suggest paper trading any new strategy; live trading is opt-in.
5. **Honesty about results.** Report losses, small samples and caveats plainly.

This pack is an educational and research tool, not financial advice.
