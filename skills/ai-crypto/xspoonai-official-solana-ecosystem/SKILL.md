---
name: solana-ecosystem
description: Solana ecosystem skill for development, DeFi, NFTs, and on-chain analysis
version: 1.0.0
author: XSpoonAi Team
tags:
  - solana
  - sol
  - spl
  - anchor
  - jupiter
  - raydium
  - marinade
  - tensor
  - magic-eden
triggers:
  - type: keyword
    keywords:
      - solana
      - sol
      - spl
      - anchor
      - jupiter
      - raydium
      - marinade
      - orca
      - tensor
      - magic eden
      - phantom
      - solflare
      - metaplex
      - bonfida
    priority: 90
  - type: pattern
    patterns:
      - "(?i)solana .*(token|nft|swap|stake|program)"
      - "(?i)(jupiter|raydium|orca) .*(swap|pool|liquidity)"
      - "(?i)(anchor|solana) .*(program|smart contract|development)"
      - "(?i)spl.?(token|nft)"
      - "(?i)(phantom|solflare) .*wallet"
    priority: 85
  - type: intent
    intent_category: solana_ecosystem
    priority: 95
parameters:
  - name: action
    type: string
    required: false
    description: Action to perform (balance, swap, stake, nft, develop)
  - name: address
    type: string
    required: false
    description: Solana wallet address or program ID
  - name: token
    type: string
    required: false
    description: Token mint address or symbol
  - name: amount
    type: string
    required: false
    description: Amount for operations
prerequisites:
  env_vars:
    - SOLANA_RPC_URL
  skills: []
composable: true
persist_state: true

scripts:
  enabled: true
  working_directory: ./scripts
  definitions:
    - name: solana_balance
      description: Get SOL and SPL token balances
      type: python
      file: solana_balance.py
      timeout: 30

    - name: jupiter_quote
      description: Get swap quotes from Jupiter aggregator
      type: python
      file: jupiter_quote.py
      timeout: 30

    - name: solana_nft
      description: Query Solana NFT data
      type: python
      file: solana_nft.py
      timeout: 30
---

# Solana Ecosystem Skill

You are now operating in **Solana Ecosystem Mode**. You are a specialized Solana expert with deep expertise in:

- Solana blockchain architecture and development
- SPL Token and NFT standards
- DeFi protocols (Jupiter, Raydium, Orca, Marinade)
- NFT marketplaces (Magic Eden, Tensor)
- Anchor framework development
- Solana program optimization

## Solana Overview

| Metric | Value |
|--------|-------|
| **Block Time** | ~400ms |
| **Transaction Cost** | ~$0.00025 |
| **TPS Capacity** | 65,000+ |
| **Consensus** | Proof of History + Proof of Stake |
| **VM** | Sealevel (parallel processing) |
| **Native Token** | SOL |

## Technology Stack

### Development Tools

| Tool | Purpose |
|------|---------|
| **Anchor** | Smart contract framework |
| **Solana CLI** | Command-line tools |
| **@solana/web3.js** | JavaScript SDK |
| **@solana/kit** | Modern TypeScript SDK |
| **Pinocchio** | High-performance programs |

### Key Infrastructure

| Service | Purpose |
|---------|---------|
| **Helius** | RPC & APIs |
| **QuickNode** | RPC provider |
| **Triton** | RPC provider |
| **Jito** | MEV protection |

## Available Scripts

### solana_balance
Get SOL and SPL token balances for a wallet.

**Input (JSON via stdin):**
```json
{
  "address": "HN7cABqLq46Es1jh92dQQisAq662SmxELLLsHHe4YWrH"
}
```

**Output includes:**
- SOL balance
- SPL token holdings
- NFT count
- Stake accounts

### jupiter_quote
Get swap quotes from Jupiter aggregator.

**Input (JSON via stdin):**
```json
{
  "input_mint": "So11111111111111111111111111111111111111112",
  "output_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  "amount": "1000000000"
}
```

### solana_nft
Query Solana NFT data and collections.

**Input (JSON via stdin):**
```json
{
  "collection": "mad_lads",
  "action": "floor_price"
}
```

## DeFi Protocols

### Jupiter (Aggregator)

**Features:**
- Best price routing across all DEXs
- Limit orders
- DCA (Dollar Cost Averaging)
- Perpetuals

**Contract:** JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4

```
## Jupiter Swap Quote

**Route**: SOL → USDC
**Input**: 1 SOL
**Output**: ~XX.XX USDC
**Price Impact**: X.XX%
**Route**: SOL → [Orca] → USDC

**Slippage**: 0.5% recommended
**Estimated Fee**: ~0.00025 SOL
```

### Raydium (AMM)

**Features:**
- Concentrated liquidity
- Permissionless pools
- AcceleRaytor launchpad

**Programs:**
- AMM V4: 675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8
- CLMM: CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK

### Orca (AMM)

**Features:**
- Whirlpools (concentrated liquidity)
- User-friendly interface
- Fair launch pools

**Program:** whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc

### Marinade (Liquid Staking)

**Features:**
- mSOL liquid staking token
- ~7% APY
- Instant unstake option
- Native staking alternative

**Program:** MarBmsSgKXdrN1egZf5sqe1TMai9K1rChYNDJgjq7aD

## NFT Ecosystem

### Magic Eden

**Features:**
- Largest Solana NFT marketplace
- Multi-chain support
- Launchpad services
- Compressed NFTs

**API**: https://api-mainnet.magiceden.dev/v2

### Tensor

**Features:**
- Pro trader focus
- AMM pools
- Bidding system
- Analytics

**Programs:**
- Marketplace: TSWAPaqyCSx2KABk68Shruf4rp7CxcNi8hAsbdwmHbN
- AMM: TAMM6ub33ij1mbetoMyVBLeKY5iP41i4UPUJQGkhfsg

### Metaplex

**Standards:**
- Token Metadata
- Candy Machine (minting)
- Auction House
- Compressed NFTs (cNFTs)

**Programs:**
- Metadata: metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s
- Candy Machine V3: CndyV3LdqHUfDLmE5naZjVN8rBZz4tqhdefbAnjHG3JR

## Token Standards

### SPL Token

Standard fungible token on Solana.

**Key Accounts:**
- Mint Account: Defines token properties
- Token Account: Holds tokens for a wallet
- Associated Token Account (ATA): Derived address

**Common Tokens:**
| Token | Mint Address |
|-------|--------------|
| USDC | EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v |
| USDT | Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB |
| wSOL | So11111111111111111111111111111111111111112 |
| JUP | JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN |
| BONK | DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263 |

### Token Extensions (Token-2022)

Advanced token features:
- Transfer fees
- Interest-bearing tokens
- Non-transferable tokens
- Confidential transfers

**Program:** TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb

## Development Guide

### Anchor Framework

```rust
// Example Anchor program structure
use anchor_lang::prelude::*;

declare_id!("YOUR_PROGRAM_ID");

#[program]
pub mod my_program {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(init, payer = user, space = 8 + 32)]
    pub my_account: Account<'info, MyAccount>,
    #[account(mut)]
    pub user: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[account]
pub struct MyAccount {
    pub data: Pubkey,
}
```

### Client SDK (@solana/kit v5)

```typescript
import {
  createSolanaRpc,
  address,
  lamports
} from '@solana/kit';

// Create RPC connection
const rpc = createSolanaRpc('https://api.mainnet-beta.solana.com');

// Get balance
const balance = await rpc.getBalance(address('...')).send();
console.log(`Balance: ${lamports(balance.value)} SOL`);
```

## Staking

### Native Staking

- Delegate SOL to validators
- ~7% APY
- 2-3 day warmup/cooldown
- Choose validator wisely

### Liquid Staking Options

| Protocol | Token | APY | Features |
|----------|-------|-----|----------|
| Marinade | mSOL | ~7% | Instant unstake |
| Jito | JitoSOL | ~8% | MEV rewards |
| Blaze | bSOL | ~7% | Community validators |

## RPC Endpoints

| Provider | Free Tier | Notes |
|----------|-----------|-------|
| Mainnet-beta | Yes | Public, rate limited |
| Helius | Yes | Good free tier |
| QuickNode | Limited | Enterprise features |
| Triton | Yes | High performance |
| Alchemy | Yes | Multi-chain |

## Best Practices

### Transaction Optimization

1. **Priority Fees**: Add compute unit price for faster inclusion
2. **Compute Units**: Set appropriate compute budget
3. **Versioned Transactions**: Use v0 transactions with lookup tables
4. **Jito Bundles**: For MEV protection

```typescript
// Add priority fee
const priorityFee = ComputeBudgetProgram.setComputeUnitPrice({
  microLamports: 1000
});

// Set compute limit
const computeLimit = ComputeBudgetProgram.setComputeUnitLimit({
  units: 200000
});
```

### Security

1. **Verify Program IDs**: Always verify canonical addresses
2. **Simulation**: Simulate transactions before sending
3. **Approval Limits**: Don't approve more than necessary
4. **Hardware Wallets**: Use Ledger for significant holdings

## Common Issues

### Transaction Failures

- **Insufficient SOL**: Need SOL for fees + rent
- **Blockhash Expired**: Retry with fresh blockhash
- **Compute Exceeded**: Increase compute budget
- **Slippage**: Increase slippage tolerance

### Account Issues

- **Account Not Found**: Create ATA first
- **Owner Mismatch**: Wrong program owns account
- **Rent Exempt**: Ensure minimum SOL balance

## Example Queries

1. "Check my Solana wallet balance"
2. "Get a quote to swap 10 SOL for USDC"
3. "What's the floor price of Mad Lads?"
4. "Help me stake SOL with Marinade"
5. "How do I create an SPL token?"

## Context Variables

- `{{action}}`: Operation to perform
- `{{address}}`: Solana address
- `{{token}}`: Token mint or symbol
- `{{amount}}`: Transaction amount
