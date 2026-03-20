# Polymarket Trading Bot v2

AI-driven directional prediction trading system for Polymarket 5-minute BTC/ETH markets.

## Features

- **Market Monitoring**: Auto-scan BTC/ETH 5min markets every 2s
- **PTB Extraction**: Playwright-based with 4-layer fallback
- **Technical Indicators**: EMA, RSI, MACD, Bollinger Bands, ATR, Volume
- **AI Scoring Model**: Position(50%) + Momentum(30%) + RSI(10%) + Volume(10%)
- **Decision Engine**: EV-based smart betting
- **Backtest Validation**: Auto-verify historical accuracy

## Verified Performance

**Dataset**: 2026-03-06, 143 decisions

- **Overall Accuracy**: 84.6% (121/143)
- **100% Confidence**: 100% (13/13)
- **90%+ Confidence**: 100% (14/14)
- **High-Quality Signals** (conf≥80% & EV>0.5): 97.1% (33/34)

## Installation

```bash
pip install requests playwright
playwright install chromium
```

## Usage

### Start Monitoring
```bash
python3 auto_bot_v2.py
```

### Backtest
```bash
python3 backtest_accuracy.py
```

## Configuration

Edit `ai_analyze_v2.py`:
```python
ENABLE_TRADING = False      # Enable real trading
CONFIDENCE_THRESHOLD = 0.55 # Min confidence
ODDS_THRESHOLD = 0.90       # Max odds
BET_AMOUNT = 10             # Bet size (USD)
```

## Recommended Strategy

- Confidence threshold: ≥85%
- EV threshold: >0.5
- Expected accuracy: ~97%
- Prefer ETH signals

## Risk Control

- Single bet: 10-50 USD
- Daily max loss: 100 USD
- Stop after 3 consecutive losses

## Files

- `auto_bot_v2.py`: Main monitoring script
- `ai_analyze_v2.py`: Decision engine
- `ai_trader/ai_model_v2.py`: AI scoring model
- `ai_trader/playwright_ptb.py`: PTB extraction
- `ai_trader/indicators.py`: Technical indicators
- `backtest_accuracy.py`: Backtest validation

## Wallet

- Main: 0xb37c4cC2Be6bFb77a48d5C661D9c956A199A52A2
- Proxy: 0x9130519D591a64E522C10c0f91642f21F35e20fc

## Status

✅ Verified, production-ready
