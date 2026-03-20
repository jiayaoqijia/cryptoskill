---
name: yield-shark
description: 🦈 YieldShark - DeFi stablecoin yield monitor with real-time APY tracking across 50+ platforms
version: 1.0.3
author: gztanht
license: MIT
tags: [defi, yield, crypto, finance, stablecoin, usdt, usdc, apy, aave, compound]
pricing:
  free_tier: 5 queries/day
  sponsorship: 0.5 USDT or 0.5 USDC for unlimited
  note: "Feel free to sponsor more if you find it useful!"
wallet:
  usdt_erc20: "0x33f943e71c7b7c4e88802a68e62cca91dab65ad9"
  usdc_erc20: "0xcb5173e3f5c2e32265fbbcaec8d26d49bf290e44"
metadata:
  clawdbot:
    emoji: 🦈
    requires:
      bins: [npm, node]
---

# 🦈 YieldShark - DeFi Yield Shark

**Smell the Money** - Hunt for the highest APY in the DeFi ocean!

## Overview

YieldShark monitors real-time stablecoin yields across 50+ DeFi platforms including Aave, Compound, Curve, Uniswap, Yearn, Beefy, and more. Get data-driven insights for your crypto investments.

## Features

- **Real-time Data**: Direct integration with DeFiLlama API (free, public)
- **Multi-Token Support**: USDT, USDC, DAI
- **Multi-Chain**: Ethereum, Arbitrum, Optimism, Base, Polygon, BSC
- **Smart Filtering**: Excludes LP pools, filters APY outliers (<30%), TVL >$100k
- **Risk Ratings**: A-E safety scores based on audits and insurance
- **Gas Estimation**: Calculate net APY after transaction costs
- **Platform Comparison**: Side-by-side analysis of top protocols

## Installation

```bash
clawhub install yield-shark
```

## Usage

### Quick Start

```bash
# Query USDT yields
node scripts/monitor.mjs USDT

# Query USDC with custom limit
node scripts/monitor.mjs USDC --limit 10

# Query DAI on specific chain
node scripts/monitor.mjs DAI --chain ethereum
```

### All Scripts

```bash
# Monitor yields
node scripts/monitor.mjs USDT

# Compare platforms
node scripts/compare.mjs --token USDT

# Calculate net APY
node scripts/calculate.mjs --amount 5000 --platform compound

# Set yield alerts
node scripts/alert.mjs --apy 5

# Generate report
node scripts/report.mjs --format markdown
```

### NPM Commands

```bash
npm run monitor    # Run monitor script
npm run compare    # Compare platforms
npm run test:usdt  # Test USDT query
npm run test:usdc  # Test USDC query
npm run test:dai   # Test DAI query
```

## Output Example

```
💰 USDT 最优收益排行 (DeFiLlama 实时数据)

排名  平台 (链)            APY      风险    Gas     TVL
──────────────────────────────────────────────────────────────────────
🥇 Compound V3  (Optimism)   3.5%     🟢 A+    $0.3   $1M
🥈 Beefy        (Optimism)   3.4%     🟡 B+    $0.3   $1M
🥉 Compound V3  (Polygon)    2.9%     🟢 A+    $0.5   $0M

💡 智能推荐:
   ✅ Compound V3 (Optimism) 综合最优 - 3.47% APY
```

## Supported Platforms

### Lending Protocols
- **Aave V3** (A rating, multi-chain) - https://app.aave.com
- **Compound V3** (A+ rating, lowest gas) - https://app.compound.finance
- **Spark** (A rating, high yields) - https://app.spark.fi
- **Morpho** (B+ rating, optimized rates) - https://app.morpho.org
- **Euler** (B rating, innovative features) - https://app.euler.finance

### DEX Liquidity Pools
- **Curve** (A rating, stablecoin specialist) - https://curve.fi
- **Uniswap V3** (A rating, highest volume) - https://app.uniswap.org
- **Balancer** (A rating, multi-token pools) - https://app.balancer.fi
- **Convex** (B+ rating, CRV boosting) - https://www.convexfinance.com

### Yield Aggregators
- **Yearn V2** (B+ rating, auto-compound) - https://yearn.finance
- **Beefy** (B+ rating, multi-chain) - https://app.beefy.com
- **Automata** (B rating, privacy-focused) - https://www.ata.network

### Stablecoin Specialists
- **Ethena** (B+ rating, synthetic dollar) - https://www.ethena.fi
- **Ondo** (A rating, RWA-backed) - https://www.ondo.finance
- **MakerDAO** (A+ rating, DAI issuer) - https://makerdao.com

## Data Sources

- **Primary**: DeFiLlama API (https://yields.llama.fi/pools)
- **Update Frequency**: Real-time (5-minute cache)
- **Coverage**: 50+ platforms, 7 chains, 3 stablecoins

## Pricing

| Tier | Price | Limit |
|------|-------|-------|
| Free | $0 | 3 queries/day |
| Pay-per-use | 0.01 USDT | Unlimited |
| Monthly | 10 USDT | Unlimited + priority support |

## Sponsor

Support development:

- **USDT (ERC20)**: `0x33f943e71c7b7c4e88802a68e62cca91dab65ad9`
- **USDC (ERC20)**: `0xcb5173e3f5c2e32265fbbcaec8d26d49bf290e44`

## Security & Risk Disclaimer

⚠️ **Important**: DeFi protocols carry smart contract risk. Always:

1. Check protocol audits (we provide risk ratings)
2. Start with small amounts
3. Diversify across platforms
4. Never invest more than you can afford to lose

**This tool provides information only, not financial advice. DYOR!**

## Roadmap

- [ ] Multi-token comparison (--tokens USDT,USDC)
- [ ] Historical yield trends
- [ ] Telegram/Email notifications
- [ ] Platform website links
- [ ] Additional chains (Monad, Sonic, etc.)

## Support

- GitHub: https://github.com/gztanht/yield-shark
- ClawHub: https://clawhub.com/skills/yield-shark

---

**Made with 🦈 by @gztanht**

*Smell the Money*
