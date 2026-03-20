# System Orchestration

## Agent/tool mapping in this repository

- `market-data-aggregator`: data ingestion, normalization, and snapshots.
- `technical-analysis-engine`: indicator and pattern signals.
- `risk-position-manager`: strategy-level sizing and portfolio constraints.
- `strategy-optimizer`: parameter search and challenger generation.
- `trade-signal-processor-executor`: order creation and routing.
- `performance-reporter-learner`: P&L reporting and adaptation loop.
- `profit-forecaster`: goal-based profit planning from stated constraints.
- `temp-rl-proto`: experimental RL retraining flow.

## Standard execution loop

1. **Pre-market / session-start**
   - refresh universe and screening candidates
   - compute regime tags and volatility buckets
   - generate watchlist hypotheses
2. **Periodic intraday checks**
   - refresh signals on cadence (for example hourly for swing)
   - check trigger conditions and place gated orders
   - publish concise condition update to user
3. **Post-session review**
   - write fills/positions/metrics
   - evaluate performance drift and risk adherence
   - queue retraining or parameter tests if thresholds are breached

## Strategy-specific risk adaptation

- Each strategy carries its own risk profile:
  - risk per trade
  - max concurrent positions
  - exposure cap
  - drawdown stop
  - cooldown rules
- User feedback can override profile values for that strategy only.

## Self-improvement lifecycle

1. Detect underperformance or repeated failure pattern.
2. Log a structured lesson with context and remediation hypothesis.
3. Run backtest/challenger training on retained data.
4. Compare against champion with fixed acceptance criteria.
5. Promote only if risk-adjusted metrics improve and drawdown constraints hold.

## Messaging outputs to user

- Daily: portfolio status, open hypotheses, risk usage, major events.
- Pre-market/mid-day/hourly (as configured): market condition summary and new trigger alerts.
- Weekly: strategy scorecards, proposed improvements, and strategy-specific risk tuning suggestions.
