from pathlib import Path

from openclaw_trading_suite.goals import (
    GoalComparator,
    GoalTarget,
    RiskMode,
    TradingMandate,
    derive_effective_risk_limit_pct,
    evaluate_mandate_progress,
)
from openclaw_trading_suite.strategy import (
    PromotionMetrics,
    evaluate_promotion_with_goals,
    load_strategy_builder_config,
)


def test_mandate_progress_tracks_target_and_risk_adjustment() -> None:
    mandate = TradingMandate(
        mandate_id="m1",
        name="Daily Net Goal",
        base_currency="USD",
        risk_mode=RiskMode.HYBRID,
        intent_align_ref="intent-align://goal/daily-net",
        constraints={"risk_floor_pct": 0.003, "risk_ceiling_pct": 0.03, "risk_ramp_pct": 0.002},
        targets=[
            GoalTarget(
                metric="net_pnl",
                period="day",
                target_value=1000,
                comparator=GoalComparator.GTE,
            )
        ],
    )
    progress = evaluate_mandate_progress(mandate, {("net_pnl", "day"): 600})
    assert progress.all_targets_met is False
    effective = derive_effective_risk_limit_pct(mandate, base_strategy_risk_limit_pct=0.02, progress=progress)
    assert effective < 0.02


def test_promotion_with_goals_blocks_when_goal_progress_too_low() -> None:
    cfg = load_strategy_builder_config(Path("configs/strategies/swing_baseline.json"))
    metrics = PromotionMetrics(
        sample_trades=120,
        active_days=80,
        win_rate=0.58,
        expectancy=0.02,
        max_drawdown=0.08,
        execution_error_rate=0.01,
        risk_rule_adherence=0.99,
    )
    mandate = TradingMandate(
        mandate_id="m1",
        name="Daily Net Goal",
        base_currency="USD",
        risk_mode=RiskMode.FIXED,
        targets=[GoalTarget(metric="net_pnl", period="day", target_value=1000)],
        constraints={},
    )
    progress = evaluate_mandate_progress(mandate, {("net_pnl", "day"): 700})
    decision = evaluate_promotion_with_goals(
        config=cfg,
        metrics=metrics,
        mandate_progress=progress,
        require_goal_progress=True,
        min_goal_progress_ratio=0.9,
    )
    assert decision.promote is False
    assert "goal_progress_below_required_ratio" in decision.reasons
