---
name: anti-dilution-and-ratchets
domain: investing/anti-dilution-and-ratchets
trigger: "Reading anti-dilution protection when a round prices below the last."
anti_trigger: "Not for a fairness opinion, and not for legal advice."
scope: "Down-round protection and the full-ratchet/broad-based-weighted-average spectrum."
status: seedling
---

# Anti-dilution and ratchets

## Standard

Anti-dilution provisions adjust a preferred series' conversion price when the company issues new stock at a lower price — a down round. The adjustment increases the number of common shares each preferred share converts into, which dilutes everyone not protected. The two ends of the spectrum: a full ratchet reprices the entire series to the new, lower round price as if the protected investor had bought at that price from the start; a broad-based weighted average blends the old and new prices in proportion to the shares outstanding, producing a far smaller adjustment.

The spectrum matters because it moves dilution between parties. A full ratchet in a severe down round can transfer a large fraction of the company from founders and employees to the protected series — the arithmetic is exact and unforgiving. Broad-based weighted average is the market convention precisely because it splits the difference; narrow-based variants sit in between by excluding more share counts from the average. Pay-to-play provisions add the other side: a series that declines to invest pro rata in the new round can forfeit its anti-dilution protection, converting the protection into a participation obligation.

Primary sources: <https://www.law.cornell.edu/> and <https://pages.stern.nyu.edu/~adamodar/>.

## Decision rules

- Record each series' anti-dilution formula type: full ratchet, broad-based weighted average, or narrow variant.
- Compute the adjusted conversion price and the new conversion ratio for each series under a modelled down round.
- Record any pay-to-play provision and what it takes to keep the protection.
- Distinguish a stock split or recapitalisation from a down round: a formula's trigger may treat them differently.
- Note that anti-dilution adjustments to conversion price do not affect the preference amount, which stays keyed to the original issue price.
- State who bears the dilution from each adjustment — the classes whose conversion ratio did not change.

## Procedure

1. Extract each series' anti-dilution formula from its certificate of incorporation.
2. Model the down round at the new price per share.
3. Compute each series' adjusted conversion price and new conversion ratio.
4. Recompute the cap table with the adjustments and identify who lost what percentage.
5. Check for pay-to-play conditions and their effect on the modelled outcome.
6. Write the down-round analysis with the dilution transfer stated in percentage points.

## Anti-patterns

- Applying full-ratchet arithmetic to a weighted-average provision.
- Adjusting the preference amount instead of the conversion price.
- Ignoring pay-to-play until the round is signed.
- Treating a split as triggering anti-dilution when the formula may exclude it.
- Forgetting that the adjustment compounds: multiple down rounds stack.

## Done checklist

- [ ] Formula type recorded per series.
- [ ] Adjusted conversion prices computed.
- [ ] New conversion ratios computed.
- [ ] Cap table recomputed with dilution transfer identified.
- [ ] Pay-to-play checked.
- [ ] Stacking across multiple down rounds noted.

## Sources

- Statutory reference on charter provisions: <https://www.law.cornell.edu/>
- Form D filings for round terms: <https://www.sec.gov/edgar/search/>
- Investor education on private placements: <https://www.investor.gov/introduction-investing>
