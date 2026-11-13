---
name: securitisation-record
domain: investing/securitisation-record
trigger: "Writing the record of a securitisation structure and a tranche's position in it."
anti_trigger: "Not for recommending a tranche, and not for the offering memorandum itself."
scope: "The written structure record: tranche, enhancement, triggers, and servicer terms."
status: seedling
---

# Securitisation record

## Standard

The structure record states the tranche's attachment and detachment, the enhancement beneath it and how quickly that enhancement erodes, the triggers that could redirect cash, the servicer and its commingling provisions, and the weighted average life under a range of prepayment speeds. Those six facts describe the position; the rating describes an opinion about it.

The record also carries the deal's own definitions, because they differ between transactions for the same asset class. What counts as a delinquency, how losses are calculated, and which triggers are tested are all document-specific, and a comparison built on headline labels rather than on the definitions is a comparison of two different things. Stating the definitions at entry is what makes a later comparison valid.

Primary sources: <https://www.sec.gov/investor> and <https://osf.io/prereg/>.

## Decision rules

- Record the deal, tranche, attachment, detachment, and notional.
- Record the enhancement beneath the tranche and its erosion in stress.
- Record each trigger with its threshold and current level.
- Record the servicer, its rating, and the commingling provisions.
- Record the WAL assumption and range, separately from legal maturity.
- Record the deal's own definitions for delinquency, loss, and default.

## Procedure

1. Record the structural position of the tranche.
2. Record enhancement and its weakest component.
3. Record triggers and distances to breach.
4. Record servicing arrangements.
5. Record WAL under a speed range.
6. Record the definitions and the file reference.

## Anti-patterns

- Recording the rating as if it were the position.
- Omitting the enhancement's composition.
- Leaving triggers out because they have not breached.
- Comparing two tranches without checking their definitions.
- Treating legal maturity as the horizon.

## Done checklist

- [ ] Tranche position recorded.
- [ ] Enhancement recorded with weakest component.
- [ ] Triggers and buffers recorded.
- [ ] Servicing recorded.
- [ ] WAL range recorded.
- [ ] Definitions recorded with reference.

The record earns its keep at review, when the question is whether the tranche is behaving as it did at entry: the attachment point, the trigger buffers, and the servicer's rating are all quantities that move, and a review that compares the current figures against dated entry assumptions can say whether the structure has weakened or merely aged.

Storing the definitions verbatim rather than summarised is worth the space: when the same term appears in two deals with different meanings, the record is the only place the difference survives, and a comparison built from summaries will quietly treat them as the same measure.

## Sources

- Asset-backed securities disclosure: <https://www.sec.gov/investor>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Securitisation standards: <https://www.bis.org/>
