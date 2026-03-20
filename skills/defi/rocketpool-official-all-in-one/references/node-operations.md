# Node Operations

## rocketNodeManager

Node registration, withdrawal addresses, smoothing pool opt-in, megapool deployment, and express tickets.

### Key Functions

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

### Cast Examples

```bash
cast call $NODE_MGR "getNodeCount()(uint256)" --rpc-url $RPC_URL
cast call $NODE_MGR "getNodeExists(address)(bool)" $NODE_ADDR --rpc-url $RPC_URL
cast call $NODE_MGR "getSmoothingPoolRegistrationState(address)(bool)" $NODE_ADDR --rpc-url $RPC_URL
cast call $NODE_MGR "getMegapoolAddress(address)(address)" $NODE_ADDR --rpc-url $RPC_URL
```

---

## rocketNodeDeposit

Handles ETH deposits from node operators to create validators.

### Key Functions

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

---

## rocketNodeStaking

RPL staking for node operators. Manages staked RPL, collateralization ratios, and locking.

### Key Functions

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

### Cast Examples

```bash
cast call $NODE_STAKING "getNodeStakedRPL(address)(uint256)" $NODE_ADDR --rpc-url $RPC_URL
cast call $NODE_STAKING "getNodeETHCollateralisationRatio(address)(uint256)" $NODE_ADDR --rpc-url $RPC_URL
cast call $NODE_STAKING "getTotalStakedRPL()(uint256)" --rpc-url $RPC_URL
```

---

## rocketMinipoolManager

Registry for all minipools (legacy 16 ETH and 8 ETH validators).

### Key Functions

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

### Cast Examples

```bash
cast call $MINIPOOL_MGR "getMinipoolCount()(uint256)" --rpc-url $RPC_URL
cast call $MINIPOOL_MGR "getNodeMinipoolCount(address)(uint256)" $NODE_ADDR --rpc-url $RPC_URL
```

---

## rocketMinipoolDelegate

Logic contract for individual minipool instances. Each minipool is a proxy that delegates to this.

### Key Functions

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

---

## rocketMinipoolBondReducer

Allows node operators to reduce minipool bond from 16 ETH to 8 ETH (or 8 to 4 ETH with LEB4).

```
beginReduceBondAmount(address _minipoolAddress, uint256 _newBondAmount)
canReduceBondAmount(address _minipoolAddress) → bool [view]
getReduceBondTime(address _minipoolAddress) → uint256 [view]
getReduceBondValue(address _minipoolAddress) → uint256 [view]
```

---

## Megapool Contracts (Saturn upgrade)

Megapools replace minipools as the new validator structure. A single megapool contract per node can manage multiple validators.
No ABI files are bundled for `rocketMegapoolFactory`, `rocketMegapoolDelegate`, `rocketMegapoolManager`, or `rocketMegapoolPenalties` in this skill. Use raw signatures with `cast`.

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

### Gotchas

- Megapools are Saturn (v1.4+) — testnet-first, live on mainnet
- Deploy megapool via `rocketNodeManager.deployMegapool()`, not the factory directly
- Each node has exactly one megapool address, but can have multiple validators within it
- Minipool statuses: 0=Initialised, 1=Prelaunch, 2=Staking, 3=Withdrawable, 4=Dissolved
- Bond reduction has a waiting period and can be cancelled by the oDAO
