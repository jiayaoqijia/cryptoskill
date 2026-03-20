---
name: binance-signal-engine
description: Multi-timeframe crypto technical analysis with scored trading signals, structured trade plans, and position sizing via Binance public API. Use when user asks to "analyze BTC", "what's the signal on ETH/USDT", "crypto analysis", "trade setup for SOL", "scan crypto pairs", "check the trend on BTC", "multi-timeframe analysis", "generate a trading signal", "what's the bias on ETH", "TA on BTC/USDT", "is it a good time to buy BTC", or "position size for a crypto trade".
version: 1.0.2
homepage: https://github.com/eplt/binance-signal-engine
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins:
        - python3
    install:
      - kind: uv
        package: ccxt pandas numpy ta
        label: "Install Python dependencies (ccxt, pandas, numpy, ta)"
    files:
      - "scripts/*"

---

# Binance Signal Engine

Multi-timeframe technical analysis signal generator for cryptocurrency markets. Layers three timeframes into a single weighted score and outputs a structured trade plan with position sizing.

## When to Use

Use this skill when the user wants to:

- Analyze any Binance-listed crypto pair technically
- Get a directional bias or trading signal (bullish/bearish/neutral)
- Generate entry, stop-loss, and take-profit levels for a trade
- Check trend regime (1D), momentum (4H), and entry timing (15m)
- Size a position based on account risk parameters
- Scan multiple symbols in one pass
- Get a backtest-ready data row for a symbol

## How It Works

The engine scores three independent timeframe layers and combines them:

**1D — Trend Regime**
EMA structure (9/21/50), ADX with directional indicators (DI+/DI−). Determines whether the macro environment is bullish, bearish, or neutral. This is the directional anchor — momentum and trigger signals are interpreted relative to this regime.

**4H — Momentum**
MACD line vs signal crossovers, histogram direction, and Stochastic Oscillator crosses. Stochastic signals are weighted asymmetrically depending on the regime (e.g. a bullish stoch cross from oversold in a bullish regime scores higher than in a bearish one).

**15m — Entry Trigger**
RSI oversold/overbought reclaims, Bollinger Band re-entries, volume spikes relative to the 20-period moving average, and RSI divergence detection over a 20-bar lookback. This layer determines whether *right now* is a valid entry moment.

Each component contributes a configurable weighted score. The composite maps to a five-tier bias scale: STRONG BULLISH → BULLISH → NEUTRAL → BEARISH → STRONG BEARISH, with corresponding action recommendations (BUY, WATCH LONG, WAIT, WATCH SHORT, SELL/SHORT).

When conditions align, the trade planner generates a full plan using rolling support/resistance levels, ATR-based stops, and configurable risk-reward targets. The position sizer respects account balance, risk percentage, exchange lot size rules, and minimum notional constraints.

## Usage

```bash
# Single pair — human-readable summary
python3 {baseDir}/scripts/binance_signal_engine.py BTC/USDT

# Multiple pairs
python3 {baseDir}/scripts/binance_signal_engine.py BTC/USDT ETH/USDT SOL/USDT

# JSON output for programmatic consumption
python3 {baseDir}/scripts/binance_signal_engine.py BTC/USDT --output json

# Futures mode with custom risk parameters
python3 {baseDir}/scripts/binance_signal_engine.py BTC/USDT \
  --market futures --leverage 3 --balance 5000 --risk 2

# Use a JSON config file to override all indicator/scoring parameters
python3 {baseDir}/scripts/binance_signal_engine.py ETH/USDT --config my_config.json

# Debug mode for verbose logging
python3 {baseDir}/scripts/binance_signal_engine.py BTC/USDT --debug
```

### CLI Flags

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `symbols` | | *(required)* | One or more trading pairs, e.g. `BTC/USDT ETH/USDT` |
| `--market` | `-m` | `spot` | Market type: `spot` or `futures` |
| `--exchange` | `-e` | `binance` | Exchange ID (ccxt-compatible) |
| `--balance` | `-b` | `10000` | Account balance in USD |
| `--risk` | `-r` | `1.0` | Risk per trade as a percentage |
| `--leverage` | `-l` | `1.0` | Leverage multiplier (futures only) |
| `--config` | `-c` | `None` | Path to a JSON config file for full parameter override |
| `--output` | `-o` | `summary` | Output format: `summary` (human) or `json` (machine) |
| `--debug` | | `off` | Enable debug-level logging |

## Output Structure

The JSON output contains four sections:

**signal** — composite score, per-layer breakdown (trend/momentum/trigger), bias, regime, action recommendation, and an array of human-readable reasoning strings explaining every scoring decision.

**trade_plan** — side (long/short), entry type (market/limit), entry price, stop-loss, take-profit, support, resistance, effective risk-reward ratio, tradeable flag, and plan status (ready/waiting/reject/invalid).

**position_size** — units, notional value, risk budget, actual dollar risk, potential dollar reward, position as a percentage of account, and whether the position was capped by the notional limit.

**backtest_row** — flat key-value record with timestamp, symbol, 15m close, total score, bias, plan side, tradeable flag, effective RR, and sized units. Suitable for appending to a CSV or DataFrame for historical analysis.

## Configuration

All parameters are configurable via a JSON file passed with `--config`. Key areas include:

- EMA periods (fast: 9, slow: 21, trend: 50)
- MACD parameters (12/26/9)
- ADX period and trend threshold (14, 25.0)
- RSI period and oversold/overbought levels (14, 35/65)
- Stochastic window, smoothing, and levels (14, 3, 20/80)
- Bollinger Band window and standard deviation (20, 2.0)
- ATR period and stop-loss multiplier (14, 1.5)
- Volume MA period and spike threshold (20, 1.5x)
- Support/resistance lookback and buffer multipliers
- Per-layer scoring weights (15 weights total)
- Score thresholds for weak/strong signals (10/30)
- Risk-reward ratio, minimum acceptable RR, slippage buffer
- Account balance, risk percentage, max notional, leverage

Defaults are tuned for swing/intraday crypto trading on Binance.

## Dependencies

Requires Python 3.8+ with the following packages:

```bash
pip install ccxt pandas numpy ta
```

No API key is required. The skill uses only Binance's public OHLCV endpoints.

## Limitations

- Signals are analytical tools, not financial advice. Always apply your own judgment and risk management.
- Public API rate limits apply (~1200 weight/min on Binance). The skill includes built-in delays between requests.
- The most recent (still-open) candle is automatically dropped to prevent lookahead bias.
- Short signals and position sizing for shorts are only available in `futures` mode.
- Backtest rows are point-in-time snapshots — this is not a full backtesting engine.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| `https://api.binance.com` (via ccxt) | Symbol name, timeframe, candle limit | Fetch public OHLCV price data |

No authenticated endpoints are called. No orders are placed. No private data leaves your machine.

## Security & Privacy

- **No API keys needed** — only public market data endpoints are used
- **No data exfiltration** — all indicator computation and scoring runs locally in Python
- **No writes to exchange** — strictly read-only; no orders, no account access
- **No local file writes** — output goes to stdout only unless you redirect it
- **No background processes** — runs once, prints results, exits

## Model Invocation Note

This skill may be invoked automatically by the agent when your request matches the trigger phrases in the description. This is standard OpenClaw behavior. You can disable automatic invocation by setting `disable-model-invocation: true` in the frontmatter if you prefer explicit `/binance-signal-engine` invocation only.

## Trust Statement

By installing this skill, you trust that: (1) the `ccxt` library will make HTTPS requests to Binance's public REST API to fetch candle data, and (2) all analysis runs locally on your machine. No credentials are required or sent. Only install if you are comfortable with public market data requests to `api.binance.com`.
