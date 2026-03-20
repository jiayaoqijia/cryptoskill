---
name: bybit-futures
description: Complete Bybit USDT perpetual futures trading system with risk management, paper trading, and live execution. Use when building a crypto futures trading bot, connecting to Bybit API, implementing stop-loss/take-profit, managing leverage and position sizing, paper trading strategies, backtesting, or deploying a WebSocket-based real-time trading system. Supports EMA crossover, RSI, and custom strategy templates.
---

# Bybit Futures Trading System

Complete trading infrastructure for Bybit USDT perpetual futures contracts.

## Quick Start

1. Install dependencies: `pip install ccxt websockets numpy requests`
2. Copy `scripts/config_template.py` → `config.py`, fill in API keys
3. Run paper trading: `python scripts/paper_trading_ws.py`
4. When validated, switch to live: `python scripts/live_trading.py`

## Architecture

```
config.py          ← API keys + risk parameters
risk_manager.py    ← Position sizing, daily loss limits, max positions
paper_trading_ws.py ← WebSocket real-time paper trading
live_trading.py    ← Live execution (same logic, real orders)
backtest.py        ← Historical backtesting engine
```

## Risk Management

All trades enforced by `risk_manager.py`:
- **Max position**: configurable % of capital per trade (default 20%)
- **Max leverage**: configurable (default 5x)
- **Stop loss**: automatic per-trade (default 3%)
- **Take profit**: automatic per-trade (default 6%, 2:1 R/R)
- **Daily loss limit**: halt trading after X% daily drawdown (default 10%)
- **Max concurrent positions**: configurable (default 3)

## Included Strategies

### EMA Crossover (ETH)
- EMA(12) crosses above EMA(26) → long
- EMA(12) crosses below EMA(26) → short
- Best on: ETH/USDT 1h timeframe

### RSI Mean Reversion (SOL, HYPE, PEPE)
- RSI(14) crosses up from below 30 → long
- RSI(14) crosses down from above 70 → short
- Best on: SOL, HYPE (73% WR), 1000PEPE (53% WR) 1h timeframe
- Backtested: HYPE +$339, PEPE +$210 on 90-day 1h data

### Custom Strategy Template
See `references/custom_strategy.md` for adding your own signals.

## WebSocket Real-Time Engine

The paper/live trading engine uses Bybit's WebSocket v5 API:
- **Ticker subscription**: millisecond-level price updates for SL/TP
- **Kline subscription**: signal calculation on candle close only
- **Auto-reconnect**: 5s retry on disconnect
- **State persistence**: saves every 5 minutes to JSON

## Deployment

Recommended: systemd service on a VPS.

```bash
# Create service file
sudo tee /etc/systemd/system/paper-trading.service << 'EOF'
[Unit]
Description=Paper Trading Bot (WebSocket)
After=network.target

[Service]
Type=simple
WorkingDirectory=/root/trading
ExecStart=/usr/bin/python3 paper_trading_ws.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable --now paper-trading
```

## Telegram Notifications

Built-in Telegram push for all events:
- Position opened/closed
- Stop loss / take profit hit
- 6-hourly summary reports
- Error alerts

Set `TG_BOT_TOKEN` and `TG_CHAT_ID` in config.

## Files

- `scripts/config_template.py` — Configuration template
- `scripts/risk_manager.py` — Risk management engine
- `scripts/paper_trading_ws.py` — WebSocket paper trading bot
- `scripts/live_trading.py` — Live trading bot
- `scripts/backtest.py` — Backtesting engine
- `references/custom_strategy.md` — Guide for adding custom strategies
- `references/bybit_api_notes.md` — Bybit API gotchas and tips
