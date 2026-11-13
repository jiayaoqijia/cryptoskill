---
name: inverse-and-linear-contracts
domain: crypto-trading/inverse-and-linear-contracts
trigger: "Working out the payoff and collateral of an inverse or linear crypto option."
anti_trigger: "Not for predicting the underlying, and not for generic option theory."
scope: "Coin-margined versus stablecoin-margined contracts and their P&L arithmetic."
status: seedling
---

# Inverse and linear contracts

## Standard

A linear option is priced and settled in a stablecoin: the payoff is the difference between the settlement price and the strike, multiplied by the contract size, paid in the quote currency. An inverse option is priced in the underlying coin and settled in it: the payoff is expressed in coin, so the holder's return depends on both the option's outcome and the coin's value.

That double exposure is the point and the trap. A long inverse call profits in coin terms when the underlying rises, but the coin-denominated profit is worth less in fiat if the coin itself has fallen. Conversely a short inverse put collects premium in coin that appreciates if the coin rallies, which is precisely when the short position loses. The record states the settlement currency and computes the result in both units.

Primary sources: <https://www.cftc.gov/> and <https://www.sec.gov/investor>.

## Decision rules

- Record whether the contract is inverse or linear, and the settlement currency.
- Compute the payoff in the settlement currency and convert to the account currency.
- Record the collateral posted and its currency.
- Record the effect of a move in the collateral currency on the position's value.
- Record the contract size convention, which differs between venues.
- Record the fee currency, since it may differ from both.

## Procedure

1. Identify the contract type and settlement currency.
2. Record size and strike conventions.
3. Compute the payoff in the settlement currency.
4. Convert into the account currency at a stated rate.
5. Record the collateral and its own exposure.
6. Write the arithmetic so a reviewer can reproduce it.

## Anti-patterns

- Treating an inverse contract's coin payoff as if it were stablecoin.
- Ignoring the collateral's own price risk.
- Comparing premiums across the two contract types without conversion.
- Mixing contract size conventions between venues.
- Forgetting the fee currency.

## Done checklist

- [ ] Contract type and settlement currency recorded.
- [ ] Payoff computed in settlement currency.
- [ ] Conversion to account currency recorded.
- [ ] Collateral exposure recorded.
- [ ] Size convention recorded.
- [ ] Fee currency recorded.

A further asymmetry is the collateral's own volatility: an inverse position posted in coin loses collateral value exactly when the coin falls, which is when a short put is also losing, so the two losses compound in the same direction and the margin ratio deteriorates faster than either exposure alone would suggest.


## Sources

- Regulatory information on crypto derivatives: <https://www.cftc.gov/>
- Investor guidance on complex products: <https://www.investor.gov/introduction-investing>
- Market structure context: <https://www.sec.gov/investor>
