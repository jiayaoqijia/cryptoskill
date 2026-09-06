# Order Types

Detailed reference for all GMX V2 order types, trigger conditions, and execution behavior.

## OrderType Enum

```typescript
enum OrderType {
  MarketSwap = 0,       // Swap at current oracle price
  LimitSwap = 1,        // Swap when min output amount is achievable
  MarketIncrease = 2,   // Open/increase position at market price
  LimitIncrease = 3,    // Open/increase position when trigger price reached
  MarketDecrease = 4,   // Close/decrease position at market price
  LimitDecrease = 5,    // Close/decrease position when trigger price reached (take-profit)
  StopLossDecrease = 6, // Close/decrease position to limit losses
  Liquidation = 7,      // System-triggered forced closure
  StopIncrease = 8,     // Open position when price moves past trigger (breakout)
}
```

## Market Orders (0, 2, 4)

Execute immediately at the current oracle price.

- **MarketSwap (0):** Swap tokens at oracle price. Cancelled if `minOutputAmount` not met.
- **MarketIncrease (2):** Open or add to a position at market price. Cancelled if `acceptablePrice` not met.
- **MarketDecrease (4):** Close or reduce a position at market price. Cancelled if `acceptablePrice` not met.

Execution happens within 1–5 seconds after the keeper picks up the order with fresh oracle prices.

## Limit Orders (1, 3, 5)

Execute when the oracle price reaches a specified trigger price.

### LimitSwap (1)
Swap executes when the oracle price allows `minOutputAmount` to be achieved.

### LimitIncrease (3)
Open a position at a better price than current market.

**Trigger conditions:**
| Direction | Trigger |
|-----------|---------|
| Long | Oracle price **<=** trigger price (buy the dip) |
| Short | Oracle price **>=** trigger price (sell the rally) |

### LimitDecrease (5) — Take-Profit
Close a position when price moves in your favor.

**Trigger conditions:**
| Direction | Trigger |
|-----------|---------|
| Long Take-Profit | Oracle price **>=** trigger price |
| Short Take-Profit | Oracle price **<=** trigger price |

## Stop Orders (6, 8)

### StopLossDecrease (6)
Automatically close a position to limit losses when price moves against you.

**Trigger conditions:**
| Direction | Trigger |
|-----------|---------|
| Long Stop-Loss | Oracle price **<=** trigger price |
| Short Stop-Loss | Oracle price **>=** trigger price |

### StopIncrease (8)
Open a position when price breaks past a level (breakout entry / momentum trade).

**Trigger conditions:**
| Direction | Trigger |
|-----------|---------|
| Long Stop-Increase | Oracle price **>=** trigger price |
| Short Stop-Increase | Oracle price **<=** trigger price |

## Liquidation (7)

System-triggered when a position's collateral falls below the maintenance margin. Not user-creatable. The keeper automatically liquidates positions that breach the threshold.

## Auto-Cancel Orders

Stop-loss and take-profit orders attached to a position are **auto-cancelled** when the position is fully closed.

**Maximum concurrent auto-cancel orders per position:**
| Chain | Limit |
|-------|-------|
| Arbitrum | 11 |
| Avalanche | 6 |
| Botanix | 6 |

Use `sdk.positions.getMaxAutoCancelOrders()` to check the current limit and remaining capacity.

## Sidecar Orders (SL/TP)

Sidecar orders allow attaching stop-loss and take-profit orders to a position increase in a single transaction.

### Creating with Increase Order

The `createIncreaseOrder()` method accepts:
- `createSltpEntries` — New SL/TP orders to create alongside the position
- `cancelSltpEntries` — Existing SL/TP orders to cancel
- `updateSltpEntries` — Existing SL/TP orders to modify

```typescript
type SidecarSlTpOrderEntryValid = {
  id: string;
  price: { input: string; value: bigint | null; error: string | null };
  sizeUsd: { input: string; value: bigint | null; error: string | null };
  percentage: { input: string; value: bigint | null; error: string | null };
  txnType: OrderTxnType | null;
  mode: "keepSize" | "keepPercentage" | "fitPercentage";
  order: PositionOrderInfo | null;
  decreaseAmounts: DecreasePositionAmounts;
};
```

### Typical Usage Pattern

When opening a position with SL/TP:
1. Calculate decrease amounts for the SL and TP levels
2. Pass entries via `createSltpEntries` in `createIncreaseOrder()`
3. The SDK multicalls the increase order + SL/TP orders in one transaction

## TWAP Orders

Time-Weighted Average Price orders split a large trade into smaller parts executed over a duration.

**Configuration:**
- **Number of parts:** 2–30 (default varies)
- **Duration:** Configurable hours and minutes
- **Activation:** Parts activate at staggered intervals (`duration / numberOfParts`)

### Utility Functions

Available from `@gmx-io/sdk/utils/twap`:

```typescript
// Validate TWAP parameters
getIsValidTwapParams(duration: TwapDuration, numberOfParts: number): boolean

// Calculate total duration in seconds
getTwapDurationInSeconds(duration: TwapDuration): number

// Get activation time for a specific part
getTwapValidFromTime(duration: TwapDuration, numberOfParts: number, partIndex: number): bigint

// Create a reusable getter for part activation times
makeTwapValidFromTimeGetter(duration: TwapDuration, numberOfParts: number): (part: number) => bigint
```

**Note:** Full TWAP order creation is only available via the GMX frontend UI. The SDK exports utility functions but does not provide a `createTwapOrder()` method.

## Execution Risks

- **Price skipping:** Volatile markets may skip past trigger prices. A stop-loss at $3000 may execute at $2950 if the oracle price jumps from $3010 to $2950 between updates.
- **Insufficient liquidity:** Orders may fail if the pool lacks sufficient liquidity for the trade size.
- **Execution delay:** Orders are not instant. The keeper must pick up and execute the order, typically 1–5 seconds.
- **Acceptable price:** All orders include an `acceptablePrice` parameter. If the execution price is worse than acceptable, the order is cancelled rather than executed at a bad price.
