---
name: binance-spot-trader
description: Autonomous Binance spot trading bot with LLM-powered market analysis. Supports momentum trading, mean reversion, and DCA strategies on any Binance spot pair. Use when user wants to trade on Binance, set up automated crypto trading, build a spot trading bot, or automate DCA buying. Features technical analysis, LLM sentiment evaluation, position sizing, and portfolio tracking.
metadata: {"openclaw": {"requires": {"env": ["BINANCE_API_KEY", "BINANCE_SECRET_KEY", "LLM_API_KEY"]}, "primaryEnv": "BINANCE_API_KEY", "homepage": "https://github.com/srikanthbellary"}}
---

# Binance Spot Trader

Autonomous spot trading bot for Binance. Combines technical indicators with LLM-powered market sentiment analysis to execute trades on any Binance spot pair.

## Prerequisites

- **Binance account** with API keys (spot trading enabled, withdrawal DISABLED)
- **Anthropic API key** (uses Haiku ~$0.001/eval)
- Python 3.10+

## Setup

### 1. Install

```bash
bash {baseDir}/scripts/setup.sh
```

### 2. Configure

Create `.env`:
```
BINANCE_API_KEY=<your-api-key>
BINANCE_SECRET_KEY=<your-secret-key>
LLM_API_KEY=<anthropic-api-key>
PAIRS=BTCUSDT,ETHUSDT,SOLUSDT
STRATEGY=momentum
TRADE_SIZE_PCT=5
MAX_POSITIONS=5
```

### 3. Run

```bash
python3 {baseDir}/scripts/trader.py
```

Or via cron:
```
*/5 * * * * cd /opt/trader && python3 trader.py >> trader.log 2>&1
```

## Strategies

### Momentum (default)
- Buys when price crosses above 20-EMA with volume spike
- Sells when price crosses below 20-EMA or hits TP/SL
- Best for trending markets (BTC, ETH, SOL)

### Mean Reversion
- Buys when RSI < 30 (oversold) and price near Bollinger Band lower
- Sells when RSI > 70 (overbought) or price near upper band
- Best for range-bound markets

### DCA (Dollar Cost Average)
- Buys fixed amount at regular intervals regardless of price
- Configurable interval (hourly, daily, weekly)
- Lowest risk strategy for long-term accumulation

### LLM-Enhanced (all strategies)
- Before each trade, asks Claude Haiku for market sentiment
- Evaluates: recent news, price action, volume patterns, market structure
- Can veto a trade signal if sentiment is strongly against

## Trading Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `PAIRS` | `BTCUSDT` | Comma-separated trading pairs |
| `STRATEGY` | `momentum` | `momentum`, `mean_reversion`, or `dca` |
| `TRADE_SIZE_PCT` | `5` | % of portfolio per trade |
| `MAX_POSITIONS` | `5` | Max concurrent open positions |
| `TAKE_PROFIT_PCT` | `5` | Take profit % |
| `STOP_LOSS_PCT` | `3` | Stop loss % |
| `DCA_INTERVAL` | `daily` | For DCA: `hourly`, `daily`, `weekly` |
| `DCA_AMOUNT_USDT` | `50` | USDT per DCA buy |
| `USE_LLM` | `true` | Enable LLM sentiment filter |

## Monitoring

```bash
# Check portfolio
python3 {baseDir}/scripts/portfolio.py

# View trade history
tail -50 trades.jsonl

# Check logs
tail -f trader.log
```

## ⚠️ Security Considerations

- **NEVER enable withdrawal on API keys** — trading only
- **IP-restrict your API keys** on Binance
- Use a sub-account with limited funds for bot trading
- Start with tiny amounts ($50-100) and paper trade first
- Monitor actively during first 24 hours
- Set up Binance email alerts for all trades
- **API keys on disk** — secure your server (SSH keys only, firewall, chmod 600)

## References

- See `references/binance-api.md` for REST API docs
- See `references/indicators.md` for technical analysis details
