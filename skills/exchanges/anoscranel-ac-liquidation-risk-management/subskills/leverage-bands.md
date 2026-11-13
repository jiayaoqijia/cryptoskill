---
name: leverage-bands
domain: crypto-trading/leverage-bands
trigger: Use when determining appropriate position leverage based on invalidation distance rather than conviction.
anti_trigger: Not for calculating initial maintenance margin, margin mode selection, or post-liquidation recovery.
scope: Choose leverage from the invalidation distance, never from conviction; the 10–25x vs 100x geometry; why a 0.5% liquidation distance sits inside the tool noise.
status: seedling
---

## Standard
Leverage selection must be derived strictly from technical invalidation distance rather than emotional conviction or desired profit magnitude. High conviction does not alter market volatility or the physical distance to a technical stop level. Operating at 100x leverage forces a liquidation distance of approximately 0.5% on flat-MMR venues, placing the liquidation trigger directly inside normal market noise and high-frequency spread oscillations. Conversely, operating within the 10x to 25x leverage band establishes a liquidation distance of 2% to 4%, providing a structural buffer that allows technical stop losses to execute before exchange liquidation engines intervene. Position sizing and leverage work in tandem to ensure that capital at risk remains constant regardless of nominal leverage.

Primary sources for the claims here: <https://www.bybit.com/en/help-center/article/Leverage-and-Margin> and <https://www.bitmex.com/app/leverage>.

## Decision rules
1. Calculate maximum allowable leverage by dividing the maximum acceptable risk percentage by the technical invalidation distance percentage ($L = \frac{\text{Risk \%}}{\text{Stop Distance \%}}$).
2. Prohibit the use of leverage exceeding 25x on any single directional perpetual contract unless executing sub-second arbitrage or high-frequency market making.
3. Reject any trade setup where the technical stop-loss distance is tighter than the exchange liquidation distance at the chosen leverage tier.
4. Scale position nominal size inversely with leverage to ensure dollar risk per trade remains strictly within desk risk limits.

## Procedure
1. Identify the technical invalidation level (chart support/resistance break) for the target trade setup.
2. Measure the percentage distance between the entry price and the technical invalidation level.
3. Determine the target leverage band (10x to 25x) based on volatility and holding timeframe.
4. Calculate the resulting exchange liquidation distance and verify it exceeds the technical stop distance by a minimum safety margin of 50%.
5. Adjust position size so that total dollar loss at the technical stop equals the designated risk budget.

## Anti-patterns
- Choosing 100x leverage because of high conviction in a directional breakout, ignoring that normal spread noise will liquidate the position instantly.
- Setting leverage arbitrarily and then placing a stop-loss outside the liquidation price, rendering the stop loss useless.
- Failing to reduce position size when stepping up leverage, resulting in unbudgeted account exposure.
- Treating leverage as a reward multiplier rather than a mathematical constraint dictated by market volatility.

## Done checklist
- [ ] Technical invalidation distance measured and documented.
- [ ] Leverage chosen from invalidation distance rather than emotional conviction.
- [ ] Liquidation distance verified to sit well outside standard market noise (>2% for swing trades).
- [ ] Position size scaled inversely to maintain constant dollar risk.
- [ ] Stop-loss execution price confirmed closer to entry than exchange liquidation price.

## Sources
- BitMEX Leverage and Margin Risk Management Guide: https://www.bitmex.com/app/leverage
- Bybit Risk Limit and Leverage Tiers: https://www.bybit.com/en/help-center/article/Leverage-and-Margin
