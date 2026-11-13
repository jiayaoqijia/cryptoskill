---
name: collateral-and-spv
domain: investing/collateral-and-spv
trigger: "Checking what stands behind a catastrophe bond's principal."
anti_trigger: "Not for predicting an event, and not for recommending a bond."
scope: "The special-purpose reinsurer, collateral quality, and counterparty terms."
status: seedling
---

# Collateral and SPV

## Standard

A catastrophe bond is issued by a special-purpose reinsurer that holds the proceeds in collateral and provides reinsurance to the sponsor. The investor's principal is therefore exposed to two things at once: the trigger event, and whatever the collateral is invested in. In most structures the collateral is held in high-quality short-duration assets, but the quality, the permitted investments, and the haircut applied on a downgrade are terms worth reading.

The vehicle's own structure matters as well. It is usually bankruptcy-remote and restricted to the transaction, and the swap it uses to convert collateral returns into the coupon carries a counterparty. A structure whose collateral is sound but whose swap counterparty is weak has a risk that does not appear in the peril analysis, and the record should separate the peril exposure from the collateral and counterparty exposure.

Primary sources: <https://www.sec.gov/investor> and <https://www.bis.org/>.

## Decision rules

- Record what the collateral may be invested in and the current composition.
- Record the haircut or remedy if the collateral is downgraded.
- Record the swap counterparty and the terms of the total return swap.
- Record the vehicle's permitted activities and its bankruptcy remoteness.
- Record any provision allowing reinvestment into lower-quality assets.
- Record the maturity of the collateral against the bond's expected life.

## Procedure

1. Record the vehicle's legal form and remoteness.
2. Record permitted collateral and current holdings.
3. Record downgrade remedies and haircuts.
4. Record the swap counterparty and terms.
5. Check collateral maturity against the bond's life.
6. Write the collateral summary with its counterparties named.

## Anti-patterns

- Treating the principal as riskless except for the peril.
- Ignoring the swap counterparty.
- Assuming collateral quality is maintained after a downgrade.
- Overlooking reinvestment provisions.
- Missing a maturity mismatch between collateral and bond.

## Done checklist

- [ ] Vehicle structure recorded.
- [ ] Permitted collateral recorded.
- [ ] Downgrade remedies recorded.
- [ ] Swap counterparty recorded.
- [ ] Maturity matched.
- [ ] Summary names counterparties.

The provision that deserves particular attention is the one governing what happens if the collateral is downgraded during the bond's life: some structures require the manager to move assets into permitted investments, others permit a reduced coupon instead, and a few allow the collateral to remain. Which of those applies determines whether a downgrade is a temporary annoyance or a change in the risk the investor holds.

## Sources

- Structured note and ILS disclosure: <https://www.sec.gov/investor>
- Collateral and counterparty standards: <https://www.bis.org/>
- Investor education on structured risk: <https://www.investor.gov/introduction-investing>
