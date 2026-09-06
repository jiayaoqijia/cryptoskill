#!/usr/bin/env python3
"""
Correlation Analyzer - Analyze token correlations and concentration risk
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import math


@dataclass
class CorrelationPair:
    """Represents correlation between two tokens"""
    token_a: str
    token_b: str
    correlation: float
    interpretation: str


class CorrelationAnalyzer:
    """Analyze token correlations in portfolio"""

    def __init__(self):
        """Initialize correlation analyzer with historical correlation data"""
        # Typical correlation matrix for major tokens
        self.correlation_matrix = {
            "ETH": {
                "BTC": 0.75,
                "USDC": -0.05,
                "USDT": -0.03,
                "DAI": -0.02,
                "LINK": 0.65,
                "AAVE": 0.70,
                "UNI": 0.68,
                "WBTC": 0.75,
            },
            "BTC": {
                "ETH": 0.75,
                "USDC": -0.04,
                "USDT": -0.02,
                "LINK": 0.55,
                "AAVE": 0.60,
                "WBTC": 0.98,  # Perfect correlation (wrapped)
            },
            "USDC": {
                "USDT": 0.95,
                "DAI": 0.90,
                "ETH": -0.05,
                "BTC": -0.04,
            },
            "LINK": {
                "ETH": 0.65,
                "AAVE": 0.70,
                "UNI": 0.60,
                "BTC": 0.55,
            },
            "AAVE": {
                "ETH": 0.70,
                "LINK": 0.70,
                "UNI": 0.75,
                "BTC": 0.60,
            },
        }

    def get_correlation(self, token_a: str, token_b: str) -> float:
        """Get correlation between two tokens"""
        token_a = token_a.upper()
        token_b = token_b.upper()
        
        if token_a == token_b:
            return 1.0
        
        # Check matrix
        if token_a in self.correlation_matrix:
            if token_b in self.correlation_matrix[token_a]:
                return self.correlation_matrix[token_a][token_b]
        
        if token_b in self.correlation_matrix:
            if token_a in self.correlation_matrix[token_b]:
                return self.correlation_matrix[token_b][token_a]
        
        # Default correlation for unknown pairs
        return 0.30  # Moderate positive correlation

    def interpret_correlation(self, correlation: float) -> str:
        """Interpret correlation value"""
        if correlation > 0.8:
            return "Very High (Strong positive)"
        elif correlation > 0.6:
            return "High (Positive)"
        elif correlation > 0.3:
            return "Moderate (Positive)"
        elif correlation > 0.1:
            return "Weak (Positive)"
        elif correlation > -0.1:
            return "Very Weak (Near zero)"
        elif correlation > -0.3:
            return "Weak (Negative)"
        else:
            return "Moderate+ (Negative/Hedge)"

    def calculate_portfolio_correlation(self, holdings: List[Dict]) -> float:
        """
        Calculate average correlation across portfolio holdings
        Higher = more correlated = less diversified
        """
        if len(holdings) < 2:
            return 0.0
        
        total_value = sum(h.get("value_usd", 0) for h in holdings)
        if total_value == 0:
            return 0.0
        
        correlations = []
        
        # Calculate weighted correlations
        for i, holding_a in enumerate(holdings):
            for holding_b in holdings[i+1:]:
                weight_a = holding_a.get("value_usd", 0) / total_value
                weight_b = holding_b.get("value_usd", 0) / total_value
                
                correlation = self.get_correlation(
                    holding_a.get("symbol", ""),
                    holding_b.get("symbol", "")
                )
                
                weighted_correlation = correlation * weight_a * weight_b
                correlations.append(weighted_correlation)
        
        return sum(correlations) if correlations else 0.0

    def find_correlated_pairs(
        self,
        holdings: List[Dict],
        threshold: float = 0.6
    ) -> List[CorrelationPair]:
        """Find highly correlated token pairs"""
        pairs = []
        
        for i, holding_a in enumerate(holdings):
            for holding_b in holdings[i+1:]:
                correlation = self.get_correlation(
                    holding_a.get("symbol", ""),
                    holding_b.get("symbol", "")
                )
                
                if abs(correlation) >= threshold:
                    pairs.append(CorrelationPair(
                        token_a=holding_a.get("symbol", ""),
                        token_b=holding_b.get("symbol", ""),
                        correlation=correlation,
                        interpretation=self.interpret_correlation(correlation)
                    ))
        
        return sorted(pairs, key=lambda x: abs(x.correlation), reverse=True)

    def find_hedging_pairs(
        self,
        holdings: List[Dict],
        threshold: float = -0.3
    ) -> List[CorrelationPair]:
        """Find negatively correlated pairs (hedging potential)"""
        pairs = []
        
        for i, holding_a in enumerate(holdings):
            for holding_b in holdings[i+1:]:
                correlation = self.get_correlation(
                    holding_a.get("symbol", ""),
                    holding_b.get("symbol", "")
                )
                
                if correlation <= threshold:
                    pairs.append(CorrelationPair(
                        token_a=holding_a.get("symbol", ""),
                        token_b=holding_b.get("symbol", ""),
                        correlation=correlation,
                        interpretation=self.interpret_correlation(correlation)
                    ))
        
        return sorted(pairs, key=lambda x: x.correlation)

    def analyze_diversification(self, holdings: List[Dict]) -> Dict:
        """Analyze diversification effectiveness"""
        if not holdings:
            return {
                "average_correlation": 0.0,
                "portfolio_correlation_score": 0.0,
                "diversification_ratio": 0.0,
                "correlated_pairs": [],
                "hedging_pairs": [],
                "diversification_assessment": "Insufficient data"
            }
        
        total_value = sum(h.get("value_usd", 0) for h in holdings)
        
        # Calculate average correlation
        avg_correlation = self.calculate_portfolio_correlation(holdings)
        
        # Calculate diversification ratio
        # Ideal portfolio has low average correlation
        diversification_score = (1 - avg_correlation) * 100
        
        # Find problematic and hedging pairs
        correlated_pairs = self.find_correlated_pairs(holdings, threshold=0.7)
        hedging_pairs = self.find_hedging_pairs(holdings, threshold=-0.2)
        
        # Assess diversification
        if diversification_score > 70:
            assessment = "Well diversified"
            severity = "Green"
        elif diversification_score > 50:
            assessment = "Moderately diversified"
            severity = "Yellow"
        else:
            assessment = "Poorly diversified - high correlation risk"
            severity = "Red"
        
        return {
            "average_correlation": round(avg_correlation, 3),
            "portfolio_correlation_score": round(diversification_score, 1),
            "diversification_ratio": round(1 - avg_correlation, 3),
            "num_holdings": len(holdings),
            "correlated_pairs": [
                {
                    "token_a": p.token_a,
                    "token_b": p.token_b,
                    "correlation": round(p.correlation, 3),
                    "interpretation": p.interpretation
                }
                for p in correlated_pairs[:5]
            ],
            "hedging_pairs": [
                {
                    "token_a": p.token_a,
                    "token_b": p.token_b,
                    "correlation": round(p.correlation, 3),
                    "interpretation": p.interpretation
                }
                for p in hedging_pairs[:5]
            ],
            "diversification_assessment": assessment,
            "severity": severity
        }

    def suggest_uncorrelated_assets(
        self,
        holdings: List[Dict],
        max_correlation: float = 0.3
    ) -> List[Dict]:
        """Suggest uncorrelated assets to improve diversification"""
        current_symbols = {h.get("symbol", "").upper() for h in holdings}
        
        all_tokens = {
            "BTC": "Bitcoin",
            "ETH": "Ethereum",
            "USDC": "USDC Stablecoin",
            "USDT": "USDT Stablecoin",
            "DAI": "DAI Stablecoin",
            "LINK": "Chainlink",
            "AAVE": "Aave",
            "UNI": "Uniswap",
            "WBTC": "Wrapped Bitcoin",
        }
        
        suggestions = []
        
        for token, name in all_tokens.items():
            if token in current_symbols:
                continue
            
            # Check correlation with existing holdings
            correlations = [
                self.get_correlation(token, h.get("symbol", ""))
                for h in holdings
            ]
            
            avg_corr = sum(correlations) / len(correlations) if correlations else 0
            
            if avg_corr <= max_correlation:
                suggestions.append({
                    "token": token,
                    "name": name,
                    "avg_correlation_with_portfolio": round(avg_corr, 3),
                    "diversification_benefit": "High",
                    "reason": f"Low correlation ({avg_corr:.2f}) with existing holdings"
                })
        
        return sorted(
            suggestions,
            key=lambda x: x["avg_correlation_with_portfolio"]
        )


def main():
    """Example usage"""
    import sys
    
    # Example holdings
    example_holdings = [
        {"symbol": "ETH", "value_usd": 50000},
        {"symbol": "USDC", "value_usd": 30000},
        {"symbol": "LINK", "value_usd": 15000},
        {"symbol": "AAVE", "value_usd": 10000},
    ]
    
    analyzer = CorrelationAnalyzer()
    analysis = analyzer.analyze_diversification(example_holdings)
    
    print("\n" + "="*60)
    print("CORRELATION & DIVERSIFICATION ANALYSIS")
    print("="*60)
    print(json.dumps(analysis, indent=2))
    print("\n" + "="*60)
    print("UNCORRELATED ASSET SUGGESTIONS")
    print("="*60)
    suggestions = analyzer.suggest_uncorrelated_assets(example_holdings)
    print(json.dumps([asdict(s) if hasattr(s, '__dataclass_fields__') else s for s in suggestions], indent=2))
    print("="*60)


if __name__ == "__main__":
    main()


def asdict(obj):
    """Helper for dataclass conversion"""
    if hasattr(obj, '__dataclass_fields__'):
        return {f.name: getattr(obj, f.name) for f in obj.__dataclass_fields__.values()}
    return obj
