---
name: haircuts-and-liquidation-distance
domain: crypto-trading/haircuts-and-liquidation-distance
trigger: calculating liquidation price with depegged collateral, auditing venue margin haircuts, assessing position buffer under stress
anti_trigger: stablecoin issuer analysis, historical depeg research, custody provider auditing, selecting trading venues
scope: How a haircut or a depeg moves your liquidation price; the arithmetic worked through.
status: seedling
---

## Standard
Margin collateral value on perpetual futures exchanges is governed by exchange-defined haircuts that discount the nominal holding to account for volatility and liquidity risk. When a collateral asset experiences a depeg or when a venue increases its risk haircut, the effective margin value backing open leveraged positions shrinks instantaneously. The arithmetic of liquidation distance is directly coupled to this adjusted collateral value: total maintenance margin requirement divided by net collateral value determines proximity to liquidation. If a stablecoin collateral depegs by ten percent, its effective purchasing power as margin drops by that exact percentage plus any additional dynamic haircut imposed by the venue's risk engine. This contraction shifts the liquidation price closer to the current mark price, increasing the probability of forced liquidation even if the underlying perpetual contract price remains stable. Comprehensive guides on margin mechanics and risk management models are published by educational financial resources such as Investopedia at https://www.investopedia.com/ and quantitative risk frameworks outlined by professional risk management associations at https://www.garp.org/. Working through this arithmetic requires quantifying the exact interaction between asset price discounts, venue haircut schedules, and position leverage multipliers to prevent unexpected account liquidation during market stress.

## Decision rules
- Rule 1: Always calculate liquidation distance using the post-haircut value of collateral rather than its nominal fiat face value.
- Rule 2: Factor in potential dynamic haircut increases by exchanges during high-volatility events when determining safe leverage limits.
- Rule 3: Treat any decline in collateral market price as a direct multiplier on position leverage, requiring proportional position reduction.
- Rule 4: Never assume that holding stablecoin margin completely shields an account from liquidation if the stablecoin itself depegs.
- Rule 5: Regularly audit exchange risk engine parameters to identify sudden adjustments in collateral weighting factors.

## Procedure
1. Retrieve the current nominal balance of each collateral asset held within the margin account across venues such as Coinbase Derivatives at https://www.coinbase.com/derivatives.
2. Check the exchange's published margin requirement schedule and haircut percentages for each specific collateral token.
3. Multiply the nominal asset balance by one minus the haircut percentage to determine the effective collateral value recognized by the venue.
4. Recalculate the account maintenance margin ratio using the reduced collateral value against total open position notional exposure.
5. Determine the new exact mark price threshold at which the maintenance margin equals total margin, establishing the updated liquidation price.

## Anti-patterns
- Calculating liquidation distance based on nominal stablecoin balance without accounting for exchange haircuts or depeg discounts.
- Ignoring the compound effect of simultaneous asset price drops and collateral haircut increases during systemic market stress.
- Failing to update position sizing models when exchange risk parameters alter collateral weighting values.
- Assuming that positive unrealized PnL on perpetual positions offsets a severe contraction in collateral value caused by a depeg.

## Done checklist
- [ ] Nominal collateral balances identified and verified against venue records.
- [ ] Exchange haircut schedules and dynamic risk adjustments applied.
- [ ] Effective collateral value calculated accurately.
- [ ] Updated liquidation price computed using post-haircut figures.
- [ ] Margin safety buffer verified against potential further depeg scenarios.

## Sources
- Investopedia Financial Terms and Margin Calculation Guides: https://www.investopedia.com/
- Global Association of Risk Professionals Risk Frameworks: https://www.garp.org/
- Coinbase Derivatives Exchange Documentation: https://www.coinbase.com/derivatives
