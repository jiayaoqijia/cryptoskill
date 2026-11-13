---
name: consensus-record
domain: software-engineering/consensus-record
trigger: "Writing the record for a consensus deployment."
anti_trigger: "Not for recommending a protocol, and not for the library's documentation."
scope: "The written record of protocol, quorum, leases, and incident history."
status: seedling
---

# Consensus record

## Standard

The consensus record states what the deployment actually relies on: the protocol and its configuration, the quorum arithmetic with every member's role, the authority mechanism for stale leaders, and the membership-change procedure as it will be run. Its purpose is to make the next incident investigation start from facts rather than from the documentation of a library's defaults.

The entries that carry the most weight are the authority mechanism and the read classification. A lease-based system's safety lives in its clock assumptions, and a fencing-based system's safety lives in the enforcement points; writing which one the deployment uses, and where it is checked, is the single most useful line in the record. The second is the honest list of every read API and the consistency it returns, because most consensus incidents in practice are not lost writes but misread guarantees.

Primary sources: <https://raft.github.io/raft.pdf> and <https://osf.io/prereg/>.

## Decision rules

- The record states the protocol, version, and every configuration parameter that changes behaviour.
- The quorum arithmetic is written with each member's role and failure zone.
- The authority mechanism is named, with the clock assumption or fencing points stated.
- Every read API is listed with the consistency it returns.
- The membership-change runbook is included with its rollback.
- Incidents and their findings are logged, dated, with the invariant that was at risk.

## Procedure

1. Record protocol, version, and behaviour-changing parameters.
2. Write the quorum arithmetic with roles and zones.
3. Name the authority mechanism and its assumptions.
4. Classify every read API.
5. Attach the membership-change runbook.
6. Log incidents with the invariant at risk and date each entry.

## Anti-patterns

- Recording the protocol's name but not the configuration that changes its behaviour.
- Listing read APIs without the consistency each returns.
- Omitting the clock assumption from a lease-based record.
- No membership runbook, leaving the most delicate operation to improvisation.
- Treating incidents as resolved without naming the invariant that was at risk.

## Done checklist

- [ ] Protocol and parameters recorded.
- [ ] Quorum arithmetic with roles written.
- [ ] Authority mechanism and assumptions named.
- [ ] Read APIs classified.
- [ ] Membership runbook attached.
- [ ] Incidents logged with invariants and dates.

The record should also carry the deployment's arrest thresholds: the point at which a lagging follower is deemed too far behind to promote, and the point at which an operator must intervene rather than wait for catch-up.

## Sources

- Raft paper: <https://raft.github.io/raft.pdf>
- Stated conditions practice: <https://osf.io/prereg/>
- Distributed systems patterns: <https://martinfowler.com/articles/patterns-of-distributed-systems/>
