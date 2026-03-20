---
name: rocketpool-rewards
description: Interact with Rocket Pool rewards contracts — query reward cycles, claim RPL and ETH rewards via Merkle proofs, check smoothing pool balance, manage treasury payment contracts, and query reward settings. Supports cast (Foundry CLI) and Ethereum MCP tools on mainnet and Hoodi testnet.
---

# Rocket Pool — Rewards

## Quick Start

### Check Current Reward Index
```bash
cast call 0xCba5951fc706Fc783b7C142DaE8576Ebe29c41FD "getRewardIndex()(uint256)" --rpc-url https://ethereum-rpc.publicnode.com
```

### Check Pending RPL Rewards
```bash
cast call 0xCba5951fc706Fc783b7C142DaE8576Ebe29c41FD "getPendingRPLRewards()(uint256)" --rpc-url https://ethereum-rpc.publicnode.com
```

### Check Smoothing Pool Balance
```bash
cast balance 0xd4E96eF8eee8678dBFf4d535E033Ed1a4F7605b7 --rpc-url https://ethereum-rpc.publicnode.com
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
- All ETH values are in wei (18 decimals); all percentages are 18-decimal fixed point (1e18 = 100%)
- Merkle proofs are generated off-chain by the oDAO and published to IPFS

## rocketRewardsPool

Manages the periodic RPL and ETH rewards distribution to node operators, the oDAO, and the protocol DAO.

### Functions

Reward cycle info:
```
getRewardIndex() → uint256 [view]
getClaimIntervalTime() → uint256 [view]
getClaimIntervalTimeStart() → uint256 [view]
getClaimIntervalsPassed() → uint256 [view]
```

Pending rewards:
```
getPendingRPLRewards() → uint256 [view]
getPendingETHRewards() → uint256 [view]
getPendingVoterShare() → uint256 [view]
getRPLBalance() → uint256 [view]
getEthBalance() → uint256 [view]
```

Claiming percentages:
```
getClaimingContractPerc(string _claimingContract) → uint256 [view]
getClaimingContractsPerc(string[] _claimingContracts) → uint256[] [view]
```

Oracle DAO submission:
```
submitRewardSnapshot(tuple _submission)
executeRewardSnapshot(tuple _submission)
getTrustedNodeSubmitted(address _trustedNodeAddress, uint256 _rewardIndex) → bool [view]
```

### Examples

```bash
cast call $REWARDS_POOL "getRewardIndex()(uint256)" --rpc-url $RPC_URL
cast call $REWARDS_POOL "getPendingRPLRewards()(uint256)" --rpc-url $RPC_URL
cast call $REWARDS_POOL "getPendingETHRewards()(uint256)" --rpc-url $RPC_URL
cast call $REWARDS_POOL "getClaimIntervalTime()(uint256)" --rpc-url $RPC_URL
```

## rocketMerkleDistributorMainnet

Distributes rewards to node operators via Merkle proofs. Each reward interval generates a Merkle tree.

### Functions

```
claim(address _nodeAddress, tuple[] _claims)
claimAndStake(address _nodeAddress, tuple[] _claims, uint256 _stakeAmount)
isClaimed(uint256 _rewardIndex, address _claimer) → bool [view]
claimOutstandingEth()
getOutstandingEth(address _address) → uint256 [view]
```

The `_claims` tuple: `(uint256 rewardIndex, uint256 amountRPL, uint256 amountETH, bytes32[] merkleProof)`.

`claimAndStake` claims rewards and immediately stakes the RPL portion in a single transaction.

### Examples

```bash
cast call $MERKLE_DIST "isClaimed(uint256,address)(bool)" 42 $NODE_ADDR --rpc-url $RPC_URL
```

### Gotchas

- Multiple reward intervals can be claimed in a single transaction
- `claimAndStake` is gas-efficient for operators who want to restake RPL rewards

## rocketSmoothingPool

Collects MEV and priority fees from opted-in node operators for fair distribution.

### Functions

```
withdrawEther(address _to, uint256 _amount)
version() → uint8 [view]
```

The smoothing pool receives ETH directly from validators' fee recipients. Distribution is handled by the Merkle distributor.

### Examples

```bash
cast balance $SMOOTHING_POOL --rpc-url $RPC_URL
```

## rocketClaimDAO

Manages the protocol DAO treasury. Handles recurring payment contracts and one-time spends.

### Functions

```
spend(string _invoiceID, address _recipientAddress, uint256 _amount)
newContract(string _contractName, address _recipientAddress, uint256 _amountPerPeriod, uint256 _periodLength, uint256 _startTime, uint256 _numPeriods)
updateContract(string _contractName, address _recipientAddress, uint256 _amountPerPeriod, uint256 _periodLength, uint256 _numPeriods)
payOutContracts(string[] _contractNames)
payOutContractsAndWithdraw(string[] _contractNames)
getBalance(address _recipientAddress) → uint256 [view]
getContract(string _contractName) → tuple [view]
getContractExists(string _contractName) → bool [view]
withdrawBalance(address _recipientAddress)
```

## rocketDAOProtocolSettingsRewards

Key reward parameters:

```
getRewardsClaimIntervalTime() → uint256 [view]
getRewardsClaimIntervalPeriods() → uint256 [view]
getRewardsClaimersPerc() → (uint256, uint256, uint256) [view]
getRewardsClaimersNodePerc() → uint256 [view]
getRewardsClaimersTrustedNodePerc() → uint256 [view]
getRewardsClaimersProtocolPerc() → uint256 [view]
```
