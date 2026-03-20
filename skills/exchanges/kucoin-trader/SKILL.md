---
name: kucoin-trader
description: Professional KuCoin (KC) trading system - multi-account support, spot/margin/futures trading, asset transfers. Use to check balances, transfer assets, open/close positions, and manage your KuCoin portfolio.
metadata: {"openclaw":{"emoji":"🟢","always":true,"requires":{"bins":["node"]}}}
---

# KuCoin Trader 🟢

Professional automated trading system for KuCoin (KC) - a global cryptocurrency exchange.

## 🚀 Quick Start

### Setup Credentials

Save to `~/.openclaw/credentials/kucoin.json`:
```json
{
  "apiKey": "YOUR_API_KEY",
  "secretKey": "YOUR_SECRET_KEY",
  "passphrase": "YOUR_PASSPHRASE"
}
```

### Environment Variables (alternative)
```bash
export KUCOIN_API_KEY="your_api_key"
export KUCOIN_SECRET_KEY="your_secret_key"
export KUCOIN_PASSPHRASE="your_passphrase"
```

## 📊 Basic Queries

| Command | Description |
|---------|-------------|
| `node scripts/accounts.js` | List all account balances |
| `node scripts/market.js --symbol BTC-USDT` | Get current price |
| `node scripts/query.js` | Query all active orders |

## 💰 Asset Transfer

Supported types: `main`, `trade`, `margin`, `isolated`, `futures`

```bash
# Main to Trade
node scripts/transfer.js --from main --to trade --currency USDT --amount 100

# Trade to Futures
node scripts/transfer.js --from trade --to futures --currency USDT --amount 100

# Any account transfer
node scripts/transfer.js --from <FROM> --to <TO> --currency <CURRENCY> --amount <AMOUNT>
```

## ⚡ Spot Trading

```bash
# Market Buy
node scripts/spot.js trade --symbol BTC-USDT --side buy --type market --size 0.001

# Limit Buy
node scripts/spot.js trade --symbol ETH-USDT --side buy --type limit --price 2500 --size 0.1

# Market Sell
node scripts/spot.js trade --symbol BTC-USDT --side sell --type market --size 0.001

# Limit Sell
node scripts/spot.js trade --symbol ETH-USDT --side sell --type limit --price 3000 --size 0.1

# Query orders
node scripts/spot.js orders --symbol BTC-USDT

# Cancel order
node scripts/spot.js cancel --orderId xxx
```

## 🏦 Margin Trading (Cross Margin & Isolated Margin)

```bash
# --- Cross Margin (全仓杠杆) ---
# Check borrowable
node scripts/margin.js borrowable --currency USDT

# Borrow
node scripts/margin.js borrow --currency USDT --amount 100

# Repay
node scripts/margin.js repay --currency USDT --amount 50

# Trade with leverage (5x)
node scripts/margin.js trade --symbol BTC-USDT --side buy --size 0.01 --leverage 5

# Query orders
node scripts/margin.js orders --symbol BTC-USDT
node scripts/margin.js all-orders

# --- Isolated Margin (逐仓杠杆) ---
# Check isolated account info
node scripts/margin.js info-isolated --symbol BTC-USDT

# Check borrowable
node scripts/margin.js borrowable-isolated --symbol BTC-USDT

# Borrow/Repay
node scripts/margin.js borrow-isolated --symbol BTC-USDT --amount 0.01
node scripts/margin.js repay-isolated --symbol BTC-USDT --amount 0.01

# Trade with leverage (3x)
node scripts/margin.js trade-isolated --symbol BTC-USDT --side buy --size 0.01 --leverage 3

# Enable/Disable isolated margin
node scripts/margin.js enable
node scripts/margin.js disable

# Query isolated orders
node scripts/margin.js orders-isolated --symbol BTC-USDT
```

## 📈 Futures Trading

```bash
# Long
node scripts/futures.js trade --symbol BTC-USDT --side buy --size 0.001 --leverage 10

# Short
node scripts/futures.js trade --symbol BTC-USDT --side sell --size 0.001 --leverage 10

# Set leverage
node scripts/futures.js leverage --symbol BTC-USDT --leverage 20
```

## 📈 Supported Trading Pairs

| Pair | Description |
|------|-------------|
| BTC-USDT | Bitcoin |
| ETH-USDT | Ethereum |
| SOL-USDT | Solana |
| XRP-USDT | XRP |
| DOGE-USDT | Dogecoin |
| ADA-USDT | Cardano |
| AVAX-USDT | Avalanche |
| KCS-USDT | KuCoin Token |

## 🏦 Account Types

| Type | Description |
|------|-------------|
| `main` | Funding Account - primary asset storage |
| `trade` | Spot Trading Account - for trading |
| `margin` | Cross Margin Account - leveraged trading (up to 5x) |
| `isolated` | Isolated Margin Account |
| `futures` | Futures Account - perpetual contracts |

## ⚠️ Safety Rules

1. **ALWAYS** verify position before closing
2. **ALWAYS** set Stop Loss on leveraged trades
3. **NEVER** use leverage higher than 10x without experience
4. **VERIFY** pair and quantity before executing
5. **CONFIRM** with user before executing large orders

## 🔗 Links

- [API Documentation](https://docs.kucoin.com/)
- [Create Account](https://www.kucoin.com/r/rf/QBSYNXQD)

---
*Skill for KuCoin trading with multi-account support*
