---
name: workflow-record
domain: software-engineering/workflow-record
trigger: "Writing the record of a durable workflow and its failure paths."
anti_trigger: "Not for runbook documentation, and not for API documentation."
scope: "The written record: states, compensations, timeouts, and versioning policy."
status: seedling
---

# Workflow record

## Standard

The workflow record states the states and transitions, the compensation for each step, the timeouts and heartbeat expectations, the versioning policy, and the manual paths for steps that cannot be compensated. Those five items are what an operator needs when an instance is stuck, and none of them is visible from the code without reading the whole definition.

Its second function is to make the failure paths testable. Each compensation has a test that runs it, each timeout has a test that reaches it, and each manual path has a documented owner. A workflow whose compensations have never executed is a workflow with unverified behaviour on its most consequential path.

Primary sources: <https://www.enterpriseintegrationpatterns.com/> and <https://osf.io/prereg/>.

## Decision rules

- The record states the states and the transitions between them.
- Each step records its compensation, or records that it has none and names the manual path.
- Timeouts and heartbeat intervals are recorded with their margins.
- The versioning policy records how a change is introduced and how old versions retire.
- The approval steps record their deadline and default action.
- Each compensation and timeout cites a test that exercises it.

## Procedure

1. Record the state model and transitions.
2. Record compensations and the manual paths.
3. Record timeouts and heartbeats.
4. Record the versioning policy.
5. Record approval deadlines and defaults.
6. Attach a test to each compensation and timeout.

## Anti-patterns

- Recording the happy path and leaving failure behaviour to the reader.
- Compensations with no test.
- A versioning policy that exists only as a convention.
- No owner for a manual path, so it is never executed.
- Describing the workflow in prose when a state list is what an operator needs.

## Done checklist

- [ ] States and transitions recorded.
- [ ] Compensations and manual paths recorded.
- [ ] Timeouts and heartbeats recorded.
- [ ] Versioning policy recorded.
- [ ] Approval defaults recorded.
- [ ] Tests attached.

The record should also state the maximum expected lifetime of an instance, since that number drives the versioning policy, the retention of workflow state, and the alert that fires when an instance exceeds it. A workflow with no stated lifetime accumulates stuck instances quietly.


Keeping the record beside the definition, rather than in a separate document, is what makes it survive: a workflow whose failure paths are documented in a wiki diverges from its code within a quarter, while one whose record is reviewed in the same change as the definition stays accurate.


## Sources

- Workflow patterns: <https://www.enterpriseintegrationpatterns.com/>
- Pre-registration practice for stated tests: <https://osf.io/prereg/>
- Distributed systems practice: <https://aws.amazon.com/builders-library/>
