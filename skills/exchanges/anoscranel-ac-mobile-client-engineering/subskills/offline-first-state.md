---
name: offline-first-state
domain: software-engineering/offline-first-state
trigger: "Designing state that must work without a network and reconcile later."
anti_trigger: "Not for server-side caching, and not for API contract design."
scope: "Local persistence, sync, and conflict resolution when the device was offline."
status: seedling
---

# Offline-first state

## Standard

An offline-first client treats the local store as the source of truth for the user's session and the server as a synchronisation target. That inversion is what makes the app usable on a train, and it is also what creates the hard problem: two writes can occur against the same record, one local and one remote, and the client must decide which wins without knowing what the user intended.

The decision is a policy, and it must be chosen per entity rather than globally. Last-write-wins is simple and loses data silently; server-wins discards local work; merge functions need a domain model that can express the merge. The honest approach is to record which entities tolerate which policy, and to surface the conflict to the user where none of them is acceptable.

Primary sources: <https://developer.android.com/> and <https://developer.apple.com/>.

## Decision rules

- Record which entities are cached locally and whether they are read-only or writable offline.
- Record the conflict policy per entity and why it was chosen.
- Record the ordering guarantee: whether the server applies operations in the order they were made.
- Record the idempotency key that makes a retried write safe.
- Record what the user sees when a conflict is resolved against them.
- Record the size limit of the local store and what happens when it fills.

## Procedure

1. List the entities and classify them by offline writability.
2. Choose a conflict policy per entity and record the reasoning.
3. Attach an idempotency key to every write that can be retried.
4. Record the queue's ordering and its persistence across app restarts.
5. Define the conflict surface shown to the user.
6. Test the offline path explicitly, including a week offline.

## Anti-patterns

- Applying last-write-wins globally because it is the default.
- Losing a queued write when the app is killed.
- Retrying a write without an idempotency key.
- Assuming the server receives operations in the order they were made.
- Testing offline mode for a minute rather than for a realistic period.

## Done checklist

- [ ] Entities classified by offline writability.
- [ ] Conflict policy recorded per entity.
- [ ] Idempotency keys recorded.
- [ ] Queue ordering and persistence recorded.
- [ ] Conflict surface defined.
- [ ] Long-offline path tested.

## Sources

- Android data and persistence guidance: <https://developer.android.com/>
- Apple platform data guidance: <https://developer.apple.com/>
- Web platform storage reference: <https://www.w3.org/>
