---
name: sagas-and-compensation
domain: software-engineering/sagas-and-compensation
trigger: "Undoing partial work across services that cannot share a transaction."
anti_trigger: "Not for database rollback, and not for two-phase commit."
scope: "Compensating actions, ordering, and the fact that compensation is not rollback."
status: seedling
---

# Sagas and compensation

## Standard

A saga replaces a distributed transaction with a sequence of local transactions and a compensating action for each step. When a later step fails, the completed steps are undone by running their compensations in reverse order, which leaves the system in a state that is consistent even though it passed through intermediate states that were visible.

The critical misunderstanding is that compensation is not rollback. A rollback restores the previous state invisibly; a compensation performs another business action, which is visible, may fail, and may not be possible. A refund is not the inverse of a charge — it is a second transaction with its own fees, timing, and customer communication, and a shipped order cannot be un-shipped by a compensating call. The record should state, per step, what its compensation actually does and what it cannot undo.

Primary sources: <https://www.enterpriseintegrationpatterns.com/> and <https://aws.amazon.com/builders-library/>.

## Decision rules

- Record each step and its compensating action.
- Record whether the compensation is fully effective or merely mitigating, and what it leaves.
- Record the ordering: reverse of execution, and what happens if a compensation fails.
- Record the idempotency of each compensation, since a retry may run it twice.
- Record the steps with no compensation, which are the ones requiring a manual path.
- Record whether intermediate states are visible to users, since visibility changes what must be communicated.

## Procedure

1. List the steps and their compensations.
2. Record for each whether the compensation restores or mitigates.
3. Record the compensation order and failure handling.
4. Record idempotency per compensation.
5. Identify steps with no compensation and record the manual path.
6. Write the saga with its intermediate-state visibility.

## Anti-patterns

- Calling a compensation a rollback.
- A compensation that can fail without a recorded escalation.
- Compensations that are not idempotent and run twice on retry.
- Assuming a physical effect, such as a shipment, can be compensated.
- Hiding intermediate states from users who then see an unexplained reversal.

## Done checklist

- [ ] Steps and compensations recorded.
- [ ] Restore versus mitigate recorded.
- [ ] Order and failure handling recorded.
- [ ] Compensation idempotency recorded.
- [ ] Uncompensable steps and manual path recorded.
- [ ] Visibility of intermediate states recorded.

The compensation's own failure path deserves the same design as the forward path: if a refund fails, the saga cannot simply stop, and the escalation usually has to be a human queue with the state recorded, because a saga that silently ends in an inconsistent state is worse than one that pauses for intervention.


## Sources

- Saga and compensation patterns: <https://www.enterpriseintegrationpatterns.com/>
- Distributed systems practice: <https://aws.amazon.com/builders-library/>
- Workflow design context: <https://sre.google/>
