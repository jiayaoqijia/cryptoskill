# Research Summary: Chart Patterns for Stock Swing Trading

## Overview
Recent searches (past year, academic sites like arXiv/SSRN, freshness='py') yielded few pure empirical academic papers on classical chart patterns (e.g., Head & Shoulders, flags, triangles, breakouts) specifically for swing trading with backtests. Academia often focuses on ML alternatives or dismisses TA. Closest are practitioner backtests, statistical analyses (e.g., Bulkowski-derived), and ML detection methods. Prioritized empirical/backtested studies. Summaries below (4 top sources).

## 1. 12 Data-Proven Chart Patterns All Traders Need for Success
- **Authors/Source:** Liberated Stock Trader (2025)
- **Link:** https://www.liberatedstocktrader.com/chart-patterns-reliable-profitable/
- **Key Findings:** Historical performance analysis (using thepatternsite.com / Tom Bulkowski data) finds strong reliability for bullish breakouts: Inverse H&S (89% success, 45% avg move), Double Bottom (88%, 50%), Triple Bottom (87%, 45%), Descending Triangle (87%, 38%), Rectangle Top (85%, 51%, highest profitability). Bearish H&S top reported at 81% with `-16%`.
- **Patterns:** H&S (inverse/top), double/triple bottoms, triangles, rectangles, bull flags, wedges.
- **Success Rates:** High-80% range for many reversal/continuation setups in bull markets; pennants notably weaker (~46%).
- **Implementation for Algo Bots:** Auto-detect patterns (e.g., TradingView-style rules), enter on breakout close, target measured move (pattern height), place stop beyond swing structure.

## 2. Chart Patterns: The Ultimate 2026 Trading Guide (Reliability Ranked)
- **Authors/Source:** Forex Tester (2026)
- **Link:** https://forextester.com/blog/chart-patterns/
- **Key Findings:** Cross-asset backtests (stocks/forex/crypto) rank H&S (89%), Double Bottom (88%), and Bull Flag (85%) as top patterns. Emphasizes breakout volume expansion and RSI confirmation.
- **Patterns:** Reversals (H&S, double top/bottom, cup-and-handle, wedges), continuations (flags/pennants/rectangles), bilateral (triangles).
- **Success Rates:** Top-tier reliability reported at 85-89%, with fakeout risk when confirmation is missing.
- **Implementation for Algo Bots:** Entry on confirmed close beyond neckline/range, stop beyond swing invalidation, target measured move, and add volume/RSI gates.

## 3. I Tested Head & Shoulders Pattern on ALL Markets and Timeframes: Here are Results
- **Authors/Source:** Reddit `u/anonymous` (Dec 2025)
- **Link:** https://www.reddit.com/r/Daytrading/comments/1pwu2th/i_tested_head_shoulders_pattern_on_all_markets/
- **Key Findings:** Rule-based Python tests across stocks, crypto, futures, and forex suggest inconsistent edge. Crypto shows frequent false breaks, forex is noisy, and stocks/futures show only selective trend-context performance.
- **Patterns:** H&S and inverse H&S via neckline break/close logic.
- **Success Rates:** No robust numeric consistency reported; qualitative result indicates unstable expectancy.
- **Implementation for Algo Bots:** Encode strict shoulder/head geometry, confirm neckline close, and use invalidation stop + trailing or fixed TP.

## 4. Real-Time Head-and-Shoulders Pattern Detection for AI Trading Strategies
- **Authors/Source:** Jiri Pik (2025, from *Hands-On AI Trading with Python, QuantConnect and AWS*)
- **Link:** https://jiripik.com/2025/12/30/real-time-head-and-shoulders-pattern-detection-for-ai-trading-strategies/
- **Key Findings:** PyTorch CNN detects bearish H&S tops with 97% synthetic-data accuracy. Used as a risk overlay (position gate) rather than direct alpha.
- **Patterns:** Bearish H&S top.
- **Success Rates:** 97% accuracy on synthetic patterns; no full live-trading backtest performance published.
- **Implementation for Algo Bots:** Use normalized OHLC windows, stream inference, and require persistence (`k` consecutive bars) before de-risking.

## Bonus: Candlestick Patterns (Close Proxy)
- SSRN: *A Study on Profitability of Bullish Reversal Candlestick Chart Patterns in NIFTY 50* (2025)
- Findings: Harami (72.85% success), with Inverted Hammer and Engulfing as other top performers.
- Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5755102

## Notes
- Swing trading (days-weeks): Focus daily/4h; higher success in trends.
- Common: Volume + momentum (RSI/MACD) filters reduce fakeouts.
- Algo: Rule-based or CNN for detection; backtest rigorously.
- Scarce recent journals; practitioner data dominates.
