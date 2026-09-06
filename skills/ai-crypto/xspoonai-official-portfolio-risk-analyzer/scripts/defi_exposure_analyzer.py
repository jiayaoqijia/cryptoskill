#!/usr/bin/env python3
"""
DeFi Exposure Analyzer - Analyze DeFi lending/borrowing positions and liquidation risk
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ProtocolType(Enum):
    """Supported DeFi protocols"""
    AAVE = "aave"
    COMPOUND = "compound"
    CURVE = "curve"
    YEARN = "yearn"
    LIDO = "lido"


@dataclass
class LendingPosition:
    """Represents a lending position"""
    protocol: str
    token: str
    amount: float
    apy: float
    value_usd: float


@dataclass
class BorrowingPosition:
    """Represents a borrowing position"""
    protocol: str
    token: str
    amount: float
    apr: float
    value_usd: float
    collateral_token: str
    collateral_amount: float


class DefiExposureAnalyzer:
    """Analyze DeFi positions and exposure"""

    def __init__(self):
        """Initialize DeFi analyzer"""
        # Sample data for protocols
        self.protocol_safety = {
            "aave": {"risk_score": 0.15, "audit_status": "Audited", "tvl_usd": 10000000000},
            "compound": {"risk_score": 0.15, "audit_status": "Audited", "tvl_usd": 3000000000},
            "curve": {"risk_score": 0.20, "audit_status": "Audited", "tvl_usd": 5000000000},
            "yearn": {"risk_score": 0.25, "audit_status": "Audited", "tvl_usd": 4000000000},
            "lido": {"risk_score": 0.30, "audit_status": "Audited", "tvl_usd": 20000000000},
        }

    def calculate_ltv_ratio(
        self,
        collateral_value: float,
        borrowed_value: float,
        max_ltv: float = 0.8
    ) -> Dict:
        """Calculate Loan-to-Value ratio"""
        if collateral_value == 0:
            ltv_ratio = 0
        else:
            ltv_ratio = borrowed_value / collateral_value
        
        # Determine health status
        if ltv_ratio > max_ltv * 0.95:  # Very close to liquidation
            health_status = "CRITICAL"
            color = "Red"
        elif ltv_ratio > max_ltv * 0.85:  # Warning zone
            health_status = "WARNING"
            color = "Orange"
        elif ltv_ratio > max_ltv * 0.70:  # Caution zone
            health_status = "CAUTION"
            color = "Yellow"
        else:  # Safe
            health_status = "SAFE"
            color = "Green"
        
        distance_to_liquidation = max_ltv - ltv_ratio
        liquidation_threshold = distance_to_liquidation / max_ltv * 100
        
        return {
            "ltv_ratio": round(ltv_ratio, 4),
            "ltv_percentage": round(ltv_ratio * 100, 2),
            "max_ltv": max_ltv,
            "health_status": health_status,
            "color": color,
            "distance_to_liquidation": round(distance_to_liquidation, 4),
            "liquidation_threshold_percent": round(liquidation_threshold, 1),
        }

    def calculate_liquidation_price(
        self,
        collateral_price: float,
        collateral_amount: float,
        borrowed_amount: float,
        borrowed_price: float,
        max_ltv: float = 0.8
    ) -> Optional[float]:
        """Calculate price at which collateral will be liquidated"""
        if collateral_amount == 0:
            return None
        
        current_collateral_value = collateral_price * collateral_amount
        borrowed_value = borrowed_amount * borrowed_price
        
        # Liquidation occurs when LTV = max_ltv
        # borrowed_value / collateral_value = max_ltv
        # liquidation_price = borrowed_value / (max_ltv * collateral_amount)
        
        liquidation_price = borrowed_value / (max_ltv * collateral_amount)
        
        return liquidation_price

    def calculate_health_factor(
        self,
        collateral_value: float,
        borrowed_value: float,
        liquidation_threshold: float = 0.8
    ) -> float:
        """
        Calculate health factor (Aave style)
        Health Factor = (collateral * liquidation_threshold) / borrowed
        Health Factor > 1.0 = Safe
        """
        if borrowed_value == 0:
            return float('inf')
        
        health_factor = (collateral_value * liquidation_threshold) / borrowed_value
        return round(health_factor, 3)

    def analyze_defi_position(
        self,
        protocol: str,
        collateral_token: str,
        collateral_amount: float,
        collateral_price: float,
        borrowed_token: str,
        borrowed_amount: float,
        borrowed_price: float,
        max_ltv: float = 0.8
    ) -> Dict:
        """Analyze a single DeFi borrowing position"""
        
        collateral_value = collateral_amount * collateral_price
        borrowed_value = borrowed_amount * borrowed_price
        
        ltv_data = self.calculate_ltv_ratio(collateral_value, borrowed_value, max_ltv)
        
        liquidation_price = self.calculate_liquidation_price(
            collateral_price,
            collateral_amount,
            borrowed_amount,
            borrowed_price,
            max_ltv
        )
        
        health_factor = self.calculate_health_factor(
            collateral_value,
            borrowed_value,
            max_ltv
        )
        
        protocol_safety = self.protocol_safety.get(
            protocol.lower(),
            {"risk_score": 0.40, "audit_status": "Unknown", "tvl_usd": 0}
        )
        
        # Calculate price change needed to liquidate
        if liquidation_price and collateral_price > 0:
            price_change_percent = ((liquidation_price - collateral_price) / collateral_price) * 100
        else:
            price_change_percent = 0
        
        return {
            "protocol": protocol,
            "collateral": {
                "token": collateral_token,
                "amount": collateral_amount,
                "price_usd": collateral_price,
                "value_usd": round(collateral_value, 2)
            },
            "borrowed": {
                "token": borrowed_token,
                "amount": borrowed_amount,
                "price_usd": borrowed_price,
                "value_usd": round(borrowed_value, 2)
            },
            "ltv": ltv_data,
            "health_factor": health_factor,
            "liquidation_analysis": {
                "liquidation_price": round(liquidation_price, 8) if liquidation_price else None,
                "price_change_percent_to_liquidation": round(price_change_percent, 2),
                "status": "SAFE" if health_factor > 1.5 else ("WARNING" if health_factor > 1.0 else "CRITICAL")
            },
            "protocol_safety": {
                "protocol": protocol,
                "risk_score": protocol_safety.get("risk_score", 0.5),
                "audit_status": protocol_safety.get("audit_status", "Unknown"),
                "tvl_usd": protocol_safety.get("tvl_usd", 0)
            },
            "risk_assessment": {
                "liquidation_risk": "HIGH" if health_factor < 1.2 else ("MEDIUM" if health_factor < 1.5 else "LOW"),
                "protocol_risk": "HIGH" if protocol_safety.get("risk_score", 0.5) > 0.30 else "MEDIUM" if protocol_safety.get("risk_score", 0.5) > 0.15 else "LOW"
            }
        }

    def analyze_portfolio_defi_exposure(
        self,
        positions: List[Dict]
    ) -> Dict:
        """Analyze total DeFi exposure across multiple positions"""
        
        if not positions:
            return {
                "total_collateral_usd": 0,
                "total_borrowed_usd": 0,
                "weighted_health_factor": float('inf'),
                "overall_status": "No positions",
                "positions_analyzed": 0,
                "highest_risk_position": None
            }
        
        total_collateral = sum(p.get("collateral_value_usd", 0) for p in positions)
        total_borrowed = sum(p.get("borrowed_value_usd", 0) for p in positions)
        
        health_factors = [p.get("health_factor", 0) for p in positions if p.get("health_factor")]
        weighted_health_factor = min(health_factors) if health_factors else float('inf')
        
        # Determine overall status
        if weighted_health_factor < 1.1:
            overall_status = "CRITICAL - Immediate action needed"
        elif weighted_health_factor < 1.3:
            overall_status = "WARNING - Monitor closely"
        elif weighted_health_factor < 1.5:
            overall_status = "CAUTION - Consider rebalancing"
        else:
            overall_status = "SAFE"
        
        # Find highest risk position
        highest_risk = min(positions, key=lambda p: p.get("health_factor", float('inf')))
        
        return {
            "total_collateral_usd": round(total_collateral, 2),
            "total_borrowed_usd": round(total_borrowed, 2),
            "total_ltv": round(total_borrowed / total_collateral, 4) if total_collateral > 0 else 0,
            "weighted_health_factor": round(weighted_health_factor, 3),
            "overall_status": overall_status,
            "positions_analyzed": len(positions),
            "highest_risk_position": {
                "protocol": highest_risk.get("protocol"),
                "health_factor": highest_risk.get("health_factor"),
                "status": highest_risk.get("liquidation_analysis", {}).get("status")
            } if highest_risk else None,
            "alerts": self._generate_alerts(positions)
        }

    def _generate_alerts(self, positions: List[Dict]) -> List[str]:
        """Generate alerts for risky positions"""
        alerts = []
        
        for pos in positions:
            hf = pos.get("health_factor", 0)
            if hf < 1.1:
                alerts.append(f"⚠️ CRITICAL: {pos.get('protocol')} position at risk of liquidation (HF: {hf})")
            elif hf < 1.3:
                alerts.append(f"⚠️ WARNING: {pos.get('protocol')} position approaching liquidation (HF: {hf})")
        
        return alerts


def main():
    """Example usage"""
    analyzer = DefiExposureAnalyzer()
    
    # Example: Analyze an Aave position
    position = analyzer.analyze_defi_position(
        protocol="aave",
        collateral_token="ETH",
        collateral_amount=10,
        collateral_price=2000,
        borrowed_token="USDC",
        borrowed_amount=12000,
        borrowed_price=1.0,
        max_ltv=0.8
    )
    
    print("\n" + "="*60)
    print("DEFI POSITION ANALYSIS")
    print("="*60)
    print(json.dumps(position, indent=2))
    print("="*60)


if __name__ == "__main__":
    main()
