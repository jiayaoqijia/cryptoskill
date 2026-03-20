---
name: Uniswap
description: Assist with Uniswap swaps, liquidity provision, and avoiding common DeFi losses.
metadata: {"clawdbot":{"emoji":"🦄","os":["linux","darwin","win32"]}}
---

## Swap Execution
- Slippage tolerance sets max acceptable price change — 0.5% for stablecoins, 1-3% for volatile pairs, higher for low liquidity tokens
- "Price impact" and "slippage" are different — impact is immediate effect of your trade size, slippage is protection against price movement
- High price impact (>2%) means you're moving the market — split large trades or use limit orders on Uniswap X
- Transaction deadline prevents stale swaps — 20-30 minutes default is usually fine, but pending tx beyond deadline will fail

## MEV and Frontrunning
- Public swaps on Uniswap are visible in mempool before execution — bots can sandwich your trade
- Use MEV protection: swap through Uniswap wallet (built-in protection), or connect via Flashbots Protect RPC
- Signs of sandwich: execution price worse than quoted, with suspicious buy before and sell after your tx
- Uniswap X routes through private order flow — significantly reduces MEV extraction

## Token Approval Traps
- First swap of any token requires approval transaction — this is normal, costs gas, and happens once per token per spender
- "Infinite approval" is the default — convenient but risky if Uniswap router is ever compromised
- Check and revoke old approvals at revoke.cash — approvals persist forever until explicitly revoked
- Approval transaction can succeed while swap fails — user pays gas for approval but swap reverts on slippage

## Fake Tokens
- Anyone can create a token with any name and symbol — "USDC" on Uniswap might not be real USDC
- Always verify token contract address on CoinGecko, CoinMarketCap, or project's official site
- Warning signs: no liquidity, recently created, honeypot (can buy but not sell), tax on transfer
- Uniswap shows warning for unverified tokens — don't ignore it, especially for tokens you found via links

## Liquidity Provision
- Impermanent loss is real and permanent when you withdraw — LPs lose vs just holding when prices diverge
- V3 concentrated liquidity amplifies both gains and losses — narrow range means more fees but higher IL risk
- Out-of-range positions earn zero fees — price moves outside your range, you hold 100% of the depreciating asset
- V2 is simpler: full range, less management, but less capital efficient — consider for volatile pairs you want to forget

## V3 Position Management
- Narrower range = more fees per dollar but more rebalancing — only worth it if you actively manage
- Gas costs to adjust positions add up — each add/remove liquidity is a transaction
- "Collect fees" is separate from "remove liquidity" — uncollected fees stay in the position
- NFT represents your V3 position — losing the NFT means losing access to the liquidity

## Gas Optimization
- Approve + swap is two transactions on first use — budget gas for both
- L2s (Arbitrum, Base, Optimism) have Uniswap with 10-50x lower fees — same interface, same liquidity depth
- Swapping during low gas periods (weekends, UTC night) saves significantly on mainnet
- Failed transactions still cost gas — simulate first if unsure about slippage or liquidity

## Failed Swap Causes
- "Insufficient liquidity" — try smaller amount or different route
- "Slippage exceeded" — price moved during pending period, increase slippage or retry
- "Transfer failed" — token has transfer tax or restrictions, may be a scam token
- "Deadline exceeded" — transaction was pending too long, just retry
- "Approve first" — need to approve token before swap, this is normal

## Uniswap X and Limit Orders
- Uniswap X uses off-chain orders filled by market makers — no gas if order isn't filled
- Limit orders let you set target price — order sits until price is reached or expires
- Partial fills possible — large orders may fill incrementally
- Check order status in the app — pending orders can be cancelled

## Safety Checklist Before Large Swaps
- Verify token contract address matches official source
- Check price impact percentage — high impact means bad execution
- Confirm slippage is set appropriately for the pair
- Use MEV protection for mainnet trades
- Consider splitting very large trades
- Double-check recipient address if sending to different wallet
