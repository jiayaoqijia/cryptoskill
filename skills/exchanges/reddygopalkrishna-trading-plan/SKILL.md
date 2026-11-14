---
name: trading-plan
description: Turn a trade idea into a complete, numbers-first plan - entry (limit, market or pattern pivot), stop options (ATR, structure, swing, pattern, percent), targets (R-multiples or next resistance), reward:risk, invalidation and position size from the account's risk rules, optionally scaled by market regime and saved to the journal. Works for stocks, ETFs, futures (contract multipliers), options underlyings and fractional crypto. Use when the user asks "how should I trade X", "where's my stop", "how many shares", "plan an entry", or after a screener/pattern hit.
license: MIT
metadata:
  author: reddygopalkrishna
  version: "0.2.0"
  pack: trading-skills
---

# Trade Planner (`trading-plan`)

Plan the trade before the trade. Every plan has an entry, a stop, a target and a size.

```bash
python3 scripts/plan.py AAPL                                        # auto: last close, structure/ATR stop, level/2R target
python3 scripts/plan.py AAPL --entry 195.5 --stop 188 --target 215  # user's numbers
python3 scripts/plan.py NVDA --entry pivot --stop pattern           # live chart-pattern trigger
python3 scripts/plan.py TSLA --side short --stop atr:2.5 --target r:2
python3 scripts/plan.py BTC-USD --stop pct:6 --fractional --lot 0.0001
python3 scripts/plan.py ES=F --stop atr:1.5 --multiplier 50          # futures point value
python3 scripts/plan.py AAPL --regime-adjust --save --setup "VCP" --thesis "why + what invalidates it"
```

Level syntax: `--entry price|market|pivot`, `--stop price|atr:M|pct:N|swing|pattern|auto`,
`--target price|r:M|pct:N|resistance|auto`.

## Auto logic

- **Stop (auto):** structural level (pattern low, nearest support, 10-bar swing) if it is 0.8-3 ATR
  away, else 2x ATR. Stops tighter than ~0.7 ATR get a warning - noise will hit them.
- **Target (auto):** next resistance (support for shorts) if it gives at least `min_reward_risk`,
  else 2R with a note that the level may cap the move.
- **Size:** fixed-fractional risk (`risk.risk_per_trade_pct`) of equity from the broker
  (paper by default), capped by `max_position_pct`; rounded to `--lot`.
- **--regime-adjust:** multiplies risk by trading-market exposure (e.g. 50% in a choppy market).

## Presenting a plan

Show the table (entry/stop/target), R:R, size and the watch-outs. Ask whether the user wants to
adjust anything, then hand the exact numbers to **trading-risk**. Use `--save` to record the plan
in the journal so analytics can later compare plan vs. execution.

## Related

trading-size (sizing what-ifs), trading-odds (odds of target before stop),
trading-risk (mandatory before orders), trading-journal.
