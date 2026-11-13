---
name: fire-sale-and-discounts
domain: investing/fire-sale-and-discounts
trigger: "Estimating what a forced sale would cost."
anti_trigger: "Not for predicting a crisis, and not for allocation policy."
scope: "What a forced seller pays, and how the discount clears the market."
status: seedling
---

# Fire sale and discounts

## Standard

A forced seller faces a different price from a patient one. The discount is the compensation the buyer requires for absorbing size quickly, and it widens with the size relative to available liquidity, with the urgency, and with the number of other sellers doing the same thing. In a stress event all three move at once, which is why fire-sale discounts are far larger than the linear extrapolation of normal execution costs.

The spiral is the mechanism that makes it a systemic concern as well as a portfolio one. Selling depresses prices, which reduces the value of collateral, which triggers margin calls, which require more selling. For an individual portfolio the practical lesson is the same as the systemic one: the cost of a forced sale is a function of how many other participants are forced at the same time.

Primary sources: <https://www.bis.org/> and <https://www.finra.org/>.

## Decision rules

- Record the position size relative to normal daily volume.
- Record the assumed discount per day of accelerated exit, with its source.
- Record the discount under a stress case where volume falls and others sell.
- Record the cost in currency for the exit schedule contemplated.
- Record whether the assets are held by others in similar positions, which predicts correlated selling.
- Record the alternative: pre-arranged facilities or a longer horizon.

## Procedure

1. Record size and normal volume.
2. Estimate the discount for a compressed schedule.
3. Estimate the stress discount with reduced volume.
4. Compute the total cost in currency for each.
5. Assess correlated selling pressure.
6. Write the comparison with the alternatives.

## Anti-patterns

- Extrapolating normal execution costs linearly to a forced sale.
- Assuming volume stays at its normal level during stress.
- Ignoring that other holders face the same constraint.
- Quoting a discount without the schedule it assumes.
- Treating the discount as a cost only when it is also a funding event.

## Done checklist

- [ ] Size and volume recorded.
- [ ] Normal discount estimated.
- [ ] Stress discount estimated.
- [ ] Total cost computed for both.
- [ ] Correlated selling assessed.
- [ ] Alternatives recorded.

The record should also note who else holds the position: a security concentrated in a handful of funds with similar redemption terms is one where the sellers arrive together, and the discount in that case reflects the queue rather than the asset's own quality, which is a risk that cannot be diversified by holding more of it.


## Sources

- Financial stability and market liquidity work: <https://www.bis.org/>
- Trading and execution guidance: <https://www.finra.org/>
- Market stress indicators: <https://fred.stlouisfed.org/>
