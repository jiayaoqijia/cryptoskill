---
name: audit-record
domain: software-engineering/audit-record
trigger: "Writing the design record for an audit trail."
anti_trigger: "Not for the log entries themselves, and not for compliance sign-off."
scope: "The written audit record: event set, chain, storage, and verification."
status: seedling
---

# Audit record

## Standard

The audit record is the trail's design document: the event set with its rationale, the identity scheme and where it can be lost, the chain and anchor parameters, the storage privileges and rotation process, the sequencing scheme and gap policy, the investigator's questions with their indexes, and the retention decision with its authority. It is written at design time because every one of these is a decision, and a decision made during an incident is a guess.

Its second function is the verification story. The record states how the chain is checked, how often, who is told on failure, and what the last verified anchor was — so that after an incident the question "was the trail intact at the relevant time" has an answer that is itself recorded, rather than reconstructed from memory. A trail whose verification history is not itself logged has a hole exactly where its credibility lives.

A record that names its own verification history also gives the incident review its first fact: if the gate-latest anchor predates the incident, the window in question was covered, and the argument moves from the trail's integrity to the trail's contents, which is where an investigation should spend its time.

Primary sources: <https://csrc.nist.gov/pubs/sp/800/92/final> and <https://www.rfc-editor.org/rfc/rfc6962.html>.

## Decision rules

- Record the event set with its derivation from the investigator's questions.
- Record identity source, propagation, and the actor classification scheme.
- Record hash function, chained bytes, anchor location, and anchoring schedule.
- Record storage privileges, the rotation process, and who may run it.
- Record sequencing, gap policy, and the verification cadence with alert routing.
- Record the retention decision, the accountable officer, and the conflict rule.

## Procedure

1. Write the event set and its derivation.
2. Write the identity scheme and its weak points.
3. Write the chain, anchor, and verification cadence.
4. Write the storage and rotation privileges.
5. Write the retention decision and conflict rule.
6. Amend by dated entries; keep released versions intact.

## Anti-patterns

- A trail in production with the design only in the implementer's memory.
- Verification cadence unspecified, so integrity checks are run never.
- The accountable officer for retention unnamed.
- Conflict between erasure and integrity left to be argued later.
- The record edited to match a later implementation, losing the design's history.

## Done checklist

- [ ] Event set recorded with derivation.
- [ ] Identity scheme and weak points recorded.
- [ ] Chain, anchor, cadence recorded.
- [ ] Storage and rotation recorded.
- [ ] Retention decision and conflict rule recorded.
- [ ] Amendments dated.

## Sources

- Audit and log management guidance: <https://csrc.nist.gov/pubs/sp/800/92/final>
- Chained-log structure and proofs: <https://www.rfc-editor.org/rfc/rfc6962.html>
- Audit evidence control expectations: <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
