---
description: Query crypto wallet portfolios, transactions, DeFi positions, and token prices across EVM chains and Solana using Zerion's MCP server.
tags:
  - blockchain
  - crypto
  - defi
  - evm
  - mcp
  - solana
  - wallet
---

# Zerion API Skill

Query crypto wallet data using the Zerion API MCP server - supports EVM chains and Solana.

## Installation

Via ClawHub:
```bash
npx clawhub install abishekdharshan/zerion-api
```

Or via Claude Code, add to your skills directory.

## Features

- Portfolio analysis (total value, chain breakdown, PnL)
- Transaction history with parsed actions
- DeFi positions across protocols
- Real-time token prices and charts
- NFT collections and individual NFT data
- Gas prices across all chains

## Chain Support

- **EVM**: Ethereum, Polygon, Arbitrum, Optimism, Base, BSC, and 50+ more
- **Solana**: Full support for Solana wallets and transactions

## Requirements

- OpenClaw or Claude Code with MCP support
- **API Key**: Get your free API key at https://developers.zerion.io
- Zerion MCP server configured with authentication

## Setup

1. Get your API key at https://developers.zerion.io
2. Add to your MCP configuration:

```json
{
  "zerion": {
    "url": "https://developers.zerion.io/mcp",
    "headers": {
      "Authorization": "Bearer YOUR_API_KEY"
    }
  }
}
```

See SKILL.md for detailed instructions and examples.

## Author

Abi Dharshan (@abishekdharshan)
Product Lead, Zerion API

## License

MIT
