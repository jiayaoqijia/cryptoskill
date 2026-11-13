---
name: ils-record
domain: investing/ils-record
trigger: "Writing the record of an insurance-linked position."
anti_trigger: "Not for recommending a bond, and not for the offering circular itself."
scope: "The written record: trigger, peril, expected loss, and season exposure."
status: seedling
---

# ILS record

## Standard

The ILS record states the trigger design and its basis risk, the peril definition and region, the expected loss with its model version, the spread and the multiple it implies, the collateral and swap counterparties, and the season window the position sits in. Those fields are what make the position reviewable; a peril label and a spread are not.

The record also carries the correlation view. A single bond is assessed on its own merits, but a book is assessed on how the positions move together, and the aggregation by peril and region is the number that determines whether the allocation is diversifying or concentrating. That aggregate belongs in the record rather than in a separate risk report, because it changes what any individual position means.

Primary sources: <https://www.artemis.bm/> and <https://osf.io/prereg/>.

## Decision rules

- Record the trigger type, reference, and basis risk in both directions.
- Record the peril definition, region, and secondary perils.
- Record expected loss with model vendor and version.
- Record spread, reference rate, and multiple.
- Record collateral, swap counterparty, and downgrade remedies.
- Record the season window and the aggregate exposure by peril.

## Procedure

1. Record trigger and peril terms.
2. Record expected loss and model.
3. Record spread and multiple.
4. Record collateral and counterparties.
5. Record season window and aggregate by peril.
6. Set review triggers at reset and at season start.

## Anti-patterns

- Recording the peril label without the definition.
- Omitting the model version behind expected loss.
- Recording the spread without the multiple.
- Leaving the collateral counterparties out.
- Aggregating by issuer rather than by peril.

## Done checklist

- [ ] Trigger and peril recorded.
- [ ] Expected loss and model recorded.
- [ ] Spread and multiple recorded.
- [ ] Collateral and counterparties recorded.
- [ ] Season window recorded.
- [ ] Aggregate by peril recorded.

The record should also state what would have to happen for the position to lose principal, in one sentence: a reader who can answer that from the record understands the bond, and a reader who cannot has a description of a security rather than an assessment of a risk.

Keeping the record beside the portfolio's other risk records is what allows the aggregate to be computed at all: an ILS book assessed on its own looks diversifying, and the same book read beside an equity portfolio's catastrophe-exposed holdings may be doubling an exposure the investor already carried.

## Sources

- ILS market data and terms: <https://www.artemis.bm/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Securities disclosure context: <https://www.sec.gov/investor>
