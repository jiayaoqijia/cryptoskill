---
name: client-delivery-realities
domain: software-engineering/client-delivery-realities
trigger: "Accounting for the delivery loss between an event firing and arriving."
anti_trigger: "Not for warehouse delivery semantics, and not for privacy of the payload."
scope: "Beacons, batching, lifecycle loss, and the gap between fires and arrives."
status: seedling
---

# Client delivery realities

## Standard

An event firing and an event arriving are different states of the world. The browser fires the event into JavaScript and the delivery layer converts it into a beacon — a request that survives page unload by design, or does not if the wrong transport is used — and the loss class between firing and arriving is not an error: it is the operating environment. The last-page-view of a session, the events during a crash, the events fired during a cross-app transition: the pattern is that events tied to lifecycle endings are disproportionately absent, and unaccounted for.

The mechanics that matter: beacons exist precisely because unload-time requests cannot rely on an in-flight request surviving, so any event fired at a lifecycle boundary uses the beacon API or an equivalent. Batching trades loss for volume: a batch manager with a time window (e.g. batch every 10 seconds) gains efficiency and absorbs the cost of events that never send when the window never closes because the tab closed. The design decision is which events may batch — analytic events sized to absorb loss — and which must fire immediately because the question they answer is exit-y.

Primary sources: <https://developer.mozilla.org/en-US/docs/Web/API/Beacon_API> and <https://developer.mozilla.org/en-US/docs/Web/API/Navigator/sendBeacon>.

## Decision rules

- Lifecycle-boundary events (page unload, app exit) use the beacon or equivalent fire-and-forget transport.
- Analytics events may batch with a window; the batch-design trade-off is documented.
- The flush-on-unload logic exists in the batching design or the loss is accepted in writing.
- An instrumentation QA step fires the event set in a real browser with devtools network open to verify arrival.
- Most-load drop and transition drop are listed as known undercount classes in the record.
- lostevent counters — self-reported gaps where the client can detect its own loss remain optional but scoped.

## Procedure

1. Classify the event set by where in the lifecycle it fires.
2. Match each lifecycle class to its transport: beacon, batched, or immediate.
3. Write the flush-on-unload behavior and test it on a real unload.
4. Fire an event QA setup at each boundary (unload, crash, background).
5. Record each known loss class in the event record.
6. Re-check delivery on platform upgrade (new OS versions change lifecycle behavior).

## Anti-patterns

- XMLHttpRequest at unload: the request dies with the page, silently.
- Batch fires without flush-on-unload.
- Timing that assumes arrival-time — looking at clock skew in the record — is collection-time.
- Treating an absence-of-events window as "nothing happened" rather than "nothing was delivered".
- A taxonomy with no loss accounting anywhere.

## Done checklist

- [ ] Events classified by lifecycle class.
- [ ] Transports matched to class.
- [ ] Flush-on-unload implemented and tested.
- [ ] QA pass fired the set at each boundary.
- [ ] Loss classes documented in the record.
- [ ] Platform-upgrade re-check on the calendar.

## Sources

- Beacon API: <https://developer.mozilla.org/en-US/docs/Web/API/Beacon_API>
- sendBeacon method reference: <https://developer.mozilla.org/en-US/docs/Web/API/Navigator/sendBeacon>
- Idle-callback alternative for page-lifetime work: <https://developer.mozilla.org/en-US/docs/Web/API/Window/requestIdleCallback>
