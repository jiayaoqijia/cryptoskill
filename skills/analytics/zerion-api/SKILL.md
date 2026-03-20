---
summary: Query crypto wallet portfolios, transactions, DeFi positions, and token prices across EVM chains and Solana using Zerion's MCP server.
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

Query crypto wallet data using the Zerion API MCP server.

## Overview

This skill provides access to Zerion's interpreted crypto wallet data through MCP tools. Supports **EVM chains** (Ethereum, Polygon, Arbitrum, Optimism, Base, BSC, and 50+ more) and **Solana**.

**Note**: API key required for authentication - get yours at https://developers.zerion.io

## Available Data

| Data Type | Description |
|-----------|-------------|
| Portfolio | Total wallet value, breakdown by chain |
| Transactions | Full transaction history with parsed actions |
| PnL | Profit/loss calculations |
| Positions | DeFi positions, staking, lending |
| Token Prices | Real-time pricing and historical charts |
| NFTs | Collections and individual NFT data |
| Gas Prices | Current gas prices across chains |

## Common Queries

### Portfolio Analysis
```
Get the portfolio for wallet 0x1234...
Show total value and breakdown by chain for 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
```

### Transaction History
```
Show recent transactions for 0x1234...
Get transaction history for 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 in the last 30 days
```

### DeFi Positions
```
Show all DeFi positions for 0x1234...
What protocols is 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 using?
```

### Token Analysis
```
Get current price of ETH
Show price chart for USDC over the last 7 days
Compare ETH price to SOL
```

### NFT Data
```
Show NFT collections owned by 0x1234...
Get details for Bored Ape #1234
List all NFTs in wallet 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
```

### Gas Prices
```
What are current gas prices on Ethereum?
Compare gas prices across all EVM chains
Show Solana transaction fees
```

## Tips

1. **Address Format**: Use 0x addresses only (e.g., 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045)
2. **Multi-Chain**: Supports EVM chains (Ethereum, Polygon, Arbitrum, Optimism, Base, BSC, etc.) and Solana
3. **Real-Time**: All data is real-time from Zerion's indexed data
4. **Auth Required**: API key needed - configure in MCP settings

## Example Workflows

### Customer Research
```
Analyze the portfolio composition of 0x1234...
What DeFi protocols are they using?
Show their transaction patterns over the last month
Calculate their PnL across all positions
```

### Token Analysis
```
Get the current price of our governance token
Compare it to historical prices
Show top holders by wallet address
```

### Competitive Analysis
```
What wallets are using Protocol X?
What's the average portfolio size?
What other protocols do they use?
Show cross-chain activity patterns
```

### Multi-Chain Analysis
```
Compare wallet activity on Ethereum vs Solana
Show portfolio breakdown across all EVM chains
Which chains have the most DeFi activity?
```

## MCP Server Details

**URL**: `https://developers.zerion.io/mcp`
**Type**: Remote HTTP MCP server
**Auth**: API key required (get at https://developers.zerion.io)
**Docs**: https://developers.zerion.io/reference/building-with-ai

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

## Related Resources

- API Docs: https://developers.zerion.io
- Zerion Dashboard: https://dashboard.zerion.io
- llms.txt: https://developers.zerion.io/llms.txt (for keeping AI tools current)

## When to Use This Skill

Use this skill when:
- Researching wallet addresses (0x format)
- Analyzing DeFi positions and protocols
- Getting real-time token prices across chains
- Investigating transaction patterns
- Exploring NFT holdings
- Checking gas prices across EVM chains and Solana
- Validating customer or competitor data
- Calculating portfolio PnL
