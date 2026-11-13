---
name: isolation-record
domain: software-engineering/isolation-record
trigger: "Writing the record of a tenancy model and its test evidence."
anti_trigger: "Not for compliance attestation, and not for pen-test reporting."
scope: "The written record: model, boundary, enforcement point, and test evidence."
status: seedling
---

# Isolation record

## Standard

The isolation record states the tenancy model, the boundary it provides, every enforcement point, and the test evidence that each point actually enforces it. The evidence is what distinguishes the record from a design document: a claim that the database enforces isolation is worth more when accompanied by a test that attempted a cross-tenant read and failed.

Its second function is to survive staff turnover. The enforcement points are discovered by reading code, and the paths that assume rather than enforce are the ones a new engineer will not know about. Recording them, with the date of the last test, means the assumption is visible before it becomes an incident rather than after.

Primary sources: <https://owasp.org/> and <https://osf.io/prereg/>.

## Decision rules

- The record states the model and the consequence of a leak that justified it.
- Every enforcement point is listed with whether it enforces or assumes.
- Each enforcement point carries a test and the date it was last run.
- Derived stores are listed: caches, indexes, replicas, exports.
- Bypass roles and connections are recorded with their justification.
- Review triggers are dated: new data path, new derived store, model change, leak incident.

## Procedure

1. Record the model and its justification.
2. List enforcement points with enforce or assume.
3. Record a test per point and its last run date.
4. Record derived stores and their coverage.
5. Record bypass roles.
6. Set review triggers and amend at each.

## Anti-patterns

- Recording the design without the test evidence.
- Listing enforcement points but not the ones that assume.
- Omitting derived stores, which are usually the gap.
- No date on the last test, so the evidence may be stale.
- Treating a leak incident as closed without adding the path to the record.

## Done checklist

- [ ] Model and justification recorded.
- [ ] Enforcement points with status recorded.
- [ ] Tests and dates recorded.
- [ ] Derived stores recorded.
- [ ] Bypass roles recorded.
- [ ] Triggers dated.

The record is also the only place a new data path gets noticed before it ships: a checklist that asks for the enforcement point and a test for each new store means the search index and the analytics replica are considered when they are introduced rather than discovered during an incident.


## Sources

- Application security verification: <https://owasp.org/>
- Pre-registration practice for stated tests: <https://osf.io/prereg/>
- Security control guidance: <https://csrc.nist.gov/>
