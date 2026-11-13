---
name: data-inventory-and-purpose
domain: software-engineering/data-inventory-and-purpose
trigger: "Establishing what personal data the system holds and why."
anti_trigger: "Not for legal interpretation, and not for security threat modelling."
scope: "What personal data exists, where, and why each field is collected."
status: seedling
---

# Data inventory and purpose

## Standard

A data inventory records, for each personal-data field, where it is stored, which systems read it, why it was collected, and how long it is kept. Its value is not the document; it is the traceability: given a field, you can name the systems that hold a copy, which is the precondition for answering any request or applying any retention rule.

Inventories fail when they are assembled as a snapshot rather than maintained as a register. A system that adds a field without registering it produces an inventory that is correct at a date and wrong within a quarter, and the wrongness is invisible until a request arrives that cannot be answered completely.

Primary sources: <https://ico.org.uk/> and <https://www.nist.gov/privacy-framework>.

## Decision rules

- Record each field with its purpose, its legal basis as determined by counsel, and its systems of record.
- Record derived copies: logs, caches, search indexes, analytics, and data warehouse tables.
- Record the system owner for each entry, since an unowned entry is never updated.
- Record the mechanism that requires a new field to be registered before it ships.
- Record third-party recipients per field, not per system.
- Record the date of the last review and the trigger for the next.

## Procedure

1. Enumerate personal-data fields from the schema and from the event streams.
2. Record purpose and systems of record for each.
3. Trace derived copies into logs, caches, and analytics.
4. Assign an owner per entry.
5. Implement the registration step in the change process.
6. Review on a schedule and record the diff.

## Anti-patterns

- Building the inventory once for an audit and never updating it.
- Recording systems rather than fields, which hides the copies.
- Omitting derived stores because they are "just logs".
- Assigning ownership to a team without a named individual.
- Leaving the registration step outside the deployment path.

## Done checklist

- [ ] Fields enumerated with purpose and systems of record.
- [ ] Derived copies traced.
- [ ] Owners assigned per entry.
- [ ] Registration step in the change process.
- [ ] Third-party recipients recorded per field.
- [ ] Review date and trigger recorded.

The inventory also earns its keep when a system is retired: knowing which fields a service holds is what allows its shutdown to include the deletion of those fields, and a retirement without that step leaves personal data in a store nobody owns. Recording the retirement path per system turns a decommission into a completable task.


## Sources

- Data protection guidance for engineering: <https://ico.org.uk/>
- NIST privacy framework: <https://www.nist.gov/privacy-framework>
- Web privacy standards: <https://www.w3.org/Privacy/>
