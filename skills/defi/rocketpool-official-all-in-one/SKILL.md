---
name: rocketpool
description: Interact with Rocket Pool protocol contracts on Ethereum mainnet and Hoodi testnet. Use for any task involving rETH (liquid staking token), RPL (governance token), ETH staking, minting/burning rETH, checking exchange rates, node operator registration, minipool/megapool management, RPL staking, governance proposals, voting, rewards claiming, deposit pool queries, network balances, smoothing pool, or any Rocket Pool smart contract interaction. Supports both cast (Foundry CLI) and Ethereum MCP tools.
---

# Rocket Pool Contracts

## Quick Start

### Query rETH Exchange Rate
```bash
cast call 0xae78736Cd615f374D3085123A210448E74Fc6393 "getExchangeRate()(uint256)" --rpc-url https://ethereum-rpc.publicnode.com
```

### Deposit ETH to Mint rETH
```bash
cast send 0xCE15294273CFb9D9b628F4D61636623decDF4fdC "deposit()" --value 1ether --rpc-url $RPC_URL --private-key $PK
```

### Check rETH Balance
```bash
cast call 0xae78736Cd615f374D3085123A210448E74Fc6393 "balanceOf(address)(uint256)" $WALLET --rpc-url https://ethereum-rpc.publicnode.com
```

## Workflow

1. Look up the contract address from `references/addresses.json`
2. Find the function signature in the relevant domain reference file (see table below)
3. Use ABI files in `assets/abis/<contractName>.json` as a reference for function signatures and tuple layouts when needed
4. Execute via `cast call` (read) or `cast send` (write), or via MCP `eth_call`/`eth_sendTransaction`

For calls that involve complex types (for example tuples), use the ABI JSON to derive the exact signature:
```bash
cast call 0xCE15294273CFb9D9b628F4D61636623decDF4fdC "getBalance()(uint256)" --rpc-url $RPC_URL
```

## Domain Reference Files

| User wants to... | Load |
|---|---|
| Mint/burn rETH, check exchange rate, query deposit pool | [liquid-staking.md](references/liquid-staking.md) |
| Register node, create validators, manage minipools/megapools, reduce bond | [node-operations.md](references/node-operations.md) |
| Vote on proposals, check governance state, security council, oDAO | [governance.md](references/governance.md) |
| Check network balances, RPL price, fees, penalties, voting power | [network.md](references/network.md) |
| Claim rewards, smoothing pool, merkle distribution, treasury | [rewards.md](references/rewards.md) |
| RPL/rETH ERC-20 ops, inflation, vault, L2 addresses | [tokens.md](references/tokens.md) |

## Network Configuration

| Network | Chain ID | RPC | rocketStorage |
|---|---|---|---|
| Mainnet | 1 | `https://ethereum-rpc.publicnode.com` | `0x1d8f8f00cfa6758d7bE78336684788Fb0ee0Fa46` |
| Hoodi | 560048 | `https://rpc.hoodi.ethpandaops.io` | `0x594Fb75D3dc2DFa0150Ad03F99F97817747dd4E1` |

All contract addresses per network are in `references/addresses.json`.

## Architecture

- **RocketStorage** is the central registry — all contracts resolve each other's addresses through it
- Contracts are upgradeable via governance: addresses in `addresses.json` reflect current deployments but can change
- To resolve an address dynamically:
  ```bash
  cast call $ROCKET_STORAGE "getAddress(bytes32)(address)" $(cast keccak "contract.addressrocketDepositPool") --rpc-url $RPC_URL
  ```
- **Minipools** (legacy): one contract per validator, 8 or 16 ETH bond
- **Megapools** (Saturn/v1.4): one contract per node, multiple validators, variable bond
- All ETH values are in wei (18 decimals); all percentages are 18-decimal fixed point (1e18 = 100%)

## ABIs

ABI JSON files are bundled for most mainnet contracts in `assets/abis/`.
The following contracts are signature-only in this skill (no bundled ABI): `rocketNetworkRevenues`, `rocketDAOSecurityUpgrade`, `rocketMegapoolFactory`, `rocketMegapoolDelegate`, `rocketMegapoolManager`, `rocketMegapoolPenalties`.
Use these files as signature references for `cast call` / `cast send`:
```bash
cast call 0xae78736Cd615f374D3085123A210448E74Fc6393 "getExchangeRate()(uint256)" --rpc-url $RPC_URL
```
