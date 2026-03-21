---
name: maiat-trust
description: Query trust scores, token safety verdicts, and reputation data for AI agents and on-chain addresses via the Maiat Protocol API. Supports agent trust verification, token forensics (honeypot/rug detection), and trust-gated swaps.
version: 0.9.0
author: JhiNResH
tags:
  - trust
  - reputation
  - agent-safety
  - token-check
  - rug-detection
  - acp
  - erc-8004
  - base
homepage: https://github.com/JhiNResH/maiat-protocol
triggers:
  - "check agent trust score"
  - "is this agent trustworthy"
  - "verify agent reputation"
  - "check token safety"
  - "is this token a rug pull"
  - "token forensics"
  - "trust-gated swap"
config:
  MAIAT_API_URL:
    description: "Maiat API endpoint (default: https://app.maiat.io)"
    default: "https://app.maiat.io"
---

# Maiat Trust — Agent & Token Trust Scores

Trust infrastructure for agent-to-agent transactions. Query trust scores, verify token safety, and gate swaps based on on-chain reputation.

## Use This When...

- "Is this agent trustworthy?"
- "Check the trust score for 0x..."
- "Is this token safe to buy?"
- "Run token forensics on [address]"
- "Get a trust-gated swap quote"
- "Show me the agent leaderboard"
- "What's the reputation of agent X?"

## API Endpoints

Base URL: `https://app.maiat.io/api/v1`

### Agent Trust Score

```bash
curl https://app.maiat.io/api/v1/agent/0x.../profile
```

Returns: `trustScore` (0-100), `completionRate`, `paymentRate`, `totalJobs`, `verdict` (trusted/caution/avoid).

### Token Safety Check

```bash
curl -X POST https://app.maiat.io/api/v1/token/check \
  -H "Content-Type: application/json" \
  -d '{"address": "0x...", "chainId": 8453}'
```

Returns: `verdict` (safe/caution/avoid), `flags` (honeypot, highTax, unverified, rugPull).

### Token Forensics (Deep Analysis)

```bash
curl -X POST https://app.maiat.io/api/v1/token/forensics \
  -H "Content-Type: application/json" \
  -d '{"address": "0x...", "chainId": 8453}'
```

Returns: ML-powered rug pull probability, holder concentration, liquidity analysis, contract risk flags.

### Trust-Gated Swap

```bash
curl -X POST https://app.maiat.io/api/v1/trust/swap \
  -H "Content-Type: application/json" \
  -d '{"tokenIn": "0x...", "tokenOut": "0x...", "amountIn": "1000000", "chainId": 8453}'
```

Returns swap quote only if token passes safety check. Verdict=avoid → no calldata returned.

### Agent Leaderboard

```bash
curl https://app.maiat.io/api/v1/agents?sort=trustScore&limit=50
```

## SDK (TypeScript)

```bash
npm install @jhinresh/maiat-sdk
```

```typescript
import { MaiatClient } from '@jhinresh/maiat-sdk';

const client = new MaiatClient({ baseUrl: 'https://app.maiat.io' });

// Check agent trust
const score = await client.getAgentScore('0x...');
console.log(score.trustScore, score.verdict);

// Check token safety
const token = await client.checkToken('0x...', 8453);
console.log(token.verdict, token.flags);
```

## Architecture

- **Guard** — Wallet-level protection, auto-checks before every transaction
- **Hook** — Uniswap V4 TrustGateHook, rewards good actors via dynamic fees
- **Evaluator** — ERC-8183 quality verification for agentic commerce
- **Wadjet** — ML risk model (60% ML + 40% heuristic) for token forensics

## On-Chain Contracts (Base Mainnet)

- MaiatOracle: `0xc6cf...c6da`
- TrustGateHook (Uniswap v4): `0xf980...daFf`
- ERC-8004 Identity Registry: `0x8004A169...9432`
- ERC-8004 Reputation Registry: `0x8004BAa1...9b63`

## ACP Offerings (Agent Commerce Protocol)

| Offering | Price | Description |
|----------|-------|-------------|
| `agent_trust` | $0.02/query | Trust score + verdict + completion rate |
| `token_check` | $0.01/query | ERC-20 safety check (honeypot/tax/unverified) |
| `token_forensics` | $0.05/query | Deep rug pull analysis (ML + heuristic) |
| `trust_swap` | $0.05/query | Token check + Uniswap quote, gated by safety |
| `agent_reputation` | $0.03/query | Community sentiment + upvote ratio |
