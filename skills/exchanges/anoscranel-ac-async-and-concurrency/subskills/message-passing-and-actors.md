---
name: message-passing-and-actors
domain: software-engineering/message-passing-and-actors
trigger: "Designing concurrency around messages instead of shared memory."
anti_trigger: "Not for distributed queues between services, and not for event streaming."
scope: "Actors, mailboxes, ownership by isolation, and where message passing beats locks."
status: seedling
---

# Message passing and actors

## Standard

Message passing removes races by removing sharing: each actor owns its state outright, other components talk to it by sending messages, and only the actor's own thread of execution ever touches its data. A lock protects state everyone can still reach; a mailbox makes the state unreachable from everyone else. The concurrency question shifts from "who holds the lock" to "which messages arrive in which mailbox, and in what order".

The model's costs are its own. Ordering is a property of the channel, not of the clock — two messages sent from different places may arrive in either order, and a channel that guarantees ordering is a design feature, not a default. Backpressure must live somewhere, because an actor that cannot keep up accumulates an inbox, and the choice of unbounded mailbox, bounded queue, or drop policy is the system's overflow story. Deadlock does not disappear either: two actors waiting on each other's replies reproduce the classic cycle without a mutex in sight.

Primary sources: <https://martinfowler.com/articles/patterns-of-distributed-systems/> and <https://www.rfc-editor.org/rfc/rfc9000.html>.

## Decision rules

- Record which state each actor owns and verify no other path reaches it.
- Choose the mailbox policy deliberately: unbounded, bounded, or lossy.
- State the ordering guarantee per channel and what depends on it.
- Implement backpressure at the mailbox rather than at the sender's memory.
- Record request-response pairs and which awaits can deadlock a cycle.
- Prefer message passing where the state is naturally single-owner; prefer locks only where sharing is unavoidable and contended briefly.

## Procedure

1. Map each piece of shared state to a single owning actor.
2. Define the message types and the reply contracts between actors.
3. Choose mailbox policy and ordering per channel, and state both.
4. Implement backpressure and overflow behaviour.
5. Test ordering and overflow explicitly: concurrent senders, a full mailbox, a blocked actor.
6. Record ownership map, channel policies, and the deadlock review.

## Anti-patterns

- An "actor" that still exposes its state to callers.
- An unbounded mailbox with no overflow story, discovered at peak.
- Assuming cross-actor message ordering because the local send was sequential.
- Request-response pairs forming a cycle with no timeout or escape.
- Message passing as aesthetic: every state kept shared, with messages sent as notifications.

## Done checklist

- [ ] Ownership map complete; no shared state left unowned.
- [ ] Message and reply contracts defined.
- [ ] Mailbox policy and ordering recorded per channel.
- [ ] Backpressure and overflow behaviour tested.
- [ ] Deadlock cycle review done for request-response pairs.
- [ ] Decisions in the concurrency record.

## Sources

- Request-response, sequencing, and flow patterns: <https://martinfowler.com/articles/patterns-of-distributed-systems/>
- Flow control in a message protocol: <https://www.rfc-editor.org/rfc/rfc9000.html>
- Ordering and happens-before in concurrent code: <https://distill.pub>
