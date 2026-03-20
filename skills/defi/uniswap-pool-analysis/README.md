# Uniswap Pool Analysis

Analyze Uniswap pool data: liquidity distribution, fee tiers, tick ranges, TVL, and other structural properties.

→ **[SKILL.md](SKILL.md)** — Full skill specification and workflow.

## Installation

Install into Claude Code or Cursor with:

```bash
npx skills add https://github.com/wpank/Agentic-Uniswap/tree/main/.ai/skills/uniswap-pool-analysis
```

Or via Clawhub:

```bash
npx clawhub@latest install uniswap-pool-analysis
```

## When to use

Use this skill when:

- You want to **inspect the structure of a Uniswap pool** in detail.
- You need to understand **where liquidity sits**, which **fee tiers** exist, and **tick ranges** in use.
- You're designing **LP or trading strategies** that depend on pool microstructure.

## Example prompts

- "Analyze the liquidity distribution and tick ranges for the WETH/USDC 0.3% pool on mainnet."
- "Show how TVL and liquidity are distributed across ticks for a specific V3 pool on Arbitrum."
- "Compare liquidity distribution across fee tiers for USDC/ETH on Optimism."
