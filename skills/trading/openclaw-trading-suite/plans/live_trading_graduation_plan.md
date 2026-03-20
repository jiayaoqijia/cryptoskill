# Live Trading Graduation Plan

## Overview
This plan outlines the steps to transition from paper trading (simulated) to live trading (real capital) for our agentic trading system. The goal is to prove consistent profitability, robust risk management, and reliability before risking real money. All steps must be completed and reviewed by the user before advancing.

## Phase 1: Paper Trading Mastery (Current)
**Objective:** Demonstrate reliable performance in simulation to build confidence and refine strategies.

### Milestones
- **Consistent P&L**: Achieve 3-5% monthly returns over 3-6 months with <10% max drawdown.
- **Strategy Validation**: Test 5+ swing trade strategies (e.g., BTC pumps, altcoin breakouts) using technical indicators (RSI, MACD, support/resistance).
- **Risk Adherence**: Never exceed position caps (5% per trade), use stop losses (3% risk), and maintain diversification (<30% in one asset).
- **Data Sources**: Use free/low-cost APIs (Alpaca paper, Finnhub, TAAPI) for quotes, indicators, and backtests.
- **Logging & Review**: Log all trades, decisions, and rationales in `trading_logs.md`. Weekly user reviews for adjustments.

### Tools and Skills
- Paper trading via Alpaca API (paper account).
- Backtesting with historical data.
- HEARTBEAT.md tasks for ongoing monitoring.

### Exit Criteria
- 3 months of positive P&L with no major breaches.
- User approval: "Proceed to Phase 2."

## Phase 2: Backtesting & Stress Testing
**Objective:** Validate strategies against historical data and simulate worst-case scenarios.

### Milestones
- **Backtest Campaigns**: Run backtests on 1-2 year historical data for each strategy (e.g., BTC 2020-2024 cycles).
- **Stress Tests**: Simulate black swan events (e.g., 50% BTC crash, API failures) and ensure <20% total drawdown.
- **Optimization**: Fine-tune parameters (e.g., entry/exit thresholds) via ML algorithms in the investing repo.
- **Edge Case Handling**: Test for gaps, weekends, high volatility (BTC >10% range).

### Tools and Skills
- Strategy-optimizer skill for parameter tuning.
- Profit-forecaster for simulations.
- Log API errors and fallbacks.

### Exit Criteria
- Backtests show >1:3 risk/reward average.
- Stress tests pass without catastrophic losses.
- User approval: "Proceed to Phase 3."

## Phase 3: Small-Scale Live Testing
**Objective:** Dip toes in live waters with micro-trades to validate real-market behavior.

### Milestones
- **Micro-Trades**: Start with $100-500 per trade on low-vol assets (e.g., stablecoins or blue-chip alts).
- **Gradual Scaling**: Increase size only after 10+ successful trades (no losses >5%).
- **Real-Time Monitoring**: Use live APIs for execution, with manual overrides required for >$500 trades.
- **Error Handling**: Test fallbacks (e.g., if Alpaca down, pause trading).

### Tools and Skills
- Switch to Alpaca live account (small balance).
- HFT guardrails from HEARTBEAT.md.
- Daily P&L reports to user.

### Exit Criteria
- 20+ live trades with net positive P&L.
- No breaches of risk rules.
- User approval: "Proceed to Phase 4."

## Phase 4: Full Live Graduation
**Objective:** Go full live with automated loops, but under strict oversight.

### Milestones
- **Autonomous Loops**: Enable trading bot for swing trades, with daily caps and pauses.
- **Portfolio Management**: Maintain <20% exposure, rebalance weekly.
- **Performance Tracking**: Monthly reports with 3-5% target P&L.
- **Continuous Improvement**: Integrate new data (e.g., sentiment once proven) and optimize.

### Tools and Skills
- Full Alpaca live integration.
- Cron jobs for overnight analysis.
- User veto power on all trades >$1000.

### Exit Criteria
- 6 months of live positive P&L.
- Proven resilience (e.g., survived a market dip).
- User confidence: "System is live."

## Risk Management Guardrails (Always Active)
- **Position Limits**: Max 5% per trade, 20% total exposure.
- **Stop Losses**: 3% per trade, circuit breakers at 10% drawdown.
- **Diversification**: No >30% in one asset; spread across strategies.
- **Rate Limits**: <10 trades/min to avoid flags.
- **Manual Overrides**: All high-risk actions require user confirmation.
- **Logging**: Full audit trail for every decision.

## Contingencies
- **Failures**: If drawdown >10% in paper/live, pause and review.
- **API Issues**: Fallback to manual or pause.
- **Market Events**: Halt during extreme volatility (BTC >20% daily move).
- **User Involvement**: Weekly check-ins; immediate halt on user request.

## Timeline
- **Phase 1**: Ongoing (aim 3 months).
- **Phase 2**: 1 month post-Phase 1.
- **Phase 3**: 1-2 months post-Phase 2.
- **Phase 4**: Ongoing post-Phase 3.

This plan ensures we prioritize safety, proof of concept, and ethical trading. Review and approve each phase.
