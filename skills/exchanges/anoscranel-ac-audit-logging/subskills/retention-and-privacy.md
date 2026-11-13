---
name: retention-and-privacy
domain: software-engineering/retention-and-privacy
trigger: "Resolving the collision between retaining evidence and erasing personal data."
anti_trigger: "Not for legal advice, and not for general privacy programme design."
scope: "Retention law, personal data in the trail, and redaction without rewriting."
status: seedling
---

# Retention and privacy

## Standard

An audit trail pulls in two directions at once. Its integrity requires keeping every entry; privacy law in many jurisdictions requires erasing personal data on request or on schedule. The collision is structural — the entries that carry the strongest protection also carry names, identifiers, and addresses — and the design has to resolve it before the first request, because a chain cannot be edited to remove a name without breaking the very property the log exists for.

The engineering options are limited and the record should pick one deliberately rather than discover it under deadline. Minimise identity at write time — pseudonymous actor identifiers with a separate, access-controlled mapping — so erasure touches the mapping, not the chain. Or scope the retention window so entry deletion is planned, bounded, and chain-preserving. What is not an option is editing history in place, and the design says so explicitly.

Primary sources: <https://csrc.nist.gov/pubs/sp/800/92/final> and <https://w3.org/TR/trace-context>.

## Decision rules

- Record the retention requirement that applies and its authority, with the accountable officer named.
- Minimise personal data in the trail at write time; pseudonymise the actor.
- If identifiers must appear, record the planned deletion path that does not rewrite the chain.
- Keep the identity mapping access-controlled and covered by the same retention rule.
- Record the decision path when erasure and integrity conflict, before any conflict arrives.
- Never redact by editing entries; annotate or map instead.

## Procedure

1. Identify the retention regime with the accountable officer.
2. Classify every entry field for personal-data content.
3. Pseudonymise the actor and hold the mapping separately.
4. Define the bounded retention window and its chain-preserving deletion.
5. Write the conflict decision into the audit record.
6. Review the design when the retention regime or scope changes.

## Anti-patterns

- Names and email addresses written into a chain that cannot legally keep them.
- Editing entries to remove a subject's data, breaking the chain.
- Retention decided by storage cost rather than the applicable rule.
- The mapping granting identity kept for longer than the trail lawfully retains.
- Conflicts resolved by whoever receives the deletion request first.

## Done checklist

- [ ] Retention regime recorded with the authority.
- [ ] Fields classified for personal data.
- [ ] Actor pseudonymised.
- [ ] Deletion path chain-preserving.
- [ ] Conflict rule written down.
- [ ] Review triggered on regime change.

## Sources

- Log retention and protection guidance: <https://csrc.nist.gov/pubs/sp/800/92/final>
- Request context and identity fields: <https://w3.org/TR/trace-context>
- Control expectations for audit evidence: <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
