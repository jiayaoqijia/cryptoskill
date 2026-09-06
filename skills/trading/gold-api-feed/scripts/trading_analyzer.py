"""
Trading Analysis Tools for Gold API Feed
Risk management, position sizing, and trade evaluation
"""

from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime


@dataclass
class TradeSetup:
    """Trade setup parameters"""
    asset: str
    direction: str  # "buy" or "sell"
    entry_price: float
    stop_loss: float
    take_profit: float
    account_balance: float
    risk_percent: float = 1.0  # Default 1% risk


@dataclass
class TradeAnalysis:
    """Complete trade analysis output"""
    setup: TradeSetup
    risk_amount: float
    position_size: float
    stop_distance: float
    risk_reward_ratio: float
    max_loss: float
    potential_profit: float
    recommendation: str
    reasoning: List[str]


class TradingAnalyzer:
    """
    Trading analysis tools for precious metals and crypto

    Features:
    - Position sizing based on risk %
    - Risk/reward calculations
    - Trade setup evaluation
    - Portfolio risk assessment
    """

    def __init__(self):
        self.risk_rules = {
            "max_risk_per_trade": 2.0,  # %
            "min_risk_reward": 1.5,
            "max_daily_loss": 5.0,  # %
            "max_portfolio_exposure": 50.0  # %
        }

    def calculate_position_size(
        self,
        account_balance: float,
        risk_percent: float,
        entry_price: float,
        stop_loss: float
    ) -> Dict[str, float]:
        """
        Calculate optimal position size based on risk parameters

        Returns:
            {
                "risk_amount": Dollar amount at risk,
                "stop_pips": Price distance to stop,
                "position_size": Recommended lot size,
                "max_units": Position in micro-lots
            }
        """
        risk_amount = account_balance * (risk_percent / 100)
        stop_distance = abs(entry_price - stop_loss)

        if stop_distance == 0:
            return {
                "risk_amount": 0,
                "stop_pips": 0,
                "position_size": 0,
                "max_units": 0,
                "error": "Stop loss cannot equal entry price"
            }

        # For gold/crypto: 1 lot = $1 per $1 price move (simplified)
        position_size = risk_amount / stop_distance

        return {
            "risk_amount": round(risk_amount, 2),
            "stop_pips": round(stop_distance, 2),
            "position_size": round(position_size, 2),
            "max_units": int(position_size * 100)  # Micro-lots
        }

    def analyze_trade(self, setup: TradeSetup) -> TradeAnalysis:
        """
        Complete trade setup analysis

        Evaluates:
        - Position sizing
        - Risk/reward ratio
        - Trade viability
        - Risk compliance
        """
        # Calculate basic metrics
        stop_distance = abs(setup.entry_price - setup.stop_loss)
        profit_distance = abs(setup.take_profit - setup.entry_price)

        # Position sizing
        sizing = self.calculate_position_size(
            setup.account_balance,
            setup.risk_percent,
            setup.entry_price,
            setup.stop_loss
        )

        # Risk/reward ratio
        risk_reward = profit_distance / stop_distance if stop_distance > 0 else 0

        # Potential outcomes
        max_loss = sizing["risk_amount"]
        potential_profit = profit_distance * sizing["position_size"]

        # Evaluate trade
        reasoning = []
        recommendation = "NEUTRAL"

        # Check risk rules
        if setup.risk_percent > self.risk_rules["max_risk_per_trade"]:
            reasoning.append(f"❌ Risk {setup.risk_percent}% exceeds max {self.risk_rules['max_risk_per_trade']}%")
            recommendation = "REJECT"
        else:
            reasoning.append(f"✅ Risk {setup.risk_percent}% within limits")

        # Check R/R ratio
        if risk_reward < self.risk_rules["min_risk_reward"]:
            reasoning.append(f"❌ R/R ratio {risk_reward:.2f}:1 below minimum {self.risk_rules['min_risk_reward']}:1")
            if recommendation == "NEUTRAL":
                recommendation = "CAUTION"
        else:
            reasoning.append(f"✅ R/R ratio {risk_reward:.2f}:1 acceptable")

        # Check if stop is reasonable
        if stop_distance < setup.entry_price * 0.001:  # Less than 0.1%
            reasoning.append("⚠️ Stop loss very tight - risk of premature exit")

        # Overall recommendation
        if recommendation == "NEUTRAL":
            recommendation = "APPROVED"

        return TradeAnalysis(
            setup=setup,
            risk_amount=max_loss,
            position_size=sizing["position_size"],
            stop_distance=stop_distance,
            risk_reward_ratio=risk_reward,
            max_loss=max_loss,
            potential_profit=potential_profit,
            recommendation=recommendation,
            reasoning=reasoning
        )

    def format_trade_analysis(self, analysis: TradeAnalysis) -> str:
        """Format trade analysis for display"""
        setup = analysis.setup

        output = f"""
## Trade Analysis: {setup.asset.upper()} {setup.direction.upper()}

### Setup
- **Entry**: ${setup.entry_price:,.2f}
- **Stop Loss**: ${setup.stop_loss:,.2f} ({((setup.stop_loss - setup.entry_price) / setup.entry_price * 100):+.2f}%)
- **Take Profit**: ${setup.take_profit:,.2f} ({((setup.take_profit - setup.entry_price) / setup.entry_price * 100):+.2f}%)

### Risk Management
- **Account Balance**: ${setup.account_balance:,.2f}
- **Risk %**: {setup.risk_percent}%
- **Position Size**: {analysis.position_size:.2f} lots ({int(analysis.position_size * 100)} micro-lots)
- **Max Loss**: ${analysis.max_loss:,.2f}
- **Potential Profit**: ${analysis.potential_profit:,.2f}
- **R/R Ratio**: {analysis.risk_reward_ratio:.2f}:1

### Evaluation
**Recommendation**: {analysis.recommendation}

**Reasoning**:
"""
        for reason in analysis.reasoning:
            output += f"- {reason}\n"

        return output

    def calculate_correlation(
        self,
        prices1: List[float],
        prices2: List[float]
    ) -> float:
        """
        Calculate correlation coefficient between two price series

        Returns:
            Correlation coefficient (-1 to 1)
        """
        if len(prices1) != len(prices2) or len(prices1) == 0:
            return 0.0

        n = len(prices1)
        sum1 = sum(prices1)
        sum2 = sum(prices2)
        sum1_sq = sum(x ** 2 for x in prices1)
        sum2_sq = sum(x ** 2 for x in prices2)
        p_sum = sum(x * y for x, y in zip(prices1, prices2))

        num = p_sum - (sum1 * sum2 / n)
        den = ((sum1_sq - sum1 ** 2 / n) * (sum2_sq - sum2 ** 2 / n)) ** 0.5

        if den == 0:
            return 0.0

        return num / den

    def assess_portfolio_risk(
        self,
        positions: List[Dict],
        account_balance: float
    ) -> Dict:
        """
        Assess portfolio-level risk

        Args:
            positions: List of {asset, size, entry, current, stop}
            account_balance: Total account balance

        Returns:
            Risk assessment dict
        """
        total_exposure = sum(
            abs(pos["size"] * pos["current"])
            for pos in positions
        )

        total_risk = sum(
            abs(pos["size"] * (pos["entry"] - pos["stop"]))
            for pos in positions
        )

        exposure_percent = (total_exposure / account_balance) * 100
        risk_percent = (total_risk / account_balance) * 100

        warnings = []
        if exposure_percent > self.risk_rules["max_portfolio_exposure"]:
            warnings.append(f"Portfolio exposure {exposure_percent:.1f}% exceeds {self.risk_rules['max_portfolio_exposure']}% limit")

        if risk_percent > self.risk_rules["max_daily_loss"]:
            warnings.append(f"Total risk {risk_percent:.1f}% exceeds daily loss limit")

        return {
            "total_exposure": total_exposure,
            "exposure_percent": exposure_percent,
            "total_risk": total_risk,
            "risk_percent": risk_percent,
            "warnings": warnings,
            "status": "SAFE" if not warnings else "WARNING"
        }


# Quick analysis functions
def quick_trade_check(
    asset: str,
    entry: float,
    stop: float,
    target: float,
    account: float = 10000,
    risk: float = 1.0
) -> str:
    """Quick trade analysis"""
    analyzer = TradingAnalyzer()
    setup = TradeSetup(
        asset=asset,
        direction="buy" if target > entry else "sell",
        entry_price=entry,
        stop_loss=stop,
        take_profit=target,
        account_balance=account,
        risk_percent=risk
    )
    analysis = analyzer.analyze_trade(setup)
    return analyzer.format_trade_analysis(analysis)


def position_size_calculator(
    account: float,
    risk_percent: float,
    entry: float,
    stop: float
) -> Dict:
    """Quick position size calculation"""
    analyzer = TradingAnalyzer()
    return analyzer.calculate_position_size(account, risk_percent, entry, stop)


if __name__ == "__main__":
    # Test
    print(quick_trade_check(
        asset="XAUUSD",
        entry=4640,
        stop=4620,
        target=4680,
        account=10000,
        risk=1.0
    ))
