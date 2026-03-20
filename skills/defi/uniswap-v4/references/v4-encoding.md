# Uniswap V4 Universal Router Encoding Reference

## Universal Router Command Encoding

The UniversalRouter uses `execute(bytes commands, bytes[] inputs, uint256 deadline)`.

### Command Bytes
Each byte in `commands` is a command type. The corresponding `inputs[i]` holds ABI-encoded params.

### V4 Swap Command (0x10 = V4_SWAP)
Command byte: `0x10`

Input encoding:
```
abi.encode(
  bytes actions,    // V4 action sequence
  bytes[] params    // One per action
)
```

### V4 Action Bytes (from official Actions.sol)
Source: `@uniswap/v4-periphery/src/libraries/Actions.sol`

| Action               | Byte | Description                         | Params Encoding |
|----------------------|------|-------------------------------------|-----------------|
| SWAP_EXACT_IN_SINGLE | 0x06 | Single-hop exact input swap         | (PoolKey, bool, uint128, uint128, bytes) |
| SWAP_EXACT_IN        | 0x07 | Multi-hop exact input swap          | (ExactInputParams) |
| SWAP_EXACT_OUT_SINGLE| 0x08 | Single-hop exact output swap        | (PoolKey, bool, uint128, uint128, bytes) |
| SWAP_EXACT_OUT       | 0x09 | Multi-hop exact output swap         | (ExactOutputParams) |
| DONATE               | 0x0a | Donate to a pool                    | (PoolKey, uint256, uint256, bytes) |
| SETTLE               | 0x0b | Settle exact amount                 | (Currency, uint256, bool payerIsUser) |
| SETTLE_ALL           | 0x0c | Settle all owed                     | (Currency, uint256 maxAmount) |
| SETTLE_PAIR          | 0x0d | Settle pair                         | (Currency, Currency) |
| TAKE                 | 0x0e | Take exact amount                   | (Currency, address, uint256) |
| TAKE_ALL             | 0x0f | Take all earned                     | (Currency, uint256 minAmount) |
| TAKE_PORTION         | 0x10 | Take a portion                      | (Currency, address, uint256) |
| TAKE_PAIR            | 0x11 | Take pair                           | (Currency, Currency, address) |
| CLOSE_CURRENCY       | 0x12 | Close currency                      | (Currency) |
| CLEAR_OR_TAKE        | 0x13 | Clear or take                       | (Currency, uint256) |
| SWEEP                | 0x14 | Sweep                               | (Currency, address) |
| WRAP                 | 0x15 | Wrap ETH → WETH                     | (uint256) |
| UNWRAP               | 0x16 | Unwrap WETH → ETH                   | (uint256) |

> ⚠️ **SETTLE = 0x0b ≠ SETTLE_ALL = 0x0c.** Previous version of this doc had them swapped.
> SETTLE requires a `bool payerIsUser` param; SETTLE_ALL does not.

### Recommended Action Sequence for ExactInputSingle

**`0x06 0x0c 0x0f`** = SWAP_EXACT_IN_SINGLE + SETTLE_ALL + TAKE_ALL

### SWAP_EXACT_IN_SINGLE Params (0x06)
```solidity
struct ExactInputSingleParams {
    PoolKey poolKey;        // (currency0, currency1, fee, tickSpacing, hooks)
    bool zeroForOne;        // true = swap currency0→currency1
    uint128 amountIn;       // exact input amount
    uint128 amountOutMinimum; // slippage protection
    bytes hookData;         // arbitrary data for hooks (usually 0x)
}
```

ABI encoding: `abi.encode((address,address,uint24,int24,address), bool, uint128, uint128, bytes)`

### PoolKey Struct
```solidity
struct PoolKey {
    Currency currency0;  // address — lower address first
    Currency currency1;  // address — higher address first
    uint24 fee;
    int24 tickSpacing;
    IHooks hooks;        // address(0) for vanilla pools
}
```

**Currency ordering:** `currency0 < currency1` (sorted by numeric address value). ETH = `address(0)`.

### SETTLE_ALL Params (0x0c)
```
abi.encode(Currency currency, uint256 maxAmount)
```
Settles the full debt to the PoolManager. `maxAmount` is a safety cap.

### SETTLE Params (0x0b) — Different from SETTLE_ALL!
```
abi.encode(Currency currency, uint256 amount, bool payerIsUser)
```
Settles an exact amount. `payerIsUser=true` means tokens come from the user via Permit2.

### TAKE_ALL Params (0x0f)
```
abi.encode(Currency currency, uint256 minAmount)
```
Takes all earned tokens. `minAmount` provides slippage protection.

## Permit2 Flow
V4 swaps through the Universal Router require Permit2 token approvals:
1. `token.approve(PERMIT2, type(uint256).max)` — standard ERC20 approve
2. `Permit2.approve(token, UNIVERSAL_ROUTER, type(uint160).max, type(uint48).max)` — Permit2 allowance

### Allowance Check
```
Permit2.allowance(user, token, spender) → (uint160 amount, uint48 expiration, uint48 nonce)
```

## Pool State Reading

### Via StateView (recommended)
```
StateView.getSlot0(poolId) → (uint160 sqrtPriceX96, int24 tick, uint24 protocolFee, uint24 lpFee)
StateView.getLiquidity(poolId) → uint128 liquidity
```

### Via extsload (advanced)
```
PoolManager.extsload(slot) → bytes32
```
Where `slot = keccak256(abi.encode(poolId, 6))` for Slot0.
Liquidity slot = base slot + 3.

### Pool ID Calculation
```
poolId = keccak256(abi.encode(currency0, currency1, fee, tickSpacing, hooks))
```

## Gas Estimates (Base)
- Simple swap: ~300K-350K gas
- Multi-hop swap: ~500K-600K gas
- Permit2 approval: ~50K-100K gas

## V4Quoter (Quoter V2)
```
V4Quoter.quoteExactInputSingle(QuoteExactSingleParams) → (uint256 amountOut, uint256 gasEstimate)
```
Where `QuoteExactSingleParams = (PoolKey poolKey, bool zeroForOne, uint128 exactAmount, bytes hookData)`

The quoter simulates the swap via `eth_call` (no gas, no tx). Use the result to compute `amountOutMinimum` with slippage.
