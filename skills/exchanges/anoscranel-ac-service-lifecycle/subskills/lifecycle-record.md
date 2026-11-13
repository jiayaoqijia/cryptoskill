---
name: lifecycle-record
domain: software-engineering/lifecycle-record
trigger: "Writing down how the service starts, serves, and stops."
anti_trigger: "Not for recommending a runtime, and not for a runbook dump."
scope: "The written record: startup steps, drain plan, deadlines, and health semantics."
status: seedling
---

# Lifecycle record

## Standard

The lifecycle record documents the two edges of the service's existence: the ordered startup steps with their blocking and degrading rules, and the drain plan with its deadline and dispositions. It exists because lifecycle correctness is invisible in steady state and catastrophic only at the moment of restart, deploy, or failure — precisely when nobody has time to read code.

The most valuable sections are the deadlines and the dispositions. The deadlines: graceful window, external kill timeout, and the margin between them, so that any change to one is visible against the other. The dispositions: which in-flight work completes, which checkpoints, which hands off to a queue, and which outward effects carry idempotency keys. A record without these is a topology diagram with no timing in it.

Primary sources: <https://sre.google/> and <https://osf.io/prereg/>.

## Decision rules

- The record lists startup steps in order, each marked blocking or degrading.
- The record states the drain sequence, the graceful deadline, and the external kill timeout with the margin.
- The record lists the in-flight disposition per work type.
- The record states liveness versus readiness semantics and what each checks and omits.
- Amendments carry dates; a deadline change is visible as a change.
- The record is re-tested after any dependency, runtime, or timeout change.

## Procedure

1. Record the startup steps with blocking and degrading marks.
2. Record the drain sequence and both deadlines with the margin.
3. Record the in-flight dispositions.
4. Record the health semantics and exclusions.
5. Date every amendment.
6. Re-run the lifecycle tests after each change that could alter the edges.

## Anti-patterns

- A record of what the service does at steady state, with nothing about the edges.
- Deadlines recorded once, then drifted by config while the record stays.
- No dispositions, so each termination decides anew and differently.
- A readiness description that does not match the deployed checks.
- Untested after the last dependency migration.

## Done checklist

- [ ] Startup steps ordered and marked.
- [ ] Drain sequence and deadlines with margin.
- [ ] Dispositions per work type.
- [ ] Health semantics with exclusions.
- [ ] Amendments dated.
- [ ] Tests re-run after changes.

One entry belongs in the record no matter how short the service's life has been: the measured drain duration at peak load, refreshed after every significant traffic change. A drain plan that assumes the traffic of last quarter quietly exceeds its own deadline after growth, and the external kill starts winning exactly when the service has the most connections to lose.

## Sources

- Lifecycle and reliability practice: <https://sre.google/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Deployment patterns: <https://martinfowler.com/>
