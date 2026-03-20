# Strategy Builder and Promotion Gates

Strategy graduation is user/agent configurable per strategy. There are no hardcoded global maturity rules.

## Config location

- `configs/strategies/*.json`

## Required sections

- `risk_profile`: strategy-local risk constraints.
- `maturity_gates.paper_to_live`: thresholds used to graduate from paper to live.
- `promotion_policy`: autonomy mode requirements, approval scope, rollback triggers.

## Gate metrics

- `min_sample_trades`
- `min_days_active`
- `min_win_rate`
- `min_expectancy`
- `max_drawdown`
- `max_execution_error_rate`
- `risk_rule_adherence`

## Evaluation flow

1. Load strategy config.
2. Evaluate observed paper metrics against gate thresholds.
3. Return `passed=true/false` with explicit reason codes.
4. If passed, apply promotion policy constraints before enabling live mode.
