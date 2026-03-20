---
name: Ethereum
description: Assist with Ethereum transactions, gas optimization, token approvals, and L2 bridges.
metadata: {"clawdbot":{"emoji":"⟠","os":["linux","darwin","win32"]}}
---

## Nonce and Stuck Transactions
- Every Ethereum account has a nonce that increments with each transaction — if tx with nonce 5 is pending, nonces 6+ are blocked until 5 confirms
- To unstick: send a new tx with the SAME nonce and higher gas — this replaces the pending tx (even a 0 ETH self-transfer works)
- MetaMask "Speed up" and "Cancel" buttons do exactly this — they resubmit with same nonce and higher priority fee
- Nonce gaps cause permanent stuck state — if nonce 3 was never broadcast but 4 was, 4 will never confirm until 3 is sent

## Gas (EIP-1559)
- `maxFeePerGas` = max total you'll pay per gas unit. `maxPriorityFeePerGas` = tip to validator. `baseFee` = burned, set by protocol
- Actual cost: `min(baseFee + priorityFee, maxFee) × gasUsed` — unused gas is refunded, but failed txs still consume gas
- Gas limit is separate from gas price — setting limit too low causes "out of gas" revert, but you still pay for gas used up to that point
- Check current base fee at etherscan.io/gastracker or via `eth_gasPrice` RPC — wallets often overestimate by 20-50%

## Token Approvals (Critical Security)
- ERC-20 `approve()` grants a contract permission to spend your tokens — many dApps request unlimited (type(uint256).max) approval
- If that contract gets hacked, attacker can drain all approved tokens even years later — audit approvals at revoke.cash
- Recommend users approve only the exact amount needed, or revoke after each use
- Approvals persist forever until explicitly revoked — changing wallets doesn't help if the old address still has tokens

## Failed Transactions
- A reverted transaction is mined and consumes gas — you pay even though nothing happened
- Common causes: slippage exceeded, deadline passed, insufficient token balance, contract paused
- "Transaction failed" in explorer means it executed but reverted — completely different from "pending" (not yet mined)
- Simulating transactions before sending (via Tenderly or wallet preview) catches most revert conditions

## L2 Bridges and Withdrawals
- Optimistic rollups (Optimism, Arbitrum, Base) have 7-day withdrawal period to mainnet — this is not a bug, it's the security model
- ZK rollups (zkSync, Starknet) have faster finality but bridging back still takes 1-24 hours depending on liquidity
- Third-party bridges (Hop, Across) offer faster exits but charge fees and have smart contract risk
- Never bridge more than you can afford to wait 7 days for — or use a fast bridge and accept the fee

## MEV Protection
- Public mempool transactions can be frontrun or sandwiched — especially swaps on DEXs
- Flashbots Protect RPC (protect.flashbots.net) hides transactions from public mempool until mined
- Private transaction options: MEV Blocker, Flashbots Protect, or DEXs with native protection (CoW Swap)
- Signs of sandwich attack: swap executed at worse price than quoted, with suspicious txs immediately before and after yours

## Address Validation
- Ethereum addresses are case-insensitive but the checksum (mixed case) catches typos — `0xABC...` vs `0xabc...` are the same address
- ENS domains can expire — always verify current owner before sending to a .eth name
- Contract addresses vs EOA: contracts can reject ETH transfers or behave unexpectedly — check on etherscan if address has code
- Some tokens have multiple addresses (official + scam clones) — verify contract address on CoinGecko or project's official site
