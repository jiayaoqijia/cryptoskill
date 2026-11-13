---
name: ownership-and-escalation
domain: software-engineering/ownership-and-escalation
trigger: "Making someone accountable for a dataset's guarantees."
anti_trigger: "Not for incident command, and not for access control."
scope: "Who is accountable, and what happens when the contract is breached."
status: seedling
---

# Ownership and escalation

## Standard

A contract without an owner is a document with nobody behind it. Ownership means a named team that is accountable for the dataset's guarantees, reachable when they are broken, and empowered to change them. The team matters rather than the individual, because an individual changes role and the contract does not.

Escalation is the part that makes ownership real. When freshness is breached, there must be a route from the consumer's alert to the owner's attention, with a stated response expectation. A contract whose breach produces a ticket in a queue is a contract whose guarantees are advisory, and consumers learn to distrust the dataset even when it is usually correct.

Primary sources: <https://sre.google/> and <https://csrc.nist.gov/>.

## Decision rules

- Record the owning team and the escalation route, with a channel rather than an individual.
- Record the response expectation for a breach: acknowledgement time and resolution target.
- Record who is authorised to change the contract, since a contract edited by consumers is not a contract.
- Record the process for a consumer requesting a change to a guarantee.
- Record the decommissioning path: how a dataset is retired and how consumers are told.
- Record what happens to a contract when the owning team is disbanded.

## Procedure

1. Record the owning team and channel.
2. Record the acknowledgement and resolution expectations.
3. Record change authority.
4. Record the request process for a guarantee change.
5. Record the decommissioning path.
6. Write the ownership model with its escalation.

## Anti-patterns

- An owner recorded as an individual.
- A breach that files a ticket into a shared queue.
- A contract that consumers can edit.
- No decommissioning path, so datasets accumulate and nobody knows which are live.
- An owning team that has been reorganised and no longer exists.

## Done checklist

- [ ] Owning team and channel recorded.
- [ ] Response expectations recorded.
- [ ] Change authority recorded.
- [ ] Request process recorded.
- [ ] Decommissioning path recorded.
- [ ] Reorganisation handling recorded.

The escalation route should also be tested, not only documented: a channel that nobody monitors reads as ownership while functioning as an absence, and a periodic test page to the owning team is the only way to know the route works before a consumer needs it.


## Sources

- Service ownership practice: <https://sre.google/>
- Governance and control guidance: <https://csrc.nist.gov/>
- Incident escalation context: <https://sre.google/workbook/table-of-contents/>
