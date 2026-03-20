from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class GoalComparator(str, Enum):
    GTE = "gte"
    LTE = "lte"


class RiskMode(str, Enum):
    FIXED = "fixed"
    AGENT_DEFINED = "agent_defined"
    HYBRID = "hybrid"


@dataclass(frozen=True)
class GoalTarget:
    metric: str
    period: str
    target_value: float
    comparator: GoalComparator = GoalComparator.GTE


@dataclass(frozen=True)
class TradingMandate:
    mandate_id: str
    name: str
    base_currency: str
    risk_mode: RiskMode
    targets: list[GoalTarget]
    constraints: dict[str, Any]
    intent_align_ref: str | None = None


@dataclass(frozen=True)
class TargetProgress:
    metric: str
    period: str
    target_value: float
    actual_value: float
    comparator: GoalComparator
    met: bool
    progress_ratio: float


@dataclass(frozen=True)
class MandateProgressSummary:
    mandate_id: str
    all_targets_met: bool
    target_progress: list[TargetProgress]


def _progress_ratio(target: GoalTarget, actual: float) -> float:
    if target.target_value == 0:
        return 1.0 if actual == 0 else 0.0
    if target.comparator == GoalComparator.GTE:
        return actual / target.target_value
    if actual == 0:
        return 1.0
    return target.target_value / actual


def evaluate_mandate_progress(
    mandate: TradingMandate,
    actual_metrics: dict[tuple[str, str], float],
) -> MandateProgressSummary:
    progress_rows: list[TargetProgress] = []
    for target in mandate.targets:
        key = (target.metric, target.period)
        actual = float(actual_metrics.get(key, 0.0))
        if target.comparator == GoalComparator.GTE:
            met = actual >= target.target_value
        else:
            met = actual <= target.target_value
        progress_rows.append(
            TargetProgress(
                metric=target.metric,
                period=target.period,
                target_value=target.target_value,
                actual_value=actual,
                comparator=target.comparator,
                met=met,
                progress_ratio=_progress_ratio(target, actual),
            )
        )

    return MandateProgressSummary(
        mandate_id=mandate.mandate_id,
        all_targets_met=all(row.met for row in progress_rows),
        target_progress=progress_rows,
    )


def derive_effective_risk_limit_pct(
    mandate: TradingMandate,
    base_strategy_risk_limit_pct: float,
    progress: MandateProgressSummary,
) -> float:
    if mandate.risk_mode == RiskMode.FIXED:
        return base_strategy_risk_limit_pct

    floor = float(mandate.constraints.get("risk_floor_pct", 0.0025))
    ceiling = float(mandate.constraints.get("risk_ceiling_pct", base_strategy_risk_limit_pct))
    ramp = float(mandate.constraints.get("risk_ramp_pct", 0.001))

    if mandate.risk_mode == RiskMode.AGENT_DEFINED:
        baseline = floor
    else:
        baseline = base_strategy_risk_limit_pct

    if progress.all_targets_met:
        return max(floor, min(ceiling, baseline))

    avg_progress = 0.0
    if progress.target_progress:
        avg_progress = sum(row.progress_ratio for row in progress.target_progress) / len(progress.target_progress)

    if avg_progress < 0.75:
        return max(floor, baseline - ramp)
    if avg_progress < 1.0:
        return max(floor, baseline - (ramp / 2))
    return max(floor, min(ceiling, baseline))
