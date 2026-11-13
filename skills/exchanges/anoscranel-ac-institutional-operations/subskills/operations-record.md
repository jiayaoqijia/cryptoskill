---
name: operations-record
domain: investing/operations-record
trigger: "Writing the record of an institutional operational arrangement."
anti_trigger: "Not for legal advice, and not for recommending a provider."
scope: "The written record: counterparties, timelines, obligations, and escalations."
status: seedling
---

# Operations record

## Standard

The operations record names every counterparty in the chain, the deadline each stage must meet, the obligation that falls on each party, and the escalation path when something breaks. It is written before the first trade settles, because the moment a break occurs is the worst time to discover that nobody knows who owns the fix.

Its second function is continuity. Operations knowledge concentrates in individuals, and the record is what allows a different person to identify which affirmation is outstanding, which margin call is due, and which custodian holds which asset. A record that requires the original operator to interpret it is not a record; it is a memory with a filename.

Primary sources: <https://www.bis.org/> and <https://osf.io/prereg/>.

## Decision rules

- The record lists each counterparty with its role and the jurisdiction it sits in.
- Each stage has a deadline with a timezone and an owner.
- Each obligation is stated with the document that creates it.
- The escalation path is written with names or roles and time limits.
- Settlement, margin, and lending terms are referenced rather than duplicated.
- The record is reviewed on a schedule and after any change of counterparty.

## Procedure

1. List counterparties with roles and jurisdictions.
2. Record each stage with deadline and owner.
3. Record obligations and their source documents.
4. Write the escalation path.
5. Reference the terms rather than restating them.
6. Set the review schedule.

## Anti-patterns

- A record that lists counterparties without deadlines.
- Omitting timezones on cross-border stages.
- Restating legal terms instead of referencing them.
- An escalation path with no time limits.
- No review after a counterparty changes.

## Done checklist

- [ ] Counterparties listed with roles.
- [ ] Stages recorded with deadlines and owners.
- [ ] Obligations referenced to documents.
- [ ] Escalation path written.
- [ ] Terms referenced not duplicated.
- [ ] Review scheduled.

The record should also name the person who can authorise an exception: every operations chain has moments when a deadline cannot be met and someone must decide whether to accept the exposure, and leaving that decision unnamed means it is made by whoever is closest to the problem at the time.


A final field deserves its own line: the date the arrangement was last tested, whether by a reconciliation, a mock call, or a completed settlement. An untested arrangement is an assumption, and the record should say so rather than imply a capability that has never been exercised.


## Sources

- Market infrastructure and settlement standards: <https://www.bis.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Market structure context: <https://www.sec.gov/investor>
