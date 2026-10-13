
# Shared packages (@metamask/perps-controller)

Companion to `parity.md`. Tracks what's shared, what should be, and what can't be.

## Already Shared via @metamask/perps-controller

**Utils** (`src/utils/`) and **Services** (`src/services/`) of `@metamask/perps-controller`: check them on core `main` before adding a client-side copy.

## Priority 1 -- Move to Controller (pure TS, no React deps)

| Utility | Mobile Path | What It Does |
|---|---|---|
| `pnlCalculations.ts` | `UI/Perps/utils/` | P&L math, ROE |
| `positionCalculations.ts` | `UI/Perps/utils/` | Liquidation price, position value |
| `marginUtils.ts` | `UI/Perps/utils/` | Risk assessment, margin math |
| `orderUtils.ts` | `UI/Perps/utils/` | Order price resolution, trigger validation |
| `marketHours.ts` | `UI/Perps/utils/` | Market hours logic |
| `orderBookGrouping.ts` | `UI/Perps/utils/` | Order book aggregation |
| `tpslValidation.ts` | `UI/Perps/utils/` | TP/SL validation |
| `amountConversion.ts` | `UI/Perps/utils/` | USD <-> size conversions |

Once in controller, extension imports directly instead of reimplementing.

## Priority 2 -- Exact Duplicates to Consolidate

| Function | Mobile | Extension | Identical? |
|---|---|---|---|
| `getDisplayName`/`getDisplaySymbol` | controller `marketUtils.ts` | `ui/components/app/perps/utils.ts` | YES |
| `getPositionDirection` | `UI/Perps/utils/` | `ui/components/app/perps/utils.ts` | YES |
| `formatOrderType`/`formatStatus` | `UI/Perps/utils/` | `ui/components/app/perps/utils.ts` | YES |
| `filterMarketsByQuery` | `UI/Perps/utils/filterAndSortMarkets.ts` | `ui/components/app/perps/utils.ts` | YES |
| `isHip3Market`/`isCryptoMarket` | `UI/Perps/utils/` | `ui/components/app/perps/utils.ts` | YES |
| `groupTransactionsByDate` | `UI/Perps/utils/transactionTransforms.ts` | `ui/components/app/perps/utils/transactionTransforms.ts` | Near-identical |

## Can't Share (platform-bound)

| File | Reason |
|---|---|
| `formatUtils.ts` | i18n dependency (only pure logic extractable) |
| `translatePerpsError.ts` | i18n strings |
| `buttonColors.ts` | React Native color system |
| Color utilities | Platform-specific color enums |
| `tokenIconUtils.ts` | Mobile-specific image handling |

## Sync Mechanism

The controller lives in Core (`packages/perps-controller`) and both clients consume the published `@metamask/perps-controller`; there is no in-repo copy or sync script any more.

**Steps for each Priority 1 item:**
1. Move the utility from `app/components/UI/Perps/utils/X.ts` into `core/packages/perps-controller/src/utils/X.ts` and export it
2. Publish the controller package
3. Bump `@metamask/perps-controller` in mobile and extension and import from the package
4. Delete both clients' duplicates
