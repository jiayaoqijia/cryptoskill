---
name: chainflip-baas-mcp
description: "Cross-chain cryptocurrency swaps via Chainflip. Get quotes, execute swaps, and track progress across Bitcoin, Ethereum, Solana, and Arbitrum."
version: 1.0.0
homepage: https://chainflip-broker.io/ai
tags:
  - chainflip
  - cross-chain
  - swaps
  - dex
  - mcp
metadata:
  openclaw:
    tags: [chainflip, cross-chain, swaps, dex, mcp, bitcoin, ethereum, solana, arbitrum, defi]
    official: false
    source: "https://github.com/CumpsD/broker-as-a-service"
---

# Chainflip Broker as a Service MCP Server

Official MCP server for cross-chain cryptocurrency swaps through the [Chainflip](https://chainflip.io) decentralized exchange.

This remote MCP server enables AI agents to discover assets, get swap quotes, execute cross-chain swaps, and track swap progress. Supports Bitcoin, Ethereum, Solana, Arbitrum, and all assets on supported chains. No API key required to get started.

## Supported Chains

- Bitcoin
- Ethereum (ETH, USDC, USDT, FLIP, WBTC)
- Solana (SOL, USDC, USDT)
- Arbitrum (ETH, USDC, USDT)

## Tools

| Tool | Description |
|---|---|
| `list_assets` | Discover all available assets with tickers, networks, decimals, minimum amounts, and live USD prices |
| `get_quotes` | Get swap quotes using human-readable amounts (e.g., 1.5 BTC) |
| `get_native_quotes` | Get swap quotes using native unit amounts (e.g., 150000000 satoshis) |
| `start_swap` | Execute a cross-chain swap and receive a deposit address |
| `start_dca_swap` | Execute a DCA swap that splits into multiple sub-swaps to reduce price impact on large trades |
| `check_status` | Track swap progress through its stages: Waiting, Receiving, Swapping, Sending, Sent, Completed |

## Prompts

| Prompt | Description |
|---|---|
| `swap-assistant` | Guided workflow that walks through asset discovery, quoting, swap execution, and status monitoring |

## Installation

This is a remote MCP server using Streamable HTTP transport. No local installation required.

```json
{
  "mcpServers": {
    "chainflip-baas": {
      "type": "streamable-http",
      "url": "https://chainflip-broker.io/mcp"
    }
  }
}
```

Or add it via the Claude CLI:

```bash
claude mcp add chainflip-baas --transport http https://chainflip-broker.io/mcp
```

No authentication is required. An optional API key can be provided for partner attribution by registering at https://chainflip-broker.io.

## Links

- **Website**: https://chainflip-broker.io
- **GitHub**: https://github.com/CumpsD/broker-as-a-service
- **Documentation**: https://docs.chainflip-broker.io
- **AI Documentation**: https://chainflip-broker.io/ai
- **MCP Registry**: https://registry.modelcontextprotocol.io/v0.1/servers?search=io.chainflip-broker/baas
