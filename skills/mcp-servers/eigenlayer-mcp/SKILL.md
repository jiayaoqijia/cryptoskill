---
name: eigenlayer-mcp
description: "Official MCP server from EigenLayer (Layr-Labs) that provides comprehensive EigenLayer documentation, blog articles, contract source code, middleware docs, and developer guides to AI assistants via the Model Context Protocol."
version: 1.0.0
metadata:
  openclaw:
    tags: [mcp, eigenlayer, restaking, ethereum, avs, middleware, contracts, documentation]
    official: true
    source: "https://github.com/Layr-Labs/eigenlayer-mcp-server"
---

# EigenLayer MCP Server

Official MCP server from Layr-Labs (EigenLayer).

A Model Context Protocol (MCP) server that provides EigenLayer documentation and resources to Claude or other AI assistants. Serves comprehensive EigenLayer content including blog articles, documentation overview, middleware documentation and source code, contract documentation and source code, and developer guides. Built on Next.js, it can run as a standalone server locally or as a serverless function on Vercel.

## Installation

Connect to the public hosted endpoint:

```bash
claude mcp add --transport sse eigenlayer-mcp-server https://eigenlayer-mcp-server-sand.vercel.app/sse
```

Or run locally from the source:

```bash
git clone https://github.com/Layr-Labs/eigenlayer-mcp-server
cd eigenlayer-mcp-server
pnpm install
pnpm build
pnpm dev
```

## Resources Provided

- **EigenLayer Blog Articles** - Comprehensive collection of all EigenLayer blog articles
- **EigenLayer Documentation Overview** - Overview documentation for EigenLayer
- **EigenLayer Middleware Documentation** - Documentation for EigenLayer middleware
- **EigenLayer Middleware Source** - Source code documentation for EigenLayer middleware
- **EigenLayer Contracts Source** - Source code documentation for EigenLayer contracts
- **EigenLayer Developer Documentation** - Developer documentation for EigenLayer
- **EigenLayer Contracts Documentation** - Documentation for EigenLayer contracts

## Links

- **GitHub**: https://github.com/Layr-Labs/eigenlayer-mcp-server
- **Documentation**: https://docs.eigenlayer.xyz
- **Public Endpoint**: https://eigenlayer-mcp-server-sand.vercel.app/sse
