# Liquidity Operations Reference

Contract function signatures, struct definitions, execution flows, and gas estimation formulas for GMX V2 liquidity operations. Sourced from `gmx-synthetics` Solidity contracts and `gmx-interface` frontend.

## Contract Structs

### CreateDepositParams (IDepositUtils.sol)

```solidity
struct CreateDepositParams {
    CreateDepositParamsAddresses addresses;
    uint256 minMarketTokens;           // Minimum GM tokens to receive (slippage protection)
    bool shouldUnwrapNativeToken;       // Unwrap native token on cancellation refund
    uint256 executionFee;               // Fee for keeper execution (in native token)
    uint256 callbackGasLimit;           // Gas limit for callback contract (0 if none)
    bytes32[] dataList;                 // Reserved (pass empty array)
}

struct CreateDepositParamsAddresses {
    address receiver;                   // Address to receive GM tokens
    address callbackContract;           // Callback on execution (zeroAddress if none)
    address uiFeeReceiver;             // UI fee recipient (zeroAddress if none)
    address market;                     // GM pool market token address
    address initialLongToken;           // Token to deposit as long side
    address initialShortToken;          // Token to deposit as short side
    address[] longTokenSwapPath;        // Swap path for long token (empty for direct)
    address[] shortTokenSwapPath;       // Swap path for short token (empty for direct)
}
```

### CreateWithdrawalParams (IWithdrawalUtils.sol)

```solidity
struct CreateWithdrawalParams {
    CreateWithdrawalParamsAddresses addresses;
    uint256 minLongTokenAmount;         // Minimum long tokens to receive
    uint256 minShortTokenAmount;        // Minimum short tokens to receive
    bool shouldUnwrapNativeToken;       // Unwrap WETH/WAVAX/PBTC to native on receive
    uint256 executionFee;
    uint256 callbackGasLimit;
    bytes32[] dataList;
}

struct CreateWithdrawalParamsAddresses {
    address receiver;
    address callbackContract;
    address uiFeeReceiver;
    address market;                     // GM pool market token address
    address[] longTokenSwapPath;        // Swap path for received long tokens
    address[] shortTokenSwapPath;       // Swap path for received short tokens
}
```

### CreateShiftParams (IShiftUtils.sol)

> Note: No `shouldUnwrapNativeToken` field — shifts only move GM tokens between pools.

```solidity
struct CreateShiftParams {
    CreateShiftParamsAddresses addresses;
    uint256 minMarketTokens;            // Minimum to-market GM tokens to receive
    uint256 executionFee;
    uint256 callbackGasLimit;
    bytes32[] dataList;
}

struct CreateShiftParamsAddresses {
    address receiver;
    address callbackContract;
    address uiFeeReceiver;
    address fromMarket;                 // Source GM pool market token address
    address toMarket;                   // Destination GM pool market token address
}
```

### CreateGlvDepositParams (IGlvDepositUtils.sol)

> Note: Uses `minGlvTokens` (not `minMarketTokens`).

```solidity
struct CreateGlvDepositParams {
    CreateGlvDepositParamsAddresses addresses;
    uint256 minGlvTokens;              // Minimum GLV tokens to receive
    uint256 executionFee;
    uint256 callbackGasLimit;
    bool shouldUnwrapNativeToken;
    bool isMarketTokenDeposit;          // true = depositing GM tokens, false = depositing raw tokens
    bytes32[] dataList;
}

struct CreateGlvDepositParamsAddresses {
    address glv;                        // GLV vault address
    address market;                     // Constituent GM market to deposit through
    address receiver;
    address callbackContract;
    address uiFeeReceiver;
    address initialLongToken;
    address initialShortToken;
    address[] longTokenSwapPath;
    address[] shortTokenSwapPath;
}
```

### CreateGlvWithdrawalParams (IGlvWithdrawalUtils.sol)

```solidity
struct CreateGlvWithdrawalParams {
    CreateGlvWithdrawalParamsAddresses addresses;
    uint256 minLongTokenAmount;
    uint256 minShortTokenAmount;
    bool shouldUnwrapNativeToken;
    uint256 executionFee;
    uint256 callbackGasLimit;
    bytes32[] dataList;
}

struct CreateGlvWithdrawalParamsAddresses {
    address receiver;
    address callbackContract;
    address uiFeeReceiver;
    address market;                     // Constituent GM market to withdraw from
    address glv;                        // GLV vault address
    address[] longTokenSwapPath;
    address[] shortTokenSwapPath;
}
```

## Execution Flows

### GM Deposit Flow

1. **Approve** long/short tokens to `SyntheticsRouter` (one-time per token)
2. **Multicall** on `ExchangeRouter`:
   - `sendWnt(DepositVault, executionFee + nativeDepositAmount)`
   - `sendTokens(longToken, DepositVault, longAmount)` — skip if native token
   - `sendTokens(shortToken, DepositVault, shortAmount)` — skip if native token
   - `createDeposit(params)` → returns `bytes32` request key
3. **Keeper executes** with oracle prices (1–30s)
4. **GM tokens minted** to `receiver`
5. **Excess execution fee refunded** to `receiver`

### GM Withdrawal Flow

1. **Approve** GM tokens to `SyntheticsRouter`
2. **Multicall** on `ExchangeRouter`:
   - `sendWnt(WithdrawalVault, executionFee)` — only execution fee
   - `sendTokens(marketToken, WithdrawalVault, gmTokenAmount)`
   - `createWithdrawal(params)` → returns request key
3. **Keeper executes** — GM tokens burned, underlying tokens sent to `receiver`

### Shift Flow

1. **Approve** from-market GM tokens to `SyntheticsRouter`
2. **Multicall** on `ExchangeRouter`:
   - `sendWnt(ShiftVault, executionFee)`
   - `sendTokens(fromMarketToken, ShiftVault, fromAmount)`
   - `createShift(params)` → returns request key
3. **Keeper executes** — from-market GM burned, to-market GM minted to `receiver`

### GLV Deposit Flow (raw tokens)

1. **Approve** long/short tokens to `SyntheticsRouter`
2. **Multicall** on `GlvRouter`:
   - `sendWnt(GlvVault, executionFee + nativeDepositAmount)`
   - `sendTokens(longToken, GlvVault, longAmount)`
   - `createGlvDeposit(params)` with `isMarketTokenDeposit: false`
3. **Keeper executes** — first deposits into constituent GM market, then deposits GM into GLV
4. **GLV tokens minted** to `receiver`

### GLV Deposit Flow (GM tokens)

1. **Approve** GM tokens to `SyntheticsRouter`
2. **Multicall** on `GlvRouter`:
   - `sendWnt(GlvVault, executionFee)`
   - `sendTokens(gmToken, GlvVault, gmAmount)`
   - `createGlvDeposit(params)` with `isMarketTokenDeposit: true`
3. **Keeper executes** — GM tokens deposited into GLV directly (faster, less gas)

### GLV Withdrawal Flow

1. **Approve** GLV tokens to `SyntheticsRouter`
2. **Multicall** on `GlvRouter`:
   - `sendWnt(GlvVault, executionFee)`
   - `sendTokens(glvToken, GlvVault, glvAmount)`
   - `createGlvWithdrawal(params)`
3. **Keeper executes** — GLV tokens burned, withdraws from constituent GM, underlying tokens sent to `receiver`

## Gas Estimation

### Gas Limit Formulas

Field names correspond to `GasLimitsConfig` from `sdk.utils.getGasLimits()`:

| Operation | Formula |
|-----------|---------|
| GM Deposit | `depositToken + swapsCount × singleSwap` |
| GM Withdrawal | `withdrawalMultiToken + swapsCount × singleSwap` |
| Shift | `shift` |
| GLV Deposit (raw) | `glvDepositGasLimit + marketsCount × glvPerMarketGasLimit + depositToken + swapsCount × singleSwap` |
| GLV Deposit (GM) | `glvDepositGasLimit + marketsCount × glvPerMarketGasLimit` |
| GLV Withdrawal | `glvWithdrawalGasLimit + marketsCount × glvPerMarketGasLimit + withdrawalMultiToken + swapsCount × singleSwap` |

**Important:** `marketsCount` for GLV operations must reflect the actual number of constituent GM markets in the vault. GLV [WETH-USDC] and [WBTC-USDC] on Arbitrum have 40+ constituent markets — use `marketsCount: 53`. The contract reverts with `InsufficientExecutionFee` (selector `0x5dac504d`) if the fee is too low. Excess fee is refunded by the keeper.

### Oracle Price Count Formulas

| Operation | Formula |
|-----------|---------|
| GM Deposit | `3 + swapsCount` |
| GM Withdrawal | `3 + swapsCount` |
| Shift | `4` |
| GLV Deposit | `2 + marketsCount + swapsCount` |
| GLV Withdrawal | `2 + marketsCount + swapsCount` |

### Execution Fee Calculation

```typescript
// 1. Get gas parameters from SDK
const gasLimits = await sdk.utils.getGasLimits();
const gasPrice = await sdk.utils.getGasPrice();

// 2. Calculate estimated gas limit (use formulas above)
const estimatedGasLimit = gasLimits.depositToken; // example: GM deposit, no swaps

// 3. Calculate oracle price count
const oraclePriceCount = 3n; // example: GM deposit, no swaps

// 4. adjustGasLimitForEstimate (mirrors contract GasUtils.sol)
let gasLimit = gasLimits.estimatedGasFeeBaseAmount;
gasLimit += gasLimits.estimatedGasFeePerOraclePrice * oraclePriceCount;
// applyFactor: multiply then divide by 10^30 (precision factor)
gasLimit += estimatedGasLimit * gasLimits.estimatedFeeMultiplierFactor / (10n ** 30n);

// 5. Calculate execution fee
const executionFee = gasLimit * gasPrice;
```

## Key Contract Addresses (Quick Reference)

Duplicated from [contract-addresses.md](../../gmx-trading/references/contract-addresses.md) for convenience. For the latest addresses, see [`sdk/src/configs/contracts.ts`](https://github.com/gmx-io/gmx-interface/blob/release/sdk/src/configs/contracts.ts) in gmx-interface.

### Arbitrum (42161)

| Contract | Address |
|----------|---------|
| ExchangeRouter | `0x1C3fa76e6E1088bCE750f23a5BFcffa1efEF6A41` |
| SyntheticsRouter | `0x7452c558d45f8afC8c83dAe62C3f8A5BE19c71f6` |
| DepositVault | `0xF89e77e8Dc11691C9e8757e84aaFbCD8A67d7A55` |
| WithdrawalVault | `0x0628D46b5D145f183AdB6Ef1f2c97eD1C4701C55` |
| ShiftVault | `0xfe99609C4AA83ff6816b64563Bdffd7fa68753Ab` |
| GlvRouter | `0x7EAdEE2ca1b4D06a0d82fDF03D715550c26AA12F` |
| GlvVault | `0x393053B58f9678C9c28c2cE941fF6cac49C3F8f9` |

### Avalanche (43114)

| Contract | Address |
|----------|---------|
| ExchangeRouter | `0x8f550E53DFe96C055D5Bdb267c21F268fCAF63B2` |
| SyntheticsRouter | `0x820F5FfC5b525cD4d88Cd91aCf2c28F16530Cc68` |
| DepositVault | `0x90c670825d0C62ede1c5ee9571d6d9a17A722DFF` |
| WithdrawalVault | `0xf5F30B10141E1F63FC11eD772931A8294a591996` |
| ShiftVault | `0x7fC46CCb386e9bbBFB49A2639002734C3Ec52b39` |
| GlvRouter | `0x7E425c47b2Ff0bE67228c842B9C792D0BCe58ae6` |
| GlvVault | `0x527FB0bCfF63C47761039bB386cFE181A92a4701` |

### Botanix (3637)

| Contract | Address |
|----------|---------|
| ExchangeRouter | `0xBCB5eA3a84886Ce45FBBf09eBF0e883071cB2Dc8` |
| SyntheticsRouter | `0x3d472afcd66F954Fe4909EEcDd5c940e9a99290c` |
| DepositVault | `0x4D12C3D3e750e051e87a2F3f7750fBd94767742c` |
| WithdrawalVault | `0x46BAeAEdbF90Ce46310173A04942e2B3B781Bf0e` |
| ShiftVault | `0xa7EE2737249e0099906cB079BCEe85f0bbd837d4` |
| GlvRouter | `0xC92741F0a0D20A95529873cBB3480b1f8c228d9F` |
| GlvVault | `0xd336087512BeF8Df32AF605b492f452Fd6436CD8` |

## Known GLV Vaults

| Chain | Name | GLV Token Address | Long Token | Short Token |
|-------|------|-------------------|-----------|-------------|
| Arbitrum | GLV [WETH-USDC] | `0x528A5bac7E746C9A509A1f4F6dF58A03d44279F9` | WETH `0x82aF49447D8a07e3bd95BD0d56f35241523fBab1` | USDC `0xaf88d065e77c8cC2239327C5EDb3A432268e5831` |
| Arbitrum | GLV [WBTC-USDC] | `0xdF03EEd325b82bC1d4Db8b49c30ecc9E05104b96` | WBTC `0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f` | USDC `0xaf88d065e77c8cC2239327C5EDb3A432268e5831` |
| Avalanche | GLV [WAVAX-USDC] | `0x901eE57f7118A7be56ac079cbCDa7F22663A3874` | WAVAX `0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7` | USDC `0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E` |
| Botanix | — | No vaults configured | — | — |

GM pool addresses are dynamic and should be discovered via `sdk.markets.getMarkets()`. GLV vault addresses can be found in [`sdk/src/configs/markets.ts`](https://github.com/gmx-io/gmx-interface/blob/release/sdk/src/configs/markets.ts).

## Source Files

- `gmx-synthetics/contracts/deposit/IDepositUtils.sol` — CreateDepositParams
- `gmx-synthetics/contracts/withdrawal/IWithdrawalUtils.sol` — CreateWithdrawalParams
- `gmx-synthetics/contracts/shift/IShiftUtils.sol` — CreateShiftParams
- `gmx-synthetics/contracts/glv/glvDeposit/IGlvDepositUtils.sol` — CreateGlvDepositParams
- `gmx-synthetics/contracts/glv/glvWithdrawal/IGlvWithdrawalUtils.sol` — CreateGlvWithdrawalParams
- `gmx-synthetics/contracts/router/IExchangeRouter.sol` — ExchangeRouter interface
- `gmx-synthetics/contracts/router/GlvRouter.sol` — GlvRouter implementation
- `gmx-synthetics/contracts/gas/GasUtils.sol` — Gas estimation logic
- `gmx-interface/sdk/src/utils/fees/executionFee.ts` — TypeScript gas estimation functions
