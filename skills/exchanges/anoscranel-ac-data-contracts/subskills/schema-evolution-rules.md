---
name: schema-evolution-rules
domain: software-engineering/schema-evolution-rules
trigger: "Changing a dataset's schema without breaking its consumers."
anti_trigger: "Not for database migration mechanics, and not for event versioning between services."
scope: "Additive versus breaking, and who bears the migration."
status: seedling
---

# Schema evolution rules

## Standard

A schema change is additive or breaking, and the classification is decided by the consumer rather than the producer. Adding a nullable column is additive for a reader that selects named columns and breaking for one that selects everything positionally. Removing a column is breaking for anyone who read it. Changing a type is breaking unless the new type is a widening that every reader can accept.

The rules should therefore be stated in terms of consumer behaviour, and the migration burden should be assigned rather than assumed. A common arrangement is that the producer keeps a field until every registered consumer has stopped reading it, which requires knowing who the consumers are — which is what the registration in the contract provides.

Primary sources: <https://www.w3.org/> and <https://csrc.nist.gov/>.

## Decision rules

- Record the compatibility rule the contract enforces: backward, forward, or full.
- Record what counts as additive and what counts as breaking for this dataset's consumers.
- Record the deprecation period before a breaking change, and how it is announced.
- Record who bears the migration cost, which is usually the consumer unless the producer offers a compatibility layer.
- Record the registry of consumers, since a change cannot be assessed against unknown readers.
- Record the dual-write or shadow period for changes that must be validated before cutover.

## Procedure

1. Record the compatibility rule.
2. Classify each change type against that rule.
3. Record the consumer registry and how it is maintained.
4. Record the deprecation period and notification.
5. Record the migration responsibility.
6. Write the policy with its classification table.

## Anti-patterns

- Assuming a nullable column is always additive.
- Dropping a column after one announcement.
- A consumer registry that is a spreadsheet nobody updates.
- Changing a type in place and calling it a widening when a reader cannot parse it.
- Leaving migration burden unassigned, so it falls on whoever notices.

## Done checklist

- [ ] Compatibility rule recorded.
- [ ] Change classification recorded.
- [ ] Consumer registry recorded.
- [ ] Deprecation period recorded.
- [ ] Migration responsibility recorded.
- [ ] Validation period recorded where needed.

The compatibility rule should also be recorded per consumer, not only per dataset: an internal dashboard that reads two columns tolerates changes a partner integration cannot, and a single blanket rule either over-constrains the producer or under-protects the partner.


## Sources

- Schema and compatibility standards: <https://www.w3.org/>
- Data governance guidance: <https://csrc.nist.gov/>
- Interface evolution context: <https://csrc.nist.gov/publications>
