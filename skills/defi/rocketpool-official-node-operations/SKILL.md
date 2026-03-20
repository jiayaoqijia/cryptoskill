---
name: rocketpool-node-operations
description: Interact with Rocket Pool node operator contracts — register nodes, create validators, manage minipools and megapools, stake RPL, handle bond reduction, distribute rewards, and manage withdrawal addresses. Supports cast (Foundry CLI) and Ethereum MCP tools on mainnet and Hoodi testnet.
---

# Rocket Pool — Node Operations

## Quick Start

### Check Node Count
```bash
cast call 0xcf2d76A7499d3acB5A22ce83c027651e8d76e250 "getNodeCount()(uint256)" --rpc-url https://ethereum-rpc.publicnode.com
```

### Check If Address Is Registered Node
```bash
cast call 0xcf2d76A7499d3acB5A22ce83c027651e8d76e250 "getNodeExists(address)(bool)" $NODE_ADDR --rpc-url https://ethereum-rpc.publicnode.com
```

### Check Staked RPL
```bash
cast call 0xedFc7DCaE43fF954577a2875a9D805874490eE3E "getNodeStakedRPL(address)(uint256)" $NODE_ADDR --rpc-url https://ethereum-rpc.publicnode.com
```

## Workflow

1. Look up the contract address from `references/addresses.json`
2. Find the function signature below
3. Load the ABI from `assets/abis/<contractName>.json` when available (Megapool contracts in this skill are signature-only)
4. Execute via `cast call` (read) or `cast send` (write)

## Network Configuration

| Network | Chain ID | RPC | rocketStorage |
|---|---|---|---|
| Mainnet | 1 | `https://ethereum-rpc.publicnode.com` | `0x1d8f8f00cfa6758d7bE78336684788Fb0ee0Fa46` |
| Hoodi | 560048 | `https://rpc.hoodi.ethpandaops.io` | `0x594Fb75D3dc2DFa0150Ad03F99F97817747dd4E1` |

## Architecture

- **RocketStorage** is the central registry — all contracts resolve each other's addresses through it
- **Minipools** (legacy): one contract per validator, 8 or 16 ETH bond
- **Megapools** (Saturn/v1.4): one contract per node, multiple validators, variable bond
- Deploy megapool via `rocketNodeManager.deployMegapool()`, not the factory directly
- All ETH values are in wei (18 decimals); all percentages are 18-decimal fixed point (1e18 = 100%)

## rocketNodeManager

Node registration, withdrawal addresses, smoothing pool opt-in, megapool deployment, and express tickets.

### Functions

Registration:
```
registerNode(string _timezoneLocation)
getNodeExists(address _nodeAddress) → bool [view]
getNodeCount() → uint256 [view]
getNodeAt(uint256 _index) → address [view]
getNodeAddresses(uint256 _offset, uint256 _limit) → address[] [view]
getNodeRegistrationTime(address _nodeAddress) → uint256 [view]
getNodeTimezoneLocation(address _nodeAddress) → string [view]
```

Withdrawal addresses:
```
getNodeWithdrawalAddress(address _nodeAddress) → address [view]
getNodeRPLWithdrawalAddress(address _nodeAddress) → address [view]
getNodeRPLWithdrawalAddressIsSet(address _nodeAddress) → bool [view]
setRPLWithdrawalAddress(address _nodeAddress, address _newAddr, bool _confirm)
confirmRPLWithdrawalAddress(address _nodeAddress)
```
Primary withdrawal address is set on rocketStorage, not here.

Smoothing pool:
```
getSmoothingPoolRegistrationState(address _nodeAddress) → bool [view]
getSmoothingPoolRegistrationChanged(address _nodeAddress) → uint256 [view]
setSmoothingPoolRegistrationState(bool _state)
```

Megapool:
```
deployMegapool() → address
getMegapoolAddress(address _nodeAddress) → address [view]
```

Express tickets:
```
getExpressTicketCount(address _nodeAddress) → uint256 [view]
getExpressTicketsProvisioned(address _nodeAddress) → bool [view]
```

Fee distributor:
```
initialiseFeeDistributor()
getFeeDistributorInitialised(address _nodeAddress) → bool [view]
getAverageNodeFee(address _nodeAddress) → uint256 [view]
```

### Examples

```bash
cast call $NODE_MGR "getNodeCount()(uint256)" --rpc-url $RPC_URL
cast call $NODE_MGR "getNodeExists(address)(bool)" $NODE_ADDR --rpc-url $RPC_URL
cast call $NODE_MGR "getSmoothingPoolRegistrationState(address)(bool)" $NODE_ADDR --rpc-url $RPC_URL
cast call $NODE_MGR "getMegapoolAddress(address)(address)" $NODE_ADDR --rpc-url $RPC_URL
```

## rocketNodeDeposit

Handles ETH deposits from node operators to create validators.

### Functions

```
deposit(uint256 _bondAmount, bool _useExpressTicket, bytes _validatorPubkey, bytes _validatorSignature, bytes32 _depositDataRoot) [payable]
depositWithCredit(uint256 _bondAmount, bool _useExpressTicket, bytes _validatorPubkey, bytes _validatorSignature, bytes32 _depositDataRoot) [payable]
depositMulti(tuple[] _deposits) [payable]
depositEthFor(address _nodeAddress) [payable]
```

Credit queries:
```
getNodeDepositCredit(address _nodeAddress) → uint256 [view]
getNodeUsableCredit(address _nodeAddress) → uint256 [view]
getNodeEthBalance(address _nodeAddress) → uint256 [view]
getNodeCreditAndBalance(address _nodeAddress) → uint256 [view]
getBondRequirement(uint256 _numValidators) → uint256 [view]
withdrawEth(address _nodeAddress, uint256 _amount)
```

## rocketNodeStaking

RPL staking for node operators. Manages staked RPL, collateralization ratios, and locking.

### Functions

Staking:
```
stakeRPL(uint256 _amount)
stakeRPLFor(address _nodeAddress, uint256 _amount)
unstakeRPL(uint256 _amount)
unstakeRPLFor(address _nodeAddress, uint256 _amount)
withdrawRPL()
withdrawRPLFor(address _nodeAddress)
```

Legacy:
```
unstakeLegacyRPL(uint256 _amount)
unstakeLegacyRPLFor(address _nodeAddress, uint256 _amount)
```

Queries:
```
getNodeStakedRPL(address _nodeAddress) → uint256 [view]
getNodeLegacyStakedRPL(address _nodeAddress) → uint256 [view]
getNodeMegapoolStakedRPL(address _nodeAddress) → uint256 [view]
getNodeUnstakingRPL(address _nodeAddress) → uint256 [view]
getNodeLastUnstakeTime(address _nodeAddress) → uint256 [view]
getNodeETHBonded(address _nodeAddress) → uint256 [view]
getNodeETHBorrowed(address _nodeAddress) → uint256 [view]
getNodeETHCollateralisationRatio(address _nodeAddress) → uint256 [view]
getNodeMinipoolETHBonded(address _nodeAddress) → uint256 [view]
getNodeMinipoolETHBorrowed(address _nodeAddress) → uint256 [view]
getNodeMegapoolETHBonded(address _nodeAddress) → uint256 [view]
getNodeMegapoolETHBorrowed(address _nodeAddress) → uint256 [view]
getNodeMinimumLegacyRPLStake(address _nodeAddress) → uint256 [view]
getTotalStakedRPL() → uint256 [view]
getTotalLegacyStakedRPL() → uint256 [view]
getTotalMegapoolStakedRPL() → uint256 [view]
```

Locking (for governance proposals):
```
lockRPL(address _nodeAddress, uint256 _amount)
unlockRPL(address _nodeAddress, uint256 _amount)
getNodeLockedRPL(address _nodeAddress) → uint256 [view]
getRPLLockingAllowed(address _nodeAddress) → bool [view]
setRPLLockingAllowed(address _nodeAddress, bool _allowed)
```

### Examples

```bash
cast call $NODE_STAKING "getNodeStakedRPL(address)(uint256)" $NODE_ADDR --rpc-url $RPC_URL
cast call $NODE_STAKING "getNodeETHCollateralisationRatio(address)(uint256)" $NODE_ADDR --rpc-url $RPC_URL
cast call $NODE_STAKING "getTotalStakedRPL()(uint256)" --rpc-url $RPC_URL
```

## rocketMinipoolManager

Registry for all minipools (legacy 16 ETH and 8 ETH validators).

### Functions

```
getMinipoolCount() → uint256 [view]
getActiveMinipoolCount() → uint256 [view]
getStakingMinipoolCount() → uint256 [view]
getFinalisedMinipoolCount() → uint256 [view]
getMinipoolAt(uint256 _index) → address [view]
getMinipoolExists(address _minipoolAddress) → bool [view]
getMinipoolByPubkey(bytes _pubkey) → address [view]
getMinipoolPubkey(address _minipoolAddress) → bytes [view]
getNodeMinipoolCount(address _nodeAddress) → uint256 [view]
getNodeMinipoolAt(address _nodeAddress, uint256 _index) → address [view]
getNodeActiveMinipoolCount(address _nodeAddress) → uint256 [view]
getNodeStakingMinipoolCount(address _nodeAddress) → uint256 [view]
getNodeValidatingMinipoolCount(address _nodeAddress) → uint256 [view]
```

### Examples

```bash
cast call $MINIPOOL_MGR "getMinipoolCount()(uint256)" --rpc-url $RPC_URL
cast call $MINIPOOL_MGR "getNodeMinipoolCount(address)(uint256)" $NODE_ADDR --rpc-url $RPC_URL
```

## rocketMinipoolDelegate

Logic contract for individual minipool instances. Each minipool is a proxy that delegates to this.

### Functions

Status:
```
getStatus() → uint8 [view]
getStatusTime() → uint256 [view]
getNodeAddress() → address [view]
getNodeFee() → uint256 [view]
getFinalised() → bool [view]
getDepositType() → uint8 [view]
```

Balances:
```
getNodeDepositBalance() → uint256 [view]
getNodeRefundBalance() → uint256 [view]
getUserDepositBalance() → uint256 [view]
getUserDepositAssigned() → bool [view]
calculateNodeShare(uint256 _balance) → uint256 [view]
calculateUserShare(uint256 _balance) → uint256 [view]
```

Lifecycle:
```
stake(bytes _validatorSignature, bytes32 _depositDataRoot)
distributeBalance(bool _rewardsOnly)
finalise()
dissolve()
close()
refund()
```

Minipool statuses: 0=Initialised, 1=Prelaunch, 2=Staking, 3=Withdrawable, 4=Dissolved

## rocketMinipoolFactory

Creates minipool proxy contracts. Called internally by the deposit flow.

## rocketMinipoolBase

Base proxy contract for individual minipool instances. Delegates calls to rocketMinipoolDelegate.

## rocketMinipoolQueue

Manages the queue of minipools waiting for ETH assignment from the deposit pool.

## rocketMinipoolPenalty

Tracks penalty counts for individual minipools (MEV theft, missed duties).

## rocketNodeDistributorFactory

Creates fee distributor contracts for node operators.

## rocketNodeDistributorDelegate

Logic contract for node fee distributors. Handles ETH distribution between the node and the protocol.

## rocketMinipoolBondReducer

Allows node operators to reduce minipool bond from 16 ETH to 8 ETH (or 8 to 4 ETH with LEB4).

### Functions

```
beginReduceBondAmount(address _minipoolAddress, uint256 _newBondAmount)
canReduceBondAmount(address _minipoolAddress) → bool [view]
getReduceBondTime(address _minipoolAddress) → uint256 [view]
getReduceBondValue(address _minipoolAddress) → uint256 [view]
```

## Megapool Contracts (Saturn)

Megapools replace minipools as the new validator structure. A single megapool contract per node can manage multiple validators.
No ABI files are bundled for `rocketMegapoolFactory`, `rocketMegapoolDelegate`, `rocketMegapoolManager`, `rocketMegapoolPenalties`, or `rocketMegapoolProxy` in this skill. Use the raw signatures below with `cast`.

### rocketMegapoolFactory

```
deployContract(address _nodeAddress) → address
getExpectedAddress(address _nodeAddress) → address [view]
getMegapoolDeployed(address _nodeAddress) → bool [view]
```

### rocketMegapoolDelegate (per-megapool logic)

```
newValidator(uint256 _bondAmount, bool _useExpressTicket, bytes _validatorPubkey, bytes _validatorSignature, bytes32 _depositDataRoot)
stake(uint32 _validatorId)
distribute()
claim()
```

Queries:
```
getNodeAddress() → address [view]
getNodeBond() → uint256 [view]
getAssignedValue() → uint256 [view]
getUserCapital() → uint256 [view]
getValidatorCount() → uint32 [view]
getActiveValidatorCount() → uint32 [view]
getExitingValidatorCount() → uint32 [view]
getValidatorInfo(uint32 _validatorId) → ValidatorInfo [view]
getValidatorPubkey(uint32 _validatorId) → bytes [view]
getPendingRewards() → uint256 [view]
getDebt() → uint256 [view]
getRefundValue() → uint256 [view]
calculateRewards(uint256 _amount) → (nodeRewards, voterRewards, protocolDAORewards, rethRewards) [view]
getNewValidatorBondRequirement() → uint256 [view]
```

### rocketMegapoolManager (global megapool operations)

```
getValidatorCount() → uint256 [view]
getValidatorInfo(uint256 _index) → (bytes pubkey, ValidatorInfo, address megapool, uint32 validatorId) [view]
```

### rocketMegapoolPenalties

```
penalise(address _megapool, uint256 _block, uint256 _amount)
executePenalty(address _megapool, uint256 _block, uint256 _amount)
getCurrentMaxPenalty() → uint256 [view]
```

### rocketMegapoolProxy

Base proxy contract for megapool instances. Delegates calls to rocketMegapoolDelegate.

### Gotchas

- Deploy megapool via `rocketNodeManager.deployMegapool()`, not the factory directly
- Each node has exactly one megapool address, but can have multiple validators within it
- Bond reduction has a waiting period and can be cancelled by the oDAO
