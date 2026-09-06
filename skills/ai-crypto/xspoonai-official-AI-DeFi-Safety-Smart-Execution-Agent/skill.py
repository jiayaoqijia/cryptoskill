"""
AI DeFi Safety & Smart Execution Agent - Main Entry Point

This module serves as the orchestration layer for the DeFi safety analysis skill.
It coordinates all sub-modules to analyze a DeFi action and return a comprehensive
safety assessment.
"""

from typing import Optional
from dataclasses import dataclass, asdict

from .safety_analyzer import SafetyAnalyzer, TokenRiskResult
from .swap_simulator import SwapSimulator, SwapSimulationResult
from .risk_engine import RiskEngine, SafetyVerdict
from .ai_explainer import AIExplainer


@dataclass
class DeFiActionInput:
    """Input schema for a DeFi action analysis request."""
    action: str
    from_token: str
    to_token: str
    amount: float
    chain: str
    max_slippage: float = 1.0
    risk_tolerance: str = "medium"

    @classmethod
    def from_dict(cls, data: dict) -> "DeFiActionInput":
        """Create input from dictionary, with validation."""
        required = ["action", "from_token", "to_token", "amount", "chain"]
        for field in required:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        return cls(
            action=data["action"],
            from_token=data["from_token"].upper(),
            to_token=data["to_token"].upper(),
            amount=float(data["amount"]),
            chain=data["chain"],
            max_slippage=float(data.get("max_slippage", 1.0)),
            risk_tolerance=data.get("risk_tolerance", "medium").lower()
        )


@dataclass
class DeFiAnalysisResult:
    """Complete analysis result for a DeFi action."""
    input_summary: dict
    from_token_analysis: dict
    to_token_analysis: dict
    swap_simulation: dict
    safety_score: int
    verdict: str
    explanation: str
    recommendation: str

    def to_dict(self) -> dict:
        """Convert result to dictionary."""
        return asdict(self)


def analyze_defi_action(input_data: dict) -> dict:
    """
    Main entry point for analyzing a DeFi action.
    
    Orchestrates all analysis modules and returns a comprehensive
    safety assessment with scoring and explanations.
    
    Args:
        input_data: Dictionary containing DeFi action parameters
            - action: str (e.g., "swap")
            - from_token: str (e.g., "USDC")
            - to_token: str (e.g., "ETH")
            - amount: float (e.g., 500)
            - chain: str (e.g., "Arbitrum")
            - max_slippage: float (optional, default 1.0)
            - risk_tolerance: str (optional, "low"|"medium"|"high")
    
    Returns:
        Dictionary containing complete analysis results
    """
    # Parse and validate input
    action_input = DeFiActionInput.from_dict(input_data)
    
    # Initialize analyzers
    safety_analyzer = SafetyAnalyzer()
    swap_simulator = SwapSimulator()
    risk_engine = RiskEngine()
    ai_explainer = AIExplainer()
    
    # Step 1: Analyze token safety for both tokens
    from_token_risk = safety_analyzer.analyze_token(
        token=action_input.from_token,
        chain=action_input.chain
    )
    to_token_risk = safety_analyzer.analyze_token(
        token=action_input.to_token,
        chain=action_input.chain
    )
    
    # Step 2: Simulate the swap
    swap_result = swap_simulator.simulate_swap(
        from_token=action_input.from_token,
        to_token=action_input.to_token,
        amount=action_input.amount,
        chain=action_input.chain,
        max_slippage=action_input.max_slippage
    )
    
    # Step 3: Calculate safety score and verdict
    safety_result = risk_engine.calculate_safety_score(
        from_token_risk=from_token_risk,
        to_token_risk=to_token_risk,
        swap_result=swap_result,
        risk_tolerance=action_input.risk_tolerance
    )
    
    # Step 4: Generate AI explanation
    explanation = ai_explainer.explain(
        action_input=action_input,
        from_token_risk=from_token_risk,
        to_token_risk=to_token_risk,
        swap_result=swap_result,
        safety_result=safety_result
    )
    
    # Build recommendation based on verdict
    recommendation = _build_recommendation(safety_result.verdict, action_input.risk_tolerance)
    
    # Compile final result
    result = DeFiAnalysisResult(
        input_summary={
            "action": action_input.action,
            "from_token": action_input.from_token,
            "to_token": action_input.to_token,
            "amount": action_input.amount,
            "chain": action_input.chain,
            "max_slippage": action_input.max_slippage,
            "risk_tolerance": action_input.risk_tolerance
        },
        from_token_analysis=from_token_risk.to_dict(),
        to_token_analysis=to_token_risk.to_dict(),
        swap_simulation=swap_result.to_dict(),
        safety_score=safety_result.score,
        verdict=safety_result.verdict,
        explanation=explanation,
        recommendation=recommendation
    )
    
    return result.to_dict()


def _build_recommendation(verdict: str, risk_tolerance: str) -> str:
    """Generate actionable recommendation based on verdict and user's risk tolerance."""
    recommendations = {
        "SAFE": {
            "low": "This action appears safe. You may proceed with standard precautions.",
            "medium": "This action appears safe. Proceed with confidence.",
            "high": "This action is safe. Execute when ready."
        },
        "CAUTION": {
            "low": "This action has moderate risks. Consider reducing amount or avoiding entirely.",
            "medium": "This action has some risks. Proceed carefully and verify details.",
            "high": "This action has moderate risks but is within your tolerance. Proceed with awareness."
        },
        "DANGEROUS": {
            "low": "This action is high-risk. Strongly recommend avoiding.",
            "medium": "This action is dangerous. Avoid unless you fully understand the risks.",
            "high": "This action is dangerous. Only proceed if you accept potential losses."
        }
    }
    return recommendations.get(verdict, {}).get(risk_tolerance, "Unable to generate recommendation.")


# Convenience function for direct module execution
if __name__ == "__main__":
    import json
    
    # Example usage
    sample_input = {
        "action": "swap",
        "from_token": "USDC",
        "to_token": "ETH",
        "amount": 500,
        "chain": "Arbitrum",
        "max_slippage": 1.0,
        "risk_tolerance": "medium"
    }
    
    result = analyze_defi_action(sample_input)
    print(json.dumps(result, indent=2))
