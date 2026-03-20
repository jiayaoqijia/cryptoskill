# Gate MCP

One-click installer for all Gate MCP servers, supporting spot trading, futures, wallet, market data, and news queries.

## Features

- **One-Click Install** - Installs all MCP servers by default
- **Flexible Selection** - Supports installing individual servers
- **Secure Configuration** - Automatically manages API keys
- **Ready to Use** - Works out of the box after download

## Included MCP Servers

| Server | Type | Function | Auth |
|--------|------|----------|------|
| `gate` | stdio | Spot/Futures/Options trading | API Key + Secret |
| `gate-dex` | HTTP | DEX operations | x-api-key built-in (MCP_AK_8W2N7Q) + Authorization: Bearer ${GATE_MCP_TOKEN} |
| `gate-info` | HTTP | Market data | No auth required |
| `gate-news` | HTTP | News feed | No auth required |

## Quick Start

### Installation

```bash
# Run from the gate-skills repository root (clone https://github.com/gate/gate-skills first)
./skills/gate-mcp-openclaw-installer/scripts/install.sh
```

### Usage

```bash
# Check BTC price (no auth required)
mcporter call gate-info.list_tickers currency_pair=BTC_USDT

# Check account balance (requires auth)
mcporter call gate.list_spot_accounts

# Check news (no auth required)
mcporter call gate-news.list_news

# List installed servers
mcporter config list | grep gate
```

## Installation Options

### Default: Install All
```bash
./skills/gate-mcp-openclaw-installer/scripts/install.sh
```

### Selective Installation
```bash
./skills/gate-mcp-openclaw-installer/scripts/install.sh --select
# or
./skills/gate-mcp-openclaw-installer/scripts/install.sh -s
```

## Detailed Documentation

See [SKILL.md](SKILL.md) for full usage instructions.

## Getting API Keys

1. Visit **https://www.gate.com/myaccount/profile/api-key/manage** (after login: Avatar -> API Management)
2. Create an API Key and select the required permissions:
   - **Read** - Market queries, account info
   - **Trade** - Spot/Margin/Futures
   - **Withdraw** - Wallet operations

**Gate-Dex Authorization**: When a gate-dex query (balance/transfer/swap, etc.) returns an authorization required message, first open [https://web3.gate.com/](https://web3.gate.com/) to create or bind a wallet; the assistant will return a clickable Google authorization link for you to complete OAuth.

## License

MIT License
