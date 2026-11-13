---
name: peer-group-traps
domain: investing/peer-group-traps
trigger: "Using a peer group comparison and its limits."
anti_trigger: "Not for selecting a manager, and not for predicting returns."
scope: "Survivorship, classification, and the median that hides everything."
status: seedling
---

# Peer group traps

## Standard

A peer group is a universe someone else defined. The definition determines the result: funds that closed are usually excluded, which removes the failures and lifts the average; the classification may put strategies with different risks in the same bucket; and the median hides the dispersion, which is often wider than the difference between the top and bottom quartiles being celebrated.

The comparison is still useful when read correctly. A ranking is a statement about a specific universe over a specific period, and it says nothing about the universe the investor would actually have chosen from. The record should state the universe, its construction, whether survivorship was addressed, and the dispersion around the median, so that a ranking can be read as a position within a distribution rather than as a verdict.

Primary sources: <https://www.cfainstitute.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the universe: its membership rule, size, and any exclusions.
- Record whether closed or failed funds are included.
- Record the classification criteria and the risk differences within the group.
- Record the dispersion, not only the median and the quartile boundaries.
- Record the period and whether every member has data for all of it.
- Where survivorship cannot be corrected, record it as a bias affecting the ranking.

## Procedure

1. Identify the universe and its construction.
2. Check survivorship treatment.
3. Record classification and any heterogeneity.
4. Compute dispersion alongside the ranking.
5. Record the period and data coverage.
6. Write the comparison with the bias stated.

## Anti-patterns

- Treating a top-quartile ranking as evidence of skill.
- Ignoring closed funds removed from the universe.
- Comparing funds classified differently.
- Quoting the median without the dispersion.
- Comparing rankings from universes with different membership rules.

## Done checklist

- [ ] Universe and construction recorded.
- [ ] Survivorship treatment recorded.
- [ ] Classification recorded.
- [ ] Dispersion computed.
- [ ] Period and coverage recorded.
- [ ] Bias stated.

A useful addition is to compare the dispersion with the difference being claimed: when the interquartile range is larger than the gap between the top and second quartile, a ranking within that band carries almost no information, and reporting it as a distinction overstates what the universe can support.


Recording the universe definition alongside the ranking is the single practice that keeps a comparison honest, because it makes the next comparison check its own basis instead of assuming the previous one still holds.

## Sources

- Performance standards and peer comparison guidance: <https://www.cfainstitute.org/>
- Investor education on fund comparison: <https://www.investor.gov/introduction-investing>
- Fund and market data: <https://fred.stlouisfed.org/>
