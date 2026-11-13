---
name: optimistic-updates
domain: software-engineering/optimistic-updates
trigger: "Applying a write before the server confirms it, and taking it back on failure."
anti_trigger: "Not for designing the write API, and not for offline queues."
scope: "Instant writes, rollback on failure, and reconciliation."
status: seedling
---

# Optimistic updates

## Standard

An optimistic update shows the user the result of their action before the server confirms it. The copy is a promise: the UI now displays a state that is not yet true, and the client owes the user either the confirmation or a visible retraction. The promise is worth making when the write succeeds often and the experience gain is real: likes, edits, reorders. It is a lie, not a feature, when failures are common or when the server's response materially changes what should be shown.

Rollback is the part that ships last and breaks first. The three patterns are: restore-from-snapshot (capture the affected copy, put it back), inverse-apply (apply the operation's undo), and refetch (drop the copy and pull the truth). Snapshot is simplest and always correct; inverse-apply scales but must mirror the forward path exactly; refetch trades a flicker for guaranteed correctness. Whichever is chosen, the user must see that the action failed, in more than a console log.

Primary sources: <https://tanstack.com/query/latest/docs/framework/react/overview> and <https://web.dev/learn/performance>.

## Decision rules

- Justify optimism per action: high success rate plus meaningful latency cost, not a blanket default.
- Choose the rollback pattern per action and implement it with the optimistic path, never after.
- Users are told when the write fails — a retraction without notification is silent data loss.
- Server responses win: reconcile the local copy with the server's actual state on return.
- Pessimistic is the correct choice for money, permissions, and anything a user cannot see reversed.
- Concurrent mutations to the same key need ordering or last-write-wins, chosen and stated.

## Procedure

1. Classify the action's failure rate and latency cost; decide optimistic versus pessimistic.
2. Choose the rollback pattern: snapshot, inverse-apply, or refetch.
3. Implement apply, rollback, and reconcile together.
4. Add the failure notification path.
5. State the concurrency rule for simultaneous writes to one key.
6. Test the failure path explicitly: server error, timeout, and contradicted response.

## Anti-patterns

- Optimistic by default because a blog post said so.
- Applying the optimistic change with no rollback implemented.
- Rollback that restores stale data when the server also wrote something else.
- Optimism on payments or permission changes.
- Treating a returned error as success until the next refetch reveals it.

## Done checklist

- [ ] Optimism justified per action.
- [ ] Rollback pattern chosen and implemented.
- [ ] Failure visible to the user.
- [ ] Reconciliation with server response.
- [ ] Concurrency rule stated.
- [ ] Failure paths tested.

## Sources

- Data-layer mutation patterns: <https://tanstack.com/query/latest/docs/framework/react/overview>
- Rendering and interaction cost: <https://web.dev/learn/performance>
- Web platform devtools: <https://developer.chrome.com/docs/devtools/>
