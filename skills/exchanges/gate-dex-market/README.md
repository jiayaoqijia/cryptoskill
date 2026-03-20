# Gate DEX Market

> **Market Data Skill** — OpenAPI mode, AK/SK authentication for direct API calls

Provides complete market data query capabilities through Gate DEX OpenAPI, supporting K-line charts, token information, security audits, rankings, and other functions.

---

## 🎯 Architecture

| Mode | Connection Method | Features | Use Cases |
|------|---------|------|---------|
| ⚡ **OpenAPI Mode** | AK/SK direct calls | Independent and fast, rich functionality | Market queries, token info, security audits |

---

## 🚀 Quick Installation

### Method 1: Automated Installation Script (Recommended)

```bash
# Run market data-specific installation script
./gate-dex-market/install.sh
```

Script features:
- 🔍 Auto-detects AI platform and configures
- 📈 Optimizes Skill loading order for market data
- 🎯 Generates market data-prioritized routing file

### Method 2: Manual Configuration

See [Root README.md](../README.md) for detailed configuration methods.

---

## 🚀 Quick Usage

### Trigger Methods

- **Market Data**: `K-line`, `quotes`, `price trends`, `trading volume`
- **Token Information**: `token details`, `holder analysis`, `new token discovery`
- **Security Audit**: `token security`, `risk check`, `honeypot detection`
- **Rankings**: `gainers/losers`, `volume rankings`, `trending tokens`

### Example Conversations

```text
💬 "View ETH USDT K-line chart"          → Query K-line data
💬 "Latest token security audit reports"  → Security risk analysis
💬 "Today's biggest gainers ranking"      → Rankings query
```

---

## 📁 File Structure

```text
gate-dex-market/
├── README.md              # This document
├── SKILL.md               # Agent specification
├── CHANGELOG.md           # Change log
└── references/            # Sub-module reference documentation
    ├── openapi.md         # ⚡ OpenAPI complete specification
    └── README-openapi.md  # OpenAPI usage guide
```

---

## 🔧 Prerequisites

**OpenAPI Mode**:
- Config file: `~/.gate-dex-openapi/config.json`
- Endpoint: `https://openapi.gateweb3.cc/api/v1/dex`

See [Root README.md](../README.md) for detailed configuration methods.

---

## 🔗 Related Skills

- [gate-dex-wallet](../gate-dex-wallet/) — Wallet comprehensive (auth, assets, transfer, DApp)
- [gate-dex-trade](../gate-dex-trade/) — Trade execution