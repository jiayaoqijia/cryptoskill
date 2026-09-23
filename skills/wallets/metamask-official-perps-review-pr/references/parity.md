# Mobile / Extension parity

Mobile is the reference implementation for perps. Extension was built after mobile without rigorous
comparison. Use this map to check that a change on one platform has, or explicitly does not need, its
counterpart on the other. Check the extension for parity only; never copy its patterns into mobile.
When the reference checkout is not available the parity step reports "not checked" with the reason.


## Screen/Route Mapping

| Mobile Screen | Extension Equivalent | Extension Route | Status |
|---|---|---|---|
| PerpsHomeView | PerpsView (`ui/pages/perps/`) | `/perps` | Diverged name |
| PerpsMarketListView | market-list/index | `/perps/market-list` | Diverged name |
| PerpsMarketDetailsView | perps-market-detail-page | `/perps/market/:symbol` | Equivalent |
| PerpsOrderView | perps-order-entry-page | `/perps/trade/:symbol` | Diverged name |
| PerpsPositionsView | perps-positions-orders | inline in `/perps` | Inline, not page |
| PerpsClosePositionView | close-position-modal | modal | Modal equivalent |
| PerpsCloseAllPositionsView | close-all-positions-modal | modal | Modal equivalent |
| PerpsCancelAllOrdersView | cancel-all in perps-positions-orders | inline in `/perps` | Inline, not page |
| PerpsTPSLView | auto-close-section | inline | Modal equivalent |
| PerpsAdjustMarginView | edit-margin-modal | modal | Modal equivalent |
| PerpsTransactionsView | perps-activity-page | `/perps/activity` | Equivalent |
| PerpsWithdrawView | withdraw page | `/perps/withdraw` | Equivalent |
| PerpsOrderBookView | -- | -- | **MISSING** |
| PerpsOrderDetailsView | -- | -- | **MISSING** |

## Hook Mapping

Mobile: ~94 hooks. Extension: ~15. Extension consolidates heavily.

### Stream hooks (both channel-based)

Both: `usePerpsLivePositions`, `usePerpsLiveOrders`, `usePerpsLiveAccount`, `usePerpsLivePrices`, `usePerpsLiveCandles`, `usePerpsLiveOrderBook`, `usePerpsTopOfBook`, `usePerpsLiveFills`

Extension adds: `usePerpsLiveMarketData`, `usePerpsStreamManager`, `usePerpsViewActive`, `usePerpsChannel`

### Form/trade hooks (major consolidation on extension)

| Mobile | Extension |
|---|---|
| `usePerpsOrderForm` + `usePerpsOrderFees` + `usePerpsOrderValidation` + `usePerpsOrderExecution` | `usePerpsOrderForm` (single) |
| `usePerpsClosePosition` + `usePerpsClosePositionValidation` | Inline in `close-position-modal.tsx` |
| `usePerpsTPSLForm` + `usePerpsTPSLUpdate` | Inline in `auto-close-section.tsx` |
| `usePerpsMarginAdjustment` + `usePerpsAdjustMarginData` | `usePerpsMarginCalculations` |

### Missing on extension

`usePerpsNavigation`, `usePerpsRewards`, `usePerpsSearch`, `usePerpsSorting`, `usePerpsProvider`, `usePerpsWithdrawStatus`, `usePerpsCloseAllPositions`, `usePerpsCancelAllOrders`, `usePerpsOrderBookGrouping`, `usePerpsFirstTimeUser`

## Formatting Divergence

See `formatting-rules` knowledge file for full rules.

| Platform | Formatter | Behavior |
|---|---|---|
| Mobile | `formatPerpsFiat` | Adaptive sig-dig by price range |
| Extension | `formatCurrencyWithMinThreshold` | Generic, no sig-dig |
| Extension | `formatNumber({min:2,max:2})` | Always 2 decimals |
| Extension | `.toFixed(2)` | Hardcoded 2 decimals |

**Files with hardcoded formatting (extension):**
- `ui/components/app/perps/utils/transactionTransforms.ts` -- `.toFixed(2)` x7
- `ui/components/app/perps/order-entry/components/auto-close-section/` -- `{min:2, max:2}`
- `ui/components/app/perps/order-entry/components/limit-price-input/` -- `{min:2, max:2}`
- `ui/components/app/perps/edit-margin/edit-margin-modal-content.tsx` -- `.toFixed(2)`
- `ui/components/app/perps/reverse-position/reverse-position-modal.tsx` -- `.toFixed(2)`
- `ui/hooks/perps/usePerpsOrderForm.ts` -- `formatCurrencyWithMinThreshold` x6

## TestID Mapping

Convention: mobile = PascalCase selectors, extension = kebab-case strings.

| Concept | Mobile | Extension |
|---|---|---|
| Position card | `PerpsPositionCardSelectorsIDs.CARD` | `position-card-{symbol}` |
| Order card | -- | `order-card-{orderId}` |
| Balance | `PerpsMarketBalanceActionsSelectorsIDs.BALANCE_VALUE` | `perps-balance-dropdown-balance` |
| Order submit | `PerpsOrderViewSelectorsIDs.*` | `order-entry-submit-button` |
| Direction tabs | -- | `direction-tab-long` / `direction-tab-short` |
| TP price input | `PerpsTPSLViewSelectorsIDs.TAKE_PROFIT_PRICE_INPUT` | `tp-price-input` |
| Market item | `PerpsMarketRowItemSelectorsIDs.ROW_ITEM` | `explore-crypto-{symbol}` |
| Close modal | `PerpsClosePositionViewSelectorsIDs.*` | `perps-close-position-modal` |

## Duplicated Utilities

Identical or near-identical between codebases:

| Function | Shareable? |
|---|---|
| `getDisplayName` / `getDisplaySymbol` | YES -- already in controller |
| `getPositionDirection` | YES |
| `formatOrderType` / `formatStatus` | YES |
| `filterMarketsByQuery` | YES |
| `isHip3Market` / `isCryptoMarket` | YES |
| `groupTransactionsByDate` | Near-identical |

**Rule**: When modifying any of these on extension, check the mobile equivalent first.

## Key File Paths

**Mobile:**
- Screens: `app/components/UI/Perps/Views/`
- Hooks: `app/components/UI/Perps/hooks/`
- Utils: `app/components/UI/Perps/utils/`
- TestIDs: `app/components/UI/Perps/Perps.testIds.ts`
- Controller: `app/controllers/perps/`

**Extension:**
- Components: `ui/components/app/perps/`
- Pages: `ui/pages/perps/`
- Hooks: `ui/hooks/perps/`
- Utils: `ui/components/app/perps/utils.ts`
- Transforms: `ui/components/app/perps/utils/transactionTransforms.ts`
- Stream bridge: `app/scripts/controllers/perps/perps-stream-bridge.ts`
