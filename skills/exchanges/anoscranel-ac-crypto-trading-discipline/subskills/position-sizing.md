---
name: position-sizing
domain: crypto-trading/position-sizing
trigger: "Calculating position size from invalidation distance and risk budget; adjusting for volatility and liquidity"
anti_trigger: "Sizing positions based on conviction level, account size impulse, or available leverage"
scope: "Deriving size from invalidation distance and risk budget rather than conviction; volatility and liquidity adjustments"
status: seedling
---

# Position Sizing

## Standard

- **Kelly, "A New Interpretation of Information Rate" (1956)**: optimal allocation is derived mathematically from edge and odds. <https://www.bell-labs.com/institute/about/history-bell-labs/bell-system-technical-journal/>
- **Vince, _The Mathematics of Money Management_ (1992)**: position size is a direct function of risk capital and stop distance. <https://www.wiley.com/en-us/The+Mathematics+of+Money+Management+Risk+Analysis+for+Portfolio+Decisions-p-9780471549994>
- **Covel, _Trend Following_ (2004)**: volatility-adjusted sizing prevents high-volatility assets from dominating portfolio variance. <https://www.wiley.com/en-us/Trend+Following+%28Updated+Edition%29%3A+How+Great+Traders+Make+Millions+in+The+Up+and+Down+Markets-p-9781118016831>
- **Eldor et al., "The Determinants of Trading Volume" (2006)**: liquidity constraints limit maximum position size to avoid slippage. <https://www.sciencedirect.com/science/article/abs/pii/S105752190500109X>
- ⚠️ Practitioner heuristic: fixed-fractional sizing allocates capital such that distance to stop loss equals the dollar risk budget.

## Decision rules

1. Position size is strictly an output of the risk budget and invalidation distance; conviction has zero weight.
2. Monetary risk divided by percentage distance to invalidation determines total notional value.
3. Volatility adjustments reduce position size when market variance expands.
4. Liquidity constraints cap maximum position size against order book depth.
5. Leverage is never used to increase risk exposure; it is a mechanical tool for collateral efficiency.
6. Recalculation is forbidden once orders are placed unless scaling rules are documented.
7. ⚠️ House: sizing based on available margin rather than invalidation distance is a critical violation.

## Procedure

1. Retrieve the pre-committed dollar risk budget from the risk ledger.
2. Identify entry price and invalidation price from the memo.
3. Calculate percentage distance between entry and invalidation.
4. Divide dollar risk budget by invalidation distance percentage for notional value.
5. Apply volatility scaling based on baseline versus current asset variance.
6. Verify execution slippage limits against order book depth.
7. Output final position size and execute strictly matching calculations.

## Anti-patterns

- **Conviction sizing.** Allocating more capital to high-conviction trades. Fix: restrict size entirely to risk budget mathematics.
- **Margin-based sizing.** Using available margin as the sizing base. Fix: calculate size from dollar risk.
- **Ignoring liquidity.** Sizing larger than order book depth. Fix: cap size as a fraction of volume.
- **Averaging down without budget.** Adding to losers without recalculating risk. Fix: treat additions as unauthorized risk inflation.

## Done checklist

- [ ] Position size is derived from risk budget and invalidation distance.
- [ ] Volatility adjustments have been applied.
- [ ] Liquidity and order book depth constraints have been verified.
- [ ] Leverage is used strictly for capital efficiency.
- [ ] Size calculation is documented in the pre-trade memo.

## Sources

- Kelly, "A New Interpretation of Information Rate": <https://www.bell-labs.com/institute/about/history-bell-labs/bell-system-technical-journal/>
- Vince, _The Mathematics of Money Management_: <https://www.wiley.com/en-us/The+Mathematics+of+Money+Management+Risk+Analysis+for+Portfolio+Decisions-p-9780471549994>
- Covel, _Trend Following_: <https://www.wiley.com/en-us/Trend+Following+%28Updated+Edition%29%3A+How+Great+Traders+Make+Millions+in+The+Up+and+Down+Markets-p-9781118016831>

⚠️ Gaps: sudden liquidity evaporation in crypto order books can cause execution slippage exceeding planned invalidation levels.
