# Trading And DeFi Prompts

## Quote-Only Trading

```text
Get a quote to swap $20 of SOL to USDC on Solana. Do not execute.
Find the best ETH to USDC route on Base and summarize fees.
Compare two swap routes for 0.5 ETH to USDC and explain slippage tradeoffs.
Get a quote to swap HBAR to USDC on Hedera. Do not execute.
Get a quote to swap MATIC to USDC on Polygon. Do not execute.
```

## Solana Intent-Style Trading

```text
Quote $100 of JUP on Solana. Do not execute.
Quote BONK exposure using 0.5 SOL on Solana. Stop before execution.
Estimate the route and expected spend for reaching roughly 100k BONK on Solana, then stop at the plan.
Prepare a quote-first plan to swap 50 USDC to BONK on Solana and stop before execution.
If BONK is ambiguous, show me the candidate token addresses first.
```

## EVM And Hedera Swaps

```text
Prepare a swap plan for $100 of ETH to USDC on Base, but stop before execution.
Show the exact transaction summary and approval steps before any swap.
Quote this trade with a maximum slippage tolerance of 1%.
Find the best BSC route to swap BNB into USDC, summarize fees, and wait for explicit confirmation before execution.
Show me the preferred native USDC route on Base instead of bridged USDbC.
```

## DeFi And Yield

```text
Show USDC yield candidates above 8% APY from supported data sources, with timestamps and risk notes.
Compare ETH/USDC liquidity pools by fee tier and depth, then rank for review only.
Screen for lower-risk stablecoin yield candidates and explain the main risks and assumptions.
Build a review-only shortlist of SOL/USDC LP opportunities with a short risk summary.
Compare lending, LP, and staking options for idle USDC in a decision table; no execution.
```

## Meme Token Discovery By Platform

```text
Show trending Clanker tokens on Base with enough liquidity for safe review and planning.
Build a watchlist of new PumpFun launches on Solana with growing holders and volume.
Show FourMeme tokens on BSC that pass basic liquidity and activity filters.
Find active MemeJob tokens on Hedera and summarize observed traction metrics.
Build a meme-token watchlist above 10k market cap, filter obvious rugs, and stop at watchlist output.
```
