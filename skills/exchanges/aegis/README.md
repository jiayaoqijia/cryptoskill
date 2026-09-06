# Aegis + Flaunch Integration

Aegis provides a safety layer for AI agents trading on [Flaunch](https://flaunch.gg), the memecoin launch and trading protocol built on Base (Uniswap V4). This integration lets an agent verify that a Flaunch-launched token is safe before buying or selling it.

## Why this matters

Flaunch lets anyone launch a token in seconds. That speed is a feature for creators, but it means agents are constantly exposed to new, unaudited contracts. Aegis sits between the agent's decision to trade and the actual on-chain execution, scanning for honeypot mechanics, concentrated holdings, and contract-level exploits.

## Architecture

```
Agent decides to buy token on Flaunch
        |
        v
Agent calls Aegis MCP `assess_risk` tool
        |
        v
Aegis scans the token contract (source or bytecode)
Aegis checks sellability (anti-honeypot)
Aegis simulates the swap transaction
        |
        v
Aegis returns: ALLOW / WARN / BLOCK
        |
        v
Agent proceeds only on ALLOW (or WARN with caution)
```

## Prerequisites

- Node.js 18+
- An MCP-compatible agent (Claude Code, or any agent using the MCP SDK)
- Aegis MCP server running (`npx aegis-defi`)
- `@flaunch/sdk` installed (`npm install @flaunch/sdk`)
- A Base RPC endpoint (public default: `https://mainnet.base.org`)

## Setup

### 1. Install dependencies

```bash
npm install @flaunch/sdk viem aegis-defi
```

### 2. Start Aegis MCP server

```bash
npx aegis-defi
```

Or add it to your Claude Code config:

```bash
claude mcp add aegis npx aegis-defi
```

### 3. Connect the Flaunch SDK

```typescript
import { createFlaunch } from "@flaunch/sdk";
import { createPublicClient, http } from "viem";
import { base } from "viem/chains";

const publicClient = createPublicClient({
  chain: base,
  transport: http(),
});

const flaunch = createFlaunch({ publicClient });
```

## Aegis MCP tools used

| Tool | Purpose |
|------|---------|
| `check_token` | Anti-honeypot check - verifies the token can be sold, checks for concentrated holdings |
| `scan_contract` | Static analysis of the token's source code or bytecode for exploit patterns |
| `simulate_transaction` | Dry-run of the swap on a forked chain to catch reverts and gas anomalies |
| `assess_risk` | All-in-one check that combines scanning, simulation, and token checks into a single ALLOW/WARN/BLOCK decision |

## Workflow

1. Agent discovers a Flaunch token (via the Flaunch API, social feed, or user request).
2. Agent retrieves the token's contract address and the coin metadata using `flaunch.getCoinMetadata(coinAddress)`.
3. Agent calls Aegis `assess_risk` with `action: "swap"`, passing the token address and the Flaunch router as `targetContract`.
4. If Aegis returns `ALLOW` - agent proceeds with `flaunch.buyCoin(...)`.
5. If Aegis returns `WARN` - agent informs the user of risks and asks for confirmation.
6. If Aegis returns `BLOCK` - agent refuses the trade and explains why.

## Supported chains

| Chain | Chain ID | Status |
|-------|----------|--------|
| Base | 8453 | Supported |
| Base Sepolia | 84532 | Supported (testnet) |

## Example

See [example.ts](./example.ts) for a complete working example of a Flaunch trading agent that uses Aegis for safety checks before every swap.

## Skill file

See [skill.md](./skill.md) for a skill file that teaches an AI agent how to safely trade on Flaunch using Aegis. Optionally set `SOLODIT_API_KEY` to cross-reference detected risks against 50K+ real audit findings (free key at solodit.cyfrin.io).

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BASE_RPC` | No | Base mainnet RPC URL (defaults to `https://mainnet.base.org`) |
| `ETHERSCAN_API_KEY` | No | Basescan API key for fetching verified contract source |
| `ATTESTER_PRIVATE_KEY` | No | Private key for signing on-chain attestations (MCP-only mode works without it) |
