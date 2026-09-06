"""
Risk Manager Module
Inspired by TradingAgents Risk Management
Monitors volatility, liquidity, and portfolio risk in real-time
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import math


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RiskAlert:
    """Risk alert notification"""
    timestamp: datetime
    level: RiskLevel
    category: str  # volatility, exposure, correlation, drawdown
    message: str
    recommendation: str
    severity_score: float  # 0.0 to 1.0


@dataclass
class VolatilityMetrics:
    """Volatility analysis"""
    asset: str
    current_volatility: float  # Standard deviation of returns
    atr_14: float  # Average True Range
    volatility_regime: str  # low, normal, high, extreme
    var_95: float  # Value at Risk (95% confidence)
    expected_shortfall: float  # Conditional VaR


@dataclass
class LiquidityMetrics:
    """Liquidity analysis"""
    asset: str
    bid_ask_spread: float
    spread_percent: float
    volume_24h: float
    liquidity_score: float  # 0.0 to 1.0
    slippage_estimate: float


@dataclass
class RiskReport:
    """Complete risk assessment"""
    timestamp: datetime
    portfolio_risk_level: RiskLevel
    volatility_metrics: Dict[str, VolatilityMetrics]
    liquidity_metrics: Dict[str, LiquidityMetrics]
    alerts: List[RiskAlert]
    overall_score: float  # 0.0 (safe) to 1.0 (dangerous)
    recommendations: List[str]


class RiskManager:
    """
    Risk Manager inspired by TradingAgents

    Monitors:
    - Portfolio exposure and concentration
    - Volatility regimes
    - Liquidity conditions
    - Drawdown levels
    - Correlation risks
    """

    def __init__(
        self,
        max_daily_drawdown: float = 5.0,
        max_position_size: float = 10.0,  # % of portfolio
        max_correlation: float = 0.8,
        volatility_threshold: float = 30.0,  # Annualized %
        liquidity_min_score: float = 0.3
    ):
        self.max_daily_drawdown = max_daily_drawdown
        self.max_position_size = max_position_size
        self.max_correlation = max_correlation
        self.volatility_threshold = volatility_threshold
        self.liquidity_min_score = liquidity_min_score

        # Risk tracking
        self.daily_high = 0.0
        self.daily_low = float('inf')
        self.peak_equity = 0.0
        self.current_drawdown = 0.0
        self.alerts: List[RiskAlert] = []

        # Volatility tracking
        self.price_history: Dict[str, List[Tuple[datetime, float]]] = {}
        self.returns_history: Dict[str, List[float]] = {}

        # Asset correlations
        self.correlation_matrix: Dict[str, Dict[str, float]] = {}

    def update_price(self, asset: str, price: float, timestamp: datetime = None):
        """Update price history for volatility calculation"""
        if timestamp is None:
            timestamp = datetime.now()

        if asset not in self.price_history:
            self.price_history[asset] = []
            self.returns_history[asset] = []

        # Add price
        self.price_history[asset].append((timestamp, price))

        # Keep only last 100 prices
        if len(self.price_history[asset]) > 100:
            self.price_history[asset].pop(0)

        # Calculate return if we have previous price
        if len(self.price_history[asset]) > 1:
            prev_price = self.price_history[asset][-2][1]
            daily_return = (price - prev_price) / prev_price
            self.returns_history[asset].append(daily_return)

            # Keep only last 30 returns
            if len(self.returns_history[asset]) > 30:
                self.returns_history[asset].pop(0)

    def calculate_volatility(self, asset: str) -> VolatilityMetrics:
        """Calculate volatility metrics for asset"""
        returns = self.returns_history.get(asset, [])

        if len(returns) < 10:
            # Not enough data - return default
            return VolatilityMetrics(
                asset=asset,
                current_volatility=0.15,  # 15% annualized
                atr_14=price * 0.01 if 'price' in locals() else 1.0,
                volatility_regime="unknown",
                var_95=0.0,
                expected_shortfall=0.0
            )

        # Calculate standard deviation of returns
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        std_dev = math.sqrt(variance)

        # Annualize (assuming daily returns)
        annualized_vol = std_dev * math.sqrt(252)

        # Calculate ATR approximation
        prices = [p for _, p in self.price_history.get(asset, [])]
        if len(prices) >= 14:
            atr = self._calculate_atr(prices)
        else:
            atr = prices[-1] * 0.01 if prices else 1.0

        # Determine regime
        if annualized_vol < 0.15:
            regime = "low"
        elif annualized_vol < 0.30:
            regime = "normal"
        elif annualized_vol < 0.50:
            regime = "high"
        else:
            regime = "extreme"

        # Calculate VaR (95%)
        var_95 = mean_return - 1.645 * std_dev

        # Expected shortfall (average of returns below VaR)
        tail_returns = [r for r in returns if r < var_95]
        es = sum(tail_returns) / len(tail_returns) if tail_returns else var_95 * 1.5

        return VolatilityMetrics(
            asset=asset,
            current_volatility=annualized_vol,
            atr_14=atr,
            volatility_regime=regime,
            var_95=var_95,
            expected_shortfall=es
        )

    def _calculate_atr(self, prices: List[float], period: int = 14) -> float:
        """Calculate Average True Range"""
        if len(prices) < period + 1:
            return prices[-1] * 0.01 if prices else 1.0

        tr_values = []
        for i in range(1, min(period + 1, len(prices))):
            high = max(prices[-i], prices[-i-1])
            low = min(prices[-i], prices[-i-1])
            tr = high - low
            tr_values.append(tr)

        return sum(tr_values) / len(tr_values) if tr_values else prices[-1] * 0.01

    def assess_liquidity(
        self,
        asset: str,
        bid_ask_spread: float = 0.5,
        volume_24h: float = 1000000
    ) -> LiquidityMetrics:
        """Assess liquidity conditions"""
        # Get current price
        prices = self.price_history.get(asset, [])
        current_price = prices[-1][1] if prices else 1.0

        spread_pct = (bid_ask_spread / current_price) * 100

        # Calculate liquidity score
        score = 1.0

        # Reduce score for wide spreads
        if spread_pct > 0.1:
            score -= 0.3
        if spread_pct > 0.5:
            score -= 0.3

        # Reduce score for low volume
        if volume_24h < 100000:
            score -= 0.2
        if volume_24h < 10000:
            score -= 0.3

        # Estimate slippage
        slippage = bid_ask_spread * 0.5

        return LiquidityMetrics(
            asset=asset,
            bid_ask_spread=bid_ask_spread,
            spread_percent=spread_pct,
            volume_24h=volume_24h,
            liquidity_score=max(0, score),
            slippage_estimate=slippage
        )

    def check_drawdown(self, current_equity: float) -> Tuple[float, RiskLevel]:
        """Check current drawdown level"""
        # Update peak
        if current_equity > self.peak_equity:
            self.peak_equity = current_equity

        # Calculate drawdown
        if self.peak_equity > 0:
            drawdown = (self.peak_equity - current_equity) / self.peak_equity * 100
        else:
            drawdown = 0.0

        self.current_drawdown = drawdown

        # Determine risk level
        if drawdown < 2:
            level = RiskLevel.LOW
        elif drawdown < self.max_daily_drawdown:
            level = RiskLevel.MEDIUM
        elif drawdown < self.max_daily_drawdown * 2:
            level = RiskLevel.HIGH
        else:
            level = RiskLevel.CRITICAL

        return drawdown, level

    def check_correlation_risk(
        self,
        positions: Dict[str, float]
    ) -> List[RiskAlert]:
        """Check for correlation concentration risk"""
        alerts = []

        # Asset class mapping
        asset_classes = {
            "XAU": "precious_metal",
            "XAG": "precious_metal",
            "BTC": "crypto",
            "ETH": "crypto",
            "XPD": "precious_metal",
            "XPT": "precious_metal"
        }

        # Group by asset class
        class_exposure = {}
        for asset, size in positions.items():
            asset_class = asset_classes.get(asset, "other")
            class_exposure[asset_class] = class_exposure.get(asset_class, 0) + size

        # Check concentration
        for asset_class, exposure in class_exposure.items():
            if exposure > self.max_position_size * 2:  # Allow 2x for same class
                alerts.append(RiskAlert(
                    timestamp=datetime.now(),
                    level=RiskLevel.HIGH,
                    category="correlation",
                    message=f"High concentration in {asset_class}: {exposure:.1f}%",
                    recommendation="Diversify across uncorrelated assets",
                    severity_score=0.7
                ))

        return alerts

    def generate_risk_report(
        self,
        assets: List[str],
        portfolio_value: float
    ) -> RiskReport:
        """Generate comprehensive risk report"""
        alerts = []
        recommendations = []
        overall_score = 0.0

        volatility_metrics = {}
        liquidity_metrics = {}

        # Check drawdown
        drawdown, dd_level = self.check_drawdown(portfolio_value)
        if dd_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            alerts.append(RiskAlert(
                timestamp=datetime.now(),
                level=dd_level,
                category="drawdown",
                message=f"Current drawdown: {drawdown:.2f}%",
                recommendation="Consider reducing position sizes",
                severity_score=min(drawdown / 10, 1.0)
            ))
            recommendations.append("Reduce exposure until drawdown recovers")
            overall_score += 0.3

        # Analyze each asset
        for asset in assets:
            # Volatility
            vol = self.calculate_volatility(asset)
            volatility_metrics[asset] = vol

            if vol.volatility_regime == "extreme":
                alerts.append(RiskAlert(
                    timestamp=datetime.now(),
                    level=RiskLevel.CRITICAL,
                    category="volatility",
                    message=f"{asset} in extreme volatility regime",
                    recommendation="Reduce position size or hedge",
                    severity_score=0.9
                ))
                recommendations.append(f"Consider hedging {asset} exposure")
                overall_score += 0.2

            # Liquidity
            liq = self.assess_liquidity(asset)
            liquidity_metrics[asset] = liq

            if liq.liquidity_score < self.liquidity_min_score:
                alerts.append(RiskAlert(
                    timestamp=datetime.now(),
                    level=RiskLevel.MEDIUM,
                    category="liquidity",
                    message=f"{asset} liquidity below threshold",
                    recommendation="Use limit orders, reduce position",
                    severity_score=0.5
                ))
                overall_score += 0.1

        # Determine overall risk level
        if overall_score > 0.7:
            portfolio_level = RiskLevel.CRITICAL
        elif overall_score > 0.4:
            portfolio_level = RiskLevel.HIGH
        elif overall_score > 0.2:
            portfolio_level = RiskLevel.MEDIUM
        else:
            portfolio_level = RiskLevel.LOW

        if not recommendations:
            recommendations.append("Risk levels acceptable - maintain current positions")

        return RiskReport(
            timestamp=datetime.now(),
            portfolio_risk_level=portfolio_level,
            volatility_metrics=volatility_metrics,
            liquidity_metrics=liquidity_metrics,
            alerts=alerts,
            overall_score=min(overall_score, 1.0),
            recommendations=recommendations
        )

    def format_risk_report(self, report: RiskReport) -> str:
        """Format risk report for display"""
        level_emoji = {
            RiskLevel.LOW: "🟢",
            RiskLevel.MEDIUM: "🟡",
            RiskLevel.HIGH: "🟠",
            RiskLevel.CRITICAL: "🔴"
        }

        output = f"""
## ⚠️ Risk Assessment Report

### Portfolio Status
- **Overall Risk**: {level_emoji[report.portfolio_risk_level]} {report.portfolio_risk_level.value.upper()}
- **Risk Score**: {report.overall_score:.1%}
- **Active Alerts**: {len(report.alerts)}

### Volatility Metrics
"""
        for asset, vol in report.volatility_metrics.items():
            regime_emoji = {
                "low": "🟢",
                "normal": "🟡",
                "high": "🟠",
                "extreme": "🔴",
                "unknown": "⚪"
            }.get(vol.volatility_regime, "⚪")

            output += f"- **{asset}**: {vol.current_volatility:.1%} annualized "
            output += f"({regime_emoji} {vol.volatility_regime})\n"

        if report.alerts:
            output += "\n### 🚨 Active Alerts\n"
            for alert in report.alerts[:5]:  # Show top 5
                emoji = level_emoji[alert.level]
                output += f"\n{emoji} **{alert.category.upper()}**: {alert.message}\n"
                output += f"   → {alert.recommendation}\n"

        output += "\n### 📋 Recommendations\n"
        for rec in report.recommendations:
            output += f"- {rec}\n"

        return output


# Quick risk check functions
def check_volatility(
    prices: List[float],
    window: int = 20
) -> float:
    """Quick volatility calculation"""
    if len(prices) < window:
        return 0.0

    recent = prices[-window:]
    returns = [(recent[i] - recent[i-1]) / recent[i-1] for i in range(1, len(recent))]

    if not returns:
        return 0.0

    mean = sum(returns) / len(returns)
    variance = sum((r - mean) ** 2 for r in returns) / len(returns)
    std = math.sqrt(variance)

    # Annualize
    return std * math.sqrt(252)


def check_liquidity(
    spread: float,
    price: float
) -> str:
    """Quick liquidity assessment"""
    spread_pct = (spread / price) * 100

    if spread_pct < 0.05:
        return "🟢 Excellent"
    elif spread_pct < 0.1:
        return "🟡 Good"
    elif spread_pct < 0.5:
        return "🟠 Moderate"
    else:
        return "🔴 Poor"


if __name__ == "__main__":
    # Test
    rm = RiskManager()

    # Add some price history
    for i in range(50):
        rm.update_price("XAU", 4640 + (i % 10 - 5) * 2)

    report = rm.generate_risk_report(["XAU"], 10000)
    print(rm.format_risk_report(report))
