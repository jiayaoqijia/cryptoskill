# Binance Signal Engine

> Multi-timeframe crypto technical analysis signal generator for OpenClaw / ClawHub.

[![ClawHub](https://img.shields.io/badge/ClawHub-binance--signal--engine-blue)](https://clawhub.ai/eplt/binance-signal-engine)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## What It Does

Binance Signal Engine layers three timeframes (1D / 4H / 15m) into a single weighted technical analysis score for any Binance-listed crypto pair. When conditions align, it generates a complete trade plan with entry, stop-loss, take-profit, and position sizing.

```
═══════════════════════════════════════════════════
  BTC/USDT  |  SPOT  |  Score: 37.0
═══════════════════════════════════════════════════
  Regime : bullish
  Bias   : STRONG BULLISH
  Action : BUY
  Trend  : +25.0  |  Momentum: +7.0  |  Trigger: +5.0

  Signal Reasons:
    • Price > EMA50 (1D)
    • EMA9 > EMA21 (1D)
    • ADX=32.4 strong bullish trend
    • MACD > Signal (4H)
    • MACD histogram rising (4H)
    • RSI reclaimed above oversold (38.2)
    ...

  Trade Plan (READY):
    Side       : long
    Entry_type : market
    Entry      : 97432.10
    Stop_loss  : 95891.30
    Take_profit: 100514.70
    Effective_risk_reward: 2.00

  Position Size:
    Units      : 0.00648
    Notional   : $631.48
    Risk Budget: $100.00
═══════════════════════════════════════════════════
```

## Installation

### Via ClawHub (recommended)

```bash
npx clawhub@latest install binance-signal-engine
```

### Manual

```bash
# Clone into your OpenClaw skills directory
git clone https://github.com/eplt/binance-signal-engine.git \
  ~/.openclaw/skills/binance-signal-engine

# Install Python dependencies
pip install ccxt pandas numpy ta
```

## Usage

### From OpenClaw Chat

Just ask naturally:

- *"Analyze BTC/USDT"*
- *"What's the signal on ETH?"*
- *"Give me a trade setup for SOL/USDT on futures with 3x leverage"*
- *"Scan BTC, ETH, and SOL"*

### From the Command Line

```bash
# Basic analysis
python3 scripts/binance_signal_engine.py BTC/USDT

# Multiple pairs, JSON output
python3 scripts/binance_signal_engine.py BTC/USDT ETH/USDT SOL/USDT -o json

# Futures with custom parameters
python3 scripts/binance_signal_engine.py BTC/USDT -m futures -l 3 -b 5000 -r 2
```

## Architecture

```
1D  (high)  →  Trend Regime    EMA 9/21/50, ADX, DI+/DI−
4H  (mid)   →  Momentum        MACD cross/histogram, Stochastic
15m (low)   →  Entry Trigger   RSI reclaim, BB re-entry, volume spike, divergence
                    ↓
              Weighted Score  →  Bias  →  Trade Plan  →  Position Size
```

Each layer contributes independently to a composite score. The trend regime contextualises how momentum and trigger signals are interpreted — a bullish stochastic cross from oversold carries more weight in a bullish regime than a bearish one.

## Documentation

Full documentation is in **[references/guide.md](references/guide.md)**. The guide covers configuration, indicators, scoring, trade plans, position sizing, and examples. Review it for detailed explanations and common scenarios.

## Configuration

Create a JSON file and pass it with `--config`:

```json
{
  "ema_fast": 9,
  "ema_slow": 21,
  "ema_trend": 50,
  "adx_trend_threshold": 25.0,
  "rsi_oversold": 35.0,
  "rsi_overbought": 65.0,
  "atr_sl_multiplier": 1.5,
  "risk_reward_ratio": 2.0,
  "account_balance": 10000.0,
  "account_risk_pct": 1.0
}
```

All 40+ parameters are documented in the `Config` dataclass in the source.

## Security

- No API keys required — public OHLCV data only
- No orders placed — read-only exchange interaction
- No data exfiltration — all computation is local
- No files written to disk

## Requirements

- Python 3.8+
- `ccxt` `pandas` `numpy` `ta`

## License

MIT

## Author

[Edward Tsang](https://github.com/eplt) — blockchain & AI engineer. Open to consulting → [Email](mailto:edward@odw.ai) · [LinkedIn](https://www.linkedin.com/in/edwardtsang/)
