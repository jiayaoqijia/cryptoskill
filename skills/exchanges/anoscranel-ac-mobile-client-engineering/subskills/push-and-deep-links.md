---
name: push-and-deep-links
domain: software-engineering/push-and-deep-links
trigger: "Designing push delivery and deep links that must survive install."
anti_trigger: "Not for in-app notifications, and not for store policy."
scope: "Delivery guarantees, tokens, and links that must survive install."
status: seedling
---

# Push and deep links

## Standard

Push delivery is best-effort at every layer. The platform may throttle it, the device may be offline or in a battery-saving state, and the token that identifies the device changes without notice when the app is reinstalled or restored to a new handset. A notification treated as a guaranteed delivery is a notification that will sometimes not arrive.

Deep links carry a parallel problem: a link clicked before the app is installed has to survive the store detour and arrive at the right screen after first launch. That deferred deep link is a platform-specific mechanism, and where it is unavailable the link must degrade to a web page rather than to the home screen.

Primary sources: <https://developer.android.com/> and <https://developer.apple.com/>.

## Decision rules

- Record the delivery semantics: best-effort, with no acknowledgement from the app.
- Record the token lifecycle and what triggers a refresh.
- Record the fallback for a notification that is not delivered.
- Record whether the payload is trusted, and validate anything that carries an action.
- Record the deferred deep-link mechanism and its degradation path.
- Record the handling of a link whose target no longer exists.

## Procedure

1. Record the delivery guarantee and state explicitly that it is best-effort.
2. Record token acquisition, refresh, and invalidation.
3. Record the in-app fallback for a missed notification.
4. Validate notification payloads before acting on them.
5. Record the deep-link routing table and the unknown-link fallback.
6. Test the uninstalled-link path on both platforms.

## Anti-patterns

- Treating a push as delivery confirmation.
- Assuming a device token is stable across reinstalls.
- Acting on a notification payload without validation.
- Routing a deep link to the home screen when the target is unknown.
- Ignoring the deferred-link path because it is awkward to test.

## Done checklist

- [ ] Delivery semantics recorded as best-effort.
- [ ] Token lifecycle recorded.
- [ ] In-app fallback recorded.
- [ ] Payload validation recorded.
- [ ] Deep-link routing table recorded.
- [ ] Deferred link path tested.

The deferred link also has a measurement problem: when it fails it fails silently, and the user simply arrives at the home screen, so the failure rate is unknown unless it is instrumented. Recording the arrival path for links that came through an install is the only way to know whether the mechanism works.


## Sources

- Android messaging guidance: <https://developer.android.com/>
- Apple notification and universal link guidance: <https://developer.apple.com/>
- Web linking standards: <https://www.w3.org/>
