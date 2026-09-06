"""
Risk Scoring Engine Module

Combines all safety signals into a unified Safety Score (0-100)
with a clear verdict for decision making.

Scoring weights:
- Token safety: 35%
- Liquidity: 25%
- Slippage/Execution: 20%
- Gas/Stability: 20%
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum

from .safety_analyzer import TokenRiskResult
from .swap_simulator import SwapSimulationResult


class Verdict(Enum):
    """Safety verdict classifications."""
    SAFE = "SAFE"           # Score 80-100
    CAUTION = "CAUTION"     # Score 50-79
    DANGEROUS = "DANGEROUS"  # Score < 50


@dataclass
class SafetyVerdict:
    """Final safety scoring result."""
    score: int
    verdict: str
    breakdown: dict


class RiskEngine:
    """
    Aggregates all risk signals into a final safety score and verdict.
    
    The engine uses weighted scoring across multiple categories:
    - Token Safety (35%): Combined risk from both tokens
    - Liquidity (25%): Pool depth and execution certainty
    - Execution (20%): Slippage and price impact
    - Stability (20%): Gas costs, MEV risk, market conditions
    
    Risk tolerance adjusts the final thresholds:
    - "low": Conservative, penalizes any risk signals
    - "medium": Balanced approach
    - "high": Aggressive, tolerates higher risk
    """
    
    # Scoring weights
    WEIGHTS = {
        "token_safety": 0.35,
        "liquidity": 0.25,
        "execution": 0.20,
        "stability": 0.20
    }
    
    # Verdict thresholds (adjusted by risk tolerance)
    BASE_THRESHOLDS = {
        "safe": 80,
        "caution": 50
    }
    
    # Risk tolerance adjustments
    TOLERANCE_ADJUSTMENTS = {
        "low": {"safe": 85, "caution": 60},
        "medium": {"safe": 80, "caution": 50},
        "high": {"safe": 70, "caution": 40}
    }
    
    def calculate_safety_score(
        self,
        from_token_risk: TokenRiskResult,
        to_token_risk: TokenRiskResult,
        swap_result: SwapSimulationResult,
        risk_tolerance: str = "medium"
    ) -> SafetyVerdict:
        """
        Calculate overall safety score from all analysis components.
        
        Args:
            from_token_risk: Risk analysis for source token
            to_token_risk: Risk analysis for destination token
            swap_result: Swap simulation results
            risk_tolerance: User's risk tolerance level
        
        Returns:
            SafetyVerdict with score, verdict, and breakdown
        """
        # Calculate component scores (0-100, higher = safer)
        token_score = self._calculate_token_score(from_token_risk, to_token_risk)
        liquidity_score = self._calculate_liquidity_score(from_token_risk, to_token_risk)
        execution_score = self._calculate_execution_score(swap_result)
        stability_score = self._calculate_stability_score(swap_result)
        
        # Apply weights
        weighted_score = (
            token_score * self.WEIGHTS["token_safety"] +
            liquidity_score * self.WEIGHTS["liquidity"] +
            execution_score * self.WEIGHTS["execution"] +
            stability_score * self.WEIGHTS["stability"]
        )
        
        final_score = int(round(weighted_score))
        
        # Determine verdict based on risk tolerance
        verdict = self._determine_verdict(final_score, risk_tolerance)
        
        # Build breakdown for transparency
        breakdown = {
            "token_safety": {
                "score": token_score,
                "weight": f"{self.WEIGHTS['token_safety']*100:.0f}%",
                "weighted_contribution": round(token_score * self.WEIGHTS["token_safety"], 1)
            },
            "liquidity": {
                "score": liquidity_score,
                "weight": f"{self.WEIGHTS['liquidity']*100:.0f}%",
                "weighted_contribution": round(liquidity_score * self.WEIGHTS["liquidity"], 1)
            },
            "execution": {
                "score": execution_score,
                "weight": f"{self.WEIGHTS['execution']*100:.0f}%",
                "weighted_contribution": round(execution_score * self.WEIGHTS["execution"], 1)
            },
            "stability": {
                "score": stability_score,
                "weight": f"{self.WEIGHTS['stability']*100:.0f}%",
                "weighted_contribution": round(stability_score * self.WEIGHTS["stability"], 1)
            },
            "risk_tolerance_applied": risk_tolerance
        }
        
        return SafetyVerdict(
            score=final_score,
            verdict=verdict,
            breakdown=breakdown
        )
    
    def _calculate_token_score(
        self,
        from_risk: TokenRiskResult,
        to_risk: TokenRiskResult
    ) -> float:
        """
        Calculate token safety score from both token risk profiles.
        
        Inverts risk scores (0=risky, 100=safe) to safety scores.
        Takes the worse of the two tokens as primary concern.
        """
        # Convert risk scores to safety scores
        from_safety = 100 - from_risk.risk_score
        to_safety = 100 - to_risk.risk_score
        
        # Weight toward the riskier token (it's the weak link)
        # 60% weight on riskier token, 40% on safer token
        min_safety = min(from_safety, to_safety)
        max_safety = max(from_safety, to_safety)
        
        weighted_safety = (min_safety * 0.6) + (max_safety * 0.4)
        
        # Bonus for verified and audited tokens
        verification_bonus = 0
        if from_risk.is_verified and to_risk.is_verified:
            verification_bonus += 5
        if from_risk.has_audit and to_risk.has_audit:
            verification_bonus += 5
        
        return min(100, weighted_safety + verification_bonus)
    
    def _calculate_liquidity_score(
        self,
        from_risk: TokenRiskResult,
        to_risk: TokenRiskResult
    ) -> float:
        """
        Calculate liquidity score based on pool depths.
        """
        # Use the lower liquidity as the constraint
        min_liquidity = min(from_risk.liquidity_usd, to_risk.liquidity_usd)
        
        # Scoring tiers
        if min_liquidity >= 100_000_000:  # $100M+
            return 100
        elif min_liquidity >= 50_000_000:  # $50M+
            return 90
        elif min_liquidity >= 10_000_000:  # $10M+
            return 75
        elif min_liquidity >= 1_000_000:   # $1M+
            return 55
        elif min_liquidity >= 100_000:     # $100K+
            return 35
        else:
            return 15
    
    def _calculate_execution_score(self, swap_result: SwapSimulationResult) -> float:
        """
        Calculate execution quality score based on slippage and price impact.
        """
        total_loss = swap_result.price_impact_percent + swap_result.slippage_percent
        
        # Scoring based on total expected loss
        if total_loss <= 0.3:
            score = 100
        elif total_loss <= 0.5:
            score = 90
        elif total_loss <= 1.0:
            score = 75
        elif total_loss <= 2.0:
            score = 55
        elif total_loss <= 5.0:
            score = 35
        else:
            score = 15
        
        # Penalize for warnings
        warning_penalty = len(swap_result.warnings) * 5
        
        return max(0, score - warning_penalty)
    
    def _calculate_stability_score(self, swap_result: SwapSimulationResult) -> float:
        """
        Calculate stability score based on gas and MEV risk.
        """
        base_score = 100
        
        # MEV risk penalties
        mev_penalties = {
            "low": 0,
            "medium": 15,
            "high": 35
        }
        base_score -= mev_penalties.get(swap_result.mev_risk, 10)
        
        # Gas cost relative penalty (assuming typical swap of $1000)
        # High gas relative to value is concerning
        gas_ratio = swap_result.gas_estimate_usd / 1000 * 100
        if gas_ratio > 5:
            base_score -= 20
        elif gas_ratio > 2:
            base_score -= 10
        elif gas_ratio > 1:
            base_score -= 5
        
        return max(0, base_score)
    
    def _determine_verdict(self, score: int, risk_tolerance: str) -> str:
        """
        Determine verdict based on score and risk tolerance.
        """
        thresholds = self.TOLERANCE_ADJUSTMENTS.get(
            risk_tolerance,
            self.TOLERANCE_ADJUSTMENTS["medium"]
        )
        
        if score >= thresholds["safe"]:
            return Verdict.SAFE.value
        elif score >= thresholds["caution"]:
            return Verdict.CAUTION.value
        else:
            return Verdict.DANGEROUS.value
