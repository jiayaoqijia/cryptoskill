from pathlib import Path

from openclaw_trading_suite.strategy import (
    PromotionMetrics,
    evaluate_paper_to_live_promotion,
    load_strategy_builder_config,
)


def test_gate_passes_when_all_thresholds_are_met() -> None:
    cfg = load_strategy_builder_config(
        Path("configs/strategies/swing_baseline.json")
    )
    metrics = PromotionMetrics(
        sample_trades=100,
        active_days=60,
        win_rate=0.56,
        expectancy=0.02,
        max_drawdown=0.08,
        execution_error_rate=0.01,
        risk_rule_adherence=0.99,
    )
    result = evaluate_paper_to_live_promotion(cfg, metrics)
    assert result.passed is True
    assert result.reasons == []


def test_gate_returns_reasons_when_thresholds_fail() -> None:
    cfg = load_strategy_builder_config(
        Path("configs/strategies/swing_baseline.json")
    )
    metrics = PromotionMetrics(
        sample_trades=10,
        active_days=10,
        win_rate=0.40,
        expectancy=-0.01,
        max_drawdown=0.2,
        execution_error_rate=0.05,
        risk_rule_adherence=0.8,
    )
    result = evaluate_paper_to_live_promotion(cfg, metrics)
    assert result.passed is False
    assert "min_sample_trades_not_met" in result.reasons
    assert "max_drawdown_exceeded" in result.reasons

