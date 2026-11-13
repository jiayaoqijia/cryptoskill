---
name: contract-enforcement
domain: software-engineering/contract-enforcement
trigger: "Making a data contract executable rather than documentary."
anti_trigger: "Not for API gateway policy, and not for access control."
scope: "Making the contract executable rather than documentary."
status: seedling
---

# Contract enforcement

## Standard

A contract that lives in a wiki is a description. A contract that is enforced by a registry, a schema definition in the repository, and a validation step in the pipeline is a contract. The difference appears at the first change: a documented contract is updated when someone remembers, while an enforced one fails the build when it is violated.

Enforcement has degrees. The weakest is validation at publish time, which prevents a producer from shipping a schema that contradicts the contract. A stronger form validates the data against the schema on every batch, which catches a producer that shipped conforming structure with non-conforming content. The strongest couples the registry to the consumers, so a breaking change is rejected unless every registered consumer has acknowledged it.

Primary sources: <https://www.w3.org/> and <https://csrc.nist.gov/>.

## Decision rules

- Record where the contract is defined: repository file, registry, or both.
- Record the validation point: publish, ingest, or query.
- Record what happens when validation fails, and whether it blocks or quarantines.
- Record whether the registry rejects a breaking change without consumer acknowledgement.
- Record the contract's version and how consumers pin to a version.
- Record the escape hatch, since a validation that cannot be bypassed in an emergency becomes an outage.

## Procedure

1. Record where the contract lives and how it is versioned.
2. Record the validation points and their behaviour on failure.
3. Record the change gate and its consumer acknowledgement step.
4. Record consumer pinning.
5. Record the emergency bypass and its audit.
6. Write the enforcement model with its failure behaviour.

## Anti-patterns

- A contract in a wiki that no pipeline reads.
- Validation only at publish, so content defects reach consumers.
- A change gate that any producer can override silently.
- No way to bypass validation during an incident.
- Consumers pinned to a version that is never retired.

## Done checklist

- [ ] Contract location and versioning recorded.
- [ ] Validation points recorded.
- [ ] Failure behaviour recorded.
- [ ] Change gate recorded.
- [ ] Consumer pinning recorded.
- [ ] Bypass and audit recorded.

The enforcement point also determines who discovers a violation: validation at publish tells the producer before consumers are affected, while validation at ingest tells the consumer after the data has already been attempted. Recording which point is authoritative prevents a gap where both sides assume the other validates.


## Sources

- Schema and interchange standards: <https://www.w3.org/>
- Control and audit guidance: <https://csrc.nist.gov/>
- Governance context: <https://csrc.nist.gov/publications>
