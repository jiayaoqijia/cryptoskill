# Tokens

## rocketTokenRPL

The RPL governance and staking token. Has built-in inflation mechanism. Implements ERC-20 with burn.

### Key Functions

ERC-20:
```
balanceOf(address account) → uint256 [view]
transfer(address recipient, uint256 amount) → bool
transferFrom(address sender, address recipient, uint256 amount) → bool
approve(address spender, uint256 amount) → bool
allowance(address owner, address spender) → uint256 [view]
totalSupply() → uint256 [view]
decimals() → uint8 [view]  (18)
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

### Cast Examples

```bash
cast call $RPL "balanceOf(address)(uint256)" $WALLET --rpc-url $RPC_URL
cast call $RPL "totalSupply()(uint256)" --rpc-url $RPC_URL
cast call $RPL "inflationCalculate()(uint256)" --rpc-url $RPC_URL
```

---

## rocketTokenRPLFixedSupply

The original fixed-supply RPL token (pre-migration). Can be swapped 1:1 for new RPL via `rocketTokenRPL.swapTokens()`. Standard ERC-20 only.

---

## rocketVault

Central vault holding all protocol ETH and token balances. Internal accounting per contract name.

### Key Functions

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

### Cast Examples

```bash
cast call $VAULT "balanceOf(string)(uint256)" "rocketDepositPool" --rpc-url $RPC_URL
cast call $VAULT "balanceOfToken(string,address)(uint256)" "rocketDepositPool" $RPL --rpc-url $RPC_URL
```

## L2 Token Addresses

rETH and RPL are bridged to multiple L2s. See `addresses.json` under `tokens` for all addresses. These are standard ERC-20 tokens on their respective chains — use the standard `balanceOf`, `transfer`, `approve` interface with the appropriate L2 RPC.
