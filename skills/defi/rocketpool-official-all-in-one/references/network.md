# Network

## rocketStorage

Central registry for all protocol contract addresses and key-value storage. All contracts resolve addresses through this.

### Key Functions

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

### Cast Examples

Resolve a contract address by key (keccak256 of "contract.address" + contract name):
```bash
cast call $STORAGE "getAddress(bytes32)(address)" $(cast keccak "contract.addressrocketDepositPool") --rpc-url $RPC_URL
```

Get node withdrawal address:
```bash
cast call $STORAGE "getNodeWithdrawalAddress(address)(address)" $NODE_ADDR --rpc-url $RPC_URL
```

### Gotchas

- Contract addresses in `addresses.json` are current but can change via governance upgrades
- To resolve dynamically: `rocketStorage.getAddress(keccak256(abi.encodePacked("contract.address", contractName)))`
- The key format is the keccak256 of the concatenated string, not of separate arguments

---

## rocketNetworkBalances

Stores total ETH balance, staking ETH, and rETH supply as reported by the oracle DAO.

### Key Functions

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

### Cast Examples

```bash
cast call $NET_BALANCES "getTotalETHBalance()(uint256)" --rpc-url $RPC_URL
cast call $NET_BALANCES "getStakingETHBalance()(uint256)" --rpc-url $RPC_URL
cast call $NET_BALANCES "getTotalRETHSupply()(uint256)" --rpc-url $RPC_URL
cast call $NET_BALANCES "getETHUtilizationRate()(uint256)" --rpc-url $RPC_URL
```

---

## rocketNetworkPrices

Stores the RPL/ETH price as reported by the oracle DAO.

### Key Functions

```
getRPLPrice() → uint256 [view]
getPricesBlock() → uint256 [view]
submitPrices(uint256 _block, uint256 _slotTimestamp, uint256 _rplPrice)
executeUpdatePrices(uint256 _block, uint256 _slotTimestamp, uint256 _rplPrice)
```

### Cast Examples

```bash
cast call $NET_PRICES "getRPLPrice()(uint256)" --rpc-url $RPC_URL
```

RPL price is in ETH terms with 18 decimals (e.g., 0.01e18 means 1 RPL = 0.01 ETH).

---

## rocketNetworkFees

Dynamic commission fee based on deposit pool supply/demand.

### Key Functions

```
getNodeFee() → uint256 [view]
getNodeDemand() → int256 [view]
getNodeFeeByDemand(int256 _nodeDemand) → uint256 [view]
```

### Cast Examples

```bash
cast call $NET_FEES "getNodeFee()(uint256)" --rpc-url $RPC_URL
```

Fee is 18-decimal (e.g., 0.14e18 = 14% commission).

---

## rocketNetworkPenalties

Tracks and applies penalties to minipools for MEV theft or other infractions.

```
submitPenalty(address _minipool, uint256 _block)
executeUpdatePenalty(address _minipool, uint256 _block)
getPenaltyCount(address _minipool) → uint256 [view]
getCurrentMaxPenalty() → uint256 [view]
getCurrentPenaltyRunningTotal() → uint256 [view]
```

---

## rocketNetworkSnapshots

On-chain snapshot storage for governance voting power at specific blocks.

```
push(bytes32 _key, uint224 _value)
lookup(bytes32 _key, uint32 _block) → uint224 [view]
lookupRecent(bytes32 _key, uint32 _block, uint256 _recency) → uint224 [view]
latest(bytes32 _key) → (bool, uint32, uint224) [view]
latestBlock(bytes32 _key) → uint32 [view]
latestValue(bytes32 _key) → uint224 [view]
length(bytes32 _key) → uint256 [view]
```

---

## rocketNetworkVoting

Delegation and voting power for protocol governance.

```
setDelegate(address _newDelegate)
getCurrentDelegate(address _nodeAddress) → address [view]
getDelegate(address _nodeAddress, uint32 _block) → address [view]
getVotingPower(address _nodeAddress, uint32 _block) → uint256 [view]
getNodeCount(uint32 _block) → uint256 [view]
```

### Cast Examples

```bash
cast call $NET_VOTING "getVotingPower(address,uint32)(uint256)" $NODE_ADDR $BLOCK --rpc-url $RPC_URL
cast call $NET_VOTING "getCurrentDelegate(address)(address)" $NODE_ADDR --rpc-url $RPC_URL
```

---

## rocketNetworkRevenues (Saturn)

Revenue splitting between node operators, voters, protocol DAO, and rETH holders.
No ABI file is bundled for this contract in this skill. Use raw signatures with `cast call`.

```
getCurrentNodeShare() → uint256 [view]
getCurrentVoterShare() → uint256 [view]
getCurrentProtocolDAOShare() → uint256 [view]
calculateSplit(uint64 _sinceTime) → (nodeShare, voterShare, protocolDAOShare, rethShare) [view]
getNodeCapitalRatio(address _nodeAddress) → uint256 [view]
```

## DAO Protocol Settings (Network)

Key protocol parameters queryable from `rocketDAOProtocolSettingsNetwork`:

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
