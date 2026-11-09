# Order types with GmxApiSdk

Use string `kind` / `orderType` values in `prepareOrder()`. The API builds the contract enum and calldata. This reference targets `@gmx-io/sdk@2.2.1`; see [request types](https://github.com/gmx-io/gmx-interface/blob/release/sdk/src/utils/orderTransactions/api.ts) and [official examples](https://docs.gmx.io/docs/sdk/v2/examples/).

## Request mapping and triggers

| Intent | `kind` | `orderType` | Long trigger | Short trigger |
|--------|--------|-------------|--------------|---------------|
| Open/add now | `increase` | `market` | Current oracle execution | Current oracle execution |
| Limit entry | `increase` | `limit` | Price <= trigger | Price >= trigger |
| Breakout entry | `increase` | `stop-market` | Price >= trigger | Price <= trigger |
| Close/reduce now | `decrease` | `market` | Current oracle execution | Current oracle execution |
| Take profit | `decrease` | `take-profit` | Price >= trigger | Price <= trigger |
| Stop loss | `decrease` | `stop-loss` | Price <= trigger | Price >= trigger |
| Swap now | `swap` | `market` | Output minimum must be met | Not directional |
| Scheduled parts | `increase` or `decrease` | `twap` | Per-part schedule/constraints | Per-part schedule/constraints |

Only market swaps work through the API today: `limit` and `twap` swaps pass request validation but fail preparation with `NO_SWAP_PATH`. `Liquidation` is not a user-creatable API order.

For reference, the contract `OrderType` enum is `MarketSwap=0`, `LimitSwap=1`, `MarketIncrease=2`, `LimitIncrease=3`, `MarketDecrease=4`, `LimitDecrease=5`, `StopLossDecrease=6`, `Liquidation=7`, `StopIncrease=8`. A take-profit is a `LimitDecrease` on-chain.

## Units

| Field | Unit |
|-------|------|
| Increase/decrease `size`, `tpsl[].size`, edit `newSize` | USD, 30 decimals |
| Position `triggerPrice` / edit `newTriggerPrice` | USD price, 30 decimals |
| `collateralToPay.amount` (also the swap input) | Input token decimals |
| Collateral operation `amount` | Position collateral token decimals |
| `slippage`, `executionFeeBufferBps` | Numeric basis points, 10,000 = 100% |
| `twapConfig.duration` | Seconds |

Use `parseUnits()` and bigint arithmetic. `triggerPrice` and `acceptablePrice` on `fetchOrders()` results are contract prices (`price30 / 10**indexTokenDecimals`), not USD30; swap orders store a raw ratio. Convert a kept perpetual order price with `parseContractPrice(price, indexTokenDecimals)` from `@gmx-io/sdk/utils/tokens` before passing it back to the API. See [editing](sdk-reference.md#edit-cancel-or-change-collateral).

## TP/SL at entry

`prepareOrder()` accepts up to 10 `tpsl` entries with an increase of type `market`, `limit` or `stop-market`. Prices and sizes below illustrate a user-selected strategy, not recommended levels. Reuse the resolved market/token and account from [SDK reference](sdk-reference.md).

```typescript
const withProtection = await sdk.prepareOrder({
  kind: "increase",
  symbol: market.symbol,
  direction: "long",
  orderType: "limit",
  size: parseUnits("500", 30),
  triggerPrice: parseUnits("3000", 30),
  collateralToken: usdc.symbol,
  collateralToPay: { amount: parseUnits("100", usdc.decimals), token: usdc.symbol },
  tpsl: [
    { type: "take-profit", triggerPrice: parseUnits("3300", 30), size: parseUnits("250", 30) },
    { type: "stop-loss", triggerPrice: parseUnits("2850", 30) },
  ],
  mode: "express",
  from: account,
});
```

Omitting a TP/SL `size` uses the increase `size`, not the resulting position, so a TP/SL added to an existing position covers only the added size. Attached TP/SL orders get no acceptable price (0 for longs, `maxUint256` for shorts); the trigger is their only price guard. Review the resulting batch. Existing pending TP/SL orders also matter; an additional batch can overlap their size. Use `fetchPositionsInfo({ address, includeRelatedOrders: true })` and `fetchOrders()` to inspect them.

Auto-cancellation is an order property, not a promise for every conditional order. Check the returned `autoCancel` and current contract constraints rather than hardcoding per-chain maximums. TP/SL creation does not prove that an entry filled or that every attached trigger will later execute.

## Swaps

```typescript
const swap = await sdk.prepareOrder({
  kind: "swap",
  orderType: "market",
  collateralToPay: { amount: parseUnits("25", usdc.decimals), token: usdc.symbol },
  receiveToken: "ETH",
  slippage: 30,
  mode: "express",
  from: account,
});
```

The input amount comes from `collateralToPay.amount`; swaps need no `symbol` or `size`. Resolve the receive token on the chosen chain first. Inspect the prepared route, fees and minimum output. `manualSwapPath`, when supplied, contains market addresses, not token addresses. Native and wrapped tokens have different funding/receipt behavior. Existing swap orders cannot be edited.

## TWAP

TWAP creation is available through the API SDK; it is no longer frontend-only. `twapConfig` requires a positive duration and a safe-integer `parts` between 2 and 30. It cannot be combined with `tpsl`.

```typescript
const twap = await sdk.prepareOrder({
  kind: "increase",
  symbol: market.symbol,
  direction: "long",
  orderType: "twap",
  size: parseUnits("1000", 30),
  collateralToken: usdc.symbol,
  collateralToPay: { amount: parseUnits("200", usdc.decimals), token: usdc.symbol },
  twapConfig: { duration: 600, parts: 2 },
  mode: "express",
  from: account,
});
```

The size/input is the total to split, not the per-part amount. Check per-part minimums and aggregate fees. For a near-full decrease, inspect the effective `estimates.sizeDeltaUsd` before division. Track every returned order key through execution or cancellation; a single part's receipt is not completion of the TWAP. To change a TWAP, cancel its parts instead of editing them: an edit resets `validFromTime`, so the edited part becomes executable immediately.

## Execution outcomes

Market orders still require keeper execution after creation. A price trigger becoming true does not guarantee a fill: oracle updates, available liquidity, acceptable price, execution fees and position validity can prevent it. Conditional orders can remain pending/frozen when execution constraints fail; market requests may be cancelled. Inspect status and cancellation/error data rather than promising a fixed execution time or guaranteed stop price.

Use the bounded polling flow in [SDK reference](sdk-reference.md). For limit/stop placement, `created` is the expected initial success state. Do not retry placement simply because it has not reached `executed`.
