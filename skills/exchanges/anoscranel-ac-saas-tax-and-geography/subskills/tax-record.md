---
name: tax-record
domain: software-engineering/tax-record
trigger: "Writing the per-sale evidence bundle that a tax question or audit will ask for."
anti_trigger: "Not for filing returns; not the general ledger; not legal advice."
scope: "The evidence bundle: place-of-supply decision, IDs used, evidence used, amount remitted, per sale."
status: seedling
---

# Tax record

## Standard

Every tax question about a sale — from an auditor, a customer's finance team, or your own year-end — resolves to the same query: what made this sale's treatment correct? The answer is a per-sale bundle: the place-of-supply rules applied, the customer's type and identifiers with their validation state, the location evidence and which pieces of it were relied on, the treatment's mechanism, the amount collected or the reason none was, the display basis, and the invoice's sequence number and issue date.

The record is assembled when the sale is processed because that is the only moment its inputs are all present. A retro-fitted bundle is a reconstruction, and a reconstruction is distinguishable from a record by exactly the thing that makes it not a record: the determination it claims to evidence was made before the evidence was gathered, not simultaneously with it.

No sale exists without its bundle; the aggregate of the bundles is what a filing period draws from, and the bundles are why the filing can be re-checked when the question comes a year later.

Primary sources: <https://stripe.com/docs/tax> and <https://en.wikipedia.org/wiki/Value-added_tax>.

## Decision rules

- One bundle per sale, assembled at processing time, stored with the sale record.
- The bundle carries the rule identifiers, not a narrative of the determination.
- Validation states and dates come along with the identifiers used.
- The evidence used is recorded, with values, not just referenced in the abstract.
- The mechanism — collection, zero-rate with identifier, or reverse charge — is named, and the tax amount or its zero is recorded.
- Sequence gaps, treatment changes, and evidence re-evaluations are dated events on the bundle, never edits to a previous state.

## Procedure

1. Enumerate the bundle's sections from the leaves' outputs: place of supply, identifiers, evidence, mechanism, display basis, amounts.
2. Assemble at sale-processing time, in the same transaction as the charge.
3. Store with the sale's identifier and the invoice's serial for two-way lookup.
4. Emit amendment events — never in-place edits — for later changes in any input.
5. Aggregate bundles for the filing period queries, with the bundle as the unit auditors sample.
6. Archive for the longest archival period among the applicable jurisdictions.

## Anti-patterns

- A bundle built from the payment record at year-end by inference.
- Rule names recorded without their versions or the evidence values used.
- A tax amount with no mechanism named, or a zero with no reason.
- Bundles that silently changed after the sale because a later re-evaluation edited them in place.
- Storage that expires before the shortest applicable archival period.

## Done checklist

- [ ] Bundle schema enumerated from the leaves.
- [ ] Assembly at processing time, transactional with the charge.
- [ ] Identifiers with validation dates.
- [ ] Evidence with values recorded.
- [ ] Mechanism and amount paired.
- [ ] Amendment events dated, archived for the longest period.

## Sources

- Stripe Tax, reporting and record behaviour: <https://stripe.com/docs/tax>
- Value-added tax context: <https://en.wikipedia.org/wiki/Value-added_tax>
- Consumption tax comparison: <https://en.wikipedia.org/wiki/Consumption_tax>
