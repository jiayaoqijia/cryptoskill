# Uniswap Swap Simulation

Simulate and analyze Uniswap swaps: price impact, slippage, routing, gas estimation, and MEV considerations.

→ **[SKILL.md](SKILL.md)** — Full skill specification and workflow.

## Installation

Install into Claude Code or Cursor with:

```bash
npx skills add https://github.com/wpank/Agentic-Uniswap/tree/main/.ai/skills/uniswap-swap-simulation
```

Or via Clawhub:

```bash
npx clawhub@latest install uniswap-swap-simulation
```

## When to use

Use this skill when:

- You want to **simulate a swap before executing it**.
- You care about **price impact, slippage, and gas cost** for a proposed trade.
- You want to see **how different routes or venues** compare for a given swap.

## Example prompts

- "Simulate swapping 100,000 USDC to WETH on Base and show price impact and gas."
- "Compare routing options and slippage for swapping 10 WBTC to ETH on Arbitrum."
- "Estimate the effective execution price and cost for a large UNI sell on mainnet."
