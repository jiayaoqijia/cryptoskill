---
name: anatomy-and-events
domain: software-engineering/anatomy-and-events
trigger: "Modeling a notification as data before choosing channels."
anti_trigger: "Not for channel API mechanics, and not for template copywriting."
scope: "The notification as data: event, recipient, template, and channels."
status: seedling
---

# Anatomy and events

## Standard

A notification is event data routed through templates to recipients on channels. The event — payment failed, mention created, build finished — is a fact with an actor, an object, a timestamp, and a priority. The notification is a derived artefact: the event plus what it should become for whom. Keeping that derivation explicit — event in, rendered notification out — prevents the classic defect where the notification is constructed ad hoc at each call site, so the same event arrives as three differently-worded, differently-prioritised interruptions across code paths.

Priority must be part of the event's contract, not a rendering afterthought: a security warning and a social mention differ not in wording but in how they may be deferred, batched, and suppressed. The model carries priority from the source, and the routing layer consumes it; rendering trivially from a shared template per channel reduces the fan-out problem to per-channel formatting of an agreed meaning.

Primary sources: <https://developer.mozilla.org/en-US/docs/Web/API/Push_API> and <https://developer.apple.com/documentation/usernotifications>.

## Decision rules

- Model the notification idempotently at the event level: an event id plus a recipient id form the operation key.
- Carry priority and category on the model — they are routing inputs, not decorations.
- Distinguish a notification from its event in the data model: one event fans to several notification records, each per channel.
- Define the template as the data-facing interface: variable names, variable types, fallback text.
- Bind the event id, the timestamps of the event, and the model version — this is the audit lineage of the interruption.
- Keep the model free of source-specific header fields; those are fan-out additions, not universal properties.

## Procedure

1. List distinct events that generate notifications, each with actor, object, and priority class.
2. Define the notification model: the event id, recipient, category, priority, and template identifier, all explicit fields.
3. Declare a stable template-variable contract for each category.
4. Migrate any existing inline constructions into events + templates.
5. Record for each model the idempotency key and the expected channel behaviour.
6. Verify the send site: it produces one event, not several channel-specific hand-rolled strings.

## Anti-patterns

- Constructing the notification at each call site, so wording and priority drift across code paths.
- Priority decided by the channel code, producing the same event at different priorities on different channels.
- A model missing an event id, so retries can never be recognised as duplicates.
- Templates whose variable names differ per channel, so the fan-out writes per-channel glue code.
- No timestamp on the model, so a vendor delay cannot be distinguished from a late send decision.

## Done checklist

- [ ] Events inventoried with priority classes.
- [ ] Model carries event id, recipient, category, priority.
- [ ] Template contract declared per category.
- [ ] Idempotency key defined at event × recipient.
- [ ] Send site emits one event, not per-channel strings.
- [ ] Model version recorded for audit lineage.

## Sources

- Web push overview: <https://developer.mozilla.org/en-US/docs/Web/API/Push_API>
- Local notifications on Apple platforms: <https://developer.apple.com/documentation/usernotifications>
- FCM primary docs: <https://firebase.google.com/docs/cloud-messaging>
