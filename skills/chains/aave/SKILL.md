---
name: Aave
description: Assist with Aave lending, borrowing, liquidations, and risk management across chains.
metadata: {"clawdbot":{"emoji":"👻","os":["linux","darwin","win32"]}}
---

## Core Concepts
- Supply assets to earn interest — deposit, receive aTokens representing position
- Borrow against collateral — must supply first, then borrow up to limit
- aTokens accrue interest — balance grows over time automatically
- Health Factor determines liquidation risk — below 1.0 = liquidation
- Variable and stable rates available — stable costs more but predictable

## Health Factor (Critical)
- Health Factor = (Collateral × Liquidation Threshold) / Borrowed
- Above 1.0 is safe — higher is safer
- At 1.0, liquidation begins — partial position closed
- Monitor actively during volatility — prices move, health factor changes
- Add collateral or repay debt to improve — before liquidation happens

## Supplying (Lending)
- Deposit supported assets — ETH, stablecoins, various tokens
- Receive aTokens 1:1 — aETH, aUSDC, etc.
- Interest accrues in real-time — aToken balance grows
- Can withdraw anytime if liquidity available — high utilization may block withdrawals
- Enable as collateral to borrow against — optional per asset

## Borrowing
- Must have collateral supplied first — can't borrow without
- Borrow up to LTV (Loan-to-Value) ratio — varies by asset, usually 70-85%
- Interest accrues on borrowed amount — must repay more than borrowed
- Variable rate changes with market — stable rate fixed but higher
- Debt tokens represent borrowing — not transferable

## Liquidations
- Triggered when Health Factor < 1 — automated, permissionless
- Liquidators repay portion of debt — receive collateral + bonus
- Liquidation penalty 5-10% — you lose this bonus amount
- Up to 50% of debt liquidated at once — may need multiple liquidations
- Prevention: monitor and manage HF actively

## Multi-Chain Deployment
- Aave V3 on Ethereum, Polygon, Arbitrum, Optimism, Avalanche, more
- Same interface, different markets — assets and rates differ
- Bridged assets may differ — USDC vs USDC.e
- Portals enable cross-chain — supply on one chain, borrow on another

## E-Mode (Efficiency Mode)
- Higher LTV for correlated assets — stablecoins to stablecoins, ETH to stETH
- Up to 97% LTV in E-Mode — vs ~80% normally
- Only borrow assets in same E-Mode category — restricted but efficient
- Higher liquidation risk — narrow margin, monitor closely

## GHO Stablecoin
- Aave's native stablecoin — minted by borrowing
- Backed by Aave collateral — overcollateralized
- Interest paid to Aave DAO — different from regular borrowing
- stkAAVE holders get discount — reduced borrow rate

## AAVE Token
- Governance token — vote on proposals
- Staking in Safety Module — earn rewards, risk of slashing in shortfall
- stkAAVE for staking — represents staked position
- 10-day cooldown to unstake — plus 2-day unstake window

## Risk Management
- Don't max out borrowing — leave buffer for price movements
- Diversify collateral — single asset concentration increases risk
- Use stablecoins for lower volatility — stable collateral = stable HF
- Set alerts for Health Factor — services like DefiSaver
- Consider automation — automatic deleveraging tools

## Common Mistakes
- Borrowing at max LTV — immediate liquidation risk
- Ignoring variable rate changes — rates can spike quickly
- Not monitoring during volatility — HF changes fast with price
- Supplying without enabling collateral — can't borrow if not enabled
- Forgetting about interest — debt grows over time

## Gas Considerations
- Approvals needed for each new asset — first-time gas cost
- Supply and borrow are separate transactions — plan gas for both
- L2 deployments much cheaper — Arbitrum, Optimism save significantly
- Batch operations where possible — some aggregators help

## Integrations
- DefiSaver for automation — auto-repay, auto-leverage
- Instadapp for advanced management — DeFi dashboard
- 1inch, Paraswap for swaps — swap and supply in one transaction
- Flash loans for advanced users — borrow without collateral, repay in same tx
