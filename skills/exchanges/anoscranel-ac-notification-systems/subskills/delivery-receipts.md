---
name: delivery-receipts
domain: software-engineering/delivery-receipts
trigger: "Interpreting delivery and read receipts honestly across channels."
anti_trigger: "Not for template design, and not for vendor selection."
scope: "Receipts as facts, idempotency pre-send, and retry discipline."
status: seedling
---

# Delivery receipts

## Standard

Receipts are channel-specific facts with different meanings: an accepted API response is a fact about the transport receiving the message, not the user seeing it; a delivered receipt indicates that it reached the platform's delivery mechanism for the end device; a read receipt indicates engagement with a rendered message. These stages differ per channel in which of them even exist — email has delivery and opens, web push has at-most platform-level delivered, in-app has opened-because-visited — and any platform that flattens them into a single delivered state will be misread by anyone who trusts it.

Read receipts carry a strong signal and a weak guarantee. The being-honest rule is: measure them as a stronger signal, but do not confuse the absence of a read receipt with absence of a notification, because the same system that does not show a read receipt often shows the message. The corresponding discipline is idempotency pre-send: an event processed twice must result in at-most-one user-visible artefact, and only a pre-send idempotency block can guarantee that — resending after a partial failure is not idempotency, it is duplication hoping to be useful.

Primary sources: <https://firebase.google.com/docs/cloud-messaging> and <https://developer.apple.com/documentation/usernotifications>.

## Decision rules

- Model receipts per channel and per stage: transport-accepted, platform-delivered, engaged — each a distinct, recorded fact.
- Never collapse receipt stages into a single delivered flag; the ambiguity is the defect.
- Idempotency pre-send: the event id plus recipient plus channel is the unique key, checked before any send.
- Vendor delivery counts are a vigilance measure, not a success metric: an accepted response with no displayed notification is a recorded fact, not a contradiction to hide.
- A read receipt is engagement data, and only valid for the channel it comes from; do not infer results on other channels from it.
- Retry logic requires per-channel backoff, with idempotency guaranteed by the same unique key as the original send, or it must not retry at all.

## Procedure

1. Define the receipt stages possible per channel in a single table with the exact vendor event names.
2. Store each stage as a separate fact keyed by the channel job id.
3. Implement the idempotency check at the beginning of the send job, before rendering or vendor calls.
4. Map vendor webhook responses into stage facts, with vendor-specific event names recorded.
5. Query each channel's stage facts separately, using engagement only per the channel it originates from.
6. On a vendor disagreement (an accepted send with no platform-delivered), record the disagreement and investigate through the vendor's diagnostics, not by assumption.

## Anti-patterns

- An event processed twice, resending duplicate SMS that the user reads as harassment.
- A read receipt absence treated as a delivery failure and triggering a send by a second channel.
- Vendor accepted-level responses reported in the success metric, with platform delivered never measured.
- Using email open and push delivered interchangeably in a single funnel metric.
- A recipient-status model where "delivered means we called the API" is the stable definition.

## Done checklist

- [ ] Receipt stages defined per channel.
- [ ] Stages stored as distinct facts, keyed by job id.
- [ ] Idempotency check pre-send, on event × recipient × channel.
- [ ] Vendor webhook mapped to stages, with vendor event names recorded.
- [ ] Engagement signal measured per-originating channel only.
- [ ] Vendor disagreements investigated via diagnostics, not retried blindly.

## Sources

- FCM message delivery: <https://firebase.google.com/docs/cloud-messaging>
- Apple user notifications: <https://developer.apple.com/documentation/usernotifications>
- Web push lifecycle: <https://developer.mozilla.org/en-US/docs/Web/API/Push_API>
