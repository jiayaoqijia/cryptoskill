<!--
  Imported from: https://github.com/mitchellbernstein/openquant
  Source Path: SKILLS/openquant-trading/SKILL.md
  Curated for awesome-quant-skills
-->

---
name: openquant-trading
version: 1.0.0
description: Analyze stocks, generate trading signals, manage risk, and execute paper trades using the OpenQuant MCP server
triggers:
  - stock analysis
  - ticker analysis
  - trading signal
  - insider trading
  - risk assessment
  - portfolio
  - backtest strategy
  - paper trade
  - buy stock
  - sell stock
  - position size
  - market data
---

# OpenQuant Trading Skill

## When This Skill Activates

Activate this skill when the user:
- Asks about a stock or ticker (e.g., "What do you think of AAPL?")
- Wants trading signals or strategy recommendations
- Mentions insider trading, risk, VaR, or position sizing
- Wants to check their portfolio or execute a trade
- Asks about backtesting or strategy validation
- Uses terms like "analyze", "signal", "backtest", "Kelly", "insider buy"

## Prerequisites

The OpenQuant MCP server must be running. Start it:
```bash
pip install openquant-cli[mcp]
openquant-mcp
```

MCP endpoint: `http://localhost:8000/sse` (SSE transport)
Server name: `openquant`

## Common Workflows

### Workflow 1: Analyze a Stock

Use when: User asks about a ticker or wants a stock opinion.

1. Call `openquant_analyze(ticker="SYMBOL", days=90)`
2. Review the result: current_price, insider score/label, risk level, VaR, max drawdown
3. If insider score is interesting (|score| > 25), call `openquant_insider_scan(ticker="SYMBOL")` for detail
4. Summarize for the user: price, insider sentiment, risk level, and whether it's worth deeper investigation
5. Do NOT execute any trades — this is research mode

### Workflow 2: Get a Trading Signal

Use when: User wants a buy/sell recommendation for a ticker.

1. Call `openquant_strategy_list()` if user doesn't specify a strategy
2. Call `openquant_strategy_run(strategy_name="STRATEGY", ticker="SYMBOL")`
3. Review: action (BUY/SELL/HOLD), confidence (0-100), entry_price, stop_loss, take_profit, position_size_pct, reasoning
4. If confidence < 40: tell the user the signal is weak, suggest monitoring
5. If confidence >= 40: present the signal with all details but do NOT execute without confirmation

### Workflow 3: Validate a Strategy

Use when: User wants to know if a strategy works before using it.

1. Call `openquant_backtest(strategy_name="STRATEGY", ticker="SYMBOL", days=252)`
2. Review: total_trades, win_rate, total_return, max_drawdown, sharpe_ratio, avg_holding_days
3. Flag concerns: win_rate < 50%, max_drawdown > 20%, sharpe < 0.5
4. Present the backtest results with interpretation

### Workflow 4: Execute a Trade

Use when: User explicitly wants to place a trade.

1. Call `openquant_portfolio_status()` to check current balance and positions
2. Call `openquant_analyze(ticker="SYMBOL")` for the current price
3. Call `openquant_strategy_run(strategy_name="STRATEGY", ticker="SYMBOL")` for a signal
4. Call `openquant_risk_assessment(tickers="SYMBOL", days=252)` — MANDATORY before execution
5. Present full trade plan to user: action, shares, price, total cost, risk metrics
6. Get explicit user confirmation (e.g., "Should I execute this trade?")
7. Only if confirmed: call `openquant_trade_execute(action="BUY", ticker="SYMBOL", shares=N, price=X)`
8. Call `openquant_portfolio_status()` to confirm the trade went through

### Workflow 5: Portfolio Review

Use when: User wants to check their portfolio or recent trades.

1. Call `openquant_portfolio_status()` for current state
2. Call `openquant_trade_history(limit=20)` for recent trades
3. Summarize: total value, P&L, position breakdown, recent activity

## Tool Reference

| Tool | Params | Returns | Mutates State |
|------|--------|---------|---------------|
| `openquant_analyze` | `ticker`, `days=90` | Price, insider, risk | No |
| `openquant_insider_scan` | `ticker`, `days=90` | Score, patterns, alerts, trade counts | No |
| `openquant_risk_assessment` | `tickers` (csv), `days=252` | Risk level, VaR, drawdown, Kelly, sizes | No |
| `openquant_strategy_list` | — | 4 strategies with descriptions | No |
| `openquant_strategy_run` | `strategy_name`, `ticker` | Action, confidence, prices, size, reasoning | No |
| `openquant_backtest` | `strategy_name`, `ticker`, `days=252` | Trades, win rate, return, drawdown, Sharpe | No |
| `openquant_portfolio_status` | — | Balance, positions, P&L, achievements | No |
| `openquant_trade_execute` | `action`, `ticker`, `shares`, `price` | Success, cost, new balance | YES |
| `openquant_trade_history` | `limit=20` | Trade list | No |
| `openquant_game_status` | — | Leaderboard, stats | No |

## Signal Interpretation

### Strategy Results
- **action**: BUY / SELL / HOLD
- **confidence**: 0-100. Only trade if >= 40.
- **position_size_pct**: Already 0.25x Kelly, capped at 10%. Trust this value.

### Agent Signals (-1.0 to +1.0)
- > +0.3: BULLISH | -0.3 to +0.3: NEUTRAL | < -0.3: BEARISH

### Insider Scores (-100 to +100)
- >= +60: STRONG BUY | >= +25: BUY | -24 to +24: NEUTRAL | <= -25: SELL | <= -60: STRONG SELL

## Risk Rules

1. **0.25x Kelly only** — position_size_pct from tools is already quarter-Kelly. Do not scale up.
2. **10% max position** — never exceed 10% of portfolio in one ticker. System enforces this.
3. **Confidence >= 40** — do not trade on weak signals.
4. **Risk assessment required** — always call `openquant_risk_assessment` before `openquant_trade_execute`.
5. **Multi-factor alignment** — prefer when 2+ agents agree on direction.

## QuantFetch Data Units

When reading data from QuantFetch (optional, requires `QUANTFETCH_API_KEY`):

| Data | Unit | Example | Convert |
|------|------|---------|---------|
| EPS | Cents | 250 | Divide by 100 → $2.50 |
| Revenue | Thousands | 50000 | Divide by 1000 → $50M |
| Trade amounts | Dollars | 500000 | Use as-is → $500K |

## Common Pitfalls

1. **Forgetting risk assessment before trades** — This is the #1 mistake. Always run `openquant_risk_assessment` before `openquant_trade_execute`. No exceptions.

2. **Overriding Kelly sizing** — The `position_size_pct` from strategy results is already 0.25x Kelly. Do not multiply it by 4 or use full Kelly. Quarter-Kelly is deliberate to reduce drawdowns.

3. **Trading on low confidence** — Confidence < 40 means HOLD. Don't execute just because the user is enthusiastic. Explain that the signal is weak and suggest monitoring.

4. **Ignoring risk level** — If `openquant_risk_assessment` returns risk_level = "HIGH", flag this clearly to the user before proceeding. Consider reducing position size further.

5. **Mixing up data units** — QuantFetch reports EPS in cents and revenue in thousands. Always divide: EPS/100, revenue/1000 before presenting to users.

6. **Executing without confirmation** — Even in paper mode, always show the trade plan and get explicit confirmation before calling `openquant_trade_execute`.

7. **Treating agent signals as strategy signals** — Agent signals are -1.0 to +1.0 (5 agents). Strategy confidence is 0-100 (combined result). They are different scales. Don't compare them directly.

8. **Forgetting to check existing positions** — Before buying, call `openquant_portfolio_status` to see if you already hold the ticker. Avoid doubling up unintentionally.

9. **Using the wrong strategy for the situation** — `earnings-surge` is for earnings season, not random entry. `value-deep` is for long-term holds, not quick trades. Match strategy to the user's intent.

10. **Not backtesting** — Before trusting a strategy's signals, run `openquant_backtest` to verify it has a positive expected return. A strategy that generates lots of BUY signals with a 30% win rate will lose money.

## Strategies

| Name | Style | Time Horizon | Key Trigger |
|------|-------|-------------|-------------|
| `insider-momentum` | Momentum | Short-term (30 days) | 3+ insider buys/week or CEO purchase |
| `value-deep` | Value | Long-term | P/E < 15, ROE > 15%, D/E < 0.5, insider buy |
| `earnings-surge` | Event | Short-term (10 days) | Earnings estimate revisions + insider buy |
| `technical-breakout` | Trend | Medium-term | 50-day SMA breakout + 2x volume + insider buy |
