---
name: rocketpool-network
description: Interact with Rocket Pool network infrastructure contracts — RocketStorage address registry, network balances, RPL price oracle, node fees, penalties, governance snapshots, voting delegation, revenue splitting, and network settings. Supports cast (Foundry CLI) and Ethereum MCP tools on mainnet and Hoodi testnet.
---

# Rocket Pool — Network

## Quick Start

### Resolve Contract Address via RocketStorage
```bash
cast call 0x1d8f8f00cfa6758d7bE78336684788Fb0ee0Fa46 "getAddress(bytes32)(address)" $(cast keccak "contract.addressrocketDepositPool") --rpc-url https://ethereum-rpc.publicnode.com
```

### Check Total ETH Balance
```bash
cast call 0x1D9F14C6Bfd8358b589964baD8665AdD248E9473 "getTotalETHBalance()(uint256)" --rpc-url https://ethereum-rpc.publicnode.com
```

### Check RPL Price
```bash
cast call 0x25E54Bf48369b8FB25bB79d3a3Ff7F3BA448E382 "getRPLPrice()(uint256)" --rpc-url https://ethereum-rpc.publicnode.com
```

## Workflow

1. Look up the contract address from `references/addresses.json`
2. Find the function signature below
3. Load the ABI from `assets/abis/<contractName>.json` when available (some Saturn-era contracts in this skill are signature-only)
4. Execute via `cast call` (read) or `cast send` (write)

## Network Configuration

| Network | Chain ID | RPC | rocketStorage |
|---|---|---|---|
| Mainnet | 1 | `https://ethereum-rpc.publicnode.com` | `0x1d8f8f00cfa6758d7bE78336684788Fb0ee0Fa46` |
| Hoodi | 560048 | `https://rpc.hoodi.ethpandaops.io` | `0x594Fb75D3dc2DFa0150Ad03F99F97817747dd4E1` |

## Architecture

- **RocketStorage** is the central registry — all contracts resolve each other's addresses through it
- To resolve dynamically: `rocketStorage.getAddress(keccak256(abi.encodePacked("contract.address", contractName)))`
- The key format is the keccak256 of the concatenated string, not of separate arguments
- All ETH values are in wei (18 decimals); all percentages are 18-decimal fixed point (1e18 = 100%)

## rocketStorage

Central registry for all protocol contract addresses and key-value storage.

### Functions

Address resolution:
```
getAddress(bytes32 _key) → address [view]
getBool(bytes32 _key) → bool [view]
getUint(bytes32 _key) → uint256 [view]
getInt(bytes32 _key) → int256 [view]
getString(bytes32 _key) → string [view]
getBytes(bytes32 _key) → bytes [view]
getBytes32(bytes32 _key) → bytes32 [view]
```

Withdrawal address management:
```
getNodeWithdrawalAddress(address _nodeAddress) → address [view]
getNodePendingWithdrawalAddress(address _nodeAddress) → address [view]
setWithdrawalAddress(address _nodeAddress, address _newWithdrawalAddress, bool _confirm)
confirmWithdrawalAddress(address _nodeAddress)
```

Guardian:
```
getGuardian() → address [view]
setGuardian(address _newAddress)
confirmGuardian()
getDeployedStatus() → bool [view]
```

### Examples

```bash
cast call $STORAGE "getAddress(bytes32)(address)" $(cast keccak "contract.addressrocketDepositPool") --rpc-url $RPC_URL
cast call $STORAGE "getNodeWithdrawalAddress(address)(address)" $NODE_ADDR --rpc-url $RPC_URL
```

## rocketNetworkBalances

Total ETH balance, staking ETH, and rETH supply as reported by the oracle DAO.

### Functions

```
getTotalETHBalance() → uint256 [view]
getStakingETHBalance() → uint256 [view]
getTotalRETHSupply() → uint256 [view]
getETHUtilizationRate() → uint256 [view]
getBalancesBlock() → uint256 [view]
getBalancesTimestamp() → uint256 [view]
```

Oracle DAO submission:
```
submitBalances(uint256 _block, uint256 _slotTimestamp, uint256 _totalEth, uint256 _stakingEth, uint256 _rethSupply)
executeUpdateBalances(uint256 _block, uint256 _slotTimestamp, uint256 _totalEth, uint256 _stakingEth, uint256 _rethSupply)
```

### Examples

```bash
cast call $NET_BALANCES "getTotalETHBalance()(uint256)" --rpc-url $RPC_URL
cast call $NET_BALANCES "getStakingETHBalance()(uint256)" --rpc-url $RPC_URL
cast call $NET_BALANCES "getTotalRETHSupply()(uint256)" --rpc-url $RPC_URL
cast call $NET_BALANCES "getETHUtilizationRate()(uint256)" --rpc-url $RPC_URL
```

## rocketNetworkPrices

RPL/ETH price as reported by the oracle DAO.

### Functions

```
getRPLPrice() → uint256 [view]
getPricesBlock() → uint256 [view]
submitPrices(uint256 _block, uint256 _slotTimestamp, uint256 _rplPrice)
executeUpdatePrices(uint256 _block, uint256 _slotTimestamp, uint256 _rplPrice)
```

RPL price is in ETH terms with 18 decimals (e.g., 0.01e18 means 1 RPL = 0.01 ETH).

### Examples

```bash
cast call $NET_PRICES "getRPLPrice()(uint256)" --rpc-url $RPC_URL
```

## rocketNetworkFees

Dynamic commission fee based on deposit pool supply/demand.

### Functions

```
getNodeFee() → uint256 [view]
getNodeDemand() → int256 [view]
getNodeFeeByDemand(int256 _nodeDemand) → uint256 [view]
```

Fee is 18-decimal (e.g., 0.14e18 = 14% commission).

### Examples

```bash
cast call $NET_FEES "getNodeFee()(uint256)" --rpc-url $RPC_URL
```

## rocketNetworkPenalties

Tracks and applies penalties to minipools for MEV theft or other infractions.

### Functions

```
submitPenalty(address _minipool, uint256 _block)
executeUpdatePenalty(address _minipool, uint256 _block)
getPenaltyCount(address _minipool) → uint256 [view]
getCurrentMaxPenalty() → uint256 [view]
getCurrentPenaltyRunningTotal() → uint256 [view]
```

## rocketNetworkSnapshots

On-chain snapshot storage for governance voting power at specific blocks.

### Functions

```
push(bytes32 _key, uint224 _value)
lookup(bytes32 _key, uint32 _block) → uint224 [view]
lookupRecent(bytes32 _key, uint32 _block, uint256 _recency) → uint224 [view]
latest(bytes32 _key) → (bool, uint32, uint224) [view]
latestBlock(bytes32 _key) → uint32 [view]
latestValue(bytes32 _key) → uint224 [view]
length(bytes32 _key) → uint256 [view]
```

## rocketNetworkVoting

Delegation and voting power for protocol governance.

### Functions

```
setDelegate(address _newDelegate)
getCurrentDelegate(address _nodeAddress) → address [view]
getDelegate(address _nodeAddress, uint32 _block) → address [view]
getVotingPower(address _nodeAddress, uint32 _block) → uint256 [view]
getNodeCount(uint32 _block) → uint256 [view]
```

### Examples

```bash
cast call $NET_VOTING "getVotingPower(address,uint32)(uint256)" $NODE_ADDR $BLOCK --rpc-url $RPC_URL
cast call $NET_VOTING "getCurrentDelegate(address)(address)" $NODE_ADDR --rpc-url $RPC_URL
```

## rocketNetworkRevenues (Saturn)

Revenue splitting between node operators, voters, protocol DAO, and rETH holders.
No ABI file is bundled for this contract in this skill. Use the raw signatures below with `cast call`.

### Functions

```
getCurrentNodeShare() → uint256 [view]
getCurrentVoterShare() → uint256 [view]
getCurrentProtocolDAOShare() → uint256 [view]
calculateSplit(uint64 _sinceTime) → (nodeShare, voterShare, protocolDAOShare, rethShare) [view]
getNodeCapitalRatio(address _nodeAddress) → uint256 [view]
```

## rocketDAOProtocolSettingsNetwork

Key protocol parameters:

```
getNodeConsensusThreshold() → uint256 [view]
getSubmitBalancesEnabled() → bool [view]
getSubmitBalancesFrequency() → uint256 [view]
getSubmitPricesEnabled() → bool [view]
getSubmitPricesFrequency() → uint256 [view]
getMinimumNodeFee() → uint256 [view]
getMaximumNodeFee() → uint256 [view]
getTargetNodeFee() → uint256 [view]
getNodeFeeDemandRange() → uint256 [view]
getRethDepositDelay() → uint256 [view]
getNodeShare() → uint256 [view]
getVoterShare() → uint256 [view]
getProtocolDAOShare() → uint256 [view]
```

## rocketNetworkSnapshotsTime

Timestamp-based snapshot lookup.
No ABI file is bundled for this contract in this skill.
