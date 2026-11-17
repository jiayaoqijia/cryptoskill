# Crypto Futures Signal Analyzer

Read-only Python signal engine plus optional local Ollama AI explanation. **No trading or order placement.** Uses public completed Binance USD-M futures candles. No API key or Python third-party packages required.

## Windows Quick Start

```powershell
cd path\to\crypto-futures-signal-analyzer
python -m unittest discover -s tests -v
python scripts/analyze.py --symbol BTCUSDT
ollama list
ollama run llama3.1:8b
# Exit the model chat with /bye, then:
python local_agent.py
```

Install Ollama separately from https://ollama.com/download/windows and pull the model if needed: `ollama pull llama3.1:8b`. Ollama must be running for the local AI agent. `local_agent.py` supports BTC, ETH, SOL and BNB USDT pairs; the CLI supports syntactically valid USDT pairs available on Binance.

## Output and strategy

15m trend: completed 15m close > EMA21 = BULLISH, else BEARISH. BUY requires bullish trend, EMA9 > EMA21 on 1m, rolling simple RSI14 < 48, volume > current-inclusive MA10. SELL requires bearish trend, EMA9 < EMA21, RSI14 > 52, volume > MA10. Otherwise HOLD. No fresh EMA crossover required. `close_15m` and `as_of_15m_utc` distinguish the 15m trend candle from the latest completed 1m candle.

## Offline fixture

`python scripts/analyze.py --symbol BTCUSDT --fixture path/to/candles.json` where JSON has `candles_1m` and `candles_15m` arrays, each with at least 30 items containing `close`, `volume` (1m), and optional `close_time` in Unix milliseconds.

## Notes

Python unit tests are offline. Live API access depends on network and exchange availability. Ollama explanations are probabilistic and should be checked against JSON `signal` and `conditions`. Claude Code and Agensi publishing compatibility are not yet verified. Research/education only; not financial advice.

## Reliable explanations

`local_agent.py` now always prints an authoritative, deterministic explanation based on the engine's own boolean condition flags, including both candle timeframes. It rejects signal/condition mismatches. Ollama only provides an **optional, non-authoritative indicator glossary**, never live signal interpretation. If Ollama is unavailable, the verified report still prints. This is a local demonstration, **not** verified Agensi or Claude Code integration.
