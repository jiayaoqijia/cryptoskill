---
name: maiat-mcp
description: Maiat Trust Score MCP Server — query agent trust scores, token safety verdicts, and reputation data from Claude, GPT, Cursor, Codex, or any MCP-compatible AI tool.
version: 0.9.0
author: JhiNResH
tags:
  - mcp
  - trust
  - agent-safety
  - token-check
  - claude
  - cursor
homepage: https://github.com/JhiNResH/maiat-protocol/tree/master/packages/mcp-server
triggers:
  - "add maiat mcp server"
  - "trust score mcp"
  - "check agent trust in claude"
  - "token safety mcp server"
---

# Maiat MCP Server

MCP server that exposes Maiat trust scores and token safety checks to any MCP-compatible AI tool (Claude Desktop, Cursor, Codex, etc.).

## Use This When...

- "I want to check agent trust scores from Claude"
- "Add trust verification to my AI workflow"
- "Set up Maiat in Cursor/Claude Desktop"
- "Check token safety from my IDE"

## Installation

```bash
npm install -g @jhinresh/mcp-server
```

## Claude Desktop Configuration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "maiat": {
      "command": "maiat-mcp",
      "env": {
        "MAIAT_API_URL": "https://app.maiat.io"
      }
    }
  }
}
```

## Available Tools

### `maiat_agent_trust`
Query trust score for any on-chain address.

**Input**: `{ "address": "0x..." }`
**Output**: Trust score (0-100), verdict (trusted/caution/avoid), completion rate, total jobs, payment rate.

### `maiat_token_check`
Check if an ERC-20 token is safe.

**Input**: `{ "address": "0x...", "chainId": 8453 }`
**Output**: Verdict (safe/caution/avoid), flags (honeypot, highTax, unverified, rugPull).

### `maiat_token_forensics`
Deep rug pull analysis with ML scoring.

**Input**: `{ "address": "0x...", "chainId": 8453 }`
**Output**: Rug probability, holder concentration, liquidity depth, contract risk assessment.

### `maiat_leaderboard`
Get top agents by trust score.

**Input**: `{ "limit": 50 }`
**Output**: Ranked list of agents with scores and metadata.

## Running Standalone

```bash
# Via npx
npx @jhinresh/mcp-server

# Or globally installed
maiat-mcp
```

## Supported Chains

- Base (8453) — primary
- Ethereum (1)
- BNB Chain (56)
- Polygon (137)
