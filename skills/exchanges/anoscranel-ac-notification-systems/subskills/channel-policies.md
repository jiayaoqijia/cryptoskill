---
name: channel-policies
domain: software-engineering/channel-policies
trigger: "Deciding which channel carries which content at which urgency."
anti_trigger: "Not for template copy, and not for product tone decisions."
scope: "Which channel carries what, by urgency and content."
status: seedling
---

# Channel policies

## Standard

Each channel occupies a position on two axes: interruptiveness and durability. SMS interrupts hard and persists on a lock screen; push interrupts on the device if granted permission; email interrupts softly and endures searchably; the in-app badge and feed wait for the user to visit. These positions are not preferences — they are properties of attention — and a channel policy is the table that maps content classes onto them: a security-critical action interrupts hard, a social mention waits in-app, a receipt endures in email.

The policy exists because the inverse decision is made badly under deadline: code that needs to notify someone picks whatever API is closest, and the product discovers a year of finance alerts delivered as marketing-grade push. A written policy converts channel choice from a per-call-site judgment call into a data lookup keyed by the event's priority class, and the exceptions — including the ones the routing must support — include the reasoning, not just the override.

Primary sources: <https://developer.apple.com/documentation/usernotifications> and <https://developer.mozilla.org/en-US/docs/Web/API/Push_API>.

## Decision rules

- Classify events by required urgency class: security-critical, time-bounded, routine, ambient.
- Map each urgency class to allowed channels before writing any send code: what interrupts, what persists, what waits.
- Keep content-shape rules per channel: an SMS is short with the key fact; a push payload fits a lock screen; an email carries the durable record.
- Record exceptions with expiry and recall reasons; an exception without an expiry becomes the policy through attrition.
- Validate against the policy with checks, not convention: new send code looks up the policy, and needs an explicit override to differ.
- Review the policy against unsubscribe and disable rates: a channel flooded by policy violations shows up in the user's reaction.

## Procedure

1. Inventory events with their urgency classifications.
2. Write the channel policy table: event class → allowed channels, with the default channel.
3. Bind templates per channel with content-shape constraints.
4. Implement routing as a data lookup, requiring explicit recorded overrides for exceptions.
5. Review policy against delivery and engagement data per channel.
6. Record the policy version, exceptions, and reviews in the notification record.

## Anti-patterns

- A password reset sent by a channel the user can turn off as a preference.
- The same security alert marked urgent on one channel and marketing-class on another.
- An SMS that assumes the user reads the email that follows with the detail.
- An in-app feed polluted with security alerts because it was easiest to build.
- An exception granted in code review that never returned to the author.

## Done checklist

- [ ] Events classified by urgency.
- [ ] Channel policy table written.
- [ ] Content-shape rules per channel recorded.
- [ ] Routing as data lookup with explicit exceptions.
- [ ] Policy reviewed against disable rates.
- [ ] Policy version and exceptions in the record.

## Sources

- Apple notification categories: <https://developer.apple.com/documentation/usernotifications>
- Web push permissions: <https://developer.mozilla.org/en-US/docs/Web/API/Push_API>
- Cross-platform push service: <https://firebase.google.com/docs/cloud-messaging>
