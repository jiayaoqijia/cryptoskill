---
name: trading-journal
description: Keep a structured trading journal - log planned, open and closed trades with entry, stop, target, size, setup, thesis, fees, P&L, R-multiple, hold time, excursions, process grade, tags and notes; import broker trade exports from CSV and export everything back out. Shared by the planner, gate, trading-broker and performance skills. Use when the user wants to log, record or review a trade, add notes, "journal this", import trade history, or asks what trades are open.
license: MIT
metadata:
  author: reddygopalkrishna
  version: "0.2.0"
  pack: trading-skills
---

# Trade Journal (`trading-journal`)

The memory of the trading system. SQLite at `~/.trading-skills/journal.db`.
trading-broker writes to it automatically; this skill is for everything manual.

```bash
python3 scripts/journal.py plan --symbol AAPL --side long --entry 195 --stop 188 --target 212 --qty 70 \
    --setup "VCP" --thesis "3rd contraction, volume dry-up; wrong below 188"
python3 scripts/journal.py open --id 3 --price 195.4 --qty 70
python3 scripts/journal.py open --symbol MSFT --side long --price 410 --qty 20 --stop 398 --setup pullback
python3 scripts/journal.py close --id 3 --price 209.8 --reason target --fees 2.5
python3 scripts/journal.py note --id 3 --text "Held through the shakeout per plan" --grade A --tags patience
python3 scripts/journal.py update --id 3 --stop 196          # trailing the stop
python3 scripts/journal.py list --status open
python3 scripts/journal.py show --id 3
python3 scripts/journal.py import --file broker_export.csv  # symbol,side,qty,entry_price,exit_price,entry_time,exit_time[,stop,fees,setup]
python3 scripts/journal.py export --file journal.csv
```

## What to capture (prompt the user for it)

- **Setup** - a short consistent name (`VCP`, `pullback`, `ORB`, `earnings-gap`) so analytics can
  compare setups. Reuse existing names (`list` shows them).
- **Thesis** - why, and what would prove it wrong.
- **Stop at entry** - R-multiples are computed from the planned stop; without one, R is unknown.
- **Grade (A-F)** - how well the plan was followed, independent of P&L. A losing A-trade is fine;
  a winning F-trade is a warning.
- **Notes** after closing - one lesson per trade.

## Notes

- R-multiple = net P&L / (|entry - planned stop| x qty). Fees are included in P&L.
- Moving the stop with `update` keeps the original planned stop for R; this is deliberate.
- Imported trades without a stop have no R; analytics still use their P&L.
- Use **trading-review** for statistics and coaching across many trades.
