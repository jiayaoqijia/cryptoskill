---
name: gate-mcp-openclaw-installer
version: "2026.3.25-2"
updated: "2026-03-25"
description: "Gate MCP one-click installer for OpenClaw (mcporter). Use when the user asks to install or configure Gate MCP servers with OpenClaw. Triggers on 'install Gate MCP', 'OpenClaw Gate', 'mcporter Gate'."
---

# Gate MCP (OpenClaw / mcporter)

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read [gate-runtime-rules.md](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.


---

## MCP Dependencies

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| Gate (main) | ✅ Required |
| Gate-Dex | ✅ Required |
| Gate-Info | ✅ Required |
| Gate-News | ✅ Required |

### Authentication
- API Key Required: No

### Installation Check
- Required: Gate (main), Gate-Dex, Gate-Info, Gate-News
- Install: Run installer skill for your IDE
  - Cursor: `gate-mcp-cursor-installer`
  - Codex: `gate-mcp-codex-installer`
  - Claude: `gate-mcp-claude-installer`
  - OpenClaw: `gate-mcp-openclaw-installer`

## MCP Mode

**Read and strictly follow** [`references/mcp.md`](./references/mcp.md), then execute this installer workflow.

- `SKILL.md` keeps mode descriptions, quick-start semantics, and product guidance.
- `references/mcp.md` is the authoritative execution layer for mcporter install sequencing, auth gates, and fallback policy.

## Quick Start

```bash
# Install all Gate MCP servers (default)
./scripts/install.sh

# Selective installation
./scripts/install.sh --select
```

## CEX MCP modes

| Mode | mcporter name | Endpoint | Auth |
|------|-----------------|----------|------|
| **Local CEX** | `gate` | stdio `npx -y gate-mcp` | `GATE_API_KEY` / `GATE_API_SECRET` (optional for public-only) |
| **Remote CEX — Public** | `gate-cex-pub` | `https://api.gatemcp.ai/mcp` | None |
| **Remote CEX — Exchange** | `gate-cex-ex` | `https://api.gatemcp.ai/mcp/exchange` | **Gate OAuth2** — run `mcporter auth gate-cex-ex` after add |
| **DEX** | `gate-dex` | `https://api.gatemcp.ai/mcp/dex` | x-api-key `MCP_AK_8W2N7Q` + `Authorization: Bearer ${GATE_MCP_TOKEN}` |
| **Info** | `gate-info` | `https://api.gatemcp.ai/mcp/info` | None |
| **News** | `gate-news` | `https://api.gatemcp.ai/mcp/news` | None |

Details: [gate-mcp README](https://github.com/gate/gate-mcp).

## MCP Servers (summary)

| Server | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `gate` | `npx -y gate-mcp` | API Key + Secret | Local CEX (stdio) |
| `gate-cex-pub` | `https://api.gatemcp.ai/mcp` | None | Remote public market data |
| `gate-cex-ex` | `https://api.gatemcp.ai/mcp/exchange` | OAuth2 (`mcporter auth gate-cex-ex`) | Remote private CEX |
| `gate-dex` | `https://api.gatemcp.ai/mcp/dex` | x-api-key + Bearer | DEX |
| `gate-info` | `https://api.gatemcp.ai/mcp/info` | None | Info & analysis |
| `gate-news` | `https://api.gatemcp.ai/mcp/news` | None | News |

## Installation Modes

### 1. Install All (Default)
```bash
./scripts/install.sh
```
Installs all configured servers. Prompts for Gate API credentials when adding **gate** (local).

### 2. Selective Install
```bash
./scripts/install.sh --select
# or
./scripts/install.sh -s
```
Interactive menu to choose a server (1–6).

## Common Commands

```bash
# Market / info (no auth)
mcporter call gate-info.list_tickers currency_pair=BTC_USDT
mcporter call gate-news.list_news

# Remote CEX public — list tools first, then call cex_* tools
mcporter list gate-cex-pub

# Local CEX trading (requires API keys in mcporter env)
mcporter call gate.list_spot_accounts

# Remote CEX exchange (OAuth2) — authorize first
mcporter auth gate-cex-ex

# DEX (wallet; may require web3 + OAuth)
mcporter call gate-dex.list_balances
```

## API Configuration

### Getting API Keys (Local `gate` server)
1. Visit https://www.gate.com/myaccount/profile/api-key/manage
2. Create API key with permissions as needed (Read / Trade / Withdraw).

### Gate-Dex authorization
When a **gate-dex** query returns "need authorization": (1) Open https://web3.gate.com/ to create or bind a wallet if needed; (2) Complete OAuth via the link the assistant provides.

### Remote CEX exchange (OAuth2)
After install, run `mcporter auth gate-cex-ex` and complete Gate OAuth2 in the browser.

### Storing Credentials
The installer stores credentials in mcporter config where applicable.

## Troubleshooting

**mcporter not found**
```bash
npm install -g mcporter
```

**Connection failed**
- Verify API keys are correct (for `gate`)
- For `gate-cex-ex`, run `mcporter auth gate-cex-ex`
- Check network: `mcporter daemon status` if using daemon

## References

- [Gate MCP GitHub](https://github.com/gate/gate-mcp)
- [Gate Skills](https://github.com/gate/gate-skills)
- [Gate API Docs](https://www.gate.com/docs/developers/apiv4/en/)
