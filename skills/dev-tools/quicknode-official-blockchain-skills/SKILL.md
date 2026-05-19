---
name: quicknode-official-blockchain-skills
description: " > A collection of AI agent skills for blockchain development, powered by [Quicknode](https://www.quicknode.com/)"
---

# quicknode-official-blockchain-skills

_Source: [github.com/quiknode-labs/blockchain-skills](https://github.com/quiknode-labs/blockchain-skills). The body below is the upstream README.md captured at the time of registration._

---

# Blockchain Skills

> A collection of AI agent skills for blockchain development, powered by [Quicknode](https://www.quicknode.com/)

## Introduction

This repository contains a curated set of skills that enable AI agents to interact with blockchain networks, smart contracts, and decentralized applications. Each skill provides specialized knowledge and capabilities for specific blockchain ecosystems and protocols.

## What are Skills?

Skills are structured instruction sets that AI agents can use to perform blockchain-related tasks. They provide:

- **Context** - Domain-specific knowledge about protocols, APIs, and best practices
- **Capabilities** - Step-by-step guidance for common operations
- **Integration** - Direct access to Quicknode's RPC endpoints and APIs

When an AI agent loads a skill, it gains the ability to help you build, deploy, and interact with blockchain applications.

## Available Skills

| Skill | Description |
|-------|-------------|
| `quicknode-skill` | Quicknode infrastructure - RPC endpoints (80+ chains), Streams, Webhooks, IPFS, Add-ons, Yellowstone gRPC, Hypercore, SQL Explorer, Key-Value Store, SDK, Admin API, x402, MPP, Agent Subscriptions |

## Installation

### Using [skills.sh](https://skills.sh/)

```bash
npx skills add quiknode-labs/blockchain-skills
```

## Usage

Once installed, you can use natural language prompts to interact with Quicknode's infrastructure:

- "Set up a stream to monitor new blocks on Ethereum"
- "Create a filter for large USDC transfers"
- "Get the SOL balance for this wallet address"
- "Check the ETH balance across multiple wallets"
- "Query recent trades on Hyperliquid for BTC"
- "Show me whale trades above $500k notional"
- "Get liquidation data for the last 24 hours"
- "Pay an RPC call with my wallet using x402 or MPP"
- "Create a Quicknode account with my wallet and provision an endpoint"

## Quicknode Integration

This repository leverages Quicknode's infrastructure for reliable blockchain access:

### RPC Endpoints

Connect to 80+ blockchain networks with low-latency RPC endpoints:
- Ethereum, Polygon, Arbitrum, Optimism, Base
- Solana, Bitcoin, TON, TRON, StarkNet
- And many more...

### Streams

Real-time blockchain data delivery:
- Block and transaction streaming
- Custom filters and transformations
- Webhook destinations

### SQL Explorer

Direct SQL access to indexed blockchain data:
- Query indexed Hyperliquid (HyperCore) data at scale
- Standard SQL syntax with pre-built queries
- Trading, orders, fills, funding, liquidations, market data
- REST API for programmatic access

### Add-ons

Extend functionality with marketplace add-ons:
- Token and NFT APIs
- DeFi data feeds
- Historical data access
- Enhanced RPC methods

### Wallet-Paid Access for Agents

Stablecoin-paid access for autonomous agents, no API key required to start:
- **x402** and **MPP** for pay-per-request RPC ($0.001/call) on 140+ chains
- **Agent Subscriptions** to create a Quicknode account and receive a full platform API key in a single payment, unlocking the full product suite

Get your Quicknode endpoint at [Quicknode.com](https://www.quicknode.com/)

## Skill Structure

Each skill follows a consistent file organization:

```
skill-name/
├── SKILL.md          # Main skill definition
└── references/       # API and protocol references
    └── api.md
```

## Contributing

We welcome contributions! To add a new skill:

1. Fork this repository
2. Create a new directory for your skill
3. Add a `SKILL.md` with the skill definition
4. Include examples and documentation
5. Submit a pull request

### Skill Guidelines

- Focus on a specific chain, protocol, or use case
- Include practical examples with expected outputs
- Reference official documentation and APIs
- Test with real Quicknode endpoints

## License

MIT License

---

Built with Quicknode - [Get Started](https://www.quicknode.com/)
