from openclaw_trading_suite.autonomy import (
    AutonomyLevel,
    Decision,
    DecisionInput,
    evaluate_decision,
)


def _base_input(level: AutonomyLevel) -> DecisionInput:
    return DecisionInput(
        autonomy_level=level,
        strategy_id="s1",
        hypothesis_id="h1",
        estimated_risk_pct=0.01,
        strategy_risk_limit_pct=0.02,
        portfolio_drawdown_pct=0.01,
        max_portfolio_drawdown_pct=0.10,
    )


def test_cautious_requires_approval() -> None:
    out = evaluate_decision(_base_input(AutonomyLevel.CAUTIOUS))
    assert out.decision == Decision.REQUIRE_APPROVAL


def test_balanced_requires_approval_on_threshold_breach() -> None:
    inp = _base_input(AutonomyLevel.BALANCED)
    inp = DecisionInput(**{**inp.__dict__, "estimated_risk_pct": 0.03})
    out = evaluate_decision(inp)
    assert out.decision == Decision.REQUIRE_APPROVAL


def test_autonomous_blocks_on_threshold_breach() -> None:
    inp = _base_input(AutonomyLevel.AUTONOMOUS)
    inp = DecisionInput(**{**inp.__dict__, "estimated_risk_pct": 0.05})
    out = evaluate_decision(inp)
    assert out.decision == Decision.BLOCK


def test_free_agent_approves_when_no_halt() -> None:
    out = evaluate_decision(_base_input(AutonomyLevel.FREE_AGENT))
    assert out.decision == Decision.APPROVE


def test_effective_threshold_uses_agent_threshold_when_present() -> None:
    inp = _base_input(AutonomyLevel.BALANCED)
    inp = DecisionInput(
        **{
            **inp.__dict__,
            "estimated_risk_pct": 0.018,
            "strategy_risk_limit_pct": 0.02,
            "agent_risk_threshold_pct": 0.015,
        }
    )
    out = evaluate_decision(inp)
    assert out.decision == Decision.REQUIRE_APPROVAL
