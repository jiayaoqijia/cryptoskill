---
name: defi
description: "Interact with DeFi protocols on MAINNET via the ChainGPT plugin. Aave V3 (supply/borrow/repay/withdraw + health-factor monitoring across 7 chains), Lido stETH staking, EigenLayer restaking. Yield discovery: Pendle yield-trading markets (PT/YT), Morpho Blue lending markets + MetaMorpho vaults. Custody-free — plugin builds unsigned tx, user signs externally. Mandatory pre-flight: check Aave health factor before any borrow or withdraw; verify approval state before any supply/repay/deposit. Triggers: aave, lido, stake eth, steth, restake, eigenlayer, supply, borrow, repay, withdraw, lending, health factor, liquidation, leverage, yield, defi position, pendle, morpho, gauntlet, fixed yield, pt, yt, metamorpho, vault, lending market."
---

# ChainGPT DeFi Skill

You manage real DeFi positions on mainnet. The plugin is custody-free — it returns unsigned transactions; the user signs externally via MetaMask, Rabby, hardware wallet, ERC-4337 smart account, or WalletConnect.

## Protocols supported

| Protocol | What | Chains |
|---|---|---|
| **Aave V3** | Lending market (supply / borrow / repay / withdraw + health) | ethereum, base, arbitrum, optimism, polygon, bsc, avalanche |
| **Lido** | stETH liquid staking | Ethereum mainnet |
| **EigenLayer** | Restake LSTs (stETH / rETH / cbETH / …) | Ethereum mainnet |
| **Pendle** (read) | Yield-trading markets — split assets into PT (fixed) + YT (floating) | ethereum, arbitrum, optimism, bsc, base, mantle |
| **Morpho Blue** (read) | Isolated lending markets + MetaMorpho curated vaults | ethereum, base |

## Hard rules for mainnet

1. **Before borrowing or withdrawing from Aave, ALWAYS call `chaingpt_defi_aave_health` and surface the health factor.** Borrowing or withdrawing collateral lowers HF; if it drops below 1.0 the position is liquidated. Refuse the action and tell the user to top up if HF would drop below 1.2 after the requested operation.
2. **Before supplying, repaying, or depositing, verify the user has approved the pool / strategy manager.** ERC-20 approval is a separate signed transaction. Use `chaingpt_dex_approve_tx token=<asset> spender=<aave-pool-or-strategy-manager> acknowledgeMainnet=true` first if not done (the ack gate applies to approvals too).
3. **Echo the USD-equivalent values** before asking for confirmation. Pull the asset price from `chaingpt_research_token` if not obvious.
4. **For Lido stake**, note that stETH **rebases** — the balance grows daily. Don't store the staked amount as the "stETH balance"; it will diverge.
5. **For EigenLayer**, note the **7-day withdrawal queue**. Deposits are functionally illiquid for a week. Surface this fact before asking for confirmation.

## The "supply on Aave" pipeline

```text
chaingpt_research_token            # confirm the asset (price, contract)
chaingpt_defi_aave_health          # current position state (if any)
chaingpt_dex_approve_tx            # approve the Aave Pool to spend the asset (acknowledgeMainnet=true)
   spender=<AAVE_POOL_ADDRESS>     # surface this from the build_tx output
chaingpt_defi_aave_supply_tx       # REFUSES mainnet unless acknowledgeMainnet=true
       │
       ▼
[user signs + broadcasts]
       │
       ▼
chaingpt_defi_aave_health          # confirm the supply landed in the position
```

## The "borrow on Aave" pipeline

```text
chaingpt_defi_aave_health          # MANDATORY — check headroom + HF
chaingpt_research_token            # confirm the asset to borrow
chaingpt_defi_aave_borrow_tx       # requires acknowledgeMainnet=true
       │
       ▼
[user signs + broadcasts]
```

Surface the post-borrow estimated health factor before asking for confirmation. Rough math: post-HF ≈ totalCollateralUsd × liquidationThreshold% / (totalDebtUsd + newBorrowUsd).

## The "stake ETH on Lido" pipeline

```text
chaingpt_research_token symbol="ETH"   # current price for USD context
chaingpt_defi_lido_stake_tx amountEth="X" from="0x…"  # requires acknowledgeMainnet
[user signs + broadcasts]
```

stETH is liquid (you can swap it back to ETH via Curve / Uniswap / 1inch any time at a small discount), unlike native staking.

## The "restake on EigenLayer" pipeline

```text
[user has stETH or another supported LST]
chaingpt_dex_approve_tx           # approve EigenLayer StrategyManager to pull the LST (acknowledgeMainnet=true)
   spender="0x858646372CC42E1A627fcE94aa7A7033e7CF075A"
chaingpt_defi_eigenlayer_deposit_tx  # requires acknowledgeMainnet
[user signs + broadcasts]
```

Common strategy addresses:
- **stETH**: `0x93c4b944D05dfe6df7645A86cd2206016c51564D`
- **rETH**: `0x1BeE69b7dFFfA4E2d53C2a2Df135C388AD25dCD2`
- **cbETH**: `0x54945180dB7943c0ed0FEE7EdaB2Bd24620256bc`

Remember: **7-day exit queue**. Don't restake more than you can afford to be illiquid for a week.

## Credit accounting

DeFi reads + tx-builds burn 0 ChainGPT credits. The funnel into credits comes from the upstream `chaingpt_research_token` / `chaingpt_news_fetch` / `chaingpt_audit_contract` calls the user makes before deciding to act.

## What this skill does NOT do

- Custody anything. The plugin never sees a private key.
- Liquidation protection or auto-deleveraging. Use a dedicated keeper service if you need automation.
- Yield optimization across protocols. The user picks the strategy; this skill executes it.
- Build Pendle PT/YT swap or Morpho supply/borrow transactions. Both protocols use complex multicall + permit2 patterns; the read tools here surface markets so the user can pick a target, then deploy via the official frontend (https://app.pendle.finance / https://app.morpho.org).
- Curve, Convex, ether.fi — deferred for future tools.

## Yield discovery flow

```text
chaingpt_defi_pendle_markets network=ethereum          # rank all active fixed-yield markets by TVL
       │  (pick the highest fixed APY / maturity that fits)
       ▼
chaingpt_defi_pendle_market network=ethereum marketAddress=0x…
       │  (review PT/YT/SY contract addresses + underlying APY)
       ▼
[deploy via Pendle UI]
```

```text
chaingpt_defi_morpho_vaults network=ethereum asset=USDC   # passive: pick a curator (Gauntlet, Steakhouse, MEV Capital)
       │  OR
chaingpt_defi_morpho_markets network=ethereum             # active: pick a specific (loan, collateral, LLTV) market
       │
       ▼
chaingpt_defi_morpho_position address=<wallet>          # confirm existing exposure
       │
       ▼
[deploy via Morpho UI]
```
