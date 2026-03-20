---
name: rocketpool-tokens
description: Interact with Rocket Pool token contracts — RPL (governance/staking token) ERC-20 operations, inflation mechanics, old RPL swap, rocketVault balance queries, and L2 token addresses for rETH and RPL on Arbitrum, Optimism, Base, Polygon, zkSync Era, Scroll, Starknet, and Unichain. Supports cast (Foundry CLI) and Ethereum MCP tools on mainnet and Hoodi testnet.
---

# Rocket Pool — Tokens

## Quick Start

### Check RPL Balance
```bash
cast call 0xD33526068D116cE69F19A9ee46F0bd304F21A51f "balanceOf(address)(uint256)" $WALLET --rpc-url https://ethereum-rpc.publicnode.com
```

### Check RPL Total Supply
```bash
cast call 0xD33526068D116cE69F19A9ee46F0bd304F21A51f "totalSupply()(uint256)" --rpc-url https://ethereum-rpc.publicnode.com
```

### Check Vault ETH Balance for a Contract
```bash
cast call 0x3bDC69C4E5e13E52A65f5583c23EFB9636b469d6 "balanceOf(string)(uint256)" "rocketDepositPool" --rpc-url https://ethereum-rpc.publicnode.com
```

## Workflow

1. Look up the contract address from `references/addresses.json`
2. Find the function signature below
3. Load the ABI from `assets/abis/<contractName>.json` if needed for complex types
4. Execute via `cast call` (read) or `cast send` (write)

## Network Configuration

| Network | Chain ID | RPC | rocketStorage |
|---|---|---|---|
| Mainnet | 1 | `https://ethereum-rpc.publicnode.com` | `0x1d8f8f00cfa6758d7bE78336684788Fb0ee0Fa46` |
| Hoodi | 560048 | `https://rpc.hoodi.ethpandaops.io` | `0x594Fb75D3dc2DFa0150Ad03F99F97817747dd4E1` |

## Architecture

- **RocketStorage** is the central registry — all contracts resolve each other's addresses through it
- All ETH values are in wei (18 decimals)
- RPL has 18 decimals
- rETH and RPL are bridged to multiple L2s as standard ERC-20 tokens

## rocketTokenRPL

The RPL governance and staking token. Has built-in inflation mechanism. Implements ERC-20 with burn.

### Functions

ERC-20:
```
balanceOf(address account) → uint256 [view]
transfer(address recipient, uint256 amount) → bool
transferFrom(address sender, address recipient, uint256 amount) → bool
approve(address spender, uint256 amount) → bool
allowance(address owner, address spender) → uint256 [view]
totalSupply() → uint256 [view]
decimals() → uint8 [view]
```

Inflation:
```
inflationCalculate() → uint256 [view]
inflationMintTokens() → uint256
getInflationIntervalRate() → uint256 [view]
getInflationIntervalStartTime() → uint256 [view]
getInflationIntervalTime() → uint256 [pure]
getInflationIntervalsPassed() → uint256 [view]
getInflationCalcTime() → uint256 [view]
getInflationRewardsContractAddress() → address [view]
```

Swap old RPL:
```
swapTokens(uint256 _amount)
totalSwappedRPL() → uint256 [view]
```

Burn:
```
burn(uint256 amount)
burnFrom(address account, uint256 amount)
```

### Examples

```bash
cast call $RPL "balanceOf(address)(uint256)" $WALLET --rpc-url $RPC_URL
cast call $RPL "totalSupply()(uint256)" --rpc-url $RPC_URL
cast call $RPL "inflationCalculate()(uint256)" --rpc-url $RPC_URL
```

## rocketTokenRPLFixedSupply

The original fixed-supply RPL token (pre-migration). Can be swapped 1:1 for new RPL via `rocketTokenRPL.swapTokens()`. Standard ERC-20 only.

## rocketVault

Central vault holding all protocol ETH and token balances. Internal accounting per contract name.

### Functions

```
balanceOf(string _networkContractName) → uint256 [view]
balanceOfToken(string _networkContractName, address _tokenAddress) → uint256 [view]
depositEther() [payable]
withdrawEther(uint256 _amount)
depositToken(string _networkContractName, address _tokenContract, uint256 _amount)
withdrawToken(address _withdrawalAddress, address _tokenAddress, uint256 _amount)
transferToken(string _networkContractName, address _tokenAddress, uint256 _amount)
burnToken(address _tokenAddress, uint256 _amount)
```

### Examples

```bash
cast call $VAULT "balanceOf(string)(uint256)" "rocketDepositPool" --rpc-url $RPC_URL
cast call $VAULT "balanceOfToken(string,address)(uint256)" "rocketDepositPool" $RPL --rpc-url $RPC_URL
```

## L2 Token Addresses

rETH and RPL are bridged to multiple L2s. These are standard ERC-20 tokens on their respective chains — use `balanceOf`, `transfer`, `approve` with the appropriate L2 RPC. See `references/addresses.json` under `tokens` for all addresses.
