---
name: tatum-blockchain-mcp
description: "MCP server providing access to the Tatum Blockchain Data API and RPC Gateway, enabling LLMs to read and write blockchain data across 130+ networks."
version: 1.0.0
metadata:
  openclaw:
    tags: [mcp, tatum, blockchain, multi-chain, rpc, api]
    official: true
    source: "https://github.com/tatumio/blockchain-mcp"
---

# Tatum Blockchain MCP

Official MCP server from Tatum.

A Model Context Protocol (MCP) server that provides access to the Tatum Blockchain Data API and RPC Gateway, enabling any LLM to read and write blockchain data across 130+ networks including Bitcoin, Ethereum, Solana, Polygon, Arbitrum, Base, Avalanche, and many more. Provides blockchain data API (blocks, transactions, balances, network info) and direct RPC gateway access.

## Installation

```bash
# From the official repo:
git clone https://github.com/tatumio/blockchain-mcp
cd blockchain-mcp
npm install
```

Or install globally:

```bash
npm install -g @tatumio/blockchain-mcp
```

## Links

- **GitHub**: https://github.com/tatumio/blockchain-mcp
- **Documentation**: https://tatum.io/mcp
