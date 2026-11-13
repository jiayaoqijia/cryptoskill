---
name: workflow-state-and-checkpoints
domain: software-engineering/workflow-state-and-checkpoints
trigger: "Making a long-running process resumable after a restart."
anti_trigger: "Not for event sourcing, and not for database transactions."
scope: "Durable state, replay, and what makes a resume correct."
status: seedling
---

# Workflow state and checkpoints

## Standard

A durable workflow records each step's completion before moving to the next, so a restart resumes from the last recorded point rather than from the beginning. The record must be written before the effect is acknowledged, or a crash between the effect and the record causes the step to run again — which is safe only if the step is idempotent, and is why the two mechanisms are designed together.

Replay is the second half. Some engines reconstruct the workflow by re-executing its code and returning recorded results for completed steps, which requires the code to be deterministic: a call to a clock, a random number, or an external service during replay produces a different answer than the one recorded, and the workflow diverges from its own history. Determinism is therefore a constraint on the code, not a property of the engine.

Primary sources: <https://aws.amazon.com/builders-library/> and <https://www.enterpriseintegrationpatterns.com/>.

## Decision rules

- Record what is persisted at each step and when, relative to the effect.
- Record whether the step is idempotent, since replay depends on it.
- Record the sources of non-determinism in the workflow code and how each is handled.
- Record the recovery point: where a restart resumes from and what it re-executes.
- Record the history size limit, since an unbounded history becomes a storage and replay cost.
- Record the retention of completed workflow state, which is a data question as much as an operational one.

## Procedure

1. List the steps and the state each persists.
2. Record the order of effect and record for each step.
3. Identify non-deterministic calls and record their treatment.
4. Record the resume point and what replays.
5. Record history limits and retention.
6. Write the state model with the determinism constraints.

## Anti-patterns

- Recording the step after the effect without idempotency.
- Calling a clock or a random source inside replayed code.
- An unbounded history that grows with every loop iteration.
- Assuming a resume re-runs nothing, when it re-executes code up to the last checkpoint.
- Retaining completed workflow state forever without a retention decision.

## Done checklist

- [ ] Persisted state recorded per step.
- [ ] Effect and record order recorded.
- [ ] Idempotency recorded per step.
- [ ] Non-determinism handled and recorded.
- [ ] Resume point recorded.
- [ ] History and retention limits recorded.

## Sources

- Distributed systems practice: <https://aws.amazon.com/builders-library/>
- Workflow and messaging patterns: <https://www.enterpriseintegrationpatterns.com/>
- Reliability context: <https://sre.google/>
