---
name: eligibility-and-selection
domain: investing/eligibility-and-selection
trigger: "Reading which securities an index's rules actually admit."
anti_trigger: "Not for predicting index returns, and not for fund selection."
scope: "Gates, screens, and the universe the rules actually admit."
status: seedling
---

# Eligibility and selection

## Standard

Eligibility rules are gates: they determine which securities the index can contain at all. Typical gates cover listing venue, free-float size, liquidity, trading history, and share class. Each gate excludes a set of securities, and the excluded set is the index's first design choice, usually invisible because it is described as a minimum standard rather than as a decision.

Selection rules then rank the eligible universe and take a subset. The cut-off and the buffer around it determine turnover: a hard cut at the fiftieth name produces more churn than a rule that requires a name to fall to sixtieth before removal. The record should state both the gates and the buffer, since the first defines the universe and the second defines its stability.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record each eligibility gate and what it excludes.
- Record the selection rule and the size of the included set.
- Record the buffer rule around the cut-off, if any.
- Record how free float is defined and measured.
- Record the treatment of multiple share classes and of foreign listings.
- Record the number of securities excluded by each gate, where data permit.

## Procedure

1. List the gates and their thresholds.
2. Estimate the excluded set per gate.
3. Record the selection rule and cut-off.
4. Record the buffer rule.
5. Note share class and listing treatment.
6. Write the eligibility summary with the exclusions named.

## Anti-patterns

- Treating a minimum size rule as neutral rather than as a choice.
- Ignoring the buffer, which drives turnover more than the cut-off.
- Assuming free float is measured consistently across vendors.
- Overlooking excluded share classes that carry the same economic exposure.
- Reading the index name as a description of its contents.

## Done checklist

- [ ] Gates listed with thresholds.
- [ ] Exclusions estimated.
- [ ] Selection rule recorded.
- [ ] Buffer rule recorded.
- [ ] Share class treatment recorded.
- [ ] Summary names the exclusions.

The excluded set is also the index's hidden exposure: an index that excludes a whole sector for a definitional reason will outperform or underperform for reasons unconnected to its stated thesis, and a user who does not know what was excluded cannot attribute the result.


## Sources

- Index methodology and disclosure context: <https://www.sec.gov/investor>
- Investor education on index investing: <https://www.investor.gov/introduction-investing>
- Market data for universe construction: <https://fred.stlouisfed.org/>
