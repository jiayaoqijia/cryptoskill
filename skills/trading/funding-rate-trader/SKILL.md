---
name: funding-rate-trader
description: Crypto funding rate arbitrage strategy. Scan negative funding rates, auto-trade with stop-loss/take-profit. No API key needed for scanning, Binance API for trading.
version: 1.0.1
author: guanjia
---

# Funding Rate Trader

Automated crypto funding rate arbitrage strategy for Binance Futures.

## Features

- 🔍 Scan 50+ coins for negative funding rates
- 📊 Score opportunities by rate + trend + RSI
- 🤖 Auto-trade with configurable leverage
- 🛡️ Auto stop-loss and take-profit
- 💰 Compound profits with rolling strategy

## Quick Start

```bash
# Scan opportunities (no API needed)
node scan.js

# Run auto-trader (requires Binance API)
node trader.js

# Monitor positions
node monitor.js
```

## Configuration

Create `~/.openclaw/secrets/binance.json`:
```json
{
  "apiKey": "your-api-key",
  "secret": "your-secret"
}
```

## Strategy

1. **Entry**: Negative funding rate + upward trend
2. **Leverage**: 20x (adjustable)
3. **Stop-loss**: -10%
4. **Take-profit**: +20%
5. **Compound**: Roll profits into next trade

## Expected Returns

| Capital | Daily Income | Annual (est) |
|---------|--------------|--------------|
| $100 | $5-15 | 1800-5400% |
| $500 | $25-75 | 1800-5400% |
| $1000 | $50-150 | 1800-5400% |

*Returns depend on market conditions and funding rates*

## Risk Warning

⚠️ High leverage trading is risky. Only trade what you can afford to lose.

## License

MIT
