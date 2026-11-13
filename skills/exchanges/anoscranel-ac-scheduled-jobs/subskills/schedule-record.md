---
name: schedule-record
domain: software-engineering/schedule-record
trigger: "Writing the register of every scheduled job and its semantics."
anti_trigger: "Not for capacity or runbook writing in general."
scope: "The written record: every job, its trigger, semantics, and owner."
status: seedling
---

# Schedule record

## Standard

The schedule record is the register of time-triggered work: every job, its trigger, its missed-run semantics, its overlap behaviour, its idempotency key scheme, its duration distribution, and its owner. It exists because scheduled work is the part of a system nobody remembers: it runs at 3am, it was added by someone who left, and the first question in any incident is always "what exactly is supposed to run, and what does the system do when it doesn't?"

The record turns the per-leaf decisions of this skill into one queryable inventory. When an outage window is planned, the record answers which jobs will miss triggers and what each will do. When a migration moves the scheduler, it enumerates what must move with it. And when a job mysteriously stops, its documented expected times are what the liveness monitor checks against.

## Decision rules

- Every job appears in the record with its trigger and expected run times.
- Missed-run semantics, overlap behaviour, and catch-up bounds are recorded per job.
- The idempotency key scheme is recorded so double-run tests can be reproduced.
- The job's owner and the downstream consumers of its output are named.
- Amendments are dated; a job's removal is recorded, not silently overwritten.
- The record is validated against the live scheduler periodically to detect drift.

## Procedure

1. Enumerate all jobs from the scheduler configuration.
2. Complete per job: trigger, semantics, key scheme, owner, consumers.
3. Record the duration distribution once measured.
4. Cross-check against the liveness monitor's expectations.
5. Audit the record against the scheduler after migrations.
6. Amend with dates, never silent overwrites.

## Anti-patterns

- An empty "owner" column that nobody can fill.
- Semantics recorded nowhere, so defaults masquerade as decisions.
- No drift audit, so the record and the scheduler disagree silently.
- Jobs removed without a record of the removal.
- Consumers unknown, so a stoppage's blast radius cannot be estimated.

## Done checklist

- [ ] All jobs enumerated with triggers.
- [ ] Semantics and key schemes recorded.
- [ ] Owner and consumers named.
- [ ] Duration distributions recorded.
- [ ] Drift audit scheduled.
- [ ] Amendments dated.

The record also earns its keep at blame time: when a consumer reports stale data, the register answers in one lookup whether the producer job was removed, its semantics changed, or its liveness monitor was never configured — three causes that look identical from the consumer's side.

## Sources

- Operational inventories and their audits: <https://sre.google/workbook/part-iii-automation/>
- Configuration as documentation: <https://learn.microsoft.com/en-us/azure/well-architected/>
- RFC 3339 timestamps for schedules: <https://www.rfc-editor.org/rfc/rfc3339>
