---
name: alchemy-mcp
description: "MCP server enabling AI agents to interact with Alchemy's blockchain APIs for token prices, NFT data, transaction history, balances, asset transfers, and onchain transactions."
version: 1.0.0
metadata:
  openclaw:
    tags: [mcp, alchemy, blockchain, nft, tokens, ethereum, api]
    official: true
    source: "https://github.com/alchemyplatform/alchemy-mcp-server"
---

# Alchemy MCP Server

Official MCP server from Alchemy.

A Model Context Protocol (MCP) server that enables AI agents to interact with Alchemy's blockchain APIs in a structured way. Allows agents to query token prices and price history, get NFT ownership information and contract data, view transaction history across multiple networks, check token balances, retrieve detailed asset transfers, send transactions via Smart Contract Accounts, and execute token swaps via DEX protocols.

## Installation

```bash
# From the official repo:
git clone https://github.com/alchemyplatform/alchemy-mcp-server
cd alchemy-mcp-server
npm install
```

Or use directly with npx:

```json
{
  "mcpServers": {
    "alchemy": {
      "command": "npx",
      "args": ["-y", "@alchemy/mcp-server"],
      "env": {
        "ALCHEMY_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

## Links

- **GitHub**: https://github.com/alchemyplatform/alchemy-mcp-server
- **Documentation**: https://docs.alchemy.com
