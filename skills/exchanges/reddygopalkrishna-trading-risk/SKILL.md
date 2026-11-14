---
name: trading-risk
description: Mandatory risk checkpoint before any order - verifies stop placement, risk per trade, reward:risk, position size, total portfolio heat, max positions, duplicate exposure, daily loss limit, losing-streak pause, drawdown circuit breaker and the kill switch, then issues a short-lived approval that trading-broker requires. Also shows a live risk dashboard. Use when about to place, submit or confirm any trade, when the user asks "can I take this trade", "am I over-risked", "how much risk do I have on", or whenever trading-broker asks for an approval.
license: MIT
metadata:
  author: reddygopalkrishna
  version: "0.2.0"
  pack: trading-skills
---

# Risk Gate (`trading-risk`)

"No plan, no trade" made mechanical. The gate enforces the user's own limits from `config.risk`.

```bash
python3 scripts/gate.py check --symbol AAPL --side long --entry 195 --stop 188 --target 212 --qty 70 \
    --setup "VCP breakout" --thesis "3 contractions, volume dry-up; invalid below 188"
python3 scripts/gate.py check --symbol AAPL --entry 195 --stop 188 --target 212 --auto-size
python3 scripts/gate.py check --plan 12          # planned trade saved by trading-plan --save
python3 scripts/gate.py status                   # heat, today's P&L, streak, drawdown, kill switch
```

Exit code 0 = PASS / PASS_WITH_WARNINGS (approval issued), 3 = FAIL.

## Checks

| check | rule (config key) |
|---|---|
| kill_switch_off | `~/.trading-skills/KILL_SWITCH` absent |
| stop_defined | stop below entry (long) / above (short) |
| risk_per_trade | risk <= `risk_per_trade_pct` |
| reward_risk | (target-entry)/(entry-stop) >= `min_reward_risk` (warn if no target) |
| position_size | notional <= `max_position_pct` of equity |
| portfolio_heat | open risk + this trade <= `max_open_risk_pct` |
| max_positions | open positions < `max_open_positions` |
| daily_loss_limit | today's realized loss < `max_daily_loss_pct` |
| loss_streak | consecutive losses < `max_consecutive_losses` |
| max_drawdown | equity drawdown from journal peak < `max_drawdown_pct` |
| no_duplicate / plan_documented | warnings |

Equity and positions come from the configured broker (paper by default); open risk from the journal.

## Rules for the agent

- Run the gate for **every** order, paper or live. Never bypass, edit approval files, or loosen
  limits to make a trade pass. If it fails, report which checks failed and offer fixes
  (reduce qty, move the stop to a structural level, skip the trade).
- Limits change only when the user explicitly asks, via `trading-setup set risk.<key> <value>`.
- A PASS approval expires (`risk.approval_ttl_minutes`, default 30) and covers one exact
  symbol/side/qty/stop. Changing any of those needs a new check.
- When the losing-streak or daily-loss check fails, the right answer is to stop trading for the
  day - say so plainly.
