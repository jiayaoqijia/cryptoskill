"""
Market Analyst Module
Inspired by TradingAgents multi-agent analysis
Provides bullish/bearish debate and confidence scoring
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class Sentiment(Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


@dataclass
class AnalystOpinion:
    """Single analyst opinion"""
    analyst_type: str  # technical, sentiment, fundamental, news
    sentiment: Sentiment
    confidence: float  # 0.0 to 1.0
    reasoning: List[str]
    key_factors: List[str]


@dataclass
class MarketAnalysis:
    """Complete market analysis with debate"""
    asset: str
    current_price: float
    overall_sentiment: Sentiment
    confidence_score: float
    bullish_points: List[str]
    bearish_points: List[str]
    analyst_opinions: List[AnalystOpinion]
    recommendation: str
    risk_level: str  # low, medium, high
    debate_rounds: int = 1
    consensus_reached: bool = False


@dataclass
class DebateRound:
    """Single debate round between bull and bear"""
    round_number: int
    bull_argument: str
    bear_argument: str
    bull_strength: float
    bear_strength: float
    winner: str  # "bull", "bear", "tie"


class MarketAnalyst:
    """
    Multi-perspective market analysis
    Inspired by TradingAgents analyst team with configurable debate rounds
    """

    def __init__(self, max_debate_rounds: int = 3):
        self.weights = {
            "technical": 0.30,
            "sentiment": 0.25,
            "fundamental": 0.25,
            "news": 0.20
        }

    def analyze_technical(
        self,
        current_price: float,
        support_levels: List[float],
        resistance_levels: List[float],
        rsi: Optional[float] = None,
        macd: Optional[float] = None,
        trend: str = "neutral"
    ) -> AnalystOpinion:
        """
        Technical Analyst perspective
        Inspired by TradingAgents Technical Analyst
        """
        reasoning = []
        key_factors = []
        sentiment = Sentiment.NEUTRAL
        confidence = 0.5

        # Support/Resistance analysis
        near_support = any(abs(current_price - s) / s < 0.02 for s in support_levels)
        near_resistance = any(abs(current_price - r) / r < 0.02 for r in resistance_levels)

        if near_support:
            sentiment = Sentiment.BULLISH
            confidence += 0.2
            key_factors.append("Price near support level")
        elif near_resistance:
            sentiment = Sentiment.BEARISH
            confidence += 0.2
            key_factors.append("Price near resistance level")

        # RSI analysis
        if rsi:
            if rsi < 30:
                sentiment = Sentiment.BULLISH
                confidence += 0.15
                key_factors.append(f"RSI oversold ({rsi:.1f})")
                reasoning.append("RSI indicates oversold conditions - potential bounce")
            elif rsi > 70:
                sentiment = Sentiment.BEARISH
                confidence += 0.15
                key_factors.append(f"RSI overbought ({rsi:.1f})")
                reasoning.append("RSI indicates overbought conditions - potential pullback")

        # MACD analysis
        if macd:
            if macd > 0:
                sentiment = Sentiment.BULLISH
                confidence += 0.1
                key_factors.append("MACD bullish")
            else:
                sentiment = Sentiment.BEARISH
                confidence += 0.1
                key_factors.append("MACD bearish")

        # Trend analysis
        if trend == "bullish":
            sentiment = Sentiment.BULLISH
            confidence += 0.1
            key_factors.append("Uptrend established")
        elif trend == "bearish":
            sentiment = Sentiment.BEARISH
            confidence += 0.1
            key_factors.append("Downtrend established")

        return AnalystOpinion(
            analyst_type="technical",
            sentiment=sentiment,
            confidence=min(confidence, 1.0),
            reasoning=reasoning,
            key_factors=key_factors
        )

    def analyze_sentiment(
        self,
        price_change_24h: float,
        volume_vs_avg: float,
        market_mood: str = "neutral"
    ) -> AnalystOpinion:
        """
        Sentiment Analyst perspective
        Inspired by TradingAgents Sentiment Analyst
        """
        reasoning = []
        key_factors = []
        sentiment = Sentiment.NEUTRAL
        confidence = 0.5

        # Price momentum sentiment
        if price_change_24h > 2:
            sentiment = Sentiment.BULLISH
            confidence += 0.2
            key_factors.append(f"Strong 24h gain (+{price_change_24h:.2f}%)")
            reasoning.append("Positive momentum suggests bullish sentiment")
        elif price_change_24h > 0.5:
            sentiment = Sentiment.BULLISH
            confidence += 0.1
            key_factors.append(f"Moderate 24h gain (+{price_change_24h:.2f}%)")
        elif price_change_24h < -2:
            sentiment = Sentiment.BEARISH
            confidence += 0.2
            key_factors.append(f"Strong 24h loss ({price_change_24h:.2f}%)")
            reasoning.append("Negative momentum suggests bearish sentiment")
        elif price_change_24h < -0.5:
            sentiment = Sentiment.BEARISH
            confidence += 0.1
            key_factors.append(f"Moderate 24h loss ({price_change_24h:.2f}%)")

        # Volume analysis
        if volume_vs_avg > 1.5:
            confidence += 0.15
            key_factors.append("High volume confirms sentiment")
            reasoning.append(f"Volume {volume_vs_avg:.1f}x above average confirms trend strength")

        # Market mood
        if market_mood == "greed":
            sentiment = Sentiment.BULLISH
            confidence += 0.1
            key_factors.append("Market greed indicator")
        elif market_mood == "fear":
            sentiment = Sentiment.BEARISH
            confidence += 0.1
            key_factors.append("Market fear indicator")

        return AnalystOpinion(
            analyst_type="sentiment",
            sentiment=sentiment,
            confidence=min(confidence, 1.0),
            reasoning=reasoning,
            key_factors=key_factors
        )

    def analyze_fundamental(
        self,
        asset: str,
        macro_trend: str = "neutral",
        inflation_data: Optional[float] = None
    ) -> AnalystOpinion:
        """
        Fundamental Analyst perspective
        Inspired by TradingAgents Fundamentals Analyst
        """
        reasoning = []
        key_factors = []
        sentiment = Sentiment.NEUTRAL
        confidence = 0.5

        # Asset-specific fundamentals
        if asset in ["XAU", "XAG"]:  # Precious metals
            if inflation_data and inflation_data > 3:
                sentiment = Sentiment.BULLISH
                confidence += 0.25
                key_factors.append(f"High inflation ({inflation_data}%) supports gold")
                reasoning.append("Inflation hedge demand likely to increase")
            elif macro_trend == "recession":
                sentiment = Sentiment.BULLISH
                confidence += 0.2
                key_factors.append("Safe haven demand in recession")
            elif macro_trend == "growth":
                sentiment = Sentiment.BEARISH
                confidence += 0.15
                key_factors.append("Risk-on sentiment reduces safe haven appeal")

        elif asset in ["BTC", "ETH"]:  # Crypto
            if macro_trend == "adoption":
                sentiment = Sentiment.BULLISH
                confidence += 0.2
                key_factors.append("Growing institutional adoption")
            elif macro_trend == "regulation":
                sentiment = Sentiment.BEARISH
                confidence += 0.2
                key_factors.append("Regulatory uncertainty")

        return AnalystOpinion(
            analyst_type="fundamental",
            sentiment=sentiment,
            confidence=min(confidence, 1.0),
            reasoning=reasoning,
            key_factors=key_factors
        )

    def analyze_news(
        self,
        recent_events: List[str],
        event_impact: str = "neutral"
    ) -> AnalystOpinion:
        """
        News Analyst perspective
        Inspired by TradingAgents News Analyst
        """
        reasoning = []
        key_factors = []
        sentiment = Sentiment.NEUTRAL
        confidence = 0.5

        if not recent_events:
            reasoning.append("No significant news events")
            return AnalystOpinion(
                analyst_type="news",
                sentiment=sentiment,
                confidence=confidence,
                reasoning=reasoning,
                key_factors=key_factors
            )

        # Analyze events
        positive_keywords = ["adoption", "bullish", "breakthrough", "partnership", "upgrade"]
        negative_keywords = ["ban", "regulation", "hack", "crash", "bearish", "sell-off"]

        positive_count = sum(1 for event in recent_events for kw in positive_keywords if kw in event.lower())
        negative_count = sum(1 for event in recent_events for kw in negative_keywords if kw in event.lower())

        if positive_count > negative_count:
            sentiment = Sentiment.BULLISH
            confidence += 0.2
            key_factors.append(f"{positive_count} positive news events")
            reasoning.append("Recent news flow is predominantly positive")
        elif negative_count > positive_count:
            sentiment = Sentiment.BEARISH
            confidence += 0.2
            key_factors.append(f"{negative_count} negative news events")
            reasoning.append("Recent news flow is predominantly negative")

        if event_impact == "high":
            confidence += 0.15
            key_factors.append("High-impact event detected")

        return AnalystOpinion(
            analyst_type="news",
            sentiment=sentiment,
            confidence=min(confidence, 1.0),
            reasoning=reasoning,
            key_factors=key_factors
        )

    def synthesize_analysis(
        self,
        asset: str,
        current_price: float,
        opinions: List[AnalystOpinion]
    ) -> MarketAnalysis:
        """
        Synthesize all analyst opinions into final recommendation
        Inspired by TradingAgents Trader Agent + Risk Management
        """
        # Calculate weighted sentiment
        bullish_score = 0
        bearish_score = 0

        for opinion in opinions:
            weight = self.weights.get(opinion.analyst_type, 0.25)
            if opinion.sentiment == Sentiment.BULLISH:
                bullish_score += opinion.confidence * weight
            elif opinion.sentiment == Sentiment.BEARISH:
                bearish_score += opinion.confidence * weight

        # Determine overall sentiment
        sentiment_diff = bullish_score - bearish_score
        if sentiment_diff > 0.2:
            overall_sentiment = Sentiment.BULLISH
            confidence_score = bullish_score
        elif sentiment_diff < -0.2:
            overall_sentiment = Sentiment.BEARISH
            confidence_score = bearish_score
        else:
            overall_sentiment = Sentiment.NEUTRAL
            confidence_score = max(bullish_score, bearish_score)

        # Extract points
        bullish_points = []
        bearish_points = []

        for opinion in opinions:
            for factor in opinion.key_factors:
                if opinion.sentiment == Sentiment.BULLISH:
                    bullish_points.append(f"[{opinion.analyst_type}] {factor}")
                elif opinion.sentiment == Sentiment.BEARISH:
                    bearish_points.append(f"[{opinion.analyst_type}] {factor}")

        # Risk assessment
        risk_level = "medium"
        if confidence_score > 0.8:
            risk_level = "high"  # High confidence = potential for big move
        elif confidence_score < 0.4:
            risk_level = "low"

        # Recommendation
        if overall_sentiment == Sentiment.BULLISH and confidence_score > 0.6:
            recommendation = "🟢 BUY - Strong bullish consensus"
        elif overall_sentiment == Sentiment.BULLISH:
            recommendation = "🟡 CAUTIOUS BUY - Moderate bullish"
        elif overall_sentiment == Sentiment.BEARISH and confidence_score > 0.6:
            recommendation = "🔴 SELL - Strong bearish consensus"
        elif overall_sentiment == Sentiment.BEARISH:
            recommendation = "🟠 CAUTIOUS SELL - Moderate bearish"
        else:
            recommendation = "⚪ NEUTRAL - Wait for clearer signal"

        return MarketAnalysis(
            asset=asset,
            current_price=current_price,
            overall_sentiment=overall_sentiment,
            confidence_score=confidence_score,
            bullish_points=bullish_points,
            bearish_points=bearish_points,
            analyst_opinions=opinions,
            recommendation=recommendation,
            risk_level=risk_level
        )

    def format_analysis(self, analysis: MarketAnalysis) -> str:
        """Format market analysis for display"""
        output = f"""
## 📊 Multi-Agent Market Analysis: {analysis.asset}

### Overview
- **Price**: ${analysis.current_price:,.2f}
- **Sentiment**: {analysis.overall_sentiment.value.upper()}
- **Confidence**: {analysis.confidence_score:.1%}
- **Risk Level**: {analysis.risk_level.upper()}

### 🐂 Bullish Points
"""
        for point in analysis.bullish_points[:5]:
            output += f"- ✅ {point}\n"

        output += "\n### 🐻 Bearish Points\n"
        for point in analysis.bearish_points[:5]:
            output += f"- ⚠️ {point}\n"

        output += f"\n### 📋 Analyst Breakdown\n"
        for opinion in analysis.analyst_opinions:
            emoji = "🟢" if opinion.sentiment == Sentiment.BULLISH else "🔴" if opinion.sentiment == Sentiment.BEARISH else "⚪"
            output += f"- {emoji} **{opinion.analyst_type.title()}**: {opinion.confidence:.0%} confidence\n"

        output += f"\n### 🎯 Recommendation\n**{analysis.recommendation}**\n"

        return output

    def run_debate_rounds(
        self,
        asset: str,
        current_price: float,
        num_rounds: int = 3
    ) -> List[DebateRound]:
        """
        Run structured debate between bull and bear cases
        Inspired by TradingAgents Researcher Team debates
        """
        rounds = []

        for i in range(num_rounds):
            round_num = i + 1

            # Generate arguments based on round number
            if round_num == 1:
                bull_arg = f"{asset} showing strong support at ${current_price * 0.99:.2f} with positive momentum"
                bear_arg = f"Resistance at ${current_price * 1.02:.2f} may cap gains near-term"
            elif round_num == 2:
                bull_arg = "Macro conditions favor safe haven flows into precious metals"
                bear_arg = "Rising interest rates increase opportunity cost of holding gold"
            else:
                bull_arg = "Institutional buying and central bank demand support long-term outlook"
                bear_arg = "Technical indicators showing overbought conditions suggest pullback"

            # Score arguments (simulated)
            bull_strength = 0.6 + (0.1 * i)  # Bulls gain strength in later rounds
            bear_strength = 0.5 + (0.05 * i)

            # Determine winner
            if bull_strength > bear_strength + 0.1:
                winner = "bull"
            elif bear_strength > bull_strength + 0.1:
                winner = "bear"
            else:
                winner = "tie"

            rounds.append(DebateRound(
                round_number=round_num,
                bull_argument=bull_arg,
                bear_argument=bear_arg,
                bull_strength=bull_strength,
                bear_strength=bear_strength,
                winner=winner
            ))

        return rounds

    def format_debate(self, rounds: List[DebateRound], asset: str) -> str:
        """Format debate rounds for display"""
        output = f"## 🎭 Structured Debate: {asset}\n\n"

        bull_wins = sum(1 for r in rounds if r.winner == "bull")
        bear_wins = sum(1 for r in rounds if r.winner == "bear")
        ties = sum(1 for r in rounds if r.winner == "tie")

        output += f"**Debate Summary**: Bull {bull_wins} - Bear {bear_wins} - Tie {ties}\n\n"

        for round in rounds:
            output += f"### Round {round.round_number}\n"
            output += f"🐂 **Bull**: {round.bull_argument}\n"
            output += f"   Strength: {round.bull_strength:.0%}\n\n"
            output += f"🐻 **Bear**: {round.bear_argument}\n"
            output += f"   Strength: {round.bear_strength:.0%}\n\n"

            winner_emoji = {"bull": "🟢", "bear": "🔴", "tie": "⚪"}
            output += f"**Winner**: {winner_emoji[round.winner]} {round.winner.upper()}\n\n"
            output += "---\n\n"

        # Overall verdict
        if bull_wins > bear_wins:
            verdict = "BULL CASE stronger overall"
        elif bear_wins > bull_wins:
            verdict = "BEAR CASE stronger overall"
        else:
            verdict = "BALANCED - No clear winner"

        output += f"### 🏆 Verdict: {verdict}\n"

        return output


# Quick analysis function
def quick_market_analysis(
    asset: str,
    current_price: float,
    support: List[float],
    resistance: List[float],
    rsi: Optional[float] = None,
    trend: str = "neutral",
    price_change_24h: float = 0
) -> str:
    """Quick market analysis"""
    analyst = MarketAnalyst()

    opinions = [
        analyst.analyze_technical(
            current_price=current_price,
            support_levels=support,
            resistance_levels=resistance,
            rsi=rsi,
            trend=trend
        ),
        analyst.analyze_sentiment(
            price_change_24h=price_change_24h,
            volume_vs_avg=1.0
        ),
        analyst.analyze_fundamental(
            asset=asset,
            macro_trend="neutral"
        )
    ]

    analysis = analyst.synthesize_analysis(asset, current_price, opinions)
    return analyst.format_analysis(analysis)


if __name__ == "__main__":
    # Test
    print(quick_market_analysis(
        asset="XAU",
        current_price=4640,
        support=[4600, 4550],
        resistance=[4700, 4750],
        rsi=58,
        trend="bullish",
        price_change_24h=0.45
    ))
