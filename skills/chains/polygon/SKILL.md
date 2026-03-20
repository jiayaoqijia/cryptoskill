---
name: Polygon
description: Assist with Polygon PoS and zkEVM transactions, bridging, gas tokens, and ecosystem navigation.
metadata: {"clawdbot":{"emoji":"🟣","os":["linux","darwin","win32"]}}
---

## Network Confusion (Critical)
- Polygon PoS is the main chain — EVM compatible, uses MATIC for gas
- Polygon zkEVM is separate — different RPC, same MATIC token but bridged separately
- MATIC is rebranding to POL — transition in progress, wallets will update
- Polygon Mainnet ≠ Ethereum Mainnet — same address format, different networks
- Sending to wrong network loses funds — always verify network before sending

## MATIC/POL Token
- MATIC used for gas on Polygon PoS — required for all transactions
- MATIC exists on Ethereum as ERC-20 — must bridge to use on Polygon
- POL replacing MATIC — same value, automatic migration for most users
- Native MATIC on Polygon vs ERC-20 MATIC on Ethereum — different networks

## Bridging
- Official Polygon Bridge: bridge.polygon.technology — safe but slow (30+ minutes to Polygon, 7 days back)
- Withdrawals to Ethereum take 7 days — checkpoint mechanism for security
- Third-party bridges faster but have smart contract risk — Hop, Across, Stargate
- Bridge MATIC before bridging tokens — need gas on destination chain
- Always have MATIC for gas after bridging — tokens without gas are stuck

## Gas and Fees
- Gas prices in gwei like Ethereum — but much cheaper (typically 30-100 gwei)
- Transactions cost fractions of a cent — major advantage over Ethereum
- Gas spikes during high activity — NFT mints, popular drops
- Failed transactions still cost gas — same as Ethereum behavior
- Priority fee for faster inclusion — same EIP-1559 model

## Tokens and DeFi
- Same token standards as Ethereum — ERC-20, ERC-721, ERC-1155 all work
- Many Ethereum tokens have Polygon versions — verify contract addresses
- Wrapped tokens need unwrapping — bridged ETH is not native ETH
- QuickSwap, Uniswap, Aave all on Polygon — same interfaces as Ethereum
- Lower liquidity than Ethereum mainnet — higher slippage on large trades

## Wallet Setup
- MetaMask supports Polygon natively — add network from chainlist.org
- Chain ID: 137 — RPC: https://polygon-rpc.com
- Block explorer: polygonscan.com — verify transactions and contracts
- Same address as Ethereum — but balances are network-specific

## Common Issues
- "Insufficient MATIC for gas" — need MATIC, not just tokens
- Transaction stuck pending — gas price too low, speed up or wait
- Tokens not showing in wallet — add custom token with contract address
- Bridge transaction pending — checkpoints take time, don't panic
- "Network not supported" — dApp may not support Polygon, check docs

## zkEVM Specifics
- Separate network from PoS — different RPC and chain ID (1101)
- Uses ETH for gas, not MATIC — bridge ETH from Ethereum
- Faster finality than optimistic rollups — ZK proofs instead of fraud proofs
- Some opcodes behave differently — minor contract compatibility issues
- Growing ecosystem — fewer dApps than PoS currently

## Staking
- MATIC staking on Ethereum mainnet — validators secure both networks
- Delegate to validators — no minimum, rewards vary by validator
- Unbonding takes 80 checkpoints (~3-4 days) — funds locked during unbonding
- Liquid staking available — stMATIC, MaticX for liquidity while staking

## Security
- Same security model as Ethereum — private key controls all
- Approve tokens carefully — revoke unused approvals at polygonscan.com
- Verify contract addresses — scam tokens use similar names
- Official bridge is safest — third-party bridges have additional risk
- Keep some MATIC for emergencies — stuck tokens without gas is common
