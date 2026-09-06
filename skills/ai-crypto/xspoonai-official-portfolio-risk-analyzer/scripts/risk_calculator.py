#!/usr/bin/env python3
"""
Risk Calculator - Calculate comprehensive risk metrics for portfolio
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import math


class RiskLevel(Enum):
    """Risk level classification"""
    LOW = "LOW"
    LOW_MODERATE = "LOW_MODERATE"
    MODERATE = "MODERATE"
    MODERATE_HIGH = "MODERATE_HIGH"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class RiskMetrics:
    """Risk metrics for portfolio"""
    risk_score: float  # 0-100
    risk_level: str
    concentration_risk: float  # 0-100
    volatility_risk: float  # 0-100
    liquidity_risk: float  # 0-100
    smart_contract_risk: float  # 0-100
    primary_risk_factor: str
    secondary_risk_factors: List[str]
    herfindahl_index: float  # Concentration measure
    sharpe_ratio: Optional[float] = None
    diversification_score: float = 0.0  # 0-100


class RiskCalculator:
    """Calculate risk metrics for portfolio"""

    def __init__(self):
        """Initialize risk calculator"""
        # Volatility data for major tokens (annualized)
        self.token_volatility = {
            "ETH": 0.75,
            "BTC": 0.70,
            "LINK": 0.85,
            "UNI": 0.90,
            "AAVE": 0.88,
            "USDC": 0.02,
            "USDT": 0.02,
            "DAI": 0.03,
            "WBTC": 0.70,
        }
        
        # Smart contract risk scores (lower is better)
        self.contract_risk_scores = {
            "AAVE": 0.15,
            "COMPOUND": 0.15,
            "CURVE": 0.20,
            "UNISWAP": 0.15,
            "WBTC": 0.25,
            "LIDO": 0.30,
            "default": 0.50,
        }

    def calculate_concentration_risk(self, holdings: List[Dict]) -> Tuple[float, float]:
        """
        Calculate concentration risk using Herfindahl-Hirschman Index (HHI)
        
        Returns: (risk_score 0-100, herfindahl_index)
        """
        if not holdings:
            return 0.0, 0.0
        
        total_value = sum(h.get("value_usd", 0) for h in holdings)
        if total_value == 0:
            return 0.0, 0.0
        
        # Calculate market shares
        shares = [h.get("value_usd", 0) / total_value for h in holdings]
        
        # Calculate HHI (sum of squared market shares)
        hhi = sum(s ** 2 for s in shares)
        
        # Convert HHI to risk score (0-100)
        # HHI ranges from 1/n (perfect diversification) to 1 (single holding)
        min_hhi = 1 / len(holdings) if holdings else 0
        max_hhi = 1.0
        
        risk_score = ((hhi - min_hhi) / (max_hhi - min_hhi)) * 100 if (max_hhi - min_hhi) > 0 else 0
        
        return min(risk_score, 100), hhi

    def calculate_volatility_risk(self, holdings: List[Dict]) -> float:
        """Calculate volatility risk for portfolio"""
        if not holdings:
            return 0.0
        
        total_value = sum(h.get("value_usd", 0) for h in holdings)
        if total_value == 0:
            return 0.0
        
        weighted_volatility = 0.0
        
        for holding in holdings:
            symbol = holding.get("symbol", "").upper()
            volatility = self.token_volatility.get(symbol, 0.60)  # Default to high volatility
            weight = holding.get("value_usd", 0) / total_value
            weighted_volatility += volatility * weight
        
        # Normalize volatility to 0-100 scale (assume max 1.5 volatility)
        return min((weighted_volatility / 1.5) * 100, 100)

    def calculate_liquidity_risk(self, holdings: List[Dict]) -> float:
        """Calculate liquidity risk for portfolio"""
        # Tokens with low liquidity risk
        high_liquidity_tokens = {"ETH", "USDC", "USDT", "DAI", "WBTC", "LINK", "AAVE"}
        
        if not holdings:
            return 0.0
        
        total_value = sum(h.get("value_usd", 0) for h in holdings)
        if total_value == 0:
            return 0.0
        
        illiquid_value = 0.0
        
        for holding in holdings:
            symbol = holding.get("symbol", "").upper()
            if symbol not in high_liquidity_tokens:
                illiquid_value += holding.get("value_usd", 0)
        
        liquidity_risk = (illiquid_value / total_value) * 100
        return min(liquidity_risk, 100)

    def calculate_smart_contract_risk(self, holdings: List[Dict]) -> float:
        """Calculate smart contract risk for portfolio"""
        if not holdings:
            return 0.0
        
        total_value = sum(h.get("value_usd", 0) for h in holdings)
        if total_value == 0:
            return 0.0
        
        weighted_contract_risk = 0.0
        
        for holding in holdings:
            symbol = holding.get("symbol", "").upper()
            risk_score = self.contract_risk_scores.get(symbol, 0.50)
            weight = holding.get("value_usd", 0) / total_value
            weighted_contract_risk += risk_score * weight
        
        # Normalize to 0-100 scale
        return weighted_contract_risk * 100

    def calculate_diversification_score(self, holdings: List[Dict]) -> float:
        """
        Calculate diversification score (0-100)
        Higher score = better diversified
        """
        if not holdings:
            return 0.0
        
        concentration_risk, _ = self.calculate_concentration_risk(holdings)
        # Diversification score is inverse of concentration risk
        return 100 - concentration_risk

    def identify_risk_factors(self, holdings: List[Dict], metrics: Dict) -> Tuple[str, List[str]]:
        """Identify primary and secondary risk factors"""
        factors = []
        
        # Check concentration
        if metrics.get("concentration_risk", 0) > 50:
            top_holding = max(holdings, key=lambda x: x.get("value_usd", 0))
            factors.append(f"Overweight in {top_holding.get('symbol', 'unknown')} "
                          f"({top_holding.get('value_usd', 0) / sum(h.get('value_usd', 0) for h in holdings) * 100:.1f}%)")
        
        # Check volatility
        if metrics.get("volatility_risk", 0) > 60:
            factors.append("High volatility exposure")
        
        # Check liquidity
        if metrics.get("liquidity_risk", 0) > 30:
            factors.append("Exposure to illiquid tokens")
        
        # Check smart contract risk
        if metrics.get("smart_contract_risk", 0) > 50:
            factors.append("High smart contract risk")
        
        primary = factors[0] if factors else "Low overall risk"
        secondary = factors[1:3]  # Max 2 secondary factors
        
        return primary, secondary

    def calculate_overall_risk(self, metrics: Dict) -> Tuple[float, str]:
        """Calculate overall portfolio risk score and level"""
        weights = {
            "concentration_risk": 0.25,
            "volatility_risk": 0.25,
            "liquidity_risk": 0.25,
            "smart_contract_risk": 0.25,
        }
        
        risk_score = sum(
            metrics.get(factor, 0) * weight
            for factor, weight in weights.items()
        )
        
        # Determine risk level
        if risk_score < 20:
            risk_level = RiskLevel.LOW.value
        elif risk_score < 35:
            risk_level = RiskLevel.LOW_MODERATE.value
        elif risk_score < 50:
            risk_level = RiskLevel.MODERATE.value
        elif risk_score < 65:
            risk_level = RiskLevel.MODERATE_HIGH.value
        elif risk_score < 80:
            risk_level = RiskLevel.HIGH.value
        else:
            risk_level = RiskLevel.CRITICAL.value
        
        return risk_score, risk_level

    def analyze_portfolio(self, holdings: List[Dict]) -> RiskMetrics:
        """Perform comprehensive portfolio risk analysis"""
        
        # Calculate individual risk metrics
        concentration_risk, hhi = self.calculate_concentration_risk(holdings)
        volatility_risk = self.calculate_volatility_risk(holdings)
        liquidity_risk = self.calculate_liquidity_risk(holdings)
        contract_risk = self.calculate_smart_contract_risk(holdings)
        diversification_score = self.calculate_diversification_score(holdings)
        
        metrics = {
            "concentration_risk": concentration_risk,
            "volatility_risk": volatility_risk,
            "liquidity_risk": liquidity_risk,
            "smart_contract_risk": contract_risk,
        }
        
        # Calculate overall risk
        overall_risk, risk_level = self.calculate_overall_risk(metrics)
        
        # Identify risk factors
        primary_factor, secondary_factors = self.identify_risk_factors(holdings, metrics)
        
        return RiskMetrics(
            risk_score=overall_risk,
            risk_level=risk_level,
            concentration_risk=concentration_risk,
            volatility_risk=volatility_risk,
            liquidity_risk=liquidity_risk,
            smart_contract_risk=contract_risk,
            primary_risk_factor=primary_factor,
            secondary_risk_factors=secondary_factors,
            herfindahl_index=hhi,
            diversification_score=diversification_score
        )


async def main():
    """Example usage"""
    import sys
    
    # Example holdings
    example_holdings = [
        {"symbol": "ETH", "value_usd": 50000},
        {"symbol": "USDC", "value_usd": 30000},
        {"symbol": "LINK", "value_usd": 15000},
        {"symbol": "AAVE", "value_usd": 10000},
    ]
    
    if len(sys.argv) > 1:
        # Load from JSON file
        try:
            with open(sys.argv[1], "r") as f:
                example_holdings = json.load(f)
        except Exception as e:
            print(f"Error loading holdings: {e}")
    
    calculator = RiskCalculator()
    metrics = calculator.analyze_portfolio(example_holdings)
    
    print("\n" + "="*60)
    print("PORTFOLIO RISK ANALYSIS")
    print("="*60)
    print(json.dumps(asdict(metrics), indent=2))
    print("="*60)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
