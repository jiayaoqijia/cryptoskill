# Rewards

## rocketRewardsPool

Manages the periodic RPL and ETH rewards distribution to node operators, the oDAO, and the protocol DAO.

### Key Functions

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

### Cast Examples

```bash
cast call $REWARDS_POOL "getRewardIndex()(uint256)" --rpc-url $RPC_URL
cast call $REWARDS_POOL "getPendingRPLRewards()(uint256)" --rpc-url $RPC_URL
cast call $REWARDS_POOL "getPendingETHRewards()(uint256)" --rpc-url $RPC_URL
cast call $REWARDS_POOL "getClaimIntervalTime()(uint256)" --rpc-url $RPC_URL
```

---

## rocketMerkleDistributorMainnet

Distributes rewards to node operators via Merkle proofs. Each reward interval generates a Merkle tree; node operators claim their share by providing proofs.

### Key Functions

```
claim(address _nodeAddress, tuple[] _claims)
claimAndStake(address _nodeAddress, tuple[] _claims, uint256 _stakeAmount)
isClaimed(uint256 _rewardIndex, address _claimer) → bool [view]
claimOutstandingEth()
getOutstandingEth(address _address) → uint256 [view]
```

The `_claims` tuple array contains: `(uint256 rewardIndex, uint256 amountRPL, uint256 amountETH, bytes32[] merkleProof)`.

`claimAndStake` allows claiming rewards and immediately staking the RPL portion in a single transaction.

### Cast Examples

```bash
cast call $MERKLE_DIST "isClaimed(uint256,address)(bool)" 42 $NODE_ADDR --rpc-url $RPC_URL
```

### Gotchas

- Merkle proofs are generated off-chain by the oDAO and published to IPFS
- Multiple reward intervals can be claimed in a single transaction
- `claimAndStake` is gas-efficient for operators who want to restake RPL rewards

---

## rocketSmoothingPool

Collects MEV and priority fees from opted-in node operators for fair distribution. A simple contract that holds ETH.

### Key Functions

```
withdrawEther(address _to, uint256 _amount)
version() → uint8 [view]
```

The smoothing pool receives ETH directly from validators' fee recipients. Distribution is handled by the Merkle distributor using the reward tree.

### Cast Examples

Check smoothing pool balance:
```bash
cast balance $SMOOTHING_POOL --rpc-url $RPC_URL
```

---

## rocketClaimDAO

Manages the protocol DAO treasury. Handles recurring payment contracts and one-time spends.

### Key Functions

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

## Reward Settings

Key reward parameters from `rocketDAOProtocolSettingsRewards`:

```
getRewardsClaimIntervalTime() → uint256 [view]
getRewardsClaimIntervalPeriods() → uint256 [view]
getRewardsClaimersPerc() → (uint256, uint256, uint256) [view]
getRewardsClaimersNodePerc() → uint256 [view]
getRewardsClaimersTrustedNodePerc() → uint256 [view]
getRewardsClaimersProtocolPerc() → uint256 [view]
```
