# SDK Reference

Full API reference for `@gmx-io/sdk` v1.5.0-alpha-4.

> **Import note:** The SDK's ESM build has broken imports (missing file extensions). Use CommonJS: `const { GmxSdk } = require("@gmx-io/sdk")`.

## GmxSdkConfig

```typescript
interface GmxSdkConfig {
  chainId: number;              // 42161 | 43114 | 3637
  rpcUrl: string;               // Blockchain RPC endpoint
  oracleUrl: string;            // GMX Oracle API URL
  subsquidUrl: string;          // GMX Subsquid GraphQL URL
  account?: string;             // Wallet address (required for write ops)
  publicClient?: PublicClient;  // Custom viem PublicClient
  walletClient?: WalletClient;  // Custom viem WalletClient (required for write ops)
  tokens?: Record<string, Partial<Token>>;         // Token config overrides
  markets?: Record<string, Partial<MarketSdkConfig>>; // Market config overrides
  settings?: {
    uiFeeReceiverAccount?: string; // UI fee recipient
  };
}
```

## GmxSdk Class

```typescript
class GmxSdk {
  // Modules
  readonly markets: Markets;
  readonly tokens: Tokens;
  readonly positions: Positions;
  readonly orders: Orders;
  readonly trades: Trades;
  readonly accounts: Accounts;
  readonly utils: Utils;
  readonly oracle: Oracle;

  // Clients
  publicClient: PublicClient;
  walletClient: WalletClient;

  constructor(config: GmxSdkConfig);

  // Core methods
  setAccount(account: Address): void;
  get chainId(): number;
  get chain(): Chain;
  get account(): Address;

  // Low-level
  executeMulticall<T>(request: MulticallRequestConfig): Promise<T>;
  callContract(address: Address, abi: Abi, method: string, params: any[], opts?: CallContractOpts): Promise<any>;
}
```

## Markets Module

```typescript
class Markets {
  // Get all market configurations
  async getMarkets(offset?: bigint, limit?: bigint): Promise<{
    marketsData?: MarketsData;
    marketsAddresses?: string[];
    error?: Error;
  }>;

  // Get markets with full info (prices, pool sizes, utilization, fees)
  async getMarketsInfo(): Promise<{
    marketsInfoData?: MarketsInfoData;
    tokensData?: TokensData;
    pricesUpdatedAt?: number;
  }>;

  // Get 24h trading volume per market
  async getDailyVolumes(): Promise<Record<string, bigint> | undefined>;
}
```

`MarketsInfoData` is a `Record<string, MarketInfo>` keyed by market address. Each `MarketInfo` includes:
- `marketTokenAddress`, `indexTokenAddress`, `longTokenAddress`, `shortTokenAddress`
- `longPoolAmount`, `shortPoolAmount` — pool liquidity
- `longInterestUsd`, `shortInterestUsd` — open interest
- `positionFeeFactorForPositiveImpact`, `positionFeeFactorForNegativeImpact`
- `swapFeeFactorForPositiveImpact`, `swapFeeFactorForNegativeImpact`
- `borrowingFactorPerSecondForLongs`, `borrowingFactorPerSecondForShorts`
- `fundingFactorPerSecond`, `longsPayShorts`
- `maxLongPoolAmount`, `maxShortPoolAmount`, `maxOpenInterestForLongs`, `maxOpenInterestForShorts`

## Tokens Module

```typescript
class Tokens {
  // Token configuration (merged with overrides)
  get tokensConfig(): Record<string, Token>;

  // Get all token data with current prices
  async getTokensData(p?: { account?: string }): Promise<{
    tokensData?: TokensData;
    pricesUpdatedAt?: number;
  }>;

  // Get token balances for an account
  async getTokensBalances(p?: {
    account?: string;
    tokensList?: { address: string; isSynthetic?: boolean }[];
  }): Promise<{
    balancesData?: TokenBalancesData;
  }>;

  // Get the chain's native token config
  getNativeToken(): Token;
}
```

`TokensData` is a `Record<string, TokenData>` where each `TokenData` includes:
- `symbol`, `name`, `decimals`, `address`
- `prices: { minPrice: bigint, maxPrice: bigint }` — 30-decimal scaled
- `balance?: bigint` — if account was provided

## Positions Module

```typescript
class Positions {
  static MAX_PENDING_UPDATE_AGE = 600_000; // 10 minutes

  // Get raw position data
  async getPositions(p: {
    marketsInfoData: MarketsInfoData;
    tokensData: TokensData;
  }): Promise<{
    positionsData?: PositionsData;
    allPossiblePositionsKeys?: string[];
    error?: Error;
  }>;

  // Get enriched position info (PnL, leverage, liquidation price)
  async getPositionsInfo(p: {
    marketsInfoData: MarketsInfoData;
    tokensData: TokensData;
    showPnlInLeverage: boolean;
  }): Promise<PositionsInfoData>;

  // Get position size limits
  async getPositionsConstants(): Promise<{
    minCollateralUsd?: bigint;
    minPositionSizeUsd?: bigint;
    maxAutoCancelOrders?: bigint;
  }>;

  // Check auto-cancel order limits
  async getMaxAutoCancelOrders(p: {
    positionOrders: OrderInfo[];
  }): Promise<{
    autoCancelOrdersLimit: number;
    canAddAutoCancelOrder: boolean;
  }>;
}
```

`PositionsInfoData` is a `Record<string, PositionInfo>` where each includes:
- `marketAddress`, `collateralTokenAddress`, `isLong`
- `sizeInUsd`, `sizeInTokens`, `collateralUsd`, `collateralAmount`
- `leverage`, `pnl`, `pnlPercentage`, `netValue`
- `liquidationPrice`, `markPrice`, `entryPrice`
- `pendingFundingFeesUsd`, `pendingBorrowingFeesUsd`

## Orders Module

```typescript
class Orders {
  // High-level convenience methods (recommended)
  async long(params: PositionIncreaseParams): Promise<any>;
  async short(params: PositionIncreaseParams): Promise<any>;
  async swap(params: SwapParams): Promise<any>;

  // Get pending orders
  async getOrders(p: {
    account?: string;
    marketsInfoData: MarketsInfoData;
    tokensData: TokensData;
    orderTypesFilter?: OrderType[];
    marketsDirectionsFilter?: MarketFilterLongShortItemData[];
  }): Promise<{
    count: number;
    ordersInfoData: OrdersInfoData;
  }>;

  // Cancel orders by key
  async cancelOrders(orderKeys: string[]): Promise<any>;

  // Low-level order creation
  async createIncreaseOrder(p: CreateIncreaseOrderParams): Promise<any>;
  async createDecreaseOrder(p: CreateDecreaseOrderParams): Promise<any>;
  async createSwapOrder(p: CreateSwapOrderParams): Promise<any>;
  async createWrapOrUnwrapOrder(p: WrapOrUnwrapParams): Promise<any>;
}
```

### PositionIncreaseParams

```typescript
type PositionIncreaseParams = (
  | { payAmount: bigint }      // Size from collateral amount
  | { sizeAmount: bigint }     // Size from position size
) & {
  marketAddress: string;
  payTokenAddress: string;
  collateralTokenAddress: string;
  allowedSlippageBps?: number;        // Default: 100 (1%)
  referralCodeForTxn?: string;
  leverage?: bigint;                  // Basis points: 50000n = 5x
  limitPrice?: bigint;                // If set, creates limit order (30 decimals)
  acceptablePriceImpactBuffer?: number;
  fixedAcceptablePriceImpactBps?: bigint;
  skipSimulation?: boolean;           // Set true (simulation deprecated)
};
```

### SwapParams

```typescript
type SwapParams = (
  | { fromAmount: bigint }     // Exact input amount
  | { toAmount: bigint }       // Desired output amount
) & {
  fromTokenAddress: string;
  toTokenAddress: string;
  allowedSlippageBps?: number;        // Default: 100 (1%)
  referralCodeForTxn?: string;
  triggerPrice?: bigint;              // If set, creates limit swap (30 decimals)
};
```

## Trades Module

```typescript
class Trades {
  async getTradeHistory(p: {
    forAllAccounts?: boolean;
    pageSize: number;
    pageIndex: number;
    fromTxTimestamp?: number;
    toTxTimestamp?: number;
    marketsInfoData?: MarketsInfoData;
    tokensData?: TokensData;
    marketsDirectionsFilter?: MarketFilterLongShortItemData[];
    orderEventCombinations?: {
      eventName?: TradeActionType;
      orderType?: OrderType;
      isDepositOrWithdraw?: boolean;
    }[];
  }): Promise<TradeAction[]>;
}
```

`TradeAction` includes: `id`, `eventName`, `orderType`, `marketAddress`, `sizeDeltaUsd`, `collateralDeltaAmount`, `triggerPrice`, `executionPrice`, `transaction.timestamp`, `transaction.hash`.

## Utils Module

```typescript
class Utils {
  // Get gas limit configs for order types
  async getGasLimits(): Promise<GasLimitsConfig>;

  // Get current gas price
  async getGasPrice(): Promise<bigint>;

  // Estimate execution fee for an order
  async getExecutionFee(
    type: "increase" | "decrease" | "swap",
    tokensData: TokensData,
    params?: {
      increaseAmounts?: IncreasePositionAmounts;
      decreaseAmounts?: DecreasePositionAmounts;
      swapAmounts?: SwapAmounts;
    }
  ): Promise<{ feeTokenAmount?: bigint; feeUsd?: bigint } | undefined>;

  // Get UI fee factor from DataStore
  async getUiFeeFactor(): Promise<bigint>;
}
```

## Oracle Module

```typescript
class Oracle {
  // Get market configs from oracle API
  getMarkets(): Promise<MarketSdkConfig[]>;

  // Get token list from oracle API
  getTokens(): Promise<{ symbol: string; address: string; decimals: number; isSynthetic: boolean }[]>;

  // Get current price tickers
  getTickers(): Promise<{
    minPrice: string;
    maxPrice: string;
    oracleDecimals: number;
    tokenSymbol: string;
    tokenAddress: string;
    updatedAt: number;
  }[]>;
}
```

## GmxApiSdk (Lightweight Client)

A lightweight HTTP-based alternative to `GmxSdk`. No RPC connection needed — uses the OpenAPI backend.

```typescript
const { GmxApiSdk } = require("@gmx-io/sdk/v2");

class GmxApiSdk {
  constructor(config: { chainId: number });

  // Returns array-like of MarketInfo objects (numeric keys, not { marketsInfoData })
  // Access: result[0].marketTokenAddress, result[0].indexTokenAddress, etc.
  fetchMarketsInfo(): Promise<MarketInfo[]>;
  fetchTokensData(): Promise<TokensDataResult>;
  fetchPositionsInfo(p: { account: string; includeRelatedOrders?: boolean }): Promise<PositionsInfoResult>;
  fetchOrders(p: { account: string }): Promise<OrdersResult>;
}
```

## BATCH_CONFIGS

Per-chain multicall batching configuration:

```typescript
// Production (Arbitrum, Avalanche, Botanix)
{
  http: { batchSize: 0, wait: 0 },          // No HTTP batching
  client: {
    multicall: { batchSize: 1024 * 1024, wait: 0 } // 1MB multicall batches
  }
}
```

## Key Types

```typescript
type MarketsInfoData = Record<string, MarketInfo>;
type TokensData = Record<string, TokenData>;
type PositionsData = Record<string, Position>;
type PositionsInfoData = Record<string, PositionInfo>;
type OrdersInfoData = Record<string, OrderInfo>;

enum OrderType {
  MarketSwap = 0,
  LimitSwap = 1,
  MarketIncrease = 2,
  LimitIncrease = 3,
  MarketDecrease = 4,
  LimitDecrease = 5,
  StopLossDecrease = 6,
  Liquidation = 7,
  StopIncrease = 8,
}
```
