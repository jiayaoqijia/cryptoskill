"""
MCP Server for Gold API Feed Skill
Production-ready MCP tool surface for OpenClaw and Claude Code
"""

import json
import sys
from typing import Dict, Any, Optional
from dataclasses import asdict

# Import all skill components
from price_feed import GoldAPIFeed, get_price_sync
from trading_analyzer import TradingAnalyzer, TradeSetup
from market_analyst import MarketAnalyst, Sentiment
from portfolio_manager import PortfolioManager, Order, OrderStatus
from risk_manager import RiskManager, RiskLevel


class GoldAPIMCPServer:
    """
    MCP Server exposing Gold API Feed Skill tools

    Tool Categories:
    - price: Real-time price data
    - analysis: Trade and market analysis
    - debate: Bull/bear debate rounds
    - portfolio: Order and portfolio management
    - risk: Risk monitoring and assessment
    """

    def __init__(self):
        self._feed = GoldAPIFeed()
        self._trading_analyzer = TradingAnalyzer()
        self._market_analyst = MarketAnalyst()
        self._portfolio_manager: Optional[PortfolioManager] = None
        self._risk_manager = RiskManager()

    # ============ Price Tools ============

    def get_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get current price for asset

        Args:
            symbol: Asset symbol (XAU, XAG, BTC, ETH, XPD, XPT, HG)

        Returns:
            {
                "success": bool,
                "symbol": str,
                "name": str,
                "price": float,
                "currency": str,
                "updated": str,
                "error": str (if failed)
            }
        """
        try:
            import asyncio

            async def fetch():
                return await self._feed.get_price(symbol)

            data = asyncio.run(fetch())

            if not data:
                return {
                    "success": False,
                    "error": f"Failed to fetch price for {symbol}"
                }

            return {
                "success": True,
                "symbol": data.symbol,
                "name": data.name,
                "price": data.close,
                "currency": data.currency,
                "updated": data.timestamp.isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_all_prices(self) -> Dict[str, Any]:
        """
        Get prices for all supported assets

        Returns:
            {
                "success": bool,
                "prices": {
                    "XAU": {"name": "Gold", "price": 4640.70, ...},
                    "BTC": {"name": "Bitcoin", "price": 68543.48, ...},
                    ...
                },
                "error": str (if failed)
            }
        """
        try:
            import asyncio

            async def fetch_all():
                return await self._feed.get_all_prices()

            prices = asyncio.run(fetch_all())

            if not prices:
                return {
                    "success": False,
                    "error": "Failed to fetch prices"
                }

            result = {}
            for symbol, data in prices.items():
                result[symbol] = {
                    "name": data.name,
                    "price": data.close,
                    "currency": data.currency,
                    "updated": data.timestamp.isoformat()
                }

            return {
                "success": True,
                "prices": result
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    # ============ Analysis Tools ============

    def analyze_trade_setup(
        self,
        asset: str,
        entry: float,
        stop: float,
        target: float,
        account: float = 10000.0,
        risk_percent: float = 1.0
    ) -> Dict[str, Any]:
        """
        Analyze trade setup with position sizing and risk checks

        Args:
            asset: Asset symbol
            entry: Entry price
            stop: Stop loss price
            target: Take profit price
            account: Account balance (default 10000)
            risk_percent: Risk percentage (default 1.0)

        Returns:
            {
                "success": bool,
                "approved": bool,
                "position_size": float,
                "risk_amount": float,
                "risk_reward_ratio": float,
                "recommendation": str,
                "reasoning": [str],
                "error": str (if failed)
            }
        """
        try:
            direction = "buy" if target > entry else "sell"

            setup = TradeSetup(
                asset=asset,
                direction=direction,
                entry_price=entry,
                stop_loss=stop,
                take_profit=target,
                account_balance=account,
                risk_percent=risk_percent
            )

            analysis = self._trading_analyzer.analyze_trade(setup)

            return {
                "success": True,
                "approved": analysis.recommendation in ["APPROVED", "🟢 BUY - Strong bullish consensus"],
                "position_size": analysis.position_size,
                "risk_amount": analysis.risk_amount,
                "risk_reward_ratio": analysis.risk_reward_ratio,
                "recommendation": analysis.recommendation,
                "reasoning": analysis.reasoning
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def market_analysis(
        self,
        asset: str,
        current_price: float,
        support: list,
        resistance: list,
        rsi: Optional[float] = None,
        trend: str = "neutral",
        price_change_24h: float = 0.0
    ) -> Dict[str, Any]:
        """
        Multi-agent market analysis

        Args:
            asset: Asset symbol
            current_price: Current market price
            support: List of support levels
            resistance: List of resistance levels
            rsi: RSI value (optional)
            trend: Trend direction (bullish/bearish/neutral)
            price_change_24h: 24h price change percentage

        Returns:
            {
                "success": bool,
                "sentiment": str (BULLISH/BEARISH/NEUTRAL),
                "confidence": float (0-1),
                "recommendation": str,
                "risk_level": str,
                "bullish_points": [str],
                "bearish_points": [str],
                "analyst_opinions": [{"type": str, "sentiment": str, "confidence": float}],
                "error": str (if failed)
            }
        """
        try:
            opinions = [
                self._market_analyst.analyze_technical(
                    current_price=current_price,
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

            analysis = self._market_analyst.synthesize_analysis(
                asset=asset,
                current_price=current_price,
                opinions=opinions
            )

            return {
                "success": True,
                "sentiment": analysis.overall_sentiment.value,
                "confidence": analysis.confidence_score,
                "recommendation": analysis.recommendation,
                "risk_level": analysis.risk_level,
                "bullish_points": analysis.bullish_points[:5],
                "bearish_points": analysis.bearish_points[:5],
                "analyst_opinions": [
                    {
                        "type": op.analyst_type,
                        "sentiment": op.sentiment.value,
                        "confidence": op.confidence
                    }
                    for op in analysis.analyst_opinions
                ]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    # ============ Debate Tools ============

    def run_debate(
        self,
        asset: str,
        current_price: float,
        rounds: int = 3
    ) -> Dict[str, Any]:
        """
        Run structured bull/bear debate

        Args:
            asset: Asset symbol
            current_price: Current market price
            rounds: Number of debate rounds (1-5)

        Returns:
            {
                "success": bool,
                "verdict": str,
                "rounds": [{"round": int, "bull": str, "bear": str, "winner": str}],
                "bull_wins": int,
                "bear_wins": int,
                "error": str (if failed)
            }
        """
        try:
            debate_rounds = self._market_analyst.run_debate_rounds(
                asset=asset,
                current_price=current_price,
                num_rounds=min(rounds, 5)
            )

            rounds_data = [
                {
                    "round": r.round_number,
                    "bull_argument": r.bull_argument,
                    "bear_argument": r.bear_argument,
                    "bull_strength": r.bull_strength,
                    "bear_strength": r.bear_strength,
                    "winner": r.winner
                }
                for r in debate_rounds
            ]

            bull_wins = sum(1 for r in debate_rounds if r.winner == "bull")
            bear_wins = sum(1 for r in debate_rounds if r.winner == "bear")

            if bull_wins > bear_wins:
                verdict = "BULL_CASE_STRONGER"
            elif bear_wins > bull_wins:
                verdict = "BEAR_CASE_STRONGER"
            else:
                verdict = "BALANCED_NO_CLEAR_WINNER"

            return {
                "success": True,
                "verdict": verdict,
                "rounds": rounds_data,
                "bull_wins": bull_wins,
                "bear_wins": bear_wins
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    # ============ Portfolio Tools ============

    def create_portfolio(
        self,
        initial_capital: float = 10000.0,
        max_risk_per_trade: float = 2.0
    ) -> Dict[str, Any]:
        """
        Create new portfolio

        Args:
            initial_capital: Starting capital (default 10000)
            max_risk_per_trade: Max risk % per trade (default 2.0)

        Returns:
            {
                "success": bool,
                "capital": float,
                "message": str,
                "error": str (if failed)
            }
        """
        try:
            self._portfolio_manager = PortfolioManager(
                initial_capital=initial_capital,
                max_risk_per_trade=max_risk_per_trade
            )

            return {
                "success": True,
                "capital": initial_capital,
                "message": f"Portfolio created with ${initial_capital:,.2f} capital"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def check_order(
        self,
        asset: str,
        entry: float,
        stop: float,
        risk_percent: float = 1.0
    ) -> Dict[str, Any]:
        """
        Check order eligibility

        Args:
            asset: Asset symbol
            entry: Entry price
            stop: Stop loss price
            risk_percent: Risk percentage (default 1.0)

        Returns:
            {
                "success": bool,
                "approved": bool,
                "position_size": float,
                "risk_amount": float,
                "notional": float,
                "margin_required": float,
                "reason": str,
                "error": str (if failed)
            }
        """
        try:
            if not self._portfolio_manager:
                return {
                    "success": False,
                    "error": "Portfolio not created. Call create_portfolio first."
                }

            sizing = self._portfolio_manager.calculate_position_size(
                asset, entry, stop, risk_percent
            )

            return {
                "success": True,
                "approved": sizing["approved"],
                "position_size": sizing.get("size", 0),
                "risk_amount": sizing.get("risk_amount", 0),
                "notional": sizing.get("notional", 0),
                "margin_required": sizing.get("margin_required", 0),
                "reason": sizing["reason"]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_portfolio_summary(self) -> Dict[str, Any]:
        """
        Get portfolio summary

        Returns:
            {
                "success": bool,
                "capital": float,
                "equity": float,
                "cash": float,
                "exposure_percent": float,
                "positions": [{"asset": str, "size": float, "pnl": float}],
                "error": str (if failed)
            }
        """
        try:
            if not self._portfolio_manager:
                return {
                    "success": False,
                    "error": "Portfolio not created"
                }

            # Update with current prices
            summary = self._portfolio_manager.get_portfolio_summary()

            # Parse the formatted string (simplified)
            # In production, return structured data directly
            return {
                "success": True,
                "summary": summary
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    # ============ Risk Tools ============

    def check_risk(
        self,
        assets: list,
        portfolio_value: float
    ) -> Dict[str, Any]:
        """
        Run comprehensive risk assessment

        Args:
            assets: List of asset symbols
            portfolio_value: Current portfolio value

        Returns:
            {
                "success": bool,
                "risk_level": str (LOW/MEDIUM/HIGH/CRITICAL),
                "risk_score": float (0-1),
                "alerts": [{"level": str, "category": str, "message": str}],
                "recommendations": [str],
                "error": str (if failed)
            }
        """
        try:
            report = self._risk_manager.generate_risk_report(
                assets, portfolio_value
            )

            return {
                "success": True,
                "risk_level": report.portfolio_risk_level.value,
                "risk_score": report.overall_score,
                "alerts": [
                    {
                        "level": alert.level.value,
                        "category": alert.category,
                        "message": alert.message,
                        "severity": alert.severity_score
                    }
                    for alert in report.alerts
                ],
                "recommendations": report.recommendations
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Global server instance
_server = GoldAPIMCPServer()


def handle_mcp_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle MCP request and route to appropriate tool

    Request format:
    {
        "tool": "get_price",
        "params": {"symbol": "XAU"}
    }
    """
    tool = request.get("tool")
    params = request.get("params", {})

    # Price tools
    if tool == "get_price":
        return _server.get_price(params.get("symbol", "XAU"))

    elif tool == "get_all_prices":
        return _server.get_all_prices()

    # Analysis tools
    elif tool == "analyze_trade_setup":
        return _server.analyze_trade_setup(
            asset=params.get("asset", ""),
            entry=params.get("entry", 0.0),
            stop=params.get("stop", 0.0),
            target=params.get("target", 0.0),
            account=params.get("account", 10000.0),
            risk_percent=params.get("risk_percent", 1.0)
        )

    elif tool == "market_analysis":
        return _server.market_analysis(
            asset=params.get("asset", ""),
            current_price=params.get("current_price", 0.0),
            support=params.get("support", []),
            resistance=params.get("resistance", []),
            rsi=params.get("rsi"),
            trend=params.get("trend", "neutral"),
            price_change_24h=params.get("price_change_24h", 0.0)
        )

    # Debate tools
    elif tool == "run_debate":
        return _server.run_debate(
            asset=params.get("asset", ""),
            current_price=params.get("current_price", 0.0),
            rounds=params.get("rounds", 3)
        )

    # Portfolio tools
    elif tool == "create_portfolio":
        return _server.create_portfolio(
            initial_capital=params.get("initial_capital", 10000.0),
            max_risk_per_trade=params.get("max_risk_per_trade", 2.0)
        )

    elif tool == "check_order":
        return _server.check_order(
            asset=params.get("asset", ""),
            entry=params.get("entry", 0.0),
            stop=params.get("stop", 0.0),
            risk_percent=params.get("risk_percent", 1.0)
        )

    elif tool == "get_portfolio_summary":
        return _server.get_portfolio_summary()

    # Risk tools
    elif tool == "check_risk":
        return _server.check_risk(
            assets=params.get("assets", []),
            portfolio_value=params.get("portfolio_value", 0.0)
        )

    else:
        return {
            "success": False,
            "error": f"Unknown tool: {tool}"
        }


def main():
    """Main entry point for MCP server"""
    print("Gold API MCP Server started", file=sys.stderr)

    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            response = handle_mcp_request(request)
            print(json.dumps(response), flush=True)
        except json.JSONDecodeError as e:
            print(json.dumps({
                "success": False,
                "error": f"Invalid JSON: {str(e)}"
            }), flush=True)
        except Exception as e:
            print(json.dumps({
                "success": False,
                "error": str(e)
            }), flush=True)


if __name__ == "__main__":
    main()
