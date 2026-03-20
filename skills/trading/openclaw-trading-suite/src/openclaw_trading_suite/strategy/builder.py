from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class PromotionMetrics:
    sample_trades: int
    active_days: int
    win_rate: float
    expectancy: float
    max_drawdown: float
    execution_error_rate: float
    risk_rule_adherence: float


@dataclass(frozen=True)
class StrategyBuilderConfig:
    strategy_id: str
    strategy_name: str
    maturity_gates: dict[str, float]
    promotion_policy: dict[str, Any]
    risk_profile: dict[str, Any]


@dataclass(frozen=True)
class GateEvaluationResult:
    passed: bool
    reasons: list[str]


def load_strategy_builder_config(path: Path) -> StrategyBuilderConfig:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return StrategyBuilderConfig(
        strategy_id=payload["strategy_id"],
        strategy_name=payload.get("strategy_name", payload["strategy_id"]),
        maturity_gates=payload["maturity_gates"]["paper_to_live"],
        promotion_policy=payload.get("promotion_policy", {}),
        risk_profile=payload.get("risk_profile", {}),
    )


def evaluate_paper_to_live_promotion(
    config: StrategyBuilderConfig,
    metrics: PromotionMetrics,
) -> GateEvaluationResult:
    g = config.maturity_gates
    reasons: list[str] = []

    if metrics.sample_trades < int(g.get("min_sample_trades", 0)):
        reasons.append("min_sample_trades_not_met")
    if metrics.active_days < int(g.get("min_days_active", 0)):
        reasons.append("min_days_active_not_met")
    if metrics.win_rate < float(g.get("min_win_rate", 0.0)):
        reasons.append("min_win_rate_not_met")
    if metrics.expectancy < float(g.get("min_expectancy", 0.0)):
        reasons.append("min_expectancy_not_met")
    if metrics.max_drawdown > float(g.get("max_drawdown", 1.0)):
        reasons.append("max_drawdown_exceeded")
    if metrics.execution_error_rate > float(g.get("max_execution_error_rate", 1.0)):
        reasons.append("execution_error_rate_exceeded")
    if metrics.risk_rule_adherence < float(g.get("risk_rule_adherence", 0.0)):
        reasons.append("risk_rule_adherence_not_met")

    return GateEvaluationResult(passed=len(reasons) == 0, reasons=reasons)

