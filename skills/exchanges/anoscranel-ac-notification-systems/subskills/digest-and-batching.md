---
name: digest-and-batching
domain: software-engineering/digest-and-batching
trigger: "Designing how many events become how many interruptions."
anti_trigger: "Not for template design, and not for marketing campaign strategy."
scope: "When many events must become one interruption."
status: seedling
---

# Digest and batching

## Standard

When event rate is high, per-event notification is an attention tax. Digest and batching are the two structural answers: batching delays a notification to accumulate related events, and digest-composes them into one artefact. Their mechanics differ, and so do their costs. Batching adds latency in exchange for fewer interruptions; digesting preserves ordering information inside one message but loses timing entirely. The design principle is that interruption count, not message count, is the budget: counting notifications as events saved is the wrong metric when the user experiences them as one more unread badge.

The batch policy must be keyed to the event class, not to a global timer: a security-critical event never batches; identical mergeable events batch to a short window with the counts preserved; a time-bounded matter batches only while the window remains useful. Every batched notification must stand alone in content — "3 new mentions since yesterday" is honest; "you have new activity" is not — because the user who opens one batched notification must be able to act on it without opening a second.

Primary sources: <https://developer.apple.com/documentation/usernotifications> and <https://developer.mozilla.org/en-US/docs/Web/API/Push_API>.

## Decision rules

- Set the interruption budget per event class and per recipient, not globally: security bypasses the budget, social lives inside it.
- Batch window duration is proportional to event rate, with a stated minimum and maximum, and reasons for both.
- Batched notifications carry within themselves the counts and the time range, so they are actionable without opening another surface.
- Digest composition requires the state after the batch window, plus the unread state before, so that a recipient opening the digest sees intended meaning, not a machine listing.
- Never digest a time-bounded event into a lower-urgency class: batch the delivery, not the meaning.
- Measure interruptedness — the counted recipient-visible artefacts per day per recipient per category — not the number of events digested.

## Procedure

1. Classify events by interruptibility: never-batch, batch-to-window, always-digest.
2. For each batchable class, pick the window duration and the count-field formats.
3. Compose the digest from the same template contract as the individual notifications, with counts and the range.
4. Implement the batcher as a queue with a timer or trigger per class, checking the interrupt budget against the delay.
5. Verify per batched class: stand-alone test that a single open conveys what the user must do.
6. Record per-class policies and window durations in the notification record.

## Anti-patterns

- A global 5-minute batch timer applied to security events "for consistency".
- A digest that says new activity exists but not what, forcing a click to learn anything.
- Batching chosen because send cost is high, without revisiting when the rate changes.
- A digest that loses the time ordering that made the events coherent.
- Measuring digest efficiency by events merged, not interruptions avoided.

## Done checklist

- [ ] Events classified by interruptibility.
- [ ] Window durations with stated min and max.
- [ ] Batch message stands alone for action.
- [ ] Digest composed from before/after unread state.
- [ ] Time-bounded meaning never downgraded.
- [ ] Interruptedness measured per recipient-category.

## Sources

- Apple notification grouping: <https://developer.apple.com/documentation/usernotifications>
- Web push limits: <https://developer.mozilla.org/en-US/docs/Web/API/Push_API>
- Cross-platform messaging: <https://firebase.google.com/docs/cloud-messaging>
