<div align="center">

# gold-api-feed

**Real-Time Precious Metals & Crypto Trading Skill with Multi-Agent Analysis**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-8A2BE2?logo=anthropic&logoColor=white)](https://claude.ai/code)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-orange)](https://openclaw.ai)
[![MCP](https://img.shields.io/badge/MCP-Server-green)](mcp_schema.json)

</div>

---

<div align="center">

🏅 [Overview](#overview) | ⚡ [Quick Install](#installation) | 🤖 [Claude Code](#claude-code-installation) | 🦾 [OpenClaw](#openclaw-installation) | 🔌 [MCP Server](#mcp-server) | 📊 [Frameworks](#trading-frameworks)

</div>

---

## Overview

**gold-api-feed** is a Claude Code skill and MCP server that gives AI agents real-time precious metals and cryptocurrency prices with a full **multi-agent trading analysis framework** — inspired by [TradingAgents](https://github.com/rawbethwebsites/TradingAgents).

Deploy specialized analyst agents — Technical, Sentiment, Fundamental, and News — that debate market conditions and produce structured buy/sell/hold recommendations.

### Supported Assets

| Symbol | Asset | Type |
|--------|-------|------|
| XAU | Gold | Precious Metal |
| XAG | Silver | Precious Metal |
| XPT | Platinum | Precious Metal |
| XPD | Palladium | Precious Metal |
| BTC | Bitcoin | Cryptocurrency |
| ETH | Ethereum | Cryptocurrency |
| HG | Copper | Industrial Metal |

---

## Multi-Agent Framework

The skill mirrors the structure of a real trading firm — analyst teams debate, researchers challenge, and a portfolio manager enforces risk.

### Analyst Team
- **Technical Analyst** — EMA crossovers, RSI, MACD, support/resistance
- **Sentiment Analyst** — 24h momentum, volume analysis, market mood
- **Fundamental Analyst** — macro context, safe haven demand, dollar correlation
- **News Analyst** — macro events, central bank signals, geopolitical risk

### Researcher Team
- **Bullish Researcher** — builds the case for entry, stress-tests bull thesis
- **Bearish Researcher** — challenges assumptions, identifies traps and fakeouts
- Configurable debate rounds (1–5) for high/low conviction decisions

### Risk Management & Portfolio Manager
- Position sizing by account risk %
- Value at Risk (VaR 95%) calculation
- Volatility regime detection (Low / Normal / High / Extreme)
- Order approval/rejection with margin checks
- Max daily drawdown enforcement

---

## Getting Your API Key

This skill fetches live prices from [gold-api.com](https://gold-api.com). You need a free API key to use it.

### Step 1 — Create your account

Go to **[https://gold-api.com](https://gold-api.com)** and click **Sign Up** (it's free).

### Step 2 — Get your key

After signing in, visit **[https://gold-api.com/docs](https://gold-api.com/docs)** — your API key is shown in the authentication section of the documentation once you're logged in.

### Step 3 — Add it to your project

Copy `.env.example` to `.env` and paste your key:

```bash
cp .env.example .env
```

```env
GOLD_API_KEY=your_api_key_here
```

The skill will raise a clear error if the key is missing or invalid, pointing you back to [gold-api.com](https://gold-api.com).

---

## Installation

### Prerequisites

- Python 3.9+
- `aiohttp` and `requests`

```bash
pip install aiohttp requests
```

---

## Claude Code Installation

### Method 1: Clone & Copy (Recommended)

```bash
# Clone the repo
git clone https://github.com/rawbethwebsites/gold-api-feed.git
cd gold-api-feed

# Copy skill to Claude Code skills directory
cp -r . ~/.claude/skills/gold-api-feed/
```

Restart Claude Code — the skill activates automatically when you ask about:
- Gold, silver, bitcoin, or ethereum prices
- Trade entries, stop losses, position sizing
- Market analysis or buy/sell decisions

### Method 2: Manual Install

```bash
mkdir -p ~/.claude/skills/gold-api-feed
curl -L https://github.com/rawbethwebsites/gold-api-feed/archive/refs/heads/main.zip -o gold-api-feed.zip
unzip gold-api-feed.zip -d ~/.claude/skills/
mv ~/.claude/skills/gold-api-feed-main ~/.claude/skills/gold-api-feed
```

### Trigger Phrases

The skill activates on:
```
"What's gold at?"
"Should I buy XAU at $4,640?"
"Run a multi-agent analysis on Bitcoin"
"Show me precious metals prices"
"Calculate position size for gold trade"
"Bull vs bear debate on XAU"
```

---

## OpenClaw Installation

### Step 1: Clone into OpenClaw workspace

```bash
git clone https://github.com/rawbethwebsites/gold-api-feed.git \
  ~/.openclaw/workspace/skills/gold-api-feed
```

### Step 2: Register the skill

Add to your OpenClaw skills registry (`~/.openclaw/workspace/skills-registry.json`):

```json
{
  "id": "gold-api-feed",
  "name": "Gold API Feed",
  "category": "Trading & Finance",
  "status": "active",
  "path": "~/.openclaw/workspace/skills/gold-api-feed",
  "entrypoint": "scripts/mcp_server.py",
  "triggerPhrases": [
    "check gold price",
    "analyze trade setup",
    "run market debate",
    "portfolio risk check"
  ]
}
```

### Step 3: Start the MCP server

```bash
python ~/.openclaw/workspace/skills/gold-api-feed/scripts/mcp_server.py
```

### Step 4: Connect via OpenClaw bridge

```python
from scripts.openclaw_bridge import OpenClawBridge

bridge = OpenClawBridge()

# Get live gold price
price = bridge.get_price("XAU")

# Run multi-agent analysis
analysis = bridge.market_analysis(
    asset="XAU",
    current_price=4640,
    support=[4620, 4600],
    resistance=[4680, 4700]
)

# Run 3-round bull/bear debate
debate = bridge.run_debate(asset="XAU", current_price=4640, rounds=3)
```

### Nova Integration

Nova calls the tool autonomously from cron jobs:

```bash
# Price check
python ~/.openclaw/workspace/skills/gold-api-feed/scripts/claude_code_tool.py

# Trade analysis
python -c "
from scripts.openclaw_bridge import OpenClawBridge
b = OpenClawBridge()
print(b.market_analysis('XAU', 4640, [4620], [4680]))
"
```

---

## MCP Server

The skill exposes a full MCP tool surface.

### Start the server

```bash
python scripts/mcp_server.py
```

### Available Tools

| Tool | Description |
|------|-------------|
| `get_price` | Live price for a single asset |
| `get_all_prices` | All 7 assets at once |
| `analyze_trade_setup` | Full trade analysis with R/R and position sizing |
| `market_analysis` | Multi-agent analysis (Technical + Sentiment + Fundamental) |
| `run_debate` | Configurable bull/bear debate (1–5 rounds) |
| `create_portfolio` | Initialize portfolio with capital and risk settings |
| `check_order` | Validate order against portfolio rules |
| `get_portfolio_summary` | Full portfolio snapshot |
| `check_risk` | VaR, volatility, liquidity, drawdown report |

### Example MCP Request

```python
from scripts.mcp_server import handle_mcp_request

# Analyze a gold trade
response = handle_mcp_request({
    "tool": "analyze_trade_setup",
    "params": {
        "asset": "XAU",
        "entry": 4640,
        "stop": 4620,
        "target": 4680,
        "account": 10000,
        "risk_percent": 1.0
    }
})
# {"success": true, "approved": true, "position_size": 0.5, "risk_reward_ratio": 2.0, ...}
```

### Response Format

All tools return consistent JSON:

```json
{
  "success": true,
  "data": { "..." : "..." },
  "error": null
}
```

---

## Trading Frameworks

### Multi-Agent Market Analysis

```
📊 Multi-Agent Market Analysis: XAU

Overview
- Price: $4,640.70
- Sentiment: BULLISH
- Confidence: 75%
- Risk Level: MEDIUM

🐂 Bullish Points
- [technical] Price near key support
- [sentiment] Strong 24h gain (+0.45%)
- [fundamental] Safe haven demand elevated

🐻 Bearish Points
- [technical] Resistance at $4,700
- [sentiment] Volume below 30-day average

📋 Analyst Breakdown
- 🟢 Technical: 70% confidence
- 🟢 Sentiment: 65% confidence
- ⚪ Fundamental: 50% confidence

🎯 Recommendation
🟢 BUY — Strong bullish consensus
```

### Bull vs Bear Debate

```
🎭 Structured Debate: XAU — Round 2 of 3

🐂 Bull: Central banks added 1,037 tonnes in 2023.
         Safe haven demand remains structurally elevated.
         Strength: 72%

🐻 Bear: Dollar strength dampens foreign buyer demand.
         Rate environment increases opportunity cost of holding gold.
         Strength: 58%

Winner: 🟢 BULL

Final Verdict: BULL CASE stronger — 2/3 rounds won
```

### Trade Signal Output

```
🟢 BUY SIGNAL: XAU/USD
Entry:  $4,640.00
Stop:   $4,620.00  (-0.43%)
Target: $4,680.00  (+0.86%)
R/R:    2:1
Size:   0.5 lots
Risk:   $100 (1% of $10,000)
```

---

## TradingAgents Integration

This skill is built on patterns from the [TradingAgents](https://github.com/rawbethwebsites/TradingAgents) framework:

| TradingAgents Component | gold-api-feed Implementation |
|-------------------------|------------------------------|
| Analyst Team | `market_analyst.py` — Technical, Sentiment, Fundamental, News |
| Researcher Team | `trading_analyzer.py` — Bullish/Bearish structured debate |
| Trader Agent | `analyze_trade_setup()` — Entry timing & position sizing |
| Risk Management | `risk_manager.py` — VaR, volatility, liquidity monitoring |
| Portfolio Manager | `portfolio_manager.py` — Order approval, exposure limits |

---

## Risk Management Rules

The Portfolio Manager enforces these rules on every order:

1. Never risk more than **2% per trade**
2. Always require a **stop loss** before entry
3. Minimum **1.5:1** reward-to-risk ratio
4. No overexposure to **correlated assets**
5. Max **50% of account** in open positions
6. Stop trading after **5% daily drawdown**

---

## Project Structure

```
gold-api-feed/
  scripts/
    price_feed.py           Real-time price fetching from gold-api.com
    trading_analyzer.py     Trade setup evaluation & bull/bear debate
    market_analyst.py       Multi-agent analysis (4 analyst types)
    risk_manager.py         VaR, volatility, liquidity, drawdown
    portfolio_manager.py    Order validation, position sizing, exposure
    mcp_server.py           MCP server (stdio transport)
    openclaw_bridge.py      OpenClaw integration layer
    claude_code_tool.py     Claude Code direct tool interface
  SKILL.md                  Claude Code skill definition
  mcp_schema.json           MCP tool schema
  requirements.txt
  README.md
```

---

## Contributing

Contributions welcome. Open an issue or pull request for:
- New assets or data sources
- Additional analyst types
- New MCP tools
- OpenClaw / Claude Code integration improvements

---

## Disclaimer

> This skill is for research and educational purposes. It does not constitute financial, investment, or trading advice. Trading performance depends on many factors. Always do your own research.

---

*Real-time market data via [gold-api.com](https://gold-api.com) — free, no API key required.*
