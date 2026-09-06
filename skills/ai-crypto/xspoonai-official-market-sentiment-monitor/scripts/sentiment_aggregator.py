"""
Sentiment Aggregator - Unified Market Sentiment Scoring System

Combines all sentiment signals into:
- Composite sentiment score
- Multi-factor risk assessment
- Trading signals and confidence levels
- Trend forecasts and alerts
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sentiment_analyzer import SentimentAnalyzer
from social_sentiment_tracker import SocialSentimentTracker
from market_trend_detector import MarketTrendDetector
from anomaly_detector import AnomalyDetector


class SentimentAggregator:
    """Aggregates all sentiment sources into comprehensive market assessment."""

    def __init__(self):
        """Initialize aggregator with all sentiment sources."""
        self.on_chain = SentimentAnalyzer()
        self.social = SocialSentimentTracker()
        self.trends = MarketTrendDetector()
        self.anomalies = AnomalyDetector()

    def aggregate_all_sentiments(self) -> Dict[str, Any]:
        """
        Aggregate all sentiment sources into comprehensive analysis.
        
        Returns:
            Complete sentiment aggregation with trading signals
        """
        print("Fetching on-chain sentiment...", end=" ", flush=True)
        on_chain = self.on_chain.analyze_sentiment_on_chain()
        print("✓")
        
        print("Fetching social sentiment...", end=" ", flush=True)
        social = self.social.analyze_social_sentiment()
        print("✓")
        
        print("Fetching market trends...", end=" ", flush=True)
        trends = self.trends.analyze_market_trends()
        print("✓")
        
        print("Fetching anomaly detection...", end=" ", flush=True)
        anomalies = self.anomalies.analyze_anomalies()
        print("✓")
        print()

        # Extract individual sentiment scores
        on_chain_score = on_chain.get("overall_sentiment_score", 50)
        social_score = social.get("overall_sentiment_score", 50)
        trend_score = self._convert_trend_to_score(trends.get("trend_signal", "HOLD"))
        anomaly_score = max(0, 100 - anomalies.get("overall_risk_score", 0))

        # Calculate weighted composite sentiment
        composite_sentiment = (
            on_chain_score * 0.30 +
            social_score * 0.25 +
            trend_score * 0.30 +
            anomaly_score * 0.15
        )

        # Generate unified signal
        unified_signal = self._generate_unified_signal(
            composite_sentiment,
            on_chain_score,
            social_score,
            trend_score,
            anomaly_score,
            anomalies.get("risk_level", "LOW")
        )

        # Calculate confidence (average of all component confidences)
        confidence = (
            on_chain.get("confidence", 85) +
            social.get("confidence", 85) +
            trends.get("confidence", 85) +
            anomalies.get("confidence", 85)
        ) / 4

        return {
            "analysis_type": "unified_sentiment",
            "composite_sentiment_score": round(composite_sentiment, 2),
            "sentiment_level": self._score_to_level(composite_sentiment),
            "unified_trading_signal": unified_signal,
            "confidence": round(confidence, 1),
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "component_scores": {
                "on_chain_sentiment": round(on_chain_score, 2),
                "social_sentiment": round(social_score, 2),
                "trend_sentiment": round(trend_score, 2),
                "risk_adjusted_sentiment": round(anomaly_score, 2)
            },
            "detailed_components": {
                "on_chain": on_chain,
                "social": social,
                "trends": trends,
                "anomalies": anomalies
            },
            "consolidated_signals": {
                "price_direction": trends["trend_signal"],
                "volume_confirmation": "YES" if trends["components"]["volume_analysis"]["volume_trend"] == "INCREASING" else "NO",
                "community_alignment": "BULLISH" if social_score > 50 else "BEARISH",
                "risk_level": anomalies["risk_level"],
                "chain_health": self._assess_chain_health(on_chain)
            },
            "trading_recommendations": self._generate_recommendations(
                composite_sentiment,
                anomalies["risk_level"]
            ),
            "key_metrics": {
                "ethereum_price": on_chain["components"]["eth_metrics"]["current_price"],
                "gas_price": on_chain["components"]["network_activity"]["fast_gas_price"],
                "market_cap": on_chain["components"]["eth_metrics"]["market_cap"],
                "24h_volume": on_chain["components"]["eth_metrics"]["volume_24h"]
            },
            "alerts": self._consolidate_alerts(anomalies, on_chain, social),
            "next_rebalance": (datetime.utcnow() + timedelta(hours=1)).isoformat()
        }

    def _convert_trend_to_score(self, trend_signal: str) -> float:
        """Convert trend signal to sentiment score."""
        mapping = {
            "STRONG BUY": 85,
            "BUY": 70,
            "HOLD": 50,
            "SELL": 30,
            "STRONG SELL": 15
        }
        return mapping.get(trend_signal, 50)

    def _score_to_level(self, score: float) -> str:
        """Convert score to sentiment level."""
        if score > 75:
            return "EXTREMELY BULLISH"
        elif score > 60:
            return "VERY BULLISH"
        elif score > 50:
            return "BULLISH"
        elif score > 40:
            return "NEUTRAL"
        elif score > 30:
            return "BEARISH"
        else:
            return "VERY BEARISH"

    def _generate_unified_signal(self, composite: float, on_chain: float, 
                                social: float, trend: float, anomaly: float,
                                risk_level: str) -> str:
        """Generate unified trading signal from all components."""
        
        # Risk-adjusted signal
        if risk_level == "CRITICAL":
            return "SELL / REDUCE EXPOSURE"
        elif risk_level == "HIGH":
            if composite > 60:
                return "BUY WITH CAUTION"
            else:
                return "WAIT FOR CONFIRMATION"
        
        # Normal conditions
        bullish_count = sum([1 for score in [on_chain, social, trend, anomaly] if score > 60])
        
        if bullish_count >= 3 and composite > 70:
            return "STRONG BUY"
        elif bullish_count >= 2 and composite > 60:
            return "BUY"
        elif composite > 50:
            return "HOLD / ACCUMULATE"
        elif composite > 40:
            return "HOLD"
        else:
            return "SELL"

    def _assess_chain_health(self, on_chain_data: Dict[str, Any]) -> str:
        """Assess blockchain network health."""
        gas_pressure = on_chain_data["components"]["network_activity"]["gas_pressure"]
        
        if gas_pressure > 70:
            return "CONGESTED"
        elif gas_pressure > 40:
            return "MODERATE"
        else:
            return "HEALTHY"

    def _generate_recommendations(self, sentiment: float, risk: str) -> List[str]:
        """Generate actionable trading recommendations."""
        recommendations = []

        if sentiment > 70 and risk != "CRITICAL":
            recommendations.append("Position Size: Large (risk: moderate)")
            recommendations.append("Entry: Accumulate gradually or dip buying")
            recommendations.append("Target: +15-25% from current levels")
            recommendations.append("Stop Loss: 5-8% below entry")

        elif sentiment > 50 and risk in ["LOW", "MEDIUM"]:
            recommendations.append("Position Size: Medium")
            recommendations.append("Entry: Dollar-cost averaging (DCA)")
            recommendations.append("Target: +8-12% from current levels")
            recommendations.append("Stop Loss: 10% below entry")

        elif sentiment > 40 or risk == "MEDIUM":
            recommendations.append("Position Size: Small (hedged)")
            recommendations.append("Action: Hold existing positions")
            recommendations.append("Watch for: Breakout signals")
            recommendations.append("Risk: Keep tight stops")

        elif risk == "HIGH":
            recommendations.append("Position Size: Reduce or exit")
            recommendations.append("Action: Rebalance to stablecoins")
            recommendations.append("Wait for: Risk metrics to normalize")

        else:
            recommendations.append("Position Size: None (wait)")
            recommendations.append("Action: Move to stablecoins/cash")
            recommendations.append("Watch for: Capitulation signals")

        return recommendations

    def _consolidate_alerts(self, anomalies: Dict, on_chain: Dict, social: Dict) -> List[str]:
        """Consolidate alerts from all sources."""
        alerts = []

        # Add anomaly alerts
        alerts.extend(anomalies.get("alerts", []))

        # Add major events
        if social["components"]["news_sentiment"]["sentiment_trend"] == "BULLISH":
            alerts.append("📰 News sentiment is positive")

        return alerts[:5]  # Return top 5 alerts


if __name__ == "__main__":
    aggregator = SentimentAggregator()
    
    print("=" * 70)
    print("REAL-TIME ON-CHAIN MARKET SENTIMENT AGGREGATOR")
    print("=" * 70)
    print()
    
    result = aggregator.aggregate_all_sentiments()
    
    print("=" * 70)
    print("UNIFIED SENTIMENT ASSESSMENT")
    print("=" * 70)
    print()
    print(f"Composite Sentiment Score: {result['composite_sentiment_score']}/100")
    print(f"Sentiment Level: {result['sentiment_level']}")
    print(f"Trading Signal: {result['unified_trading_signal']}")
    print(f"Confidence: {result['confidence']}%")
    print()
    print("Component Breakdown:")
    scores = result['component_scores']
    print(f"  - On-Chain Sentiment: {scores['on_chain_sentiment']}/100")
    print(f"  - Social Sentiment: {scores['social_sentiment']}/100")
    print(f"  - Trend Sentiment: {scores['trend_sentiment']}/100")
    print(f"  - Risk-Adjusted: {scores['risk_adjusted_sentiment']}/100")
    print()
    print("Consolidated Signals:")
    signals = result['consolidated_signals']
    print(f"  - Price Direction: {signals['price_direction']}")
    print(f"  - Volume Confirmation: {signals['volume_confirmation']}")
    print(f"  - Community: {signals['community_alignment']}")
    print(f"  - Risk Level: {signals['risk_level']}")
    print(f"  - Chain Health: {signals['chain_health']}")
    print()
    print("Key Metrics:")
    metrics = result['key_metrics']
    print(f"  - ETH Price: ${metrics['ethereum_price']:,.2f}")
    print(f"  - Gas Price (Fast): {metrics['gas_price']} Gwei")
    print(f"  - Market Cap: ${metrics['market_cap']:,.0f}")
    print()
    print("Trading Recommendations:")
    for rec in result['trading_recommendations']:
        print(f"  • {rec}")
    print()
    if result['alerts']:
        print("Alerts:")
        for alert in result['alerts']:
            print(f"  {alert}")
    print()
    print("=" * 70)
    print("✅ Sentiment Analysis Complete - Next update:", result['next_rebalance'])
    print("=" * 70)
