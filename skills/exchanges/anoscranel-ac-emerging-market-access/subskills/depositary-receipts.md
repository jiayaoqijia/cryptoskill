---
name: depositary-receipts
domain: investing/depositary-receipts
trigger: "Reading a depositary receipt and what its ratio and premium mean."
anti_trigger: "Not for the equity case, and not for predicting the premium."
scope: "ADRs and GDRs, ratios, sponsorship, and the premium to local."
status: seedling
---

# Depositary receipts

## Standard

A depositary receipt is a claim on shares held by a depositary bank in the home market, traded in a foreign market under that market's rules. The ratio states how many local shares one receipt represents, and it changes when the underlying moves — a split, a bonus issue, or a capital raise can adjust it, which changes the price of the receipt without any change in the business.

The premium or discount to the local price is the number that matters for an allocator comparing routes. It reflects the cost of creating and cancelling receipts, the demand from the foreign market, and any restriction on convertibility. A persistent premium says the foreign market values the exposure more than the local one, often because access is limited; a discount says the opposite, and neither is free money unless the holder can arbitrage between the two markets.

Primary sources: <https://www.sec.gov/investor> and <https://www.cfainstitute.org/>.

## Decision rules

- Record the ratio and its history of adjustment.
- Record whether the programme is sponsored or unsponsored.
- Record the depositary bank and its fee structure.
- Record the premium or discount to the local price and its range over time.
- Record any restriction on creation or cancellation.
- Record the receipt's voting rights and how instructions are passed through.

## Procedure

1. Record the receipt, the ratio, and the depositary.
2. Record sponsorship and the fee schedule.
3. Compute the premium or discount to the local price.
4. Record the range and any persistence.
5. Record creation and cancellation restrictions.
6. Write the receipt summary with the premium analysis.

## Anti-patterns

- Comparing receipt prices without adjusting for the ratio's history.
- Assuming a premium is an arbitrage available to any holder.
- Ignoring the depositary's fee, which reduces the return quietly.
- Overlooking a programme termination that forces conversion.
- Treating voting rights as equivalent to direct share ownership.

## Done checklist

- [ ] Ratio and adjustments recorded.
- [ ] Sponsorship and fees recorded.
- [ ] Premium computed with range.
- [ ] Restrictions recorded.
- [ ] Voting mechanics recorded.
- [ ] Summary written.

Programme termination is the risk that converts a liquid holding into a forced one: when a depositary ends a programme, holders typically receive the underlying local shares or a cash payment at a date the depositary sets, and neither outcome is the exit they would have chosen. Recording the termination provisions alongside the premium is what makes the route comparison complete.


## Sources

- Depositary receipt disclosure: <https://www.sec.gov/investor>
- Investment analysis standards: <https://www.cfainstitute.org/>
- Cross-border market context: <https://www.imf.org/>
