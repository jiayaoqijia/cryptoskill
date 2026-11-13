---
name: rates-option-liquidity
domain: investing/rates-option-liquidity
trigger: "Assessing whether a rates option can be traded and cleared at size."
anti_trigger: "Not for predicting spreads, and not for venue due diligence."
scope: "Dealer liquidity, clearing, and compression in rates options."
status: seedling
---

# Rates option liquidity

## Standard

Rates options trade over the counter through dealers and on exchanges for the standardised contracts. Liquidity concentrates in a few points: at-the-money or nearby strikes, standard expiries, and the major currencies. A trade in a wing strike or an odd expiry is a trade that may be priced but not exited, and the difference between those two states is what the liquidity assessment has to establish.

Clearing changes the credit picture and the operational one. A cleared swaption is novated to a clearing house, which reduces counterparty exposure but introduces margin calls on the position's value and on its risk sensitivities. Compression can reduce notional across offsetting trades, but it changes the position's optionality and must be evaluated rather than accepted as a free reduction.

Primary sources: <https://www.bis.org/> and <https://www.cmegroup.com/>.

## Decision rules

- Record the bid-offer at the strike and expiry traded, and the size available.
- Record which expiries and strikes are quoted continuously and which are on request.
- Record whether the trade is cleared and the margin implications.
- Record the compression terms and what optionality it removes.
- Record the counterparty or clearing house exposure.
- Record the exit route if the dealer stops quoting.

## Procedure

1. Collect two-way prices at the intended strike and expiry.
2. Record liquidity by strike and expiry bucket.
3. Record clearing status and margin requirements.
4. Record compression terms where applicable.
5. Record counterparty exposure.
6. Write the liquidity assessment.

## Anti-patterns

- Assuming an at-the-money quote applies to a wing strike.
- Ignoring margin calls on a cleared option position.
- Accepting compression without checking what it removes.
- Treating a one-way price as a market.
- Overlooking the clearing house's exposure in a stress event.

## Done checklist

- [ ] Two-way price and size recorded.
- [ ] Liquidity by bucket recorded.
- [ ] Clearing and margin recorded.
- [ ] Compression terms recorded.
- [ ] Counterparty exposure recorded.
- [ ] Exit route written.

The operational point is that clearing and compression are not free improvements: clearing converts counterparty risk into margin calls that must be funded, and compression removes optionality along with notional, so both should be recorded as changes to the position rather than as housekeeping on it.

The assessment should also record the size at which the market stops being two-way, since that number, not the quoted spread, is what determines whether a position can be reduced under stress.


## Sources

- Market structure and clearing standards: <https://www.bis.org/>
- Exchange-listed rate products: <https://www.cmegroup.com/>
- Regulatory market context: <https://www.federalreserve.gov/>
