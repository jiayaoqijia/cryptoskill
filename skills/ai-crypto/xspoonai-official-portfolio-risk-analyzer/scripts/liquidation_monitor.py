#!/usr/bin/env python3
"""
Liquidation Monitor - Real-time liquidation price monitoring and LTV tracking
"""

import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LiquidationAlert:
    """Liquidation alert data"""
    position_id: str
    protocol: str
    severity: str  # CRITICAL, WARNING, CAUTION
    current_health_factor: float
    liquidation_price: float
    price_change_needed: float
    time_to_liquidation: Optional[str] = None
    recommended_action: str = ""


class LiquidationMonitor:
    """Monitor liquidation risks in real-time"""

    def __init__(self):
        """Initialize liquidation monitor"""
        pass

    def check_liquidation_status(
        self,
        current_price: float,
        liquidation_price: float,
        health_factor: float
    ) -> Dict:
        """Check liquidation status for a position"""
        
        if health_factor >= 1.5:
            status = "SAFE"
            danger_level = 0
        elif health_factor >= 1.2:
            status = "CAUTION"
            danger_level = 1
        elif health_factor >= 1.0:
            status = "WARNING"
            danger_level = 2
        else:
            status = "LIQUIDATED"
            danger_level = 3
        
        price_drop_needed = ((liquidation_price - current_price) / current_price) * 100
        
        return {
            "status": status,
            "danger_level": danger_level,
            "health_factor": round(health_factor, 3),
            "current_price": current_price,
            "liquidation_price": round(liquidation_price, 8),
            "price_drop_needed_percent": round(price_drop_needed, 2),
            "safe": health_factor > 1.0
        }

    def calculate_time_to_liquidation(
        self,
        current_price: float,
        liquidation_price: float,
        daily_volatility: float,
        price_trend: float = 0  # -1 to 1, negative is downtrend
    ) -> Optional[str]:
        """
        Estimate time to liquidation based on volatility and trend
        Returns human-readable estimate
        """
        if current_price <= liquidation_price:
            return "ALREADY LIQUIDATED"
        
        price_buffer = current_price - liquidation_price
        percentage_buffer = (price_buffer / current_price) * 100
        
        # Estimate days based on daily volatility
        # Assuming price moves according to volatility + trend
        if daily_volatility == 0:
            return "Unknown (No volatility data)"
        
        # If price is trending down, liquidation is closer
        adjusted_volatility = daily_volatility * (1 - price_trend)
        
        estimated_days = percentage_buffer / (adjusted_volatility * 100)
        
        if estimated_days < 0:
            return "IMMEDIATE"
        elif estimated_days < 1:
            return "Within 24 hours"
        elif estimated_days < 7:
            return f"About {int(estimated_days)} days"
        elif estimated_days < 30:
            return f"About {int(estimated_days / 7)} weeks"
        else:
            return "More than a month"

    def generate_liquidation_alerts(
        self,
        positions: List[Dict]
    ) -> List[LiquidationAlert]:
        """Generate alerts for positions at risk"""
        alerts = []
        
        for i, pos in enumerate(positions):
            hf = pos.get("health_factor", 2.0)
            
            if hf < 1.5:  # Only alert if health factor is below safe threshold
                if hf < 1.1:
                    severity = "CRITICAL"
                    recommendation = "IMMEDIATE ACTION: Consider repaying debt or adding collateral"
                elif hf < 1.3:
                    severity = "WARNING"
                    recommendation = "Monitor closely and prepare to rebalance if trend continues"
                else:
                    severity = "CAUTION"
                    recommendation = "Monitor position health, consider defensive action"
                
                alert = LiquidationAlert(
                    position_id=f"position_{i}",
                    protocol=pos.get("protocol", "Unknown"),
                    severity=severity,
                    current_health_factor=hf,
                    liquidation_price=pos.get("liquidation_price", 0),
                    price_change_needed=pos.get("price_change_percent_to_liquidation", 0),
                    recommended_action=recommendation
                )
                alerts.append(alert)
        
        return sorted(alerts, key=lambda x: x.current_health_factor)

    def get_ltv_history_trend(
        self,
        ltv_history: List[Dict]
    ) -> Dict:
        """Analyze LTV trend over time"""
        if len(ltv_history) < 2:
            return {
                "trend": "Insufficient data",
                "direction": "Unknown",
                "velocity": 0.0,
                "trajectory": "Unknown"
            }
        
        # Sort by timestamp
        history = sorted(ltv_history, key=lambda x: x.get("timestamp", 0))
        
        first_ltv = history[0].get("ltv", 0)
        last_ltv = history[-1].get("ltv", 0)
        
        change = last_ltv - first_ltv
        change_percent = (change / first_ltv * 100) if first_ltv > 0 else 0
        
        # Determine trajectory
        if change_percent > 10:
            trajectory = "Rapidly increasing - High risk"
        elif change_percent > 5:
            trajectory = "Increasing - Monitor closely"
        elif change_percent > -5:
            trajectory = "Stable"
        elif change_percent > -10:
            trajectory = "Decreasing - Improving"
        else:
            trajectory = "Rapidly decreasing - Improving quickly"
        
        return {
            "trend": "Increasing" if change > 0 else "Decreasing",
            "direction": "⬆️" if change > 0 else "⬇️",
            "change_amount": round(change, 4),
            "change_percent": round(change_percent, 2),
            "velocity": round(change / len(history), 4),  # Change per data point
            "trajectory": trajectory
        }

    def calculate_rebalancing_needed(
        self,
        current_ltv: float,
        target_ltv: float,
        collateral_value: float,
        borrowed_value: float
    ) -> Optional[Dict]:
        """Calculate rebalancing needed to reach target LTV"""
        
        if current_ltv <= target_ltv:
            return {
                "rebalancing_needed": False,
                "status": "Already at or below target LTV",
                "current_ltv": current_ltv,
                "target_ltv": target_ltv
            }
        
        # To reduce LTV, either increase collateral or decrease borrowed
        
        # Option 1: Reduce borrowed amount
        new_borrowed_value = collateral_value * target_ltv
        amount_to_repay = borrowed_value - new_borrowed_value
        
        # Option 2: Increase collateral
        new_collateral_value = borrowed_value / target_ltv
        amount_to_add = new_collateral_value - collateral_value
        
        return {
            "rebalancing_needed": True,
            "current_ltv": round(current_ltv, 4),
            "target_ltv": target_ltv,
            "option_1_reduce_debt": {
                "description": "Repay borrowed amount",
                "amount_to_repay": round(amount_to_repay, 2),
                "impact": f"Reduces debt by ${amount_to_repay:.2f}"
            },
            "option_2_add_collateral": {
                "description": "Add more collateral",
                "amount_to_add": round(amount_to_add, 2),
                "impact": f"Increases collateral by ${amount_to_add:.2f}"
            },
            "recommendation": "Option 1 is usually faster if you have available funds"
        }


def main():
    """Example usage"""
    monitor = LiquidationMonitor()
    
    # Example: Check liquidation status
    status = monitor.check_liquidation_status(
        current_price=2000,
        liquidation_price=1600,
        health_factor=1.4
    )
    
    print("\n" + "="*60)
    print("LIQUIDATION MONITORING")
    print("="*60)
    print(json.dumps(status, indent=2))
    print("="*60)
    
    # Example: Generate alerts
    example_positions = [
        {
            "protocol": "Aave",
            "health_factor": 1.05,
            "liquidation_price": 1600,
            "price_change_percent_to_liquidation": -20
        },
        {
            "protocol": "Compound",
            "health_factor": 1.8,
            "liquidation_price": 1200,
            "price_change_percent_to_liquidation": -40
        }
    ]
    
    alerts = monitor.generate_liquidation_alerts(example_positions)
    print("\nGENERATED ALERTS:")
    for alert in alerts:
        print(f"\n🚨 {alert.severity}: {alert.protocol} Position")
        print(f"   Health Factor: {alert.current_health_factor}")
        print(f"   Recommendation: {alert.recommended_action}")


if __name__ == "__main__":
    main()
