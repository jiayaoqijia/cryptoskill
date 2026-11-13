---
name: what-to-record
domain: software-engineering/what-to-record
trigger: "Deciding the event set and the identity an audit entry must carry."
anti_trigger: "Not for telemetry event choice, and not for access-control rules."
scope: "The event set, the actor identity problem, and the before-and-after state."
status: seedling
---

# What to record

## Standard

An audit entry exists to answer a question that will be asked later: who acted, what was the target, what changed, when, and from where. The minimum set is actor identity, action, target, the before and after state, and the timestamp — and the before-and-after is the part general logs omit and audit logs must keep, because "changed the config" is testimony while "changed it from A to B" is evidence.

Actor identity is the hard part. A service account is not a person; a request through three proxies carries a user identity that each hop must preserve or the trail names infrastructure instead of actors. The record should state how identity is established and where it can be lost — the entry that says "admin did X" when the actor was an automated pipeline is a misidentification that undermines every other entry's credibility.

Primary sources: <https://csrc.nist.gov/pubs/sp/800/92/final> and <https://w3.org/TR/trace-context>.

## Decision rules

- Record actor, action, target, before-state, after-state, and timestamp for every audited change.
- Carry the originating identity through every hop; record where identity is translated.
- Distinguish person, service account, and automated pipeline in the actor field.
- Record the source address or request context, and treat it as evidence.
- Decide the event set by the questions an investigator would ask, not by what is easy to log.
- Record denied attempts as well as successful ones — a refusal is a fact.

## Procedure

1. List the questions an investigator would ask of this system.
2. Derive the event set from the questions, then prune nothing that answers one.
3. Define the actor field's identity source and its propagation path.
4. Add before-and-after capture to each state-changing action.
5. Include denied and failed actions in the set.
6. Record the event set and identity scheme in the audit record.

## Anti-patterns

- Logging actions without state, so the trail says that but not what.
- Service-account actors recorded as if they were people.
- Identity dropped at the first proxy hop.
- Only successful actions logged, making probes invisible.
- The event set chosen by whatever the framework logs by default.

## Done checklist

- [ ] Investigator questions listed.
- [ ] Event set derived from them.
- [ ] Identity source and propagation defined.
- [ ] Before-and-after captured.
- [ ] Denied actions included.
- [ ] Event set recorded.

## Sources

- Log management and audit guidance: <https://csrc.nist.gov/pubs/sp/800/92/final>
- Identity propagation across hops: <https://w3.org/TR/trace-context>
- Security log content guidance: <https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final>
