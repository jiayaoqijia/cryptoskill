---
name: byzantine-record
domain: software-engineering/byzantine-record
trigger: "Writing the record for a Byzantine deployment."
anti_trigger: "Not for recommending a protocol, and not for the library's manual."
scope: "The written record of f, quorums, authentication, and evidence."
status: seedling
---

# Byzantine record

## Standard

The Byzantine record states the failure model and its arithmetic: the adversary the deployment claims, f and its replica count, the phase quorums, the authentication mechanism with its recovery path, and the evidence that the configuration was ever actually exercised. A Byzantine claim without these lines is a setting inherited from a tutorial, and the difference surfaces the first time a replica misbehaves.

The evidence entry is the one most often missing. Byzantine tolerance is a claim about behaviour under fault, and it is testable the way crash tolerance is: kill a replica deliberately, make one refuse in a scripted way, then observe whether agreement holds and for how long. The verification event is written down as performed — the same rule every record in the pack follows: state what was verified, not what was designed.

Primary sources: <https://pmg.csail.mit.edu/papers/osdi99.pdf> and <https://osf.io/prereg/>.

## Decision rules

- The adversary statement names who may be faulty and how many.
- f, the replica count, and phase quorums are stated.
- The authentication mechanism per message class is stated with its recovery path.
- The view-change trigger and its evidence threshold are stated.
- Fault-injection evidence is recorded as performed, with dates.
- Review triggers fire on membership change, protocol change, or incident.

## Procedure

1. Write the adversary statement and f.
2. Compute and record the quorum arithmetic.
3. Record authentication and recovery.
4. Record the view-change threshold and alarm.
5. Perform and record one deliberate fault injection.
6. Set review triggers and amend at each.

## Anti-patterns

- Recording the protocol's name instead of the deployment's f.
- No fault-injection evidence behind a tolerance claim.
- Authentication recorded without its recovery path.
- An adversary statement too vague to disagree with.
- No membership-change trigger, letting the arithmetic drift.

## Done checklist

- [ ] Adversary and f stated.
- [ ] Quorums computed and recorded.
- [ ] Authentication and recovery recorded.
- [ ] View-change threshold recorded.
- [ ] Fault injection performed and dated.
- [ ] Triggers set.

The record should also state the deployment's degradation posture: what the system does when it loses more replicas than f, whether it halts or serves stale reads, and who decides — because the honest answer to exceeding the fault budget is a designed behaviour, not an emergent one.

A one-line restatement of the arithmetic belongs at the head of the record — f, the replica count, the phase quorum — so that a reader in an incident sees the numbers before the prose that depends on them.

## Sources

- PBFT paper: <https://pmg.csail.mit.edu/papers/osdi99.pdf>
- Stated conditions practice: <https://osf.io/prereg/>
- Byzantine model reference: <https://en.wikipedia.org/wiki/Byzantine_fault>
