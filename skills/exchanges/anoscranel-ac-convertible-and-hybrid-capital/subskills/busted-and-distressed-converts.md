---
name: busted-and-distressed-converts
domain: investing/busted-and-distressed-converts
trigger: "Analysing a convertible whose stock has fallen well below the conversion price."
anti_trigger: "Not for predicting recovery, and not for the issuer's equity case."
scope: "Busted converts, distressed conversion, and workout exposure."
status: seedling
---

# Busted and distressed converts

## Standard

A busted convertible is one whose stock trades far below the conversion price, so the option is nearly worthless and the instrument trades as a bond. Its behaviour changes character: it now responds to credit spreads rather than to the stock, its liquidity often falls, and the investor who bought it for equity exposure owns a subordinated claim with a long maturity.

At the distressed end the conversion feature can become the whole story again, for the opposite reason. When the issuer's equity is a call option on the enterprise, a conversion price far above the current stock still has value if the enterprise recovers, and the convertible becomes a way to own that recovery senior to the equity. The analysis shifts to recovery, covenant position, and what the conversion is worth in a workout.

Primary sources: <https://www.sec.gov/investor> and <https://www.cfainstitute.org/>.

## Decision rules

- Record the distance between the stock price and the conversion price.
- Record the parity and the premium over floor.
- Record the credit spread and any rating change.
- Record the position in the capital structure and the recovery estimate.
- Record the liquidity: bid-offer, issue size, and recent trading.
- Record what the conversion is worth under a recovery scenario.

## Procedure

1. Compute parity and the floor to see which dominates.
2. Record the stock-to-conversion-price distance.
3. Record credit terms and any deterioration.
4. Estimate recovery in a workout scenario.
5. Assess liquidity at the intended size.
6. Write the analysis with the dominant exposure named.

## Anti-patterns

- Treating a busted convert as equity exposure.
- Ignoring liquidity that has collapsed with the price.
- Assuming recovery from a seniority the instrument does not have.
- Ignoring the effect of a long maturity on the floor.
- Applying equity volatility analysis to a distressed credit.

## Done checklist

- [ ] Distance to conversion price recorded.
- [ ] Parity and floor computed.
- [ ] Credit terms recorded.
- [ ] Recovery estimate recorded.
- [ ] Liquidity assessed.
- [ ] Dominant exposure named.

The transition between the two regimes is the dangerous part: a convertible can drift from equity-like to credit-like over months while its holders continue to describe it as equity exposure, and the drift is usually visible first in the premium collapsing towards the floor rather than in the price, which is why the record tracks the price-to-floor ratio rather than only the level.

## Sources

- Issuer disclosure and security terms: <https://www.sec.gov/investor>
- Credit analysis standards: <https://www.cfainstitute.org/>
- Market and credit data: <https://fred.stlouisfed.org/>
