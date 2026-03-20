# Data Retention Schema

Use this schema as the baseline persistent store for analysis, optimization, and RL/ML retraining.

## Required entities

- `strategies`
  - `strategy_id`
  - `name`
  - `profile_type` (swing, contrarian, whale_mirror, latency_arb, weather_event)
  - `version`
  - `params_json`
  - `active`
  - `created_at`

- `hypotheses`
  - `hypothesis_id`
  - `strategy_id`
  - `symbol_or_contract`
  - `thesis_text`
  - `entry_plan_json`
  - `exit_plan_json`
  - `invalidation_json`
  - `confidence`
  - `created_at`

- `signals`
  - `signal_id`
  - `hypothesis_id`
  - `signal_time`
  - `features_json`
  - `signal_side`
  - `signal_strength`
  - `regime_tag`

- `risk_decisions`
  - `risk_decision_id`
  - `hypothesis_id`
  - `risk_profile_json`
  - `position_size`
  - `approval_mode` (auto, manual_required)
  - `approved`
  - `decision_reason`
  - `created_at`

- `orders`
  - `order_id`
  - `hypothesis_id`
  - `venue`
  - `symbol`
  - `side`
  - `order_type`
  - `qty`
  - `limit_price`
  - `status`
  - `created_at`

- `fills`
  - `fill_id`
  - `order_id`
  - `fill_time`
  - `fill_price`
  - `fill_qty`
  - `fee`

- `positions`
  - `position_id`
  - `strategy_id`
  - `symbol`
  - `open_time`
  - `close_time`
  - `realized_pnl`
  - `max_adverse_excursion`
  - `max_favorable_excursion`
  - `close_reason`

- `daily_metrics`
  - `metric_date`
  - `strategy_id`
  - `trades`
  - `win_rate`
  - `expectancy`
  - `sharpe`
  - `max_drawdown`
  - `net_pnl`

- `model_runs`
  - `run_id`
  - `strategy_id`
  - `model_type`
  - `feature_set_version`
  - `train_window`
  - `validation_metrics_json`
  - `promoted`
  - `created_at`

- `lessons_learned`
  - `lesson_id`
  - `strategy_id`
  - `source` (user_feedback, incident, backtest, live_trade)
  - `lesson_text`
  - `action_item`
  - `status`
  - `created_at`

## Storage guidance

- Recommended v1 backend: SQLite for local single-node operation.
- Promote to Postgres when multi-agent concurrency or remote serving is required.
- Keep raw snapshots in append-only files/object storage if available, keyed by `signal_time` and `symbol`.

## Minimum analytics outputs

- Strategy scorecard: win rate, expectancy, drawdown, and net P&L by strategy version.
- Edge decay detector: rolling comparison of last N trades vs baseline.
- Risk adherence report: number of blocked trades and reason codes.
