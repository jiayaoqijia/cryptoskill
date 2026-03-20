# 🛒 x402 Bazaar Skill

[![GitHub Stars](https://img.shields.io/github/stars/coinvest518/openclaw-x402-skill?style=social)](https://github.com/coinvest518/openclaw-x402-skill/stargazers)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/coinvest518/openclaw-x402-skill)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](#)
[![Base Network](https://img.shields.io/badge/network-Base-0052FF.svg)](https://base.org)
[![x402 v2](https://img.shields.io/badge/x402-v2%20spec-orange.svg)](https://docs.cdp.coinbase.com/x402)

> **Autonomous discovery and micropayment layer for AI agents**  
> Browse, discover, and pay for x402-compatible APIs and MCP tools using USDC on Base — no API keys, no subscriptions, just pay-per-call.

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Discovery Mode](#discovery-mode-no-wallet-needed)
  - [Payment Mode](#payment-mode-requires-wallet)
- [MCP Integration](#-mcp-integration)
- [Architecture](#-architecture)
- [Configuration](#-configuration)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)
- [Security](#-security)
- [License](#-license)

---

## 🎯 Overview

The **x402 Bazaar Skill** enables AI agents to autonomously discover and interact with pay-per-call API services through the x402 protocol. Unlike traditional API integrations that require pre-configuration, API keys, and subscription management, x402 lets agents discover services on-demand and pay with cryptocurrency micropayments.

### What is x402?

x402 is an HTTP status code protocol that enables **pay-to-call APIs**. When a client makes a request without payment, the server returns `402 Payment Required` with payment instructions. The client pays using cryptocurrency (USDC on Base), then retries the request with payment proof.

### What is the x402 Bazaar?

The **x402 Bazaar** is a decentralized discovery layer — a machine-readable catalog of all x402-compatible services. AI agents can:
- 🔍 Search and browse available services
- 💲 Filter by price, type, and functionality
- 📋 Inspect payment requirements
- 💸 Pay and call any service without pre-registration

---

## ✨ Features

### 🌐 Discovery without Barriers
- Browse all x402 services with zero setup
- No API keys, accounts, or authentication required
- Real-time catalog from multiple facilitators
- Filter by price, type (HTTP/MCP), and keywords

### 💳 Frictionless Micropayments
- Pay per API call using USDC on Base
- Sub-cent pricing ($0.001 - $0.10 typical)
- Automatic payment proof generation
- Built-in spending limits and safety controls

### 🤖 Agent-First Design
- Natural language query interface
- Autonomous service discovery and selection
- Cost-aware decision making
- Full command-line automation

### 🔒 Security & Privacy
- Non-custodial: you control your wallet
- Private key never leaves your environment
- No KYC, no accounts, no tracking
- Open-source and auditable

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **pip** package manager
- For paid calls: Base wallet with USDC (MetaMask or Coinbase Wallet)

### Installation

```bash
# Clone the repository
git clone https://github.com/coinvest518/openclaw-x402-skill.git
cd openclaw-x402-skill

# Install dependencies
pip install -r requirements.txt

# (Optional) Set up environment for paid calls
cp .env.example .env
# Edit .env and add your EVM_PRIVATE_KEY
```

### Your First Query

```bash
# Browse available services (no wallet needed)
python3 agent.py "list all services"

# Search for specific functionality
python3 agent.py "find weather APIs"

# Filter by price
python3 agent.py "show services under $0.01"
```

---

## 📦 Installation

### Standard Installation

```bash
# Install Python dependencies
pip install -r requirements.txt
```

The skill requires **only 3 dependencies**:
- `httpx` - Modern HTTP client for API requests
- `python-dotenv` - Environment variable management
- `eth-account` - Ethereum wallet and signing (only needed for paid calls)

**Note:** Browse-only mode (service discovery) requires **zero dependencies** — no installation needed to explore the Bazaar!

### OpenClaw Integration

This skill is designed for OpenClaw AI systems. Add to your skills directory:

```bash
# Copy skill to clawd skills directory
cp -r . ~/.openclaw/skills/x402-bazaar/

# Install via OpenClaw
clawd install x402-bazaar

# (Optional) Set up environment for paid calls
cp ~/.openclaw/skills/x402-bazaar/.env.example ~/.openclaw/skills/x402-bazaar/.env
# Edit .env and add your EVM_PRIVATE_KEY only if you want to make paid calls
```
cp -r . ~/clawd/skills/x402-bazaar/

# Install via OpenClaw
clawd install x402-bazaar
```

The installer will automatically:
1. Install Python dependencies
2. Validate Python 3 availability
3. Set up skill metadata

---

## 💡 Usage

### Discovery Mode (No Wallet Needed)

Browse and search the x402 Bazaar without any setup:

#### List All Services
```bash
python3 agent.py "list services"
```

**Output:**
```
🛒 x402 Bazaar — 42 services found

 1. 🌐 Weather API
    URL:      https://api.weather-x402.com/current
    Type:     http GET
    Price:    $0.001 USDC
    Network:  Base (eip155:8453)
    Updated:  2h ago

 2. 🤖 Llama 3.3 70B Inference
    URL:      https://api.x402network.com/llm/llama
    Type:     http POST
    Price:    $0.005 USDC
    Network:  Base (eip155:8453)
    Updated:  4h ago
```

#### Search by Keyword
```bash
python3 agent.py "find weather"
python3 agent.py "search for AI inference"
python3 agent.py "find web scraping services"
python3 agent.py "search sentiment analysis"
```

#### Filter by Price
```bash
python3 agent.py "services under 0.01"
python3 agent.py "services under 0.001 USDC"
python3 agent.py "cheapest services"
```

#### Filter by Type
```bash
python3 agent.py "list http services"
python3 agent.py "list mcp tools"
python3 agent.py "show only GET endpoints"
```

#### Inspect a Service
```bash
python3 agent.py "inspect https://api.example.com/x402/weather"
```

**Output:**
```
📋 Service Details

URL:         https://api.weather-x402.com/current
Type:        http GET
Price:       $0.001 USDC (0.001000 USDC)
Network:     Base (eip155:8453)
Max Amount:  $0.001 USDC
Last Update: 2026-03-03 14:23:00 UTC

Payment Details:
  Facilitator:  api.cdp.coinbase.com
  Token:        USDC (0x833589fcd6edb6e08f4c7c32d4f71b54bda02913)
  Recipient:    0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1

Description:
  Real-time weather data for any location worldwide.
  Returns temperature, conditions, humidity, wind speed.
```

---

### Payment Mode (Requires Wallet)

To make paid API calls, you need a Base wallet with USDC.

#### Setup

1. **Get a Base wallet private key:**
   - MetaMask: Account Details → Export Private Key
   - Coinbase Wallet: Settings → Security → Show Private Key

2. **Fund with USDC on Base:**
   - Buy USDC on Coinbase.com and withdraw to Base network
   - Bridge from Ethereum: [bridge.base.org](https://bridge.base.org)
   - Minimum recommended: $1 USDC (hundreds of calls)

3. **Configure environment:**
```bash
# Create .env file
cat > .env << EOF
EVM_PRIVATE_KEY="0xYourPrivateKeyHere"
MAX_SPEND_PER_CALL=0.10
BASE_RPC_URL="https://mainnet.base.org"
EOF
```

⚠️ **Security Warning:** Never commit your `.env` file or share your private key!

#### Make Paid Calls

```bash
# Call a specific endpoint
python3 agent.py "call https://api.weather-x402.com/current?location=NYC"

# Pay and call with natural language
python3 agent.py "use x402 to get weather for London"

# Autonomous: find + pay + use
python3 agent.py "find the cheapest weather API and get weather for Tokyo"
python3 agent.py "find a sentiment analysis API and analyze: 'This is amazing!'"
```

**Output:**
```
💸 x402 Payment Executed

Endpoint:    https://api.weather-x402.com/current?location=NYC
Amount Paid: $0.001 USDC
Network:     Base (eip155:8453)
TX Hash:     0xabc123def456...
Status:      200 OK
Duration:    1.2s

📦 Response:
{
  "location": "New York City",
  "temperature": 72,
  "conditions": "sunny",
  "humidity": 45,
  "wind_speed": 8,
  "timestamp": "2026-03-03T14:30:00Z"
}

💰 Wallet Balance: 0.9990 USDC remaining
```

---

## 🔌 MCP Integration

The x402 Bazaar Skill can be integrated with **Model Context Protocol (MCP)** servers to enable Claude Desktop and other MCP clients to autonomously discover and pay for x402 APIs.

### What is MCP?

Model Context Protocol (MCP) is a protocol for passing context between LLMs and AI agents. When combined with x402, it enables:

- **Autonomous API discovery** — Claude finds relevant x402 services
- **Automatic payment handling** — No manual payment steps
- **Multi-network support** — Both EVM (Base) and Solana
- **Seamless integration** — x402 services appear as native MCP tools

### Quick Example

**In Claude Desktop:**
> "Find a weather API on x402 and get the weather for San Francisco"

**What happens:**
1. Claude discovers weather services via this skill
2. Selects the cheapest option under budget
3. MCP server handles the x402 payment (0.001 USDC on Base)
4. Returns weather data to Claude
5. Claude responds: *"It's 68°F and sunny in San Francisco"*

### Full MCP Integration Guide

See **[x402-MCP.md](x402-MCP.md)** for complete setup instructions including:
- Installing and configuring MCP servers
- Claude Desktop integration
- Multi-network support (EVM + Solana)
- TypeScript implementation examples
- Troubleshooting and debugging

### MCP Architecture

```
Claude Desktop → MCP Server → x402 Bazaar → Paid API
     ↑              ↑              ↑            ↑
  User asks    Handles     Discovers      Returns
  question     payment      services       paid data
```

The integration makes x402's "pay-per-call" model completely transparent to the AI agent.

---

## 🏗️ Architecture

### System Overview

```
┌─────────────┐
│  AI Agent   │
└──────┬──────┘
       │
       │ Natural Language
       │ Commands
       ▼
┌─────────────────────────────────────┐
│     x402 Bazaar Skill (agent.py)    │
├─────────────────────────────────────┤
│  • Command parsing                  │
│  • Discovery orchestration          │
│  • Payment execution                │
│  • Result formatting                │
└──────┬──────────────┬───────────────┘
       │              │
       │              │
       ▼              ▼
┌─────────────┐  ┌──────────────┐
│ Facilitator │  │   Base       │
│  Discovery  │  │  Blockchain  │
│    APIs     │  │  (USDC)      │
└──────┬──────┘  └──────┬───────┘
       │                │
       │                │
       ▼                ▼
┌─────────────────────────────┐
│   x402 API Service          │
│   • Returns 402 initially   │
│   • Validates payment proof │
│   • Returns paid result     │
└─────────────────────────────┘
```

### x402 Payment Flow

```
1. Discovery
   Agent → Bazaar API: "find weather services"
   Bazaar → Agent: [list of weather services with prices]

2. Initial Request (no payment)
   Agent → API: GET /current?location=NYC
   API → Agent: 402 Payment Required
                + Payment details in headers

3. Payment
   Agent → Base Network: Send 0.001 USDC to facilitator
   Base → Agent: Transaction hash

4. Proof Generation
   Agent: Generate payment proof from tx hash

5. Retry with Proof
   Agent → API: GET /current?location=NYC
                + X-Payment-Proof: <proof>
   API → Agent: 200 OK + weather data
```

### x402 v2 Spec Compliance

This skill is **v2 spec-accurate** and handles:

- **Discovery response shape:** The v2 API returns `{ x402Version: 2, items: [...], pagination: {...} }` not a flat list. This implementation handles both v1 (flat) and v2 (wrapped) for resilience.

- **maxAmountRequired vs amount:** v2 uses `maxAmountRequired` in the `accepts[]` entries. v1 used `amount`. Both are handled with proper fallback.

- **MCP unique key:** Per the spec, MCP tool uniqueness is `(resource_url, tool_name)` not just the URL, since one MCP server hosts multiple tools. Deduplication handles this correctly.

- **Seller API:** The seller section references the correct v2 API (`bazaarResourceServerExtension`, `declareDiscoveryExtension()`) instead of the deprecated v1 `outputSchema` field.

Example v2 discovery response:
```json
{
  "x402Version": 2,
  "items": [
    {
      "url": "https://api.example.com/weather",
      "type": "http",
      "accepts": [
        {
          "network": "eip155:8453",
          "token": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
          "maxAmountRequired": "1000"
        }
      ]
    }
  ],
  "pagination": {
    "nextCursor": "abc123",
    "hasMore": true
  }
}
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Required for paid calls
EVM_PRIVATE_KEY="0x..." # Your Base wallet private key

# Optional settings
MAX_SPEND_PER_CALL=0.10        # Maximum USDC per call (default: 0.10)
BASE_RPC_URL="https://mainnet.base.org"  # Base RPC endpoint
TIMEOUT_SECONDS=30              # Request timeout (default: 30)
ENABLE_DEBUG=false              # Enable debug logging (default: false)

# Facilitator endpoints (advanced)
FACILITATOR_CDP="https://api.cdp.coinbase.com/platform/v2/x402/discovery/resources"
FACILITATOR_PAYAI="https://facilitator.payai.network/discovery/resources"
```

### Spending Limits

The skill enforces spending limits to prevent accidental overpayment:

- Default limit: **$0.10 USDC per call**
- Configurable via `MAX_SPEND_PER_CALL`
- Agent prompts for confirmation if cost exceeds limit

```bash
# Set custom spending limit
export MAX_SPEND_PER_CALL=0.50  # $0.50 max per call
```

---

## 📚 Examples

### Example 1: Weather Data

```bash
python3 agent.py "find weather APIs under $0.01 and get weather for San Francisco"
```

**Process:**
1. Searches Bazaar for weather services under $0.01
2. Ranks by price and reliability
3. Pays and calls the cheapest option
4. Returns weather data

### Example 2: AI Inference

```bash
python3 agent.py "find an LLM inference API and generate: write a haiku about Base"
```

**Process:**
1. Discovers AI inference services
2. Selects appropriate model (Llama, GPT-4, etc.)
3. Pays per-token pricing
4. Returns generated text

### Example 3: Web Scraping

```bash
python3 agent.py "find a web scraper and extract text from https://example.com"
```

**Process:**
1. Finds web scraping services
2. Sends URL as parameter
3. Pays for scraping job
4. Returns extracted content

### Example 4: Multi-Service Workflow

```bash
python3 agent.py "scrape https://news.site/article and analyze sentiment"
```

**Process:**
1. Finds web scraping service → scrapes article
2. Finds sentiment analysis service → analyzes text
3. Two separate micropayments
4. Returns combined result

---

## 🔧 Troubleshooting

### Common Issues

#### `EVM_PRIVATE_KEY not set`

**Problem:** Environment variable missing  
**Solution:** Add key to `.env` file (only needed for paid calls)

```bash
echo 'EVM_PRIVATE_KEY="0x..."' >> .env
```

#### `Insufficient USDC balance`

**Problem:** Wallet doesn't have enough USDC  
**Solution:** Bridge USDC to Base

1. Visit [bridge.base.org](https://bridge.base.org)
2. Connect your wallet
3. Bridge USDC from Ethereum to Base
4. Wait 1-2 minutes for confirmation

#### `Spend limit exceeded`

**Problem:** Service costs more than `MAX_SPEND_PER_CALL`  
**Solution:** Raise limit or confirm manually

```bash
export MAX_SPEND_PER_CALL=0.50  # Increase to $0.50
```

#### `402 verification failed`

**Problem:** Facilitator rejected payment proof  
**Solution:** Retry or switch facilitator

- Check transaction succeeded on [BaseScan](https://basescan.org)
- Verify USDC balance is sufficient
- Try alternative facilitator

#### `No services found`

**Problem:** Bazaar returned empty results  
**Solution:** Broaden search or retry

```bash
# Instead of specific version
python3 agent.py "find gpt-4 turbo"

# Try generic search
python3 agent.py "find language model"
```

#### `Network mismatch`

**Problem:** Service requires unsupported blockchain  
**Solution:** Filter by Base network

```bash
python3 agent.py "find services on Base network"
```

---

## 📖 API Reference

### Command Interface

The skill accepts natural language commands through `agent.py`:

#### Discovery Commands

| Command | Description | Example |
|---------|-------------|---------|
| `list services` | Show all available services | `python3 agent.py "list services"` |
| `find <keyword>` | Search by functionality | `python3 agent.py "find weather"` |
| `services under <price>` | Filter by maximum price | `python3 agent.py "services under 0.01"` |
| `list http services` | Filter by type (http/mcp) | `python3 agent.py "list mcp tools"` |
| `inspect <url>` | Show service details | `python3 agent.py "inspect https://..."` |

#### Payment Commands

| Command | Description | Example |
|---------|-------------|---------|
| `call <url>` | Pay and call endpoint | `python3 agent.py "call https://..."` |
| `pay and call <url>` | Explicit payment command | `python3 agent.py "pay and call https://..."` |
| `find <task> and <action>` | Autonomous workflow | `python3 agent.py "find weather and get NYC"` |

### Python API (Advanced)

For programmatic integration:

```python
from x402_bazaar import BazaarClient

# Initialize client
client = BazaarClient(
    private_key=os.getenv('EVM_PRIVATE_KEY'),
    max_spend=0.10
)

# Discover services
services = client.discover(
    keyword='weather',
    max_price=0.01,
    service_type='http'
)

# Call a service
result = client.call_service(
    url='https://api.weather-x402.com/current',
    params={'location': 'NYC'}
)

print(result.data)  # Weather response
print(result.cost)  # 0.001 USDC
print(result.tx_hash)  # 0xabc123...
```

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup

```bash
# Clone repository
git clone https://github.com/coinvest518/openclaw-x402-skill.git
cd openclaw-x402-skill

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linter
flake8 .
black .
```

### Contribution Guidelines

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/amazing-feature`
3. **Make your changes** with clear commit messages
4. **Add tests** for new functionality
5. **Ensure tests pass:** `pytest tests/`
6. **Submit a pull request**

### Code Standards

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints for function signatures
- Add docstrings to all public functions
- Maintain test coverage above 80%

---

## 🔒 Security

### Private Key Safety

⚠️ **NEVER commit your private key or `.env` file to version control!**

The `.gitignore` file excludes:
- `.env`
- `.env.local`
- `*.key`
- `wallet.json`

### Best Practices

1. **Use a dedicated wallet** for agent operations
2. **Fund with small amounts** (e.g., $10 USDC)
3. **Set conservative spending limits** (`MAX_SPEND_PER_CALL`)
4. **Monitor transactions** on [BaseScan](https://basescan.org)
5. **Rotate keys regularly** if used in production

### Security Audit

This skill has NOT been formally audited. Use at your own risk, especially with mainnet funds. For production deployments, consider:

- Running on Base Sepolia testnet first
- Using a hardware wallet for key storage
- Implementing additional spending controls
- Running your own facilitator node

### Reporting Vulnerabilities

Found a security issue? Please email security@openclaw.ai

**Do NOT create public GitHub issues for security vulnerabilities.**

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 OpenClaw Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🌟 Acknowledgments

- **Coinbase** for x402 protocol development and Base network
- **OpenClaw** community for AI agent framework
- **PayAI** for alternative facilitator implementation
- All x402 service providers in the Bazaar

---

## 📞 Support

- **Documentation:** [docs.openclaw.ai/skills/x402-bazaar](https://docs.openclaw.ai/skills/x402-bazaar)
- **x402 Protocol:** [docs.cdp.coinbase.com/x402](https://docs.cdp.coinbase.com/x402)
- **GitHub Issues:** [github.com/coinvest518/openclaw-x402-skill/issues](https://github.com/coinvest518/openclaw-x402-skill/issues)
- **Discord:** [discord.gg/openclaw](https://discord.gg/openclaw)
- **Twitter:** [@OpenClawAI](https://twitter.com/OpenClawAI)

---

## 🗺️ Roadmap

### v1.1 (Coming Soon)
- [ ] Solana network support
- [ ] Batch payment optimization
- [ ] Service reputation scoring
- [ ] Cached discovery results
- [ ] Web UI for service browsing

### v1.2
- [ ] Multi-token support (USDT, DAI)
- [ ] Service health monitoring
- [ ] Payment analytics dashboard
- [ ] Custom facilitator configuration
- [ ] Service provider SDK

### v2.0
- [ ] Cross-chain payments
- [ ] Subscription service support
- [ ] Service composition workflows
- [ ] Agent marketplace integration
- [ ] Enterprise features (invoicing, reporting)

---

## 🎓 Learn More

### Resources

- [x402 Protocol Specification](https://docs.cdp.coinbase.com/x402/protocol)
- [Base Network Documentation](https://docs.base.org)
- [USDC on Base](https://www.circle.com/en/usdc)
- [OpenClaw AI Framework](https://docs.openclaw.ai)

### Related Projects

- [x402-py](https://github.com/coinbase/x402-py) - Python x402 implementation
- [x402-js](https://github.com/coinbase/x402-js) - JavaScript x402 client
- [x402-server](https://github.com/coinbase/x402-server) - Build your own x402 API

### Community Examples

- [Weather Service Example](https://github.com/x402-examples/weather)
- [LLM Inference Service](https://github.com/x402-examples/llm-inference)
- [Web Scraping Service](https://github.com/x402-examples/web-scraper)

---

<div align="center">

**Made with ❤️ by the OpenClaw Community**

[⭐ Star on GitHub](https://github.com/coinvest518/openclaw-x402-skill) • [🐛 Report Bug](https://github.com/coinvest518/openclaw-x402-skill/issues) • [💡 Request Feature](https://github.com/coinvest518/openclaw-x402-skill/issues)

</div>
