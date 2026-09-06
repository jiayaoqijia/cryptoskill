# Gate DEX Wallet

> **Comprehensive Wallet Skill** — Unified entry for authentication, asset queries, transfer execution, and DApp interactions. Supports both MCP and CLI parallel implementation approaches.

Gate DEX Wallet provides complete Web3 wallet operation capabilities, dual-supported by Gate DEX MCP Server and gate-wallet CLI tool, enabling unified management and routing distribution for four core modules.

## 🔄 Auto-Update Feature

This skill automatically checks for updates from the [Gate Skills Repository](https://github.com/gate/gate-skills/tree/master/skills/gate-dex-wallet) **only at session start or first installation**:

- ⚡ **Performance Optimized**: Only checks once per session (no interaction delays)
- 🕐 **Smart Cooldown**: 1-hour minimum between version checks
- ✅ **Session Caching**: Skip repeated checks within the same session
- 🛡️ **Stable Operation**: Update failures never interrupt normal functionality  
- 🔍 **Version Tracking**: Current version displayed at session start
- 🌐 **Remote Source**: Official Gate Skills repository on GitHub

**Update Timing**:
- 🚀 **Session Start**: Check once when session begins
- 📦 **First Install**: Check during initial skill installation  
- 🔧 **Manual Trigger**: User can request "check for updates"
- ❌ **Never**: During normal user interactions (for performance)

**Update Rules**:
- 📈 Update: Local version < Remote version
- ⏭️ Skip: Remote skill doesn't exist or Local version ≥ Remote  
- 💡 User-friendly notifications for all update statuses

---

## 🎯 Core Modules

| Module | Function Scope | Typical Scenarios |
|--------|----------------|-------------------|
| 🔐 **Authentication** | Google OAuth and Gate OAuth login, token management | Login verification, session management, auto refresh |
| 💰 **Assets** | Balance queries, address retrieval, transaction history | View holdings, total assets, historical records |
| 💸 **Transfer** | Gas estimation, transaction building, signature broadcasting | Token transfers, batch transfers, fee calculation |
| 💳 **x402 Payment** | HTTP 402 — `dex_tx_x402_fetch`: pay (EVM exact / EVM upto / Solana) and retry | Gated API, flight order, usage-based upto (see [references/x402.md](./references/x402.md)) |
| 🎯 **DApp** | Wallet connection, message signing, contract interaction | DeFi operations, NFT interactions, contract approvals |

---

## 🏗️ Implementation Architecture

This skill provides two parallel wallet implementation approaches:

### MCP Implementation (AI Platform Integration)
- **Technical Approach**: Call wallet functions via MCP Server
- **Use Cases**: Wallet operations in AI conversations, cross-skill collaboration, unified authentication management
- **Core Features**: Server-side hosted signing, OAuth authentication, one-shot operations
- **Trigger Conditions**: Wallet operations mentioned in AI platform conversations

### CLI Implementation (Command Line Tool)
- **Technical Approach**: Operate via `gate-wallet` command line tool
- **Use Cases**: Script automation, developer tools, hybrid mode swap
- **Core Features**: Local tool, supports MCP hosted signing + OpenAPI hybrid mode
- **Trigger Conditions**: Users explicitly need command line operations or script integration

> **Both implementations are equivalent and complementary**: Users can choose the most suitable implementation approach based on their usage scenarios. MCP implementation focuses on seamless integration with AI platforms, CLI implementation provides command line flexibility and automation capabilities.

---

## 🚀 Quick Installation

### Method 1: Automated Installation Script (Recommended)

Run the one-click installation script from the project root directory:

```bash
# Install MCP Server + Skills (AI platform integration)
./gate-dex-wallet/install.sh

# Install gate-wallet CLI command line tool (optional)
./gate-dex-wallet/install_cli.sh
```

**MCP Installation Script Features**:
- 🔍 Auto-detect installed AI platforms (Cursor, Claude Code, Codex CLI, OpenClaw)
- ⚙️ Create corresponding MCP Server configuration files for each platform
- 🔗 Configure `gate-wallet` MCP Server connection
- 📦 Install all Gate DEX Skills (wallet, market, trade)

**CLI Installation Script Features**:
- 📋 Check Node.js / npm environment (requires Node.js >= 18)
- 📦 Globally install `gate-wallet` CLI command via npm
- 🔑 Configure OpenAPI credentials (optional, for hybrid mode swap)
- 📝 Update routing files (CLAUDE.md / AGENTS.md)

### Method 2: Manual Configuration

#### MCP Server Configuration

Add the following MCP Server to your AI platform:

**Configuration Parameters**:
- **Name**: `gate-wallet` (recommended), can also use `gate-dex`, `dex`, `wallet`, or any name
- **Type**: `HTTP`
- **URL**: `https://api.gatemcp.ai/mcp/dex`

> System auto-identifies through tool characteristics, supports any server name (as long as same URL is configured)

**Platform-Specific Configuration Methods**:

<details>
<summary><strong>Cursor Configuration</strong></summary>

Method A: Graphical Interface
- Settings → MCP → Add new MCP server → Fill in above information

Method B: Configuration File (`~/.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "gate-dex": {  // Can change to any name: gate-wallet, dex, wallet, etc.
      "url": "https://api.gatemcp.ai/mcp/dex",
      "headers": {
        "Authorization": "Bearer <your_mcp_token>"
      }
    }
  }
}
```
</details>

<details>
<summary><strong>Claude Code Configuration</strong></summary>

Method A: Command Line
```bash
claude mcp add --transport http gate-dex --scope project https://api.gatemcp.ai/mcp/dex
# Note: gate-dex can be changed to any name, such as dex, wallet, gate-wallet, etc.
```

Method B: Project Configuration File (`.mcp.json`)
```json
{
  "mcpServers": {
    "gate-dex": {  // Supports any naming
      "type": "http",
      "url": "https://api.gatemcp.ai/mcp/dex",
      "headers": {
        "Authorization": "Bearer <your_mcp_token>"
      }
    }
  }
}
```
</details>

<details>
<summary><strong>Other Platforms</strong></summary>

Add the above HTTP type server in the corresponding platform's MCP configuration, including authentication header configuration.

</details>

#### CLI Tool Configuration

```bash
# Ensure Node.js >= 18
node --version

# Install gate-wallet CLI
npm install -g gate-wallet-cli

# Verify installation
gate-wallet --version

# Configure OpenAPI credentials (optional for hybrid mode swap)
mkdir -p ~/.gate-dex-openapi
echo '{"api_key":"your_api_key","secret_key":"your_secret_key"}' > ~/.gate-dex-openapi/config.json
```

---

## 🎯 Quick Usage

### MCP Implementation (AI Platform Integration)

In AI tools like Cursor, automatically triggered when conversation contains the following intents:

**Trigger Keywords**:
- **Authentication Related**: `login`, `logout`, `authenticate`, `OAuth`, `token expired`
- **Asset Queries**: `check balance`, `total assets`, `wallet address`, `transaction history`, `token balance`
- **Transfer Operations**: `transfer`, `send tokens`, `batch transfer`, `gas fee`
- **x402 Payment**: `402 payment`, `x402 pay`, `payment required`, `pay for API/URL`, `dex_tx_x402_fetch`
- **DApp Interactions**: `connect DApp`, `sign message`, `approve`, `contract call`, `authorization`

**Example Conversations**:
```text
💬 "Help me login to Gate wallet"           → 🔐 Authentication Module
💬 "Check my ETH balance"                   → 💰 Assets Module  
💬 "Transfer 100 USDT to 0x123..."          → 💸 Transfer Module
💬 "Connect to Uniswap DApp"                → 🎯 DApp Module
```

### CLI Implementation (Command Line Tool)

Triggered when users explicitly need command line operations:

**Trigger Keywords**:
- `gate-wallet command`, `CLI tool`, `command line operations`
- `openapi-swap`, `hybrid swap`, `script automation`

**CLI Usage Examples**:
```bash
# First login
gate-wallet login

# View assets
gate-wallet balance
gate-wallet tokens

# Transfer operations
gate-wallet send --chain ETH --to 0x... --amount 0.01

# Hybrid mode swap (OpenAPI quotes + MCP signing)
gate-wallet openapi-swap --chain ARB --from - --to 0x... --amount 0.001 -y

# Interactive REPL mode
gate-wallet
```

---

## 📁 Project Structure

```text
gate-dex-wallet/
├── README.md              # This documentation
├── SKILL.md               # Agent routing and business specifications
├── CHANGELOG.md           # Change log
├── install.sh             # 🚀 MCP Server + Skills one-click installation script
├── install_cli.sh         # 🖥️ CLI tool installation script
└── references/            # Sub-module reference documentation
    ├── auth.md            # 🔐 Authentication module complete specification
    ├── transfer.md        # 💸 Transfer module complete specification
    ├── x402.md            # 💳 x402 payment (402 Payment Required) specification
    ├── dapp.md            # 🎯 DApp module complete specification
    └── cli.md             # 🖥️ CLI implementation complete specification
```

**Module Organization Principles**:
- **Main SKILL.md**: Contains complete specification for asset query module + routing rules for other modules
- **references/ Sub-documents**: Detailed implementation specifications for specialized modules
- **Dual Installation Scripts**: Separate installation for MCP implementation and CLI implementation

---

## 🔧 Prerequisites

### MCP Implementation
- **AI Platform**: Cursor, Claude Code, or other MCP-compatible platforms
- **MCP Server Configuration**:
  - Name: `gate-wallet`, `gate-dex`, `dex`, or any custom name
  - Type: `HTTP`
  - URL: `https://api.gatemcp.ai/mcp/dex`

### CLI Implementation
- **Node.js**: >= 18
- **gate-wallet CLI**: `npm install -g gate-wallet-cli`
- **OpenAPI Credentials** (optional for hybrid mode): `~/.gate-dex-openapi/config.json`

### Authentication Instructions
- **First Use**: Complete login authentication via Google OAuth or Gate OAuth
- **Token Management**: `mcp_token` automatically acquired and saved, supports silent refresh
- **Security Mechanism**: Server-side hosted signing, users don't need to manage private keys

---

## 🛡️ Security Features

- ✅ **Unified Authentication Management**: All modules share secure OAuth token mechanism
- 🔒 **Sensitive Information Protection**: `mcp_token` not displayed in plain text in conversations
- ⚡ **Auto Refresh**: Intelligent re-authentication when token expires
- 🚨 **Transaction Confirmation**: Transfers and DApp operations include mandatory user confirmation
- 📊 **Balance Verification**: Auto-verify sufficient assets before transactions
- 🔍 **Flexible Server Naming**: Auto-identify through tool characteristics, not dependent on fixed names

---

## 🔗 Related Skills

- [gate-dex-trade](../gate-dex-trade/) — Trade/DEX trading and swap
- [gate-dex-market](../gate-dex-market/) — Market data and token information queries

## 📖 Detailed Documentation

- **Authentication Module**: [references/auth.md](./references/auth.md)
- **Transfer Module**: [references/transfer.md](./references/transfer.md)
- **x402 Payment Module**: [references/x402.md](./references/x402.md) — tool `dex_tx_x402_fetch` (MCP description in English); supports exact + upto, EVM Permit2 prerequisites for upto
- **DApp Module**: [references/dapp.md](./references/dapp.md)
- **CLI Implementation**: [references/cli.md](./references/cli.md)
- **Change Log**: [CHANGELOG.md](./CHANGELOG.md)

## 🚧 Troubleshooting

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| MCP connection failed | Server not configured or misconfigured | Check MCP Server configuration, run installation script |
| Authentication failed | Token expired or invalid | Re-execute login process |
| CLI command not found | gate-wallet not installed | Run `npm install -g gate-wallet-cli` |
| OpenAPI call failed | AK/SK configuration error | Check `~/.gate-dex-openapi/config.json` |

For technical support, please provide specific error information and usage scenarios.

---

## 🆕 Update Log

View [CHANGELOG.md](./CHANGELOG.md) for detailed version change records.

---

**© 2026 Gate DEX Wallet Skill - Making Web3 Wallet Operations Simple**