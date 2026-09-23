# Magic Strings, Magic Numbers & Placeholder Values

Constants live in the controller package (`core/packages/perps-controller/src/constants/perpsConfig.ts`, exported by `@metamask/perps-controller`) and in `app/components/UI/Perps/constants/perpsConfig.ts` (UI-only). PRs must use these — not inline literals.

- **Defaulting to `0` when data is unavailable** — the most common mistake. When price/percentage/data hasn't loaded yet, use the placeholder constants, NOT `0`, `$0`, or `0%`:
  - `PERPS_CONSTANTS.FallbackPriceDisplay` (`'$---'`) — price not yet loaded
  - `PERPS_CONSTANTS.FallbackPercentageDisplay` (`'--%'`) — percentage not yet loaded
  - `PERPS_CONSTANTS.FallbackDataDisplay` (`'--'`) — generic data not yet loaded
  - `PERPS_CONSTANTS.ZeroAmountDisplay` (`'$0'`) / `ZeroAmountDetailedDisplay` (`'$0.00'`) — ONLY for actual confirmed zero values (e.g., no volume), never for "loading" or "unavailable"
  - Defaulting to `0` hides loading states, makes bugs invisible, and can mislead users into thinking their balance/PnL is actually zero.
- **Inline timeout/delay values** — hardcoded `5000`, `10000`, `300` instead of `PERPS_CONSTANTS.WebsocketTimeout`, `PERPS_CONSTANTS.ConnectionTimeoutMs`, `PERFORMANCE_CONFIG.ValidationDebounceMs`, etc. Every timing constant has a named export.
- **Hardcoded slippage** — using `0.03` or `300` instead of `ORDER_SLIPPAGE_CONFIG.DefaultMarketSlippageBps`, `DefaultTpslSlippageBps`, `DefaultLimitSlippageBps`.
- **Hardcoded leverage fallback** — using `3` or `50` instead of `PERPS_CONSTANTS.DefaultMaxLeverage` or `MARGIN_ADJUSTMENT_CONFIG.FallbackMaxLeverage`.
- **Hardcoded precision** — using `6`, `2`, `5` for decimal places instead of `DECIMAL_PRECISION_CONFIG.MaxPriceDecimals`, `MaxSignificantFigures`, `FallbackSizeDecimals`, or `CLOSE_POSITION_CONFIG.UsdDecimalPlaces`.
- **Hardcoded API URLs** — inline `'https://perps.api...'` instead of `DATA_LAKE_API_CONFIG.OrdersEndpoint`.
- **Hardcoded provider name** — `'hyperliquid'` string instead of `PROVIDER_CONFIG.DefaultProvider`.
- **Hardcoded validation thresholds** — `20` for high leverage warning, `0.1` for price deviation, instead of `VALIDATION_THRESHOLDS.HighLeverageWarning`, `VALIDATION_THRESHOLDS.PriceDeviation`.
- **Hardcoded cache durations** — inline `5 * 60 * 1000` instead of `PERFORMANCE_CONFIG.MarketDataCacheDurationMs`, `FeeDiscountCacheDurationMs`, etc.
