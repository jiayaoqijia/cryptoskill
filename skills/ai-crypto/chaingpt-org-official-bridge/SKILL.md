---
name: bridge
description: "Cross-chain bridging via the ChainGPT plugin. Across Protocol v3 — the highest-volume intent-based bridge by quote count. 10 EVM mainnets supported. Custody-free: plugin builds the unsigned depositV3 transaction; user signs externally on the origin chain, then a relayer fills on destination ~seconds later. Triggers: bridge, cross-chain, move from base to ethereum, send to arbitrum, L2 to L1, bridge USDC, optimism to polygon."
---

# ChainGPT Bridge Skill

You move funds between EVM mainnets via Across Protocol v3. Intent-based — once the deposit lands on the origin chain, a relayer (Across calls them "fillers") provides the destination liquidity within seconds. Fees: capital + relay gas + LP, all returned in the quote.

## Tools

| Tool | Purpose |
|---|---|
| `chaingpt_bridge_quote` | Fees + estimated fill time + SpokePool addresses |
| `chaingpt_bridge_build_deposit_tx` | Unsigned `depositV3` tx (refuses mainnet w/o ack) |
| `chaingpt_bridge_status` | Track a deposit by origin-chain tx hash |

## The mandatory pipeline

```text
chaingpt_bridge_quote
       │  (surface fees + fill time to user)
       ▼
chaingpt_dex_approve_tx token=<inputToken> spender=<spokePoolAddress from quote> acknowledgeMainnet=true
       │  (skip if inputToken is native — ETH/MATIC/etc.)
[user signs the approval]
       │
       ▼
chaingpt_bridge_build_deposit_tx (requires acknowledgeMainnet=true)
[user signs the deposit on the ORIGIN chain]
       │  (~seconds later)
       ▼
chaingpt_bridge_status depositTxHash=<hash>
       │  (returns destination fill tx hash once relayer fills)
       ▼
chaingpt_onchain_tx hash=<destination fill hash> chain=<destination>
```

## Supported networks

Ethereum · Base · Arbitrum · Optimism · Polygon · BSC · Avalanche · Blast · Linea · Scroll. Any pair of these can be bridged.

## Key behavior

- **Fee math**: input − relay_fee − lp_fee = output. The quote returns the exact `outputAmount` needed to keep the relayer profitable. Don't modify it.
- **Native vs ERC-20**: native bridging (ETH→ETH on a different chain) is value-bearing; the deposit tx must include `value: inputAmount`. ERC-20 sets `value: 0` and uses the prior approval.
- **Exclusivity**: each quote names an `exclusiveRelayer` for the first `exclusivityDeadline` seconds. Other relayers can fill after.
- **Fill deadline**: defaults to 4 hours. If unfilled by then, the depositor can be refunded.

## What this skill does NOT do

- Bridge to/from Solana, Sui, Aptos, or any non-EVM chain. Across is EVM-only.
- Bridge tokens that don't exist on both chains (e.g., a Base-native memecoin to Ethereum). The output token must already be deployed on the destination.
- Refund stuck deposits. After `fillDeadline`, the user has to call `requestSlowFillV3` separately — not yet a tool in this plugin.

## Credit accounting

All bridge tools cost **0 ChainGPT credits** — Across is free. Credit funnel comes from upstream `chaingpt_intel_token` (the user typically wants to research the destination token before bridging) or `chaingpt_audit_contract` (for unfamiliar destination contracts).

## Reference

- Across v3 docs: https://docs.across.to
- SpokePool ABI: this skill uses `depositV3(depositor, recipient, inputToken, outputToken, inputAmount, outputAmount, destinationChainId, exclusiveRelayer, quoteTimestamp, fillDeadline, exclusivityDeadline, message)`
