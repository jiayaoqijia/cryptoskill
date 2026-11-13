---
name: conversion-parity-and-premium
domain: investing/conversion-parity-and-premium
trigger: "Computing conversion parity and the premium a convertible trades at."
anti_trigger: "Not for predicting the stock, and not for bond pricing."
scope: "Parity, conversion premium, and what the premium pays for."
status: seedling
---

# Conversion parity and premium

## Standard

Conversion parity is what the bond would be worth if converted now: the conversion ratio multiplied by the share price. The conversion premium is the convertible's price above that parity, expressed as a percentage. A premium of twenty percent says the market pays a fifth more than the shares are worth for the coupon and the floor beneath it.

The premium moves for reasons that are not about the stock. It rises when implied volatility rises, because the embedded option is worth more; it rises when credit improves, because the floor rises with it; and it falls when the stock falls far enough that the bond floor becomes the binding value. Reading the premium without those inputs is reading one number from a three-variable equation.

Primary sources: <https://www.sec.gov/investor> and <https://www.cfainstitute.org/>.

## Decision rules

- Record the conversion ratio, the conversion price, and the share price used, with dates.
- Compute parity and the premium, and state the formula.
- Record the credit spread and the implied volatility used to explain the premium.
- Compare the premium with the issuer's own history and with comparable converts.
- Record the premium's sensitivity to a move in each of the three inputs.
- Where the conversion price is subject to adjustment, record the adjustment terms.

## Procedure

1. Extract the conversion ratio and the conversion price.
2. Compute parity from the current share price.
3. Compute the premium over parity.
4. Record credit spread and implied volatility at the same date.
5. Compare with history and with peers.
6. Write the premium analysis with its sensitivities.

## Anti-patterns

- Quoting a premium without the parity calculation.
- Comparing premiums across issuers with different credit.
- Ignoring the dividend yield, which lowers parity over time.
- Treating a falling premium as cheapness when volatility collapsed.
- Forgetting that the ratio adjusts on a corporate action.

## Done checklist

- [ ] Ratio and conversion price recorded.
- [ ] Parity computed.
- [ ] Premium computed with formula.
- [ ] Credit and volatility recorded.
- [ ] Comparison made.
- [ ] Sensitivities recorded.

The premium is also an artefact of supply: a large issue that many holders want to own can trade at a premium that has little to do with volatility or credit, and an issue that is being sold by a single holder can trade below where its terms imply. Recording the issue size and recent flow beside the premium is what separates a pricing observation from a positioning one.

## Sources

- Convertible security disclosure: <https://www.sec.gov/investor>
- Investment analysis standards: <https://www.cfainstitute.org/>
- Market and rate data: <https://fred.stlouisfed.org/>
