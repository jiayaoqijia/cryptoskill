# x402 Agent Marketplace Skill

Sell AI agent capabilities via SOL micro-payments.

## What It Does

This skill provides a complete marketplace for AI agents to sell their capabilities using SOL cryptocurrency via the x402 payment protocol.

## Features

- **15 AI Agents**: Trading Signals, Token Analysis, Memecoin Scanner, Whale Tracker, Research, Market Summary, Pump.fun Sniper, Volume Analyzer, Portfolio Tracker, News Digest, Governance Votes, Sentiment Analysis, Airdrop Hunter, DeFi Yields, Trading Patterns
- **x402 Payment Protocol**: HTTP 402 payment verification
- **SOL Micro-Payments**: Direct wallet-to-wallet payments (from 0.0005 SOL)
- **90% Revenue Share**: Agents keep 90%, 10% platform fee
- **Zero Custody**: No holding of user funds

## Installation

```bash
# Install via ClawHub
clawhub install x402-agent-marketplace
```

## Usage

### Start the Marketplace Server

```bash
cd skills/x402-agent-marketplace
pip install -r requirements.txt
python server.py
```

Server runs at `http://localhost:8000`

### API Endpoints

| Endpoint | Price | Description |
|----------|-------|-------------|
| `/api/v1/signals/trading` | 0.001 SOL | AI trading signals |
| `/api/v1/analysis/token` | 0.002 SOL | Token analysis |
| `/api/v1/scanner/memecoin` | 0.002 SOL | Memecoin scanner |
| `/api/v1/tracker/whale` | 0.003 SOL | Whale tracker |
| `/api/v1/research` | 0.005 SOL | Research agent |
| `/api/v1/market/summary` | 0.0005 SOL | Market summary |
| `/api/v1/sniper/pumpfun` | 0.005 SOL | Pump.fun sniper |
| `/api/v1/analytics/volume` | 0.002 SOL | Volume analyzer |
| `/api/v1/portfolio/track` | 0.001 SOL | Portfolio tracker |
| `/api/v1/news/digest` | 0.0015 SOL | News digest |
| `/api/v1/governance/votes` | 0.0005 SOL | Governance votes |
| `/api/v1/sentiment` | 0.0005 SOL | Sentiment analysis |
| `/api/v1/airdrop/hunt` | 0.001 SOL | Airdrop hunter |
| `/api/v1/defi/yields` | 0.0015 SOL | DeFi yields |
| `/api/v1/patterns` | 0.002 SOL | Trading patterns |

### Payment Flow

1. **Send SOL** to: `4D8jCkTMWjaQzDuZkwibk8ML34LSCKVCKS8kC6RFYuX`
2. **Get signature** from transaction
3. **Call API** with header: `X-SOL-Payment: WALLET:SIGNATURE:0.001`
4. **Receive AI response**

### Example

```bash
curl -X GET "http://localhost:8000/api/v1/signals/trading" \
  -H "X-SOL-Payment: YOUR_WALLET:TRANSACTION_SIG:0.001"
```

## Files

- `server.py` - FastAPI marketplace server
- `requirements.txt` - Python dependencies
- `dashboard.html` - Web dashboard
- `how-to-use.html` - User guide

## Requirements

- Python 3.8+
- pip
- Solana wallet (Phantom, Solflare, etc.)

## License

MIT

## Author

DahhansBot
