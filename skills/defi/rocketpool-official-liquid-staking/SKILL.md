---
name: rocketpool-liquid-staking
description: Interact with Rocket Pool liquid staking contracts — deposit ETH to mint rETH, burn rETH for ETH, check exchange rates, query deposit pool balances, and perform rETH ERC-20 operations. Supports cast (Foundry CLI) and Ethereum MCP tools on mainnet and Hoodi testnet.
---

# Rocket Pool — Liquid Staking

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
- Contracts are upgradeable via governance; addresses in `addresses.json` reflect current deployments but can change
- All ETH values are in wei (18 decimals); all percentages are 18-decimal fixed point (1e18 = 100%)
- rETH is non-rebasing: balance stays constant, value increases via exchange rate

## rocketDepositPool

Receives ETH deposits from users and routes them to node operators.

### Functions

```
deposit() [payable]
```
Deposit ETH to mint rETH at the current exchange rate.

```
getBalance() → uint256 [view]
getExcessBalance() → uint256 [view]
getUserBalance() → int256 [view]
getNodeBalance() → uint256 [view]
getMaximumDepositAmount() → uint256 [view]
```

Queue inspection:
```
getTotalQueueLength() → uint256 [view]
getStandardQueueLength() → uint256 [view]
getExpressQueueLength() → uint256 [view]
getMinipoolQueueLength() → uint256 [view]
```

Node operator functions:
```
nodeDeposit(uint256 _bondAmount) [payable]
requestFunds(uint256 _bondAmount, uint32 _validatorId, uint256 _amount, bool _expressQueue)
exitQueue(address _nodeAddress, uint32 _validatorId, bool _expressQueue)
getNodeCreditBalance(address _nodeAddress) → uint256 [view]
withdrawCredit(uint256 _amount)
reduceBond(address _nodeAddress, uint256 _amount)
assignDeposits(uint256 _max)
```

### Examples

```bash
cast call $DEPOSIT_POOL "getBalance()(uint256)" --rpc-url $RPC_URL
cast call $DEPOSIT_POOL "getMaximumDepositAmount()(uint256)" --rpc-url $RPC_URL
cast send $DEPOSIT_POOL "deposit()" --value 1ether --rpc-url $RPC_URL --private-key $PK
```

## rocketTokenRETH

The rETH liquid staking token. Value accrues via an increasing exchange rate against ETH. Implements ERC-20.

### Functions

Exchange rate:
```
getExchangeRate() → uint256 [view]
getEthValue(uint256 _rethAmount) → uint256 [view]
getRethValue(uint256 _ethAmount) → uint256 [view]
getCollateralRate() → uint256 [view]
getTotalCollateral() → uint256 [view]
```

Burn:
```
burn(uint256 _rethAmount)
```
Burns rETH and returns ETH at the current exchange rate. Reverts if insufficient collateral.

ERC-20:
```
balanceOf(address account) → uint256 [view]
transfer(address recipient, uint256 amount) → bool
transferFrom(address sender, address recipient, uint256 amount) → bool
approve(address spender, uint256 amount) → bool
allowance(address owner, address spender) → uint256 [view]
totalSupply() → uint256 [view]
name() → string [view]
symbol() → string [view]
decimals() → uint8 [view]
```

### Examples

```bash
cast call $RETH "getExchangeRate()(uint256)" --rpc-url $RPC_URL
cast call $RETH "getRethValue(uint256)(uint256)" 1000000000000000000 --rpc-url $RPC_URL
cast call $RETH "getEthValue(uint256)(uint256)" 1000000000000000000 --rpc-url $RPC_URL
cast call $RETH "balanceOf(address)(uint256)" $WALLET --rpc-url $RPC_URL
cast send $RETH "burn(uint256)" $RETH_AMOUNT --rpc-url $RPC_URL --private-key $PK
```

### Gotchas

- `deposit()` is on rocketDepositPool, not rocketTokenRETH
- `burn()` reverts if insufficient ETH collateral — check `getTotalCollateral()` first
- Exchange rate only increases; 18-decimal fixed point (1e18 = 1:1)
- There is a deposit delay (`rethDepositDelay` setting) before newly minted rETH can be transferred
