---
name: human-in-the-loop
domain: software-engineering/human-in-the-loop
trigger: "Waiting for a human approval inside a durable workflow."
anti_trigger: "Not for authentication, and not for notification delivery."
scope: "Waiting for approval without holding a worker or a transaction."
status: seedling
---

# Human in the loop

## Standard

An approval step can wait for days, and the wait must not consume a worker, a connection, or a transaction. The durable approach records that the workflow is waiting, releases all resources, and resumes when a signal arrives — an approval, a rejection, or a timeout that decides what happens by default.

The default matters more than the mechanism. A workflow that waits without a deadline accumulates instances that nobody will finish, and a workflow whose timeout approves by default has a control that fails open. The record should state the deadline, the default action, and who is accountable when the deadline passes with nobody having acted.

Primary sources: <https://aws.amazon.com/builders-library/> and <https://www.enterpriseintegrationpatterns.com/>.

## Decision rules

- Record the approval step's inputs, so a reviewer sees what they are deciding.
- Record the deadline and the default action at expiry, which should be the safe one.
- Record how the signal is authenticated, since an unauthenticated approval is not a control.
- Record the escalation path when the deadline approaches.
- Record whether the approval can be withdrawn after it is given.
- Record the audit trail: who approved, when, and on what evidence.

## Procedure

1. Record the approver role and the information presented.
2. Record the deadline and the default action.
3. Record the signal's authentication and idempotency.
4. Record escalation before expiry.
5. Record withdrawal and reversal behaviour.
6. Write the step with the audit fields.

## Anti-patterns

- Holding a worker or a database transaction while waiting.
- A default action at expiry that approves.
- An approval signal that any caller can post.
- No escalation, so the step waits until someone notices.
- No record of what the approver saw, which makes the decision unauditable.

## Done checklist

- [ ] Approver role and inputs recorded.
- [ ] Deadline and default recorded.
- [ ] Signal authentication recorded.
- [ ] Escalation recorded.
- [ ] Withdrawal behaviour recorded.
- [ ] Audit fields recorded.

The approval also has a reversibility question: a decision taken on information that has since changed should be re-openable, and recording the evidence snapshot the approver saw is what allows a later review to establish whether the approval was still valid when acted on rather than only when given.


The waiting state also needs a visible queue: an approval that sits in a workflow engine's history is invisible to the people expected to act on it, so the step usually needs a projection into a review interface with an owner, an age, and a deadline.


## Sources

- Workflow and approval patterns: <https://aws.amazon.com/builders-library/>
- Process patterns: <https://www.enterpriseintegrationpatterns.com/>
- Security controls for approval: <https://csrc.nist.gov/>
