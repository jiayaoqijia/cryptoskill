# Liquid Staking

## rocketDepositPool

Receives ETH deposits from users and routes them to node operators. The deposit pool holds ETH until it can be assigned to minipools/megapools.

### Key Functions

```
deposit() [payable]
```
Deposit ETH to mint rETH. Sent ETH is converted at the current exchange rate.

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

### Cast Examples

Query deposit pool balance:
```bash
cast call $DEPOSIT_POOL "getBalance()(uint256)" --rpc-url $RPC_URL
```

Deposit ETH to mint rETH:
```bash
cast send $DEPOSIT_POOL "deposit()" --value 1ether --rpc-url $RPC_URL --private-key $PK
```

Check max deposit:
```bash
cast call $DEPOSIT_POOL "getMaximumDepositAmount()(uint256)" --rpc-url $RPC_URL
```

---

## rocketTokenRETH

The rETH liquid staking token. Value accrues via an increasing exchange rate against ETH. Implements ERC-20.

### Key Functions

Exchange rate queries:
```
getExchangeRate() → uint256 [view]
getEthValue(uint256 _rethAmount) → uint256 [view]
getRethValue(uint256 _ethAmount) → uint256 [view]
getCollateralRate() → uint256 [view]
getTotalCollateral() → uint256 [view]
```

Mint/burn:
```
burn(uint256 _rethAmount)
```
Burns rETH and returns ETH at the current exchange rate. Only works when sufficient collateral exists in the deposit pool.

ERC-20 standard:
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

### Cast Examples

Query rETH exchange rate (returns 18-decimal fixed point, e.g., 1.05e18 means 1 rETH = 1.05 ETH):
```bash
cast call $RETH "getExchangeRate()(uint256)" --rpc-url $RPC_URL
```

Convert ETH amount to rETH equivalent:
```bash
cast call $RETH "getRethValue(uint256)(uint256)" 1000000000000000000 --rpc-url $RPC_URL
```

Convert rETH amount to ETH equivalent:
```bash
cast call $RETH "getEthValue(uint256)(uint256)" 1000000000000000000 --rpc-url $RPC_URL
```

Check rETH balance:
```bash
cast call $RETH "balanceOf(address)(uint256)" $WALLET --rpc-url $RPC_URL
```

Burn rETH to receive ETH:
```bash
cast send $RETH "burn(uint256)" $RETH_AMOUNT --rpc-url $RPC_URL --private-key $PK
```

### Gotchas

- `deposit()` on rocketDepositPool mints rETH, not a function on rocketTokenRETH itself
- `burn()` reverts if insufficient ETH collateral in deposit pool — check `getTotalCollateral()` first
- Exchange rate only increases; 18-decimal fixed point (1e18 = 1:1)
- rETH is non-rebasing: balance stays constant, value increases
- There is a deposit delay (`rethDepositDelay` setting) before newly minted rETH can be transferred
