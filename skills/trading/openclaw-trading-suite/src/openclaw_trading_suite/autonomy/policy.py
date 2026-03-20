from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AutonomyLevel(str, Enum):
    CAUTIOUS = "cautious"
    BALANCED = "balanced"
    AUTONOMOUS = "autonomous"
    FREE_AGENT = "free-agent"


class Decision(str, Enum):
    APPROVE = "approve"
    REQUIRE_APPROVAL = "require_approval"
    BLOCK = "block"


@dataclass(frozen=True)
class DecisionInput:
    autonomy_level: AutonomyLevel
    strategy_id: str
    hypothesis_id: str
    estimated_risk_pct: float
    strategy_risk_limit_pct: float
    portfolio_drawdown_pct: float
    max_portfolio_drawdown_pct: float
    safety_halt: bool = False
    agent_risk_threshold_pct: float | None = None
    user_risk_threshold_pct: float | None = None


@dataclass(frozen=True)
class DecisionOutcome:
    decision: Decision
    reason: str
    effective_risk_threshold_pct: float


def _effective_threshold(inp: DecisionInput) -> float:
    threshold = inp.strategy_risk_limit_pct
    if inp.agent_risk_threshold_pct is not None:
        threshold = min(threshold, inp.agent_risk_threshold_pct)
    if inp.user_risk_threshold_pct is not None:
        threshold = min(threshold, inp.user_risk_threshold_pct)
    return threshold


def evaluate_decision(inp: DecisionInput) -> DecisionOutcome:
    threshold = _effective_threshold(inp)

    if inp.safety_halt:
        return DecisionOutcome(
            decision=Decision.BLOCK,
            reason="safety_halt_enabled",
            effective_risk_threshold_pct=threshold,
        )

    if inp.portfolio_drawdown_pct > inp.max_portfolio_drawdown_pct:
        return DecisionOutcome(
            decision=Decision.BLOCK,
            reason="portfolio_drawdown_limit_breached",
            effective_risk_threshold_pct=threshold,
        )

    if inp.autonomy_level == AutonomyLevel.CAUTIOUS:
        return DecisionOutcome(
            decision=Decision.REQUIRE_APPROVAL,
            reason="cautious_mode_requires_confirmation",
            effective_risk_threshold_pct=threshold,
        )

    if inp.autonomy_level == AutonomyLevel.BALANCED:
        if inp.estimated_risk_pct > threshold:
            return DecisionOutcome(
                decision=Decision.REQUIRE_APPROVAL,
                reason="balanced_mode_risk_threshold_exceeded",
                effective_risk_threshold_pct=threshold,
            )
        return DecisionOutcome(
            decision=Decision.APPROVE,
            reason="balanced_mode_within_threshold",
            effective_risk_threshold_pct=threshold,
        )

    if inp.autonomy_level == AutonomyLevel.AUTONOMOUS:
        if inp.estimated_risk_pct > threshold:
            return DecisionOutcome(
                decision=Decision.BLOCK,
                reason="autonomous_mode_risk_threshold_exceeded",
                effective_risk_threshold_pct=threshold,
            )
        return DecisionOutcome(
            decision=Decision.APPROVE,
            reason="autonomous_mode_within_threshold",
            effective_risk_threshold_pct=threshold,
        )

    return DecisionOutcome(
        decision=Decision.APPROVE,
        reason="free_agent_mode_enabled",
        effective_risk_threshold_pct=threshold,
    )
