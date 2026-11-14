---
name: trading-review
description: Analyse trading performance from the journal or any trades CSV - win rate, payoff, profit factor, expectancy, R-multiples, SQN, drawdown and streaks, broken down by setup, side, symbol, weekday and month - plus rule-based coaching that flags cutting winners early, holding losers, stops not honoured, weak setups and luck concentration, with an HTML report. Use when the user asks "how am I doing", "review my trades", for a weekly or monthly review, "what's my best setup", "why am I losing", or wants a trading report card.
license: MIT
metadata:
  author: reddygopalkrishna
  version: "0.2.0"
  pack: trading-skills
---

# Performance Review (`trading-review`)

Turn the journal into decisions: what to do more of, what to stop.

```bash
python3 scripts/review.py                                # all closed trades
python3 scripts/review.py --period week                  # weekly digest (also month, quarter, year)
python3 scripts/review.py --since 2026-01-01 --report review.html
python3 scripts/review.py --setup VCP                    # one setup
python3 scripts/review.py --csv trades.csv               # trading-backtest --trades-csv or a broker export
```

## What it reports

- **Core stats:** net P&L, win rate, avg win/loss, payoff ratio, profit factor, expectancy,
  avg/median/total R, SQN, max drawdown, win/loss streaks, hold time of winners vs losers.
- **Breakdowns:** by setup, side, month, weekday, top symbols.
- **Coaching** (rule-based, explained): negative expectancy, losses larger than 1R (stops not
  honoured), holding losers longer than winners, early profit-taking, best/worst setup,
  losing-streak behaviour, process grade vs results, missing stops, profit concentration.

## How to run a review with the user

1. Run the review (offer `--report` for a shareable HTML file).
2. Lead with 3 things: expectancy (are they making money per trade?), the biggest leak
   (first coaching point), and the best setup.
3. Turn insights into one or two concrete rule changes, e.g. "risk 0.5% on breakout trades until
   avg R > 0 over the next 20", and offer to save them with trading-setup.
4. Suggest trading-odds `trades --journal` to see what the current edge implies for drawdowns.

Be direct about losing results, without moralising. Fewer than ~20 trades -> say conclusions are tentative.
