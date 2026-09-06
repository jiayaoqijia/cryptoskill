"""
Enhanced Claude Code Tool for Gold API Feed
Combines real-time price data with trading analysis
"""

from typing import Optional, Dict, List
from dataclasses import dataclass

# Import the price feed
from price_feed import GoldAPIFeed, get_price_sync

# Import trading analyzer
from trading_analyzer import (
    TradingAnalyzer,
    TradeSetup,
    quick_trade_check,
    position_size_calculator
)

# Import market analyst (TradingAgents-inspired)
from market_analyst import (
    MarketAnalyst,
    quick_market_analysis,
    Sentiment
)

# Import Portfolio Manager and Risk Manager
from portfolio_manager import PortfolioManager, Order, OrderStatus
from risk_manager import RiskManager, RiskLevel


@dataclass
class MarketSnapshot:
    """Complete market snapshot with analysis"""
    gold_price: float
    silver_price: float
    bitcoin_price: float
    ethereum_price: float
    timestamp: str


class EnhancedGoldPriceTool:
    """
    Enhanced Claude Code tool for precious metals and crypto trading

    Features:
    - Real-time price fetching
    - Trade setup analysis
    - Position sizing
    - Risk management
    - Multi-asset correlation

    Usage in Claude Code:
        from claude_code_tool import EnhancedGoldPriceTool

        tool = EnhancedGoldPriceTool()

        # Get prices
        print(tool.get_gold_price())
        print(tool.get_all_prices())

        # Analyze trade
        analysis = tool.analyze_trade_setup(
            asset="XAUUSD",
            entry=4640,
            stop=4620,
            target=4680,
            account=10000,
            risk=1.0
        )
        print(analysis)
    """

    def __init__(self):
        self._feed = GoldAPIFeed()
        self._analyzer = TradingAnalyzer()
        self._market_analyst = MarketAnalyst()  # TradingAgents-inspired
        self._portfolio_manager = PortfolioManager(initial_capital=10000.0)
        self._risk_manager = RiskManager()

    # ============ Price Functions ============

    def get_price(self, symbol: str) -> Optional[str]:
        """Fetch current price for symbol"""
        import asyncio

        async def fetch():
            return await self._feed.get_price(symbol)

        data = asyncio.run(fetch())
        if data:
            return self._feed.format_price(data)
        return None

    def get_gold_price(self) -> str:
        """Get current gold price (XAU/USD)"""
        result = self.get_price("XAU")
        return result or "❌ Unable to fetch gold price"

    def get_silver_price(self) -> str:
        """Get current silver price (XAG/USD)"""
        result = self.get_price("XAG")
        return result or "❌ Unable to fetch silver price"

    def get_bitcoin_price(self) -> str:
        """Get current bitcoin price (BTC/USD)"""
        result = self.get_price("BTC")
        return result or "❌ Unable to fetch bitcoin price"

    def get_ethereum_price(self) -> str:
        """Get current ethereum price (ETH/USD)"""
        result = self.get_price("ETH")
        return result or "❌ Unable to fetch ethereum price"

    def get_all_prices(self) -> str:
        """Get all available asset prices with market summary"""
        import asyncio

        async def fetch_all():
            return await self._feed.get_all_prices()

        prices = asyncio.run(fetch_all())

        if not prices:
            return "❌ Unable to fetch prices"

        # Build formatted output
        result = "## 📊 Live Market Prices\n\n"
        result += "| Asset | Price | Type |\n"
        result += "|-------|-------|------|\n"

        for symbol, data in prices.items():
            asset_type = self._feed.ASSETS.get(symbol, {}).get("type", "Unknown")
            result += f"| {data.name} ({symbol}) | **${data.price:,.2f}** | {asset_type} |\n"

        result += "\n*Data from gold-api.com (60s cached)*\n"
        return result

    def get_market_snapshot(self) -> MarketSnapshot:
        """Get key market snapshot"""
        import asyncio

        async def fetch_key():
            gold = await self._feed.get_price("XAU")
            silver = await self._feed.get_price("XAG")
            btc = await self._feed.get_price("BTC")
            eth = await self._feed.get_price("ETH")
            return gold, silver, btc, eth

        gold, silver, btc, eth = asyncio.run(fetch_key())

        return MarketSnapshot(
            gold_price=gold.price if gold else 0,
            silver_price=silver.price if silver else 0,
            bitcoin_price=btc.price if btc else 0,
            ethereum_price=eth.price if eth else 0,
            timestamp=datetime.now().isoformat()
        )

    # ============ Trading Analysis Functions ============

    def analyze_trade_setup(
        self,
        asset: str,
        entry: float,
        stop: float,
        target: float,
        account: float = 10000,
        risk: float = 1.0
    ) -> str:
        """
        Complete trade setup analysis

        Args:
            asset: Asset symbol (XAU, BTC, etc)
            entry: Entry price
            stop: Stop loss price
            target: Take profit price
            account: Account balance (default $10k)
            risk: Risk percentage (default 1%)

        Returns:
            Formatted trade analysis
        """
        direction = "buy" if target > entry else "sell"

        setup = TradeSetup(
            asset=asset,
            direction=direction,
            entry_price=entry,
            stop_loss=stop,
            take_profit=target,
            account_balance=account,
            risk_percent=risk
        )

        analysis = self._analyzer.analyze_trade(setup)
        return self._analyzer.format_trade_analysis(analysis)

    def calculate_position(
        self,
        account: float,
        risk_percent: float,
        entry: float,
        stop: float
    ) -> Dict:
        """Calculate position size"""
        return self._analyzer.calculate_position_size(
            account, risk_percent, entry, stop
        )

    def quick_position_size(
        self,
        account: float,
        risk_percent: float,
        entry: float,
        stop: float
    ) -> str:
        """Quick position size recommendation"""
        sizing = self.calculate_position(account, risk_percent, entry, stop)

        if "error" in sizing:
            return f"❌ Error: {sizing['error']}"

        return f"""
## 📐 Position Size Calculator

**Parameters**:
- Account: ${account:,.2f}
- Risk: {risk_percent}%
- Entry: ${entry:,.2f}
- Stop: ${stop:,.2f}

**Results**:
- 💰 Risk Amount: ${sizing['risk_amount']:,.2f}
- 📏 Stop Distance: ${sizing['stop_pips']:,.2f}
- 📊 Position Size: {sizing['position_size']:.2f} lots
- 🔢 Micro-lots: {sizing['max_units']}
"""

    def assess_risk(
        self,
        positions: List[Dict],
        account_balance: float
    ) -> str:
        """Assess portfolio risk"""
        assessment = self._analyzer.assess_portfolio_risk(positions, account_balance)

        output = "## ⚠️ Portfolio Risk Assessment\n\n"
        output += f"**Total Exposure**: ${assessment['total_exposure']:,.2f} ({assessment['exposure_percent']:.1f}%)\n"
        output += f"**Total Risk**: ${assessment['total_risk']:,.2f} ({assessment['risk_percent']:.1f}%)\n"
        output += f"**Status**: {assessment['status']}\n\n"

        if assessment['warnings']:
            output += "**Warnings**:\n"
            for warning in assessment['warnings']:
                output += f"- ⚠️ {warning}\n"
        else:
            output += "✅ All risk parameters within acceptable limits\n"

        return output

    def get_correlation_summary(self) -> str:
        """Get asset correlation summary"""
        # This would require historical data
        # For now, return typical correlations
        return """
## 📈 Asset Correlation Matrix

**Typical Correlations** (Gold as base):

| Asset | Correlation | Relationship |
|-------|-------------|--------------|
| Silver (XAG) | +0.85 | Strong positive |
| Bitcoin (BTC) | +0.45 | Moderate positive |
| Ethereum (ETH) | +0.40 | Moderate positive |
| Copper (HG) | +0.30 | Weak positive |

**Key Insights**:
- **Risk-On/Off**: Gold & Silver act as safe havens
- **Diversification**: BTC/ETH provide some decorrelation
- **Economic Indicator**: Copper tracks industrial activity

*Note: Real-time correlation requires historical data analysis*
"""

    # ============ TradingAgents-Inspired Market Analysis ============

    def market_analysis(
        self,
        asset: str,
        support: List[float],
        resistance: List[float],
        rsi: Optional[float] = None,
        trend: str = "neutral",
        price_change_24h: float = 0
    ) -> str:
        """
        Multi-agent market analysis (TradingAgents-inspired)

        Analyzes from multiple perspectives:
        - Technical Analyst (support/resistance, indicators)
        - Sentiment Analyst (price momentum, volume)
        - Fundamental Analyst (macro conditions)

        Returns synthesized recommendation with confidence score.
        """
        # Get current price
        import asyncio
        async def fetch():
            return await self._feed.get_price(asset)

        price_data = asyncio.run(fetch())
        if not price_data:
            return "❌ Unable to fetch price for analysis"

        # Build opinions from different "analysts"
        opinions = [
            self._market_analyst.analyze_technical(
                current_price=price_data.close,
                support_levels=support,
                resistance_levels=resistance,
                rsi=rsi,
                trend=trend
            ),
            self._market_analyst.analyze_sentiment(
                price_change_24h=price_change_24h,
                volume_vs_avg=1.0
            ),
            self._market_analyst.analyze_fundamental(
                asset=asset,
                macro_trend="neutral"
            )
        ]

        # Synthesize analysis
        analysis = self._market_analyst.synthesize_analysis(
            asset=asset,
            current_price=price_data.close,
            opinions=opinions
        )

        return self._market_analyst.format_analysis(analysis)

    def debate_market_outlook(
        self,
        asset: str,
        thesis: str
    ) -> str:
        """
        Bullish vs Bearish debate (TradingAgents Researcher Team concept)

        Presents arguments from both sides for balanced view.
        """
        return f"""
## 🎭 Market Debate: {asset}

### Thesis: {thesis}

---

### 🐂 Bullish Argument

**Key Points**:
1. Historical safe haven during uncertainty
2. Inflation hedge with monetary expansion
3. Central bank buying increasing demand
4. Technical support holding at key levels

**Scenario**: Risk-off sentiment drives capital to precious metals

---

### 🐻 Bearish Argument

**Key Points**:
1. Strong dollar reduces appeal
2. Risk-on environment favors equities
3. Higher interest rates increase opportunity cost
4. Resistance levels capping gains

**Scenario**: Economic strength reduces safe haven demand

---

### ⚖️ Balanced View

Consider both scenarios and position size accordingly.
Monitor: Fed policy, dollar strength, risk appetite
"""

    # ============ Portfolio Manager Integration ============

    def create_portfolio(self, initial_capital: float = 10000.0, max_risk: float = 2.0) -> str:
        """Create new portfolio with capital and risk settings"""
        self._portfolio_manager = PortfolioManager(
            initial_capital=initial_capital,
            max_risk_per_trade=max_risk
        )
        return f"✅ Portfolio created with ${initial_capital:,.2f} capital"

    def check_order(self, asset: str, entry: float, stop: float, risk: float = 1.0) -> str:
        """Check if order is eligible (Portfolio Manager validation)"""
        sizing = self._portfolio_manager.calculate_position_size(asset, entry, stop, risk)

        if sizing["approved"]:
            return f"""## ✅ Order Approved
- **Position Size**: {sizing['size']:.2f} lots
- **Risk Amount**: ${sizing['risk_amount']:,.2f}
- **Notional**: ${sizing.get('notional', 0):,.2f}
- **Margin**: ${sizing.get('margin_required', 0):,.2f}"""
        else:
            return f"""## ❌ Order Rejected
**Reason**: {sizing['reason']}"""

    def get_portfolio_summary(self) -> str:
        """Get complete portfolio summary"""
        return self._portfolio_manager.get_portfolio_summary()

    # ============ Risk Manager Integration ============

    def check_risk(self, assets: List[str], portfolio_value: float) -> str:
        """Run comprehensive risk assessment"""
        report = self._risk_manager.generate_risk_report(assets, portfolio_value)
        return self._risk_manager.format_risk_report(report)

    def run_debate(self, asset: str, rounds: int = 3) -> str:
        """Run structured debate with configurable rounds"""
        import asyncio
        async def fetch():
            return await self._feed.get_price(asset)

        price_data = asyncio.run(fetch())
        if not price_data:
            return "❌ Unable to fetch price for debate"

        debate_rounds = self._market_analyst.run_debate_rounds(asset, price_data.close, rounds)
        return self._market_analyst.format_debate(debate_rounds, asset)


# ============ Convenience Functions ============

def gold_price() -> str:
    """Quick function to get gold price"""
    return EnhancedGoldPriceTool().get_gold_price()


def bitcoin_price() -> str:
    """Quick function to get bitcoin price"""
    return EnhancedGoldPriceTool().get_bitcoin_price()


def market_summary() -> str:
    """Quick function to get all prices"""
    return EnhancedGoldPriceTool().get_all_prices()


def analyze_trade(
    asset: str,
    entry: float,
    stop: float,
    target: float,
    account: float = 10000,
    risk: float = 1.0
) -> str:
    """Quick trade analysis"""
    return EnhancedGoldPriceTool().analyze_trade_setup(asset, entry, stop, target, account, risk)


def position_size(
    account: float,
    risk_percent: float,
    entry: float,
    stop: float
) -> str:
    """Quick position size calculation"""
    return EnhancedGoldPriceTool().quick_position_size(account, risk_percent, entry, stop)


if __name__ == "__main__":
    # Test
    tool = EnhancedGoldPriceTool()
    print(tool.get_all_prices())
    print("\n" + tool.analyze_trade_setup("XAUUSD", 4640, 4620, 4680, 10000, 1.0))
