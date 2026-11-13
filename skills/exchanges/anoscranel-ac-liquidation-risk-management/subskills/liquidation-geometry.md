---
name: liquidation-geometry
domain: crypto-trading/liquidation-geometry
trigger: Use when calculating liquidation price, maintenance margin requirements, and distance from entry under flat MMR rules.
anti_trigger: Not for cross-account margin allocation, funding rate analysis, or discretionary trade journaling.
scope: MMR, leverage→liquidation-distance arithmetic with worked numbers, mark vs last price, maintenance-margin bands.
status: seedling
---

## Standard
Liquidation geometry defines the exact price threshold where a derivative position becomes insolvent and is taken over by the exchange risk engine or insurance fund. On flat maintenance margin requirement (MMR) venues, the MMR is fixed across a size tier. When maintenance margin on a flat-MMR venue is 0.5%, liquidation sits 0.5% from entry at 100x leverage, which is well inside normal market noise. At lower leverage such as 10x to 25x, the liquidation distance expands to 2% to 4%, providing adequate buffer against intraday volatility wicks. Mark price, rather than last traded price, governs liquidation triggers to prevent artificial liquidations caused by localized order book manipulation or isolated print spikes.

Primary sources for the claims here: <https://www.bybit.com/en/help-center/article/Linear-Contract-Liquidation-Price> and <https://www.binance.com/en/support/faq/liquidation-faq-360033516272>.

## Decision rules
1. Always compute the exact liquidation price prior to order submission using the formula: $P_{liq} = P_{entry} \times \left(1 \pm \frac{1}{\text{Leverage}} \mp \text{MMR}\right)$, accounting for initial margin and funding fees.
2. Treat any position where the liquidation distance is under 1.0% as critically vulnerable to standard market volatility and refuse placement unless executing a high-frequency directional scalp with pre-defined stop losses.
3. Enforce mark price monitoring across all active dashboards; never rely on last traded price feeds for risk alerts or automated margin calls.
4. Scale maintenance margin bands immediately when position size tier changes, as exchanges step up MMR brackets for large nominal exposures.

## Procedure
1. Extract the current maintenance margin requirement (MMR) from the venue contract specification (e.g., 0.5% for standard Tier 1 assets).
2. Calculate the baseline liquidation distance for the intended leverage $L$ using the formula: $\Delta P = \frac{1}{L} + \text{MMR}$ for long positions.
3. Multiply the entry price by the liquidation distance delta to establish the exact absolute liquidation price level.
4. Verify that the calculated liquidation price sits outside the immediate 95th percentile historical volatility band for the target holding period.
5. Record the liquidation price in the pre-trade risk ledger before order execution.

## Anti-patterns
- Assuming 100x leverage gives a safe margin buffer when maintenance margin sits at 0.5%, ignoring that a 0.5% adverse move triggers instant liquidation.
- Using last traded price instead of mark price for liquidation proximity monitoring during high volatility periods.
- Forgetting that fee accruals and negative funding payments steadily eat into the margin balance, bringing the liquidation price closer to the mark price over time.
- Neglecting position tier upgrades where larger nominal sizes jump the MMR bracket and instantly tighten the liquidation distance.

## Done checklist
- [ ] Maintenance margin requirement (MMR) verified directly from exchange contract specifications.
- [ ] Worked arithmetic confirms absolute liquidation price for the chosen leverage.
- [ ] Distance from entry compared against historical volatility wicks.
- [ ] Mark price feed confirmed active for all monitoring systems.
- [ ] Pre-trade risk ledger updated with exact liquidation coordinates.

## Sources
- Binance Futures Liquidation Formula Guide: https://www.binance.com/en/support/faq/liquidation-faq-360033516272
- Bybit Linear Contract Liquidation Mechanics: https://www.bybit.com/en/help-center/article/Linear-Contract-Liquidation-Price
