---
version: "2.0.0"
name: crypto-whale-tracker
description: "Track large cryptocurrency transfers (whale movements) using public APIs like Whale Alert and Etherscan. Set thresholds, monitor wallets, and generate formatted reports. Use when you need crypto whale tracker capabilities. Triggers on: crypto whale tracker, coin, threshold, hours, format, output."
author: BytesAgain
---

# 🐋 Crypto Whale Tracker

Track massive crypto transfers in real-time. Know what the whales are doing before the market reacts.

## Quick Start

```bash
# Track whale transfers above 100 BTC
bash scripts/whale_tracker.sh --coin BTC --threshold 100

# Monitor ETH whales with custom timeframe
bash scripts/whale_tracker.sh --coin ETH --threshold 500 --hours 24

# Generate HTML report
bash scripts/whale_tracker.sh --coin BTC --threshold 50 --format html --output whale_report.html

# Track specific wallet
bash scripts/whale_tracker.sh --wallet 0xABC123... --chain ethereum
```

## How It Works — Step by Step

### Step 1: Data Collection
The tool queries public APIs (Whale Alert free tier, Etherscan, Blockchair) to fetch recent large transactions. No API key is required for basic usage, but adding one increases rate limits.

### Step 2: Filtering
Transactions are filtered by your specified threshold. Only transfers above the minimum amount are included. Known exchange wallets are labeled automatically.

### Step 3: Classification
Each transfer is classified into categories:
- **Exchange → Exchange**: Likely OTC or internal transfer
- **Exchange → Unknown**: Possible withdrawal (bullish signal)
- **Unknown → Exchange**: Possible deposit for selling (bearish signal)
- **Unknown → Unknown**: Whale-to-whale transfer

### Step 4: Report Generation
Results are formatted into a clean report with:
- Transaction hash and timestamp
- Source and destination (with exchange labels)
- Amount in crypto and estimated USD value
- Movement classification and market signal

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--coin` | BTC | Cryptocurrency to track (BTC, ETH, USDT, etc.) |
| `--threshold` | 100 | Minimum transfer amount |
| `--hours` | 12 | Lookback period in hours |
| `--format` | text | Output format: text, json, html, csv |
| `--output` | stdout | Output file path |
| `--wallet` | - | Track specific wallet address |
| `--chain` | bitcoin | Blockchain network |
| `--api-key` | - | Whale Alert API key (optional) |
| `--label` | true | Label known exchange wallets |
| `--top` | 20 | Max number of transactions to show |

## Supported Chains

| Chain | Coin | API Source |
|-------|------|-----------|
| Bitcoin | BTC | Blockchair, Whale Alert |
| Ethereum | ETH, ERC-20 | Etherscan, Whale Alert |
| BSC | BNB, BEP-20 | BscScan |
| Tron | TRX, TRC-20 | Tronscan |
| Solana | SOL | Solscan |

## Exchange Wallet Labels

The tool ships with a built-in database of known exchange wallets covering:
- Binance, Coinbase, Kraken, OKX, Bybit
- Bitfinex, Huobi, KuCoin, Gate.io
- Gemini, Bitstamp, FTX (historical)

## Use Cases

1. **Market Sentiment**: Large exchange inflows often precede sell-offs
2. **Accumulation Detection**: Whales moving coins to cold storage = bullish
3. **Stablecoin Flows**: USDT/USDC whale movements signal upcoming buys
4. **Alert System**: Set up cron jobs to get periodic whale alerts

## Cron Example

```bash
# Check every 30 minutes for BTC whales
*/30 * * * * bash /path/to/whale_tracker.sh --coin BTC --threshold 200 --hours 1 --format json >> /var/log/whale_alerts.json
```

## Output Example

```
🐋 WHALE ALERT — BTC Transfers > 100 BTC (Last 12h)
══════════════════════════════════════════════════════

#1  🔴 2,500 BTC ($162.5M) — Unknown → Binance
    TX: abc123...def456
    Time: 2025-03-10 14:32 UTC
    Signal: BEARISH (possible sell preparation)

#2  🟢 1,800 BTC ($117.0M) — Coinbase → Unknown
    TX: 789ghi...jkl012
    Time: 2025-03-10 13:15 UTC
    Signal: BULLISH (withdrawal to cold storage)

Summary: 15 whale transfers totaling 12,340 BTC ($802.1M)
  Inflows to exchanges:  5,200 BTC (42.1%)
  Outflows from exchanges: 7,140 BTC (57.9%)
  Net flow: OUTFLOW (bullish signal)
```

## Limitations

- Free API tiers have rate limits (typically 10 req/min)
- Historical data limited to ~30 days without paid API
- USD values are estimates based on current price
- Some wallet labels may be outdated

## Files

- `BTC` — Btc
- `ETH` — Eth
- `BNB` — Bnb
- `TRX` — Trx
- `SOL` — Sol
---
💬 Feedback & Feature Requests: https://bytesagain.com/feedback
Powered by BytesAgain | bytesagain.com

## Commands

Run `crypto-whale-tracker help` to see all available commands.
