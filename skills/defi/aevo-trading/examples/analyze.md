# Example: Market Analysis

A comprehensive ETH market analysis using multiple data sources to build a synthesized view.

---

**User**: What's the current state of ETH?

**Assistant**: Let me pull together a full market picture for ETH. I'll check price, trend, funding, volatility, and basis all at once.

*[calls aevo_onboard to verify session]*

Session is active. Pulling market data now.

*[calls in parallel: aevo_get_index_price(asset="ETH"), aevo_market_regime(asset="ETH"), aevo_funding_analysis(instrument_name="ETH-PERP"), aevo_volatility_snapshot(asset="ETH"), aevo_basis_analysis(asset="ETH")]*

Here's my ETH market analysis:

---

**Price**: $2,450.32 (index/spot reference)

**Market Regime**: Trending Up (72% confidence)
- 24h change: +3.2%
- Support zone: ~$2,380 (prior consolidation area)
- Resistance zone: ~$2,520 (recent rejection level)
- Trend has been intact for ~5 days with higher lows on the 4h timeframe

**Funding Rate**: Mildly Positive
- Current 8h rate: +0.0065% (annualized ~8.5%)
- 7-day average: +0.0048%
- Interpretation: Longs are paying shorts, but the rate is moderate — not overheated. Market positioning is net long but not at extreme levels.

**Volatility Snapshot**:
- 30-day realized vol: 52%
- ATM implied vol (front expiry): 58%
- Vol term structure: Contango (front 58% vs back 54%)
- Vol regime: Normal — not elevated, not suppressed
- IV vs RV spread: +6 points, implying options are slightly rich relative to recent movement

**Basis Analysis**:
- Perp premium: +0.12% above spot
- Front-month futures: +0.28% (annualized ~14%)
- Basis is positive and healthy, consistent with the bullish regime. No signs of backwardation or stress.

---

**Synthesis**:

ETH is in a mild uptrend with constructive momentum. Funding is positive but not extreme, which means the trend has room to continue without a funding squeeze. Volatility is normal — realized is tracking around 52% and implied is pricing a small premium, so options aren't screaming cheap or expensive.

**Actionable takeaways**:
1. **Directional bias**: Mildly bullish. Trend favors longs above $2,380 support.
2. **Perp positioning**: Funding cost is manageable (~8.5% annualized). Holding a long perp is viable but monitor for funding spikes above 0.01%.
3. **Options angle**: With IV slightly above RV, selling premium (covered calls or put spreads) has a small edge. If you're looking to get long via options, buying calls is slightly expensive relative to realized.
4. **Key risk**: A break below $2,380 would invalidate the uptrend and likely trigger a flush toward $2,280.

Want me to dive deeper into any of these areas, or would you like to look at a specific trade?

---

**User**: How about BTC? Is it correlated with ETH right now?

**Assistant**: Let me pull the same analysis for BTC so we can compare.

*[calls in parallel: aevo_get_index_price(asset="BTC"), aevo_market_regime(asset="BTC"), aevo_funding_analysis(instrument_name="BTC-PERP"), aevo_volatility_snapshot(asset="BTC")]*

**BTC Snapshot**: $67,240

**Market Regime**: Range-Bound (64% confidence)
- 24h change: +0.8%
- Range: $65,500 - $69,000
- BTC has been consolidating for ~10 days while ETH has been trending up

**Funding**: Near neutral (+0.0022%), much lower than ETH. Positioning is balanced.

**Volatility**: 30-day RV at 42%, ATM IV at 48%. Similar IV-RV spread to ETH but lower absolute vol.

**Correlation context**: ETH is outperforming BTC over the past week — the ETH/BTC ratio has been climbing. This divergence is notable: ETH is trending while BTC consolidates. Historically, this either resolves with BTC catching up (bullish), or ETH pulling back to re-correlate (bearish for ETH).

**Takeaway**: If you're bullish ETH, the relative strength vs BTC is encouraging. But be aware that a BTC breakdown below $65,500 would likely drag ETH down regardless of its own trend.
