---
version: "2.0.0"
name: Liquidity Monitor
description: "Monitor DEX liquidity pool depth, track liquidity changes, calculate LP yield, and estimate impermanent loss. Use when you need liquidity monitor capabilities. Triggers on: liquidity monitor."
author: BytesAgain
---

# Liquidity Monitor 💧

Real-time DEX liquidity pool monitoring with impermanent loss calculation and LP yield estimation.

## Feature List

### 🔍 Pool Discovery & Monitoring
- Search liquidity pools by token pair across major DEXes
- Monitor pool TVL (Total Value Locked) in real-time
- Track liquidity depth changes over time
- Alert when liquidity drops below threshold

### 📊 Impermanent Loss Calculator
- Calculate IL for any price movement scenario
- Compare IL vs holding vs LP yield
- Model IL across different price ranges (for concentrated liquidity)
- Historical IL analysis for existing positions

### 💰 LP Yield Calculator
- Estimate APR/APY from trading fees
- Include farming rewards in yield calculation
- Project earnings over custom time periods
- Compare yields across pools and DEXes

### ⚠️ Alert System
- Liquidity removal alerts (rug pull detection)
- Large swap impact warnings
- Pool ratio imbalance notifications
- TVL drop percentage triggers

### 📈 Analytics & Reports
- Pool health score (0-100)
- Volume-to-liquidity ratio analysis
- Top liquidity providers tracking
- HTML dashboard generation

## Usage

### Monitor a Pool

```bash
bash scripts/liquidity-monitor.sh monitor \
  --dex uniswap-v2 \
  --pair "ETH/USDC" \
  --chain ethereum
```

### Calculate Impermanent Loss

```bash
bash scripts/liquidity-monitor.sh impermanent-loss \
  --token-a ETH \
  --token-b USDC \
  --entry-price 3000 \
  --current-price 4500
```

### Estimate LP Yield

```bash
bash scripts/liquidity-monitor.sh yield \
  --pool-address "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc" \
  --amount 10000 \
  --period 30
```

### Pool Health Check

```bash
bash scripts/liquidity-monitor.sh health \
  --dex raydium \
  --pair "SOL/USDC" \
  --chain solana
```

### Generate Dashboard

```bash
bash scripts/liquidity-monitor.sh dashboard \
  --pools-file my-pools.json \
  --output liquidity-dashboard.html
```

## Supported DEXes

**EVM Chains:**
- Uniswap V2 / V3 (Ethereum, Polygon, Arbitrum, Optimism, Base)
- SushiSwap (Multi-chain)
- PancakeSwap (BSC, Ethereum)
- Curve Finance (Ethereum, Polygon, Arbitrum)

**Solana:**
- Raydium (AMM & CLMM)
- Orca (Whirlpools)
- Meteora

## Impermanent Loss Reference Table

| Price Change | IL (50/50 Pool) | Equivalent Loss |
|-------------|-----------------|-----------------|
| ±25% | 0.6% | $6 per $1,000 |
| ±50% | 2.0% | $20 per $1,000 |
| ±75% | 3.8% | $38 per $1,000 |
| ±100% (2x) | 5.7% | $57 per $1,000 |
| ±200% (3x) | 13.4% | $134 per $1,000 |
| ±400% (5x) | 25.5% | $255 per $1,000 |

## Pool Health Score Criteria

| Factor | Weight | Description |
|--------|--------|-------------|
| TVL Stability | 25% | How stable is the TVL over 7 days |
| Volume/TVL Ratio | 20% | Higher ratio = better fee generation |
| LP Count | 15% | More LPs = less concentration risk |
| Age | 15% | Older pools are generally safer |
| Top LP % | 15% | Lower concentration = better |
| Smart Contract Audit | 10% | Known audited DEX protocols score higher |
---
💬 Feedback & Feature Requests: https://bytesagain.com/feedback
Powered by BytesAgain | bytesagain.com

## Commands

- `pools` — Pools
- `il-calc` — Il Calc
- `yield-compare` — Yield Compare
- `lp-calc` — Lp Calc
