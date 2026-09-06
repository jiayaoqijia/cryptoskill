# Gate MCP (OpenClaw / mcporter)

One-click installer for Gate MCP servers: **Local CEX**, **Remote CEX public**, **Remote CEX exchange (OAuth2)**, **Dex**, **Info**, **News**.

## Features

- **One-Click Install** — Installs all MCP servers by default (see table below).
- **Flexible Selection** — `./scripts/install.sh --select` for individual servers.
- **Secure Configuration** — API keys via mcporter; OAuth for remote exchange and Dex as documented in [gate-mcp](https://github.com/gate/gate-mcp).

## Included MCP Servers

| Server | Type | Function | Auth |
|--------|------|----------|------|
| `gate` | stdio | Local CEX (`npx -y gate-mcp`) | API Key + Secret (optional for public-only) |
| `gate-cex-pub` | HTTP | Remote public market data (`/mcp`) | None |
| `gate-cex-ex` | HTTP | Remote private CEX (`/mcp/exchange`) | **Gate OAuth2** — run `mcporter auth gate-cex-ex` |
| `gate-dex` | HTTP | DEX | x-api-key `MCP_AK_8W2N7Q` + Bearer `${GATE_MCP_TOKEN}` |
| `gate-info` | HTTP | Info & analysis | None |
| `gate-news` | HTTP | News | None |

## Quick Start

### Installation

```bash
# Run from the gate-skills repository root (clone https://github.com/gate/gate-skills first)
./skills/gate-mcp-openclaw-installer/scripts/install.sh
```

### Usage

```bash
# Info / news (no auth)
mcporter call gate-info.list_tickers currency_pair=BTC_USDT
mcporter call gate-news.list_news

# Remote CEX public — list tools first
mcporter list gate-cex-pub

# Remote CEX exchange — authorize once
mcporter auth gate-cex-ex

# Local CEX (requires API keys in mcporter config for `gate`)
mcporter call gate.list_spot_accounts

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

1. Visit **https://www.gate.com/myaccount/profile/api-key/manage** (after login: Avatar -> API Management).
2. Create an API Key for the **gate** (local stdio) server as needed.

**gate-cex-ex**: Use `mcporter auth gate-cex-ex` (Gate OAuth2).

**Gate-Dex**: When a query returns authorization required, open https://web3.gate.com/ for wallet setup, then complete OAuth via the assistant link.

## License

MIT License
