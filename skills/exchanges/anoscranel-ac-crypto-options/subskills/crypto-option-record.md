---
name: crypto-option-record
domain: crypto-trading/crypto-option-record
trigger: "Writing the record of a crypto option position and its liquidation risk."
anti_trigger: "Not for recommending a position, and not for the venue statement."
scope: "The written record: contract type, collateral, expiry, and liquidation distance."
status: seedling
---

# Crypto option record

## Standard

The crypto option record states the contract type and settlement currency, the collateral and its currency, the expiry and settlement time, the premium convention, and the liquidation distance for a short position. Those fields are specific to this market: an inverse contract's payoff is in coin, the collateral can move in value independently of the option, and settlement happens at a fixed time rather than at a close.

The liquidation distance is the field that separates a managed position from an unmanaged one. Computed from the venue's own methodology and expressed as an underlying move, it converts a margin requirement into a market level, and a level can be watched. The record also carries the assignment or delivery consequence, since a short position that expires in the money produces a coin position that changes the portfolio's exposure.

Primary sources: <https://www.cftc.gov/> and <https://osf.io/prereg/>.

## Decision rules

- Record the contract type, settlement currency, and contract size convention.
- Record the collateral posted and its currency.
- Record the expiry, the settlement time, and the index used.
- Record the premium and its currency.
- Record the liquidation level and the buffer as a percentage move.
- Record the assignment or delivery consequence and its effect on concentration.

## Procedure

1. Record the contract and its conventions.
2. Record collateral and settlement terms.
3. Record premium and fees.
4. Compute the liquidation level.
5. Record the assignment consequence.
6. Review at each expiry and after any material move.

## Anti-patterns

- Recording the premium without the collateral currency.
- Leaving the liquidation level uncomputed.
- Omitting the settlement time in a continuous market.
- Ignoring the assignment's effect on the portfolio.
- Reviewing only the profit and loss.

## Done checklist

- [ ] Contract type and conventions recorded.
- [ ] Collateral recorded with currency.
- [ ] Expiry and settlement time recorded.
- [ ] Premium and fees recorded.
- [ ] Liquidation level and buffer recorded.
- [ ] Assignment consequence recorded.

Recording the settlement index alongside the settlement time closes the last gap: a position can be profitable against the venue's last trade and worthless against the index, and only the record that names the index allows a later review to see which of the two the result was measured against.


## Sources

- Regulatory information on crypto derivatives: <https://www.cftc.gov/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Investor education on margin risk: <https://www.investor.gov/introduction-investing>
