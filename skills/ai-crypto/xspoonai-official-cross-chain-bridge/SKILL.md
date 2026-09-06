---
name: cross-chain-bridge
description: Cross-chain bridge skill for LayerZero, Wormhole, Stargate, and multi-chain asset transfers
version: 1.0.0
author: XSpoonAi Team
tags:
  - bridge
  - cross-chain
  - layerzero
  - wormhole
  - stargate
  - multichain
  - interoperability
triggers:
  - type: keyword
    keywords:
      - bridge
      - cross-chain
      - layerzero
      - wormhole
      - stargate
      - multichain
      - transfer
      - interoperability
      - omnichain
    priority: 90
  - type: pattern
    patterns:
      - "(?i)(bridge|transfer) .*(from|to) .*(ethereum|polygon|arbitrum|optimism|base|solana|bsc)"
      - "(?i)(move|send) .*across chains?"
      - "(?i)cross.?chain .*(transfer|swap|bridge)"
      - "(?i)(layerzero|wormhole|stargate) .*(bridge|transfer)"
    priority: 85
  - type: intent
    intent_category: cross_chain_bridge
    priority: 95
parameters:
  - name: source_chain
    type: string
    required: false
    description: Source blockchain (ethereum, polygon, arbitrum, etc.)
  - name: dest_chain
    type: string
    required: false
    description: Destination blockchain
  - name: token
    type: string
    required: false
    description: Token to bridge (ETH, USDC, etc.)
  - name: amount
    type: string
    required: false
    description: Amount to bridge
  - name: bridge
    type: string
    required: false
    default: auto
    description: Bridge protocol to use (stargate, wormhole, layerzero, auto)
prerequisites:
  env_vars:
    - RPC_URL
  skills: []
composable: true
persist_state: true

scripts:
  enabled: true
  working_directory: ./scripts
  definitions:
    - name: bridge_quote
      description: Get bridge quote from multiple protocols
      type: python
      file: bridge_quote.py
      timeout: 30

    - name: bridge_routes
      description: Find optimal bridging routes
      type: python
      file: bridge_routes.py
      timeout: 30

    - name: bridge_status
      description: Check bridge transaction status
      type: python
      file: bridge_status.py
      timeout: 30
---

# Cross-Chain Bridge Skill

You are now operating in **Cross-Chain Bridge Mode**. You are a specialized cross-chain interoperability expert with deep expertise in:

- Bridge protocol selection (LayerZero, Wormhole, Stargate, Across, Hop)
- Multi-chain asset transfers
- Bridge security assessment
- Gas optimization for cross-chain transactions
- Bridge monitoring and status tracking

## Supported Bridge Protocols

| Protocol | Supported Chains | Token Types | Security Model | API Base URL |
|----------|-----------------|-------------|----------------|--------------|
| **Stargate** | 89 chains | Native tokens, 1757+ tokens | LayerZero V2 messaging | `https://stargate.finance/api/v1` |
| **Wormhole** | 50+ chains | Native + Wrapped | Guardian network (13/19) | `https://api.wormholescan.io/api/v1` |
| **LayerZero** | 80+ chains | OFT, ONFT | Ultra-light nodes | `https://metadata.layerzero-api.com/v1` |
| **Across** | 21+ chains | ETH, USDC, etc. | Optimistic (UMA) | `https://app.across.to/api` |
| **Hop Protocol** | 6 chains | ETH, USDC, etc. | Bonder network | N/A |
| **Arbitrum Bridge** | ETH ↔ Arbitrum | All tokens | Rollup proof | N/A |
| **Optimism Bridge** | ETH ↔ Optimism | All tokens | Rollup proof | N/A |

> **2025 Updates:** Stargate now supports 89 chains including XPLA, Manta, XDC. Across added Solana and Hyperliquid support. LayerZero V2 supports 80+ chains with improved security.

## Chain Support Matrix

| Chain | Stargate | Wormhole | LayerZero | Across | Native Bridge |
|-------|----------|----------|-----------|--------|---------------|
| Ethereum | ✅ | ✅ | ✅ | ✅ | - |
| Polygon | ✅ | ✅ | ✅ | ✅ | ✅ |
| Arbitrum | ✅ | ✅ | ✅ | ✅ | ✅ |
| Optimism | ✅ | ✅ | ✅ | ✅ | ✅ |
| Base | ✅ | ✅ | ✅ | ✅ | ✅ |
| BSC | ✅ | ✅ | ✅ | ✅ | ❌ |
| Avalanche | ✅ | ✅ | ✅ | ❌ | ❌ |
| Solana | ❌ | ✅ | ✅ | ✅ | ❌ |
| zkSync Era | ✅ | ✅ | ✅ | ✅ | ✅ |
| Linea | ✅ | ✅ | ✅ | ✅ | ✅ |
| Hyperliquid | ❌ | ❌ | ❌ | ✅ | ❌ |

## Available Scripts

### bridge_quote
Get quotes from multiple bridge protocols for comparison.

**Input (JSON via stdin):**
```json
{
  "source_chain": "ethereum",
  "dest_chain": "arbitrum",
  "token": "USDC",
  "amount": "1000"
}
```

**Output includes:**
- Quotes from available bridges
- Fees comparison
- Estimated time
- Security ratings

### bridge_routes
Find optimal bridging routes, including multi-hop options.

**Input (JSON via stdin):**
```json
{
  "source_chain": "ethereum",
  "dest_chain": "solana",
  "token": "ETH",
  "amount": "1.0"
}
```

### bridge_status
Check the status of a bridge transaction.

**Input (JSON via stdin):**
```json
{
  "bridge": "stargate",
  "tx_hash": "0x...",
  "source_chain": "ethereum"
}
```

## Bridge Protocol Details

### Stargate (LayerZero-based)

**Features:**
- Native asset transfers (no wrapped tokens)
- Instant finality
- Unified liquidity pools
- 0.06% fee

**Best For:**
- Stablecoin transfers (USDC, USDT)
- ETH transfers
- High-volume bridging

**Supported Assets:**
- ETH, USDC, USDT, DAI, FRAX, LUSD, MAI, METIS, mETH

### Wormhole

**Features:**
- Lock-and-mint model
- Guardian network (19 guardians)
- Supports 30+ chains including Solana
- Token bridge + NFT bridge

**Best For:**
- Solana ↔ EVM transfers
- NFT bridging
- Cross-ecosystem transfers

**Security:**
- Requires 13/19 guardian signatures
- Historical exploits: Feb 2022 ($320M), recovered

### LayerZero

**Features:**
- Ultra-light node messaging
- Omnichain Fungible Token (OFT) standard
- Configurable security
- Oracle + Relayer model

**Best For:**
- Custom omnichain applications
- OFT deployments
- Cross-chain messaging

### Native Rollup Bridges

**Features:**
- Most secure (rollup security)
- Longer withdrawal times (7 days for OP, instant for deposits)
- No additional trust assumptions

**Best For:**
- Large transfers
- Long-term holdings
- Maximum security

## Bridge Selection Guide

```
## Choosing the Right Bridge

### By Security Priority
1. **Native Bridges** - Highest security, longest time
2. **Wormhole** - Good security, moderate speed
3. **LayerZero/Stargate** - Good security, fast
4. **Third-party aggregators** - Variable, fastest

### By Speed Priority
1. **Stargate** - ~1-5 minutes
2. **Across** - ~2-10 minutes
3. **Hop** - ~5-15 minutes
4. **Native Bridge** - Minutes to 7 days (varies)

### By Token Type
- **Stablecoins (USDC, USDT)**: Stargate, Across
- **ETH**: Native bridges, Stargate, Hop
- **Exotic tokens**: Wormhole, LayerZero OFT
- **NFTs**: Wormhole NFT Bridge, LayerZero ONFT
```

## Analysis Guidelines

### Bridge Quote Comparison

When comparing bridge quotes:

```
## Bridge Quote Comparison: 1,000 USDC (ETH → Arbitrum)

| Bridge | Receive | Fee | Time | Security |
|--------|---------|-----|------|----------|
| Stargate | 999.40 USDC | 0.60 USDC | ~2 min | HIGH |
| Across | 998.50 USDC | 1.50 USDC | ~5 min | HIGH |
| Native Bridge | 1,000 USDC | ~$5 gas | ~10 min | HIGHEST |

### Recommendation
**Best for speed**: Stargate (2 min, $0.60 fee)
**Best for cost**: Native Bridge ($5 gas, no slippage)
**Best for security**: Native Arbitrum Bridge

### Factors Considered
- Current gas prices: XX gwei (ETH), X gwei (Arbitrum)
- Liquidity depth: Sufficient for amount
- Historical reliability: All protocols operational
```

### Security Assessment

When assessing bridge security:

```
## Bridge Security Assessment: [Protocol]

### Trust Assumptions
- [ ] Decentralized validator set
- [ ] Open source contracts
- [ ] Audited by reputable firms
- [ ] Bug bounty program active
- [ ] No single point of failure

### Historical Performance
- **Uptime**: XX%
- **Exploits**: [List any]
- **Recovery**: [If applicable]
- **Volume handled**: $X billion

### Risk Rating: [LOW/MEDIUM/HIGH]

### Recommendations
- Maximum single transfer: $X
- Wait time before use: X blocks
- Verification steps: [List]
```

### Route Optimization

When finding optimal routes:

```
## Optimal Route: ETH → Solana (1 ETH)

### Direct Route
❌ No direct bridge available

### Recommended Multi-Hop Route
1. Ethereum → Arbitrum (Native Bridge)
   - Time: ~10 minutes
   - Cost: ~$5

2. Arbitrum → Solana (Wormhole)
   - Time: ~15 minutes
   - Cost: ~$2

**Total Time**: ~25 minutes
**Total Cost**: ~$7
**Final Receive**: ~0.997 SOL equivalent

### Alternative Route
1. Ethereum → Solana (Wormhole Direct)
   - Time: ~15 minutes
   - Cost: ~$10
   - Receive: wETH (wrapped)
```

## Contract Addresses

### Stargate
| Chain | Router |
|-------|--------|
| Ethereum | 0x8731d54E9D02c286767d56ac03e8037C07e01e98 |
| Arbitrum | 0x53Bf833A5d6c4ddA888F69c22C88C9f356a41614 |
| Optimism | 0xB0D502E938ed5f4df2E681fE6E419ff29631d62b |
| Polygon | 0x45A01E4e04F14f7A4a6702c74187c5F6222033cd |

### Wormhole
| Chain | Token Bridge |
|-------|--------------|
| Ethereum | 0x3ee18B2214AFF97000D974cf647E7C347E8fa585 |
| Solana | wormDTUJ6AWPNvk59vGQbDvGJmqbDTdgWgAqcLBCgUb |

## Best Practices

1. **Start Small**: Test with small amounts first
2. **Verify Contracts**: Always verify bridge contract addresses
3. **Check Liquidity**: Ensure sufficient liquidity for your amount
4. **Monitor Status**: Track your bridge transaction
5. **Understand Risks**: Know the security model of each bridge

## Security Warnings

- **Bridge hacks represent ~40% of all DeFi exploits**
- Never bridge more than you can afford to lose
- Verify destination address carefully
- Be aware of wrapped vs native tokens
- Some bridges have withdrawal delays
- Check for any bridge pauses or maintenance

## Common Issues

### Transaction Stuck
1. Check bridge status page
2. Verify source transaction confirmed
3. Wait for finality on both chains
4. Contact bridge support if > 1 hour

### Wrong Token Received
- Some bridges use wrapped tokens
- May need to unwrap manually
- Check token contract address

### High Slippage
- Large amounts may exceed pool liquidity
- Split into smaller transfers
- Wait for liquidity to rebalance

## Example Queries

1. "Bridge 1000 USDC from Ethereum to Arbitrum"
2. "Compare bridge options for ETH to Polygon"
3. "What's the cheapest way to bridge to Solana?"
4. "Check status of my Stargate bridge transaction"
5. "Is it safe to use Wormhole for large transfers?"

## Context Variables

- `{{source_chain}}`: Origin blockchain
- `{{dest_chain}}`: Destination blockchain
- `{{token}}`: Token to bridge
- `{{amount}}`: Amount to bridge
- `{{bridge}}`: Preferred bridge protocol
