---
name: index-design-record
domain: investing/index-design-record
trigger: "Writing the record of an index's design and its consequences."
anti_trigger: "Not for recommending an index, and not for fund selection."
scope: "The written record: rules, consequences, and review triggers."
status: seedling
---

# Index design record

## Standard

The index design record states the rule set, the consequences each rule produces, and the purpose the index is meant to serve. It is written so that a user can tell what the index measures without reading the full methodology, and so that a change to any rule can be seen against the consequences it alters.

The consequences section is what distinguishes a design record from a summary. A weighting scheme's consequence is its concentration; a rebalancing rule's is its turnover; a cap's is the redistribution it triggers. Recording each rule with its consequence makes the trade-offs visible and makes the index comparable with another built on different choices.

Primary sources: <https://www.sec.gov/investor> and <https://osf.io/prereg/>.

## Decision rules

- The record states the index's purpose in one sentence.
- Each eligibility gate is recorded with the universe it excludes.
- Each weighting and capping rule is recorded with its concentration consequence.
- The rebalancing rule is recorded with its turnover estimate.
- The buffer and cap mechanics are stated, not just their levels.
- Review triggers are dated: methodology revision, purpose change, market structure change.

## Procedure

1. State the purpose.
2. Record gates and exclusions.
3. Record weighting and capping with consequences.
4. Record rebalancing and turnover.
5. Record buffer and cap mechanics.
6. Set review triggers.

## Anti-patterns

- Recording rules without their consequences.
- Stating a cap level without the mechanism.
- Omitting the excluded universe, which is the first design choice.
- No review triggers, so a revised methodology is used under an old record.
- Describing the index by its name rather than its rules.

## Done checklist

- [ ] Purpose stated.
- [ ] Gates and exclusions recorded.
- [ ] Weighting and capping with consequences.
- [ ] Rebalancing and turnover recorded.
- [ ] Mechanics stated.
- [ ] Review triggers dated.

The record's practical use is comparison: two indices described this way can be compared rule by rule rather than by name, and the differences that matter usually appear in the weighting scheme and the buffer rather than in the headline description.


Keeping the record beside the methodology version it describes is what makes a later review possible, since the rules change and a record without its version cannot tell which rules it summarized.


Adding the date of the methodology version makes the record checkable against the provider's own publication, which is the only way a reader can confirm the rules recorded are the rules in force.


## Sources

- Index methodology context: <https://www.sec.gov/investor>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Investor education on index products: <https://www.investor.gov/introduction-investing>
