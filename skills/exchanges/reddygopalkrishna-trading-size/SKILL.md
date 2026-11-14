---
name: trading-size
description: Calculate exactly how much to buy or sell - fixed-fractional risk sizing from entry and stop, risk-amount sizing, lot/contract sizes with futures multipliers and margin, fractional crypto units, position-size tables, Kelly fraction, volatility-target sizing and risk-of-ruin. Pure math, no data or API needed. Use when the user asks "how many shares/lots/coins", "how much should I risk", "what if I risk 2%", about Kelly criterion, or leverage and margin math.
license: MIT
metadata:
  author: reddygopalkrishna
  version: "0.2.0"
  pack: trading-skills
---

# Position Sizer (`trading-size`)

The single most important number in a trade is its size. This skill never guesses it.

```bash
python3 scripts/size.py risk --equity 50000 --entry 120 --stop 114 --risk-pct 1
python3 scripts/size.py risk --equity 50000 --entry 120 --stop 114 --risk-amount 400 --target 135
python3 scripts/size.py risk --equity 2000000 --entry 22500 --stop 22350 --lot 50 --margin-pct 12   # futures lot
python3 scripts/size.py risk --equity 10000 --entry 64000 --stop 61000 --fractional --lot 0.0001     # crypto
python3 scripts/size.py table --equity 50000 --entry 120 --stop 114      # 0.25% .. 2% side by side
python3 scripts/size.py kelly --win-rate 0.45 --payoff 2.2
python3 scripts/size.py vol --equity 100000 --price 50 --annual-vol 35 --target-vol 10
python3 scripts/size.py ruin --win-rate 0.45 --payoff 2 --risk-pct 1 --ruin-pct 30
```

`--equity` defaults to config `account.equity`; `--risk-pct` defaults to `risk.risk_per_trade_pct`.

## Formula

`qty = floor_to_lot( equity x risk% / (|entry - stop| x multiplier + fee_per_unit) )`,
then capped by `--max-position-pct` and `--cash`. The output names the **binding constraint**
(risk, max_position or cash) - when it is not "risk", the actual risk is lower than requested.

- **Futures/F&O:** `--multiplier` = point value per contract unit, `--lot` = exchange lot size,
  `--margin-pct` = margin as % of notional (affects capital required, not risk).
- **Options:** size on premium at risk: entry = premium paid, stop = premium exit level, `--multiplier` = contract size.
- **Crypto:** `--fractional --lot 0.0001`.

## Guidance to give

- 0.5-1% risk per trade is the common professional range; 2% is aggressive.
- Show the `table` when the user is unsure - it makes the trade-off visible
  (`losses_to_-20%` = losing streak that produces a 20% drawdown).
- Kelly assumes the edge is known exactly. Recommend at most quarter-Kelly, and never Kelly on a
  backtest with fewer than ~100 trades.
