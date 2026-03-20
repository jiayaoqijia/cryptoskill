# 🦈 YieldShark

**DeFi Yield Optimization Platform** - Find the highest APY for your stablecoins!

[![Version](https://img.shields.io/github/v/release/gztanht/yield-shark)](https://github.com/gztanht/yield-shark/releases)
[![License](https://img.shields.io/github/license/gztanht/yield-shark)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-yield--shark-blue)](https://clawhub.com/skills/yield-shark)

> **Smell the Money** - In the vast ocean of DeFi, be a shark hunting for the highest yields! 🦈

---

## 🌟 Features

- **Real-Time APY Tracking** - Live data from 50+ DeFi platforms via DeFiLlama API
- **Multi-Token Support** - USDT, USDC, DAI stablecoin monitoring
- **Multi-Chain** - Ethereum, Arbitrum, Optimism, Base, Polygon, BSC, Monad
- **Smart Filtering** - Excludes LP pools, filters outliers, TVL > $100k
- **Net APY Calculator** - Accounts for gas fees
- **Yield Alerts** - Get notified when APY hits your target
- **Platform Comparison** - Side-by-side analysis

---

## 🚀 Quick Start

```bash
# Install
npx @gztanht/yield-shark

# Check USDT yields
node scripts/monitor.mjs USDT

# Compare multiple tokens
node scripts/compare-tokens.mjs

# Calculate net APY (after gas)
node scripts/calculate.mjs --amount 10000

# Get yield optimization suggestions
node scripts/optimize.mjs --token USDT --amount 10000
```

---

## 📊 Example Output

```bash
$ node scripts/monitor.mjs USDT

💰 USDT Top Yields (DeFiLlama Live Data)

Rank  Platform (Chain)       APY     Risk   TVL
─────────────────────────────────────────────────────
1     merkl (Hyperliquid)   61.68%   B      $5M
2     morpho (Arbitrum)     24.39%   B      $3M
3     aave-v3 (Optimism)    3.50%    A+     $100M

💡 Smart Pick: merkl (Hyperliquid) - Best risk-adjusted APY
```

---

## 💰 Pricing - Free First!

| Plan | Price | Limit |
|------|-------|-------|
| **Free** | $0 | **5 queries/day** |
| **Sponsor Unlock** | 0.5 USDT or 0.5 USDC | Unlimited |

> 💡 Feel free to sponsor more if you find it useful!

### Sponsorship Addresses

- **USDT (ERC20)**: `0x33f943e71c7b7c4e88802a68e62cca91dab65ad9`
- **USDC (ERC20)**: `0xcb5173e3f5c2e32265fbbcaec8d26d49bf290e44`

After sponsoring, contact @gztanht to unlock unlimited access! 🦈

---

## 📖 Documentation

| Script | Description |
|--------|-------------|
| `monitor.mjs` | Real-time yield monitoring |
| `compare.mjs` | Platform comparison tool |
| `compare-tokens.mjs` | Multi-token yield comparison |
| `calculate.mjs` | Net APY calculator (after gas) |
| `alert.mjs` | Yield alert system |
| `report.mjs` | Generate detailed reports (JSON/Markdown) |
| `optimize.mjs` | Get yield optimization suggestions |
| `history.mjs` ✨ | APY history tracking & trends |
| `card.mjs` | Shareable yield cards |

---

## 🔧 Configuration

Edit `config/platforms.json` to customize platform settings:

```json
{
  "platforms": [
    {
      "name": "Aave V3",
      "website": "https://aave.com",
      "chains": ["Ethereum", "Arbitrum", "Optimism"],
      "category": "Lending"
    }
  ]
}
```

---

## 🛡️ Security Notes

- ⚠️ DeFi protocols carry smart contract risk
- ⚠️ APY fluctuates with market conditions
- ⚠️ Gas fees affect small deposits
- ℹ️ This tool provides information only, not financial advice

**Always DYOR (Do Your Own Research)!**

---

## 📈 Roadmap

- **v1.0.x** ✅ Core features, multi-token support
- **v1.1.0** ⏳ Telegram alerts, APY history
- **v1.2.0** ⏳ One-click deposit integration
- **v2.0.0** ⏳ Portfolio tracking, auto-compound

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repo
2. Create a feature branch
3. Submit a PR

---

## 📞 Support

- **ClawHub**: https://clawhub.com/skills/yield-shark
- **Email**: support@yieldshark.shark
- **Telegram**: @YieldSharkBot

---

## 📄 License

MIT © 2026 gztanht

---

**Made with 🦈 by [@gztanht](https://github.com/gztanht)**

*Smell the Money in the DeFi Ocean!*
