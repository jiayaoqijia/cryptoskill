---
name: resilience-record
domain: software-engineering/resilience-record
trigger: "Writing the record of a service's failure behaviour."
anti_trigger: "Not for SLO documentation, and not for incident postmortems."
scope: "The written record: budgets, degradation modes, and their tests."
status: seedling
---

# Resilience record

## Standard

The resilience record states the timeout budget, the retry policy and its budget, the breaker thresholds, the bulkhead partitioning, the shedding policy, and the degradation mode for each dependency. Those six items describe what the service does when something fails, and none of them is visible from the code without reading several layers.

Its second function is to be testable. Each mechanism has a condition at which it engages, and the record should cite the test that demonstrates the condition is reached — a breaker that has never opened in a test is a breaker whose threshold is a guess. Recording the test alongside the setting converts an intention into evidence.

Primary sources: <https://sre.google/> and <https://osf.io/prereg/>.

## Decision rules

- The record states the end-to-end deadline and the per-call timeouts that fit inside it.
- The retry policy is recorded with its budget ratio and computed amplification.
- Breaker thresholds, probe size, and close conditions are recorded.
- Bulkhead partitioning and per-partition sizes are recorded.
- The shedding criterion and response are recorded.
- Each mechanism cites a test demonstrating it engages.

## Procedure

1. Record the deadline and the timeout budget.
2. Record retry policy, budget, and amplification.
3. Record breaker settings and transitions.
4. Record bulkheads and sizes.
5. Record shedding policy.
6. Attach a test to each mechanism and date them.

## Anti-patterns

- Recording settings without the test that they engage.
- A budget recorded for one dependency and not for the others.
- Degradation mode left implicit, so it is discovered during the incident.
- Recording the mechanism but not the fallback.
- No review trigger when a dependency is added.

## Done checklist

- [ ] Deadline and timeouts recorded.
- [ ] Retry policy and amplification recorded.
- [ ] Breaker settings recorded.
- [ ] Bulkheads recorded.
- [ ] Shedding policy recorded.
- [ ] Tests attached per mechanism.

The record is also the only artefact that makes a dependency change reviewable: adding a call means adding a timeout, a retry class, a fallback, and a test, and a checklist that requires those to be recorded is what prevents the new dependency from being the one path without a budget.


The record should also state which mechanisms were deliberately not deployed, and why: a service with no bulkhead because it has one dependency, or no circuit breaker because the call is already fail-fast, is a service whose design was considered. Absence that is recorded reads as a decision, while absence that is silent reads as an oversight.

## Sources

- Reliability engineering guidance: <https://sre.google/>
- Pre-registration practice for stated tests: <https://osf.io/prereg/>
- Failure handling context: <https://aws.amazon.com/builders-library/>
