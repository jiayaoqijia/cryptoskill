# Gate DEX Trade

> **Trading Comprehensive Skill** — MCP + OpenAPI dual mode, intelligently selects the best trading method

Provides complete Swap trading capabilities through Gate DEX, supporting quote retrieval, slippage control, trade execution, status tracking and other functions.

---

## 🎯 Core Modes

| Mode | Connection Method | Features | Use Cases |
|------|------------------|----------|-----------|
| 🔗 **MCP Mode** | gate-wallet MCP Server | Unified authentication, three-step confirmation | Secure trading, wallet ecosystem integration |
| ⚡ **OpenAPI Mode** | AK/SK direct calls | Complete lifecycle, multi-chain support | Fast trading, full process control |

---

## 🚀 Quick Installation

### Method 1: Automatic Installation Script (Recommended)

```bash
# Run trade-specific installation script
./gate-dex-trade/install.sh
```

Script features:
- 🔍 Auto-detect AI platforms and configure
- 📊 Optimize Skill loading order for trading functions
- 🔄 Configure MCP + OpenAPI dual mode support
- 🎯 Generate trade-priority routing files

### Method 2: Manual Configuration

See detailed configuration method in [Root README.md](../README.md).

---

## 🚀 Quick Usage

### Trigger Methods

- **Trading Intent**: `swap`, `exchange`, `buy`, `sell`, `trade`
- **Quote Query**: `quote`, `exchange rate`, `Gas fee`, `slippage`
- **Status Query**: `trade status`, `order status`, `trade history`

### Example Conversations

```text
💬 "Swap 100 USDT to ETH"              → Intelligently select best trading mode
💬 "Check ETH to BNB quote"            → Quote retrieval
💬 "My trading records"                → History query
```

---

## 📁 File Structure

```text
gate-dex-trade/
├── README.md              # This document
├── SKILL.md               # Agent dual mode routing specification
├── CHANGELOG.md           # Change log
└── references/            # Sub-module reference documentation
    ├── openapi.md         # ⚡ OpenAPI mode complete specification
    └── README-openapi.md  # OpenAPI mode usage guide
```

**MCP Mode** complete specifications are directly included in the main `SKILL.md`.

---

## 🔧 Prerequisites

**MCP Mode**:
- Server Name: `gate-wallet`  
- URL: `https://api.gatemcp.ai/mcp/dex`
- Requires user login authentication

**OpenAPI Mode**:
- Config file: `~/.gate-dex-openapi/config.json`
- Endpoint: `https://openapi.gateweb3.cc/api/v1/dex`
- Supports built-in default credentials

See detailed configuration method in [Root README.md](../README.md).

---

## 🛡️ Security Features

- ✅ **Dual Security Mechanism**: MCP mode three-step confirmation, OpenAPI mode private key protection
- 🔒 **Credential Isolation**: Two modes use different authentication mechanisms
- ⚡ **Smart Routing**: Automatically select the most suitable calling method
- 🚨 **Risk Control**: Price difference warnings, slippage alerts, MEV protection
- 📊 **Balance Pre-check**: Mandatory asset sufficiency verification before trading

---

## 🔗 Related Skills

- [gate-dex-wallet](../gate-dex-wallet/) — Wallet comprehensive (authentication, assets, transfers, DApp)
- [gate-dex-market](../gate-dex-market/) — Market data queries