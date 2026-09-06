#!/usr/bin/env python3
"""
Diversification Recommender - Generate portfolio rebalancing and diversification recommendations
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class RebalancingRecommendation:
    """Rebalancing recommendation"""
    action: str  # "Buy", "Sell", "Hold"
    token: str
    current_allocation: float  # percentage
    recommended_allocation: float  # percentage
    target_amount_usd: float
    rationale: str


class DiversificationRecommender:
    """Generate diversification and rebalancing recommendations"""

    def __init__(self):
        """Initialize recommender"""
        # Standard allocation models
        self.allocation_models = {
            "conservative": {
                "stablecoins": 0.50,
                "large_cap": 0.30,  # ETH, BTC
                "mid_cap": 0.15,    # LINK, AAVE, UNI
                "small_cap": 0.05   # Other tokens
            },
            "moderate": {
                "stablecoins": 0.30,
                "large_cap": 0.40,
                "mid_cap": 0.20,
                "small_cap": 0.10
            },
            "aggressive": {
                "stablecoins": 0.15,
                "large_cap": 0.35,
                "mid_cap": 0.35,
                "small_cap": 0.15
            }
        }
        
        # Token classifications
        self.token_classifications = {
            "stablecoins": ["USDC", "USDT", "DAI", "FRAX"],
            "large_cap": ["BTC", "ETH", "WBTC"],
            "mid_cap": ["LINK", "AAVE", "UNI", "LIDO"],
            "small_cap": ["CURVE", "CONVEX", "YEARN"]
        }

    def classify_token(self, symbol: str) -> str:
        """Classify token by market cap category"""
        symbol = symbol.upper()
        
        for category, tokens in self.token_classifications.items():
            if symbol in tokens:
                return category
        
        # Default classification
        return "small_cap"

    def get_recommended_allocation(
        self,
        holdings: List[Dict],
        risk_tolerance: str = "moderate"
    ) -> List[RebalancingRecommendation]:
        """Get rebalancing recommendations based on risk tolerance"""
        
        if risk_tolerance not in self.allocation_models:
            risk_tolerance = "moderate"
        
        target_model = self.allocation_models[risk_tolerance]
        total_value = sum(h.get("value_usd", 0) for h in holdings)
        
        if total_value == 0:
            return []
        
        recommendations = []
        
        # Calculate current allocations by category
        current_allocations = {cat: 0 for cat in self.token_classifications.keys()}
        token_values = {}
        
        for holding in holdings:
            symbol = holding.get("symbol", "")
            value = holding.get("value_usd", 0)
            token_values[symbol] = value
            
            category = self.classify_token(symbol)
            current_allocations[category] += value
        
        # Convert to percentages
        current_allocations = {
            cat: (val / total_value * 100) if total_value > 0 else 0
            for cat, val in current_allocations.items()
        }
        
        # Generate recommendations for each category
        for category, target_percent in target_model.items():
            current_percent = current_allocations.get(category, 0)
            current_usd = total_value * (current_percent / 100)
            target_usd = total_value * target_percent
            difference = target_usd - current_usd
            
            if abs(difference) > (total_value * 0.02):  # Only if >2% difference
                if difference > 0:
                    action = "Buy"
                    rationale = f"Increase {category} allocation from {current_percent:.1f}% to {target_percent*100:.1f}%"
                else:
                    action = "Sell"
                    rationale = f"Reduce {category} allocation from {current_percent:.1f}% to {target_percent*100:.1f}%"
                
                rec = RebalancingRecommendation(
                    action=action,
                    token=category,
                    current_allocation=current_percent,
                    recommended_allocation=target_percent * 100,
                    target_amount_usd=abs(difference),
                    rationale=rationale
                )
                recommendations.append(rec)
        
        return sorted(recommendations, key=lambda x: abs(x.target_amount_usd), reverse=True)

    def suggest_asset_additions(
        self,
        holdings: List[Dict],
        max_suggestions: int = 5
    ) -> List[Dict]:
        """Suggest assets to add for better diversification"""
        
        current_symbols = {h.get("symbol", "").upper() for h in holdings}
        current_categories = {self.classify_token(s) for s in current_symbols}
        
        suggestions = []
        
        # Suggest assets from underrepresented categories
        for category, tokens in self.token_classifications.items():
            if category not in current_categories:
                for token in tokens:
                    if token not in current_symbols:
                        suggestions.append({
                            "token": token,
                            "category": category,
                            "reason": f"Add to {category} exposure",
                            "allocation_suggestion": f"2-5% of portfolio"
                        })
                        break  # One token per missing category
        
        return suggestions[:max_suggestions]

    def check_single_token_risk(
        self,
        holdings: List[Dict],
        max_safe_allocation: float = 0.40
    ) -> List[Dict]:
        """Identify tokens with dangerously high allocation"""
        
        total_value = sum(h.get("value_usd", 0) for h in holdings)
        if total_value == 0:
            return []
        
        risky_holdings = []
        
        for holding in holdings:
            allocation = holding.get("value_usd", 0) / total_value
            
            if allocation > max_safe_allocation:
                risky_holdings.append({
                    "token": holding.get("symbol", ""),
                    "allocation_percent": round(allocation * 100, 1),
                    "value_usd": round(holding.get("value_usd", 0), 2),
                    "excess_allocation": round((allocation - max_safe_allocation) * 100, 1),
                    "recommendation": f"Consider reducing {holding.get('symbol', '')} allocation to below {max_safe_allocation*100:.0f}%"
                })
        
        return sorted(risky_holdings, key=lambda x: x["allocation_percent"], reverse=True)

    def generate_rebalancing_plan(
        self,
        holdings: List[Dict],
        risk_tolerance: str = "moderate"
    ) -> Dict:
        """Generate comprehensive rebalancing plan"""
        
        total_value = sum(h.get("value_usd", 0) for h in holdings)
        
        recommendations = self.get_recommended_allocation(holdings, risk_tolerance)
        risky_holdings = self.check_single_token_risk(holdings)
        suggested_additions = self.suggest_asset_additions(holdings)
        
        return {
            "portfolio_value_usd": round(total_value, 2),
            "risk_profile": risk_tolerance,
            "rebalancing_recommendations": [
                {
                    "action": rec.action,
                    "asset": rec.token,
                    "current_allocation": round(rec.current_allocation, 1),
                    "target_allocation": round(rec.recommended_allocation, 1),
                    "amount_usd": round(rec.target_amount_usd, 2),
                    "rationale": rec.rationale
                }
                for rec in recommendations
            ],
            "high_concentration_risks": risky_holdings,
            "suggested_additions": suggested_additions,
            "implementation_priority": self._generate_implementation_plan(recommendations),
            "estimated_rebalancing_cost_usd": self._estimate_gas_costs(recommendations),
            "timeline": "Execute within 24-48 hours for optimal results"
        }

    def _generate_implementation_plan(self, recommendations: List) -> List[Dict]:
        """Generate step-by-step implementation plan"""
        plan = []
        
        # Sells first
        sells = [r for r in recommendations if r.action == "Sell"]
        for i, rec in enumerate(sells, 1):
            plan.append({
                "step": i,
                "action": f"Sell {rec.token}",
                "amount_usd": round(rec.target_amount_usd, 2),
                "priority": "High"
            })
        
        # Then buys
        buys = [r for r in recommendations if r.action == "Buy"]
        for i, rec in enumerate(buys, len(sells) + 1):
            plan.append({
                "step": i,
                "action": f"Buy {rec.token}",
                "amount_usd": round(rec.target_amount_usd, 2),
                "priority": "High"
            })
        
        return plan

    def _estimate_gas_costs(self, recommendations: List) -> float:
        """Estimate transaction costs for rebalancing"""
        # Rough estimate: ~$100 per transaction on Ethereum
        num_transactions = len([r for r in recommendations if abs(r.target_amount_usd) > 100])
        return num_transactions * 100


def main():
    """Example usage"""
    recommender = DiversificationRecommender()
    
    # Example portfolio
    holdings = [
        {"symbol": "ETH", "value_usd": 50000},
        {"symbol": "USDC", "value_usd": 20000},
        {"symbol": "LINK", "value_usd": 20000},
        {"symbol": "AAVE", "value_usd": 10000},
    ]
    
    plan = recommender.generate_rebalancing_plan(holdings, "moderate")
    
    print("\n" + "="*60)
    print("REBALANCING RECOMMENDATION")
    print("="*60)
    print(json.dumps(plan, indent=2))
    print("="*60)


if __name__ == "__main__":
    main()
