---
name: crypto-futures-signal-analyzer
description: Read-only Binance USD-M futures analysis using 15m EMA21 trend, 1m EMA9/EMA21, simple rolling RSI14 and volume MA10; explain deterministic BUY/SELL/HOLD without placing trades.
---
# Crypto Futures Signal Analyzer

Use `python scripts/analyze.py --symbol BTCUSDT` from this project root (substitute the requested USDT pair). The CLI produces JSON based on completed public Binance USD-M futures candles. Requires Python 3 and outbound network access. Use `--fixture path/to/file.json` for offline data containing `candles_1m` and `candles_15m`. Never invent live market data when the tool fails.

Report the engine's `signal` unchanged. Explain `conditions.buy` and `conditions.sell` booleans. For 15m trend compare **`close_15m`** with **`ema21_15m`** (not the 1m `price`), and show the separate `as_of_15m_utc` timestamp. BUY iff bullish 15m trend, 1m EMA9 > EMA21, RSI14 < 48 and current volume > volume MA10. SELL iff bearish 15m trend, 1m EMA9 < EMA21, RSI14 > 52 and current volume > volume MA10. Otherwise HOLD. RSI is simple rolling-average RSI, not Wilder; volume MA10 includes the current candle; no fresh crossover required.

Do not place orders, request trading credentials, recommend leverage, guarantee profits, or invent entry/stop-loss levels. Educational analysis only, not financial advice. Do not circumvent exchange restrictions. Local Ollama support is optional (`python local_agent.py`) and is **not** proof of Claude Code or Agensi marketplace compatibility.

When explaining results, copy condition flags exactly; do not let a language model reinterpret timeframe or signal logic.
