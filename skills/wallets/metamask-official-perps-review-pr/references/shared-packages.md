
# Shared packages (@metamask/perps-controller)

Companion to `parity.md`. Tracks what's shared, what should be, and what can't be.

## Already Shared via @metamask/perps-controller

**Utils** (`src/utils/`) and **Services** (`src/services/`) of `@metamask/perps-controller`: check them on core `main` before adding a client-side copy.

## Perps math that must come from the controller

Reference for the blocking rule *Perps Math Comes From the Controller* in `antipatterns.md`. These Mobile utilities hold perps trading math; until each one is exported by `@metamask/perps-controller` (TAT-4477), a client PR that adds, changes or ports the same math is blocking unless it moves the math into the controller or links the Core ticket that does.

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

The controller lives in Core (`packages/perps-controller`) and Mobile, Extension and Terminal consume the published `@metamask/perps-controller`; there is no in-repo copy or sync script any more.

**Steps for each utility in *Perps math that must come from the controller*:**
1. Move the utility from `app/components/UI/Perps/utils/X.ts` into `core/packages/perps-controller/src/utils/X.ts` and export it
2. Publish the controller package
3. Bump `@metamask/perps-controller` in Mobile, Extension and Terminal and import from the package
4. Delete the clients' duplicates
