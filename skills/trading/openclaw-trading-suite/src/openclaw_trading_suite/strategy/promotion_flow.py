from __future__ import annotations

from dataclasses import dataclass

from openclaw_trading_suite.goals import MandateProgressSummary

from .builder import (
    GateEvaluationResult,
    PromotionMetrics,
    StrategyBuilderConfig,
    evaluate_paper_to_live_promotion,
)


@dataclass(frozen=True)
class PromotionDecision:
    promote: bool
    gate_result: GateEvaluationResult
    reasons: list[str]


def evaluate_promotion_with_goals(
    config: StrategyBuilderConfig,
    metrics: PromotionMetrics,
    mandate_progress: MandateProgressSummary | None = None,
    require_goal_progress: bool = False,
    min_goal_progress_ratio: float = 0.9,
) -> PromotionDecision:
    gate_result = evaluate_paper_to_live_promotion(config, metrics)
    reasons = list(gate_result.reasons)

    if not gate_result.passed:
        return PromotionDecision(promote=False, gate_result=gate_result, reasons=reasons)

    if mandate_progress is None:
        return PromotionDecision(
            promote=not require_goal_progress,
            gate_result=gate_result,
            reasons=(["goal_progress_required_but_missing"] if require_goal_progress else []),
        )

    avg_ratio = 1.0
    if mandate_progress.target_progress:
        avg_ratio = sum(r.progress_ratio for r in mandate_progress.target_progress) / len(
            mandate_progress.target_progress
        )

    if mandate_progress.all_targets_met:
        return PromotionDecision(promote=True, gate_result=gate_result, reasons=[])

    if require_goal_progress and avg_ratio < min_goal_progress_ratio:
        reasons.append("goal_progress_below_required_ratio")
        return PromotionDecision(promote=False, gate_result=gate_result, reasons=reasons)

    reasons.append("goal_progress_not_met")
    return PromotionDecision(promote=False, gate_result=gate_result, reasons=reasons)
