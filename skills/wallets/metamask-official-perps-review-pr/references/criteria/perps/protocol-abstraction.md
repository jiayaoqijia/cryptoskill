# Protocol Abstraction

- **Provider identity lost during transformation**: Preserve provider identity through fill aggregation and apply provider-specific classification at the normalization boundary. Adding a provider must retain existing providers and cover equivalent inputs with different provider semantics.

All provider access must go through `AggregatedPerpsProvider` → `ProviderRouter`. HyperLiquid is primary, MYX is feature-flagged.

- **Hardcoded provider** — uses HyperLiquid or MYX APIs directly instead of going through `AggregatedPerpsProvider` / `ProviderRouter`. All operations must route through the abstraction.
- **Provider-specific branching in UI** — `if (provider === 'hyperliquid')` in components or hooks. Provider differences must be normalized in the aggregation layer, not leaked to the view.
- **Provider-specific error handling** — catches errors from one provider but not others. All providers must have consistent error boundaries via the aggregated layer.
- **Hardcoded market symbols** — string literals `"BTC"` or `"ETH"` instead of market config constants. Breaks when new markets or providers are added.
- **Hardcoded decimals/precision** — using provider-native decimal formats without normalization. HyperLiquid and MYX use different precision for prices, sizes, and leverage. Must go through `MarketDataFormatters` (DI).
- **`detailedOrderType` rendered directly in UI** — `detailedOrderType` is provider-native text, not an enum. HyperLiquid returns `Limit`, `Market`, `Stop Limit`, `Stop Market`, `Take Profit Limit`, `Take Profit Market`; MYX (`myxAdapter.mjs`) returns `Take Profit`, `Stop Loss`, `Liquidation` — which are not in that set. Any UI that renders `detailedOrderType` directly is provider-dependent by construction. **Grep for `detailedOrderType` in any PR touching order display** — it should be mapped through a locale string or normalized constant, not rendered raw.
