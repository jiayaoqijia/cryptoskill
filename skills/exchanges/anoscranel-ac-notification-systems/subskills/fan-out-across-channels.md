---
name: fan-out-across-channels
domain: software-engineering/fan-out-across-channels
trigger: "Designing the one-event-to-many-channels delivery step."
anti_trigger: "Not for single-channel push mechanics, and not for template writing."
scope: "One event, many transports, and their differing contracts."
status: seedling
---

# Fan-out across channels

## Standard

Fan-out is the step where one event becomes several channel deliveries: the same fact rendered as an email body, a mobile push payload, an in-app badge, an SMS fragment. Each channel is a transport with its own contract — payload size limits, delivery semantics, retry conventions, and idempotency expectations — and the fan-out layer's job is to hold the shared meaning stable while adapting to each contract, rather than sending three semantically different messages that happen to share a template.

The stability that matters most is count and identity. The same event to the same user must yield at-most-one delivery per channel, and fan-out records the per-channel outcome separately — because the tribal knowledge that push silently fails while the email succeeded must be visible as data. Deduplication must happen before the sends, not after the complaints: one user resets a password on two devices, and the event-key discipline is what prevents a double SMS from one intent.

Primary sources: <https://developer.mozilla.org/en-US/docs/Web/API/Push_API> and <https://firebase.google.com/docs/cloud-messaging>.

## Decision rules

- Compose fan-out as one event → several channel-dedicated jobs; the per-channel job is the unit of retry and audit.
- Preserve at-most-one per channel with the event id, keying retries on the channel-specific job id.
- Record each channel's response as delivery data — accepted, rejected, queued, with the vendor's message id — and stamp the latency.
- Treat each transport as having its own idempotency rules: pass the event id down where the vendor supports it, and deduplicate at send time where it does not.
- Handle partial fan-out by design: a failed channel does not mark the whole event failed, and neither does it freeze the others.
- Render per channel at the last responsible moment: a mobile push payload and an email render from the same template contract with per-channel adapters.

## Procedure

1. List channels honestly supported, with their own retry and receipt behaviour documented.
2. Define per-channel jobs with their own ids, keyed to the event id.
3. Implement the send-one-job path exactly once, with idempotency protected by the job id + event id.
4. Record each transport's outcome, with accepted, rejected, queued, message id, and latency.
5. On a channel failure, record the failure and schedule the channel-specific backoff independently.
6. Review metrics once per period: delivered / rejected / failed per channel, compared against per-channel baselines.

## Anti-patterns

- Fan-out implemented per application module, each with its own templates and its own deduplication.
- Retrying the whole fan-out for one channel, resending a second unwanted email to fix a failed push.
- Treating a channel with no immediate error callback as delivered.
- A template whose mobile payload hard-codes what a web-related template omitted.
- Sending one event per channel per call-site processing its own retry, so an outage creates duplicate SMS.

## Done checklist

- [ ] One event yields several channel-dedicated jobs.
- [ ] Each channel has an explicit idempotency key.
- [ ] Each channel's response recorded as structured delivery data.
- [ ] Channel failures isolated per channel.
- [ ] Templates shared, with per-channel adapters.
- [ ] Fan-out metrics recorded and reviewed.

## Sources

- Web push: <https://developer.mozilla.org/en-US/docs/Web/API/Push_API>
- Firebase cloud messaging: <https://firebase.google.com/docs/cloud-messaging>
- Apple push and local notifications: <https://developer.apple.com/documentation/usernotifications>
