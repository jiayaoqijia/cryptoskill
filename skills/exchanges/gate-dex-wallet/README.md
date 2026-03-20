# Gate DEX Wallet

> **Comprehensive Wallet Skill** — Unified entry point for authentication, asset queries, transfer execution, and DApp interactions

Provides complete Web3 wallet operation capabilities through the Gate DEX MCP Server, supporting unified management and routing distribution for four core modules.

---

## 🎯 Core Modules

| Module | Functionality | Typical Use Cases |
|------|---------|---------|
| 🔐 **Authentication** | Google OAuth login, Token management | Login verification, session management, auto refresh |
| 💰 **Assets** | Balance queries, address retrieval, transaction history | View holdings, total assets, historical records |
| 💸 **Transfer** | Gas estimation, transaction building, signature broadcast | Token transfers, batch transfers, fee calculation |
| 🎯 **DApp** | Wallet connection, message signing, contract interaction | DeFi operations, NFT interactions, contract authorization |

---

## 🚀 Quick Installation

### Method 1: Auto Installation Script (Recommended)

```bash
# Run one-click installation script in project root directory
./gate-dex-wallet/install.sh
```

The script will automatically:
- 🔍 Detect installed AI platforms (Cursor, Claude Code, Codex CLI, OpenCode, OpenClaw)
- ⚙️ Create configuration files for each platform
- 🔗 Configure `gate-wallet` MCP Server connection
- 📦 Install all 3 Gate DEX Skills

### Method 2: Manual Configuration

See detailed configuration methods in [root README.md](../README.md).

---

## 🎯 Quick Usage

### Trigger Methods

Automatically triggered in AI tools like Cursor when user conversation contains the following intents:

- **Authentication related**: `login`, `logout`, `token expired`, `re-authentication`
- **Asset queries**: `check balance`, `total assets`, `wallet address`, `transaction history`
- **Transfer operations**: `transfer`, `send tokens`, `batch transfer`, `Gas fee`
- **DApp interactions**: `connect DApp`, `sign message`, `Approve`, `contract call`

### Example Conversations

```text
💬 "Help me login to Gate wallet"         → 🔐 Authentication module
💬 "Check my ETH balance"                 → 💰 Assets module  
💬 "Transfer 100 USDT to 0x123..."       → 💸 Transfer module
💬 "Connect to Uniswap DApp"              → 🎯 DApp module
```

---

## 📁 File Structure

```text
gate-dex-wallet/
├── README.md              # This document
├── SKILL.md               # Agent routing specification
├── CHANGELOG.md           # Change log
├── install.sh             # 🚀 One-click installation script
└── references/            # Sub-function reference documents
    ├── auth.md            # 🔐 Authentication module complete specification
    ├── transfer.md        # 💸 Transfer module complete specification
    └── dapp.md            # 🎯 DApp module complete specification
```

**Assets module** complete specification is directly included in the main `SKILL.md`, while the other three modules are organized through `references/` files.

---

## 🔧 Prerequisites

Ensure Gate DEX MCP Server is configured before use:

- **Server Name**: `gate-wallet`
- **Type**: `HTTP`
- **URL**: `https://api.gatemcp.ai/mcp/dex`

See detailed configuration methods in [root README.md](../README.md).

---

## 🛡️ Security Features

- ✅ **Unified authentication management**: All modules share secure token mechanism
- 🔒 **Sensitive information protection**: `mcp_token` not displayed in plain text in conversations
- ⚡ **Auto refresh**: Smart re-authentication when tokens expire
- 🚨 **Transaction confirmation**: Transfer and DApp operations include mandatory user confirmation
- 📊 **Balance verification**: Automatic asset sufficiency validation before transactions

---

## 🔗 Related Skills

- [gate-dex-trade](../gate-dex-trade/) — Trade/DEX trading
- [gate-dex-market](../gate-dex-market/) — Market data queries