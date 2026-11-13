---
name: user-preferences-and-attention
domain: software-engineering/user-preferences-and-attention
trigger: "Designing the preference and quiet-hours model that gates sending."
anti_trigger: "Not for product tone, and not for template content."
scope: "Permission, quiet hours, batching windows, and not sending."
status: seedling
---

# User preferences and attention

## Standard

Every channel has a permission layer the user controls: push can be denied, email can be muted, SMS can be turned off in the app. The system's job is to model that gate on every channel per user, and to treat a permission loss as routing input — not a failure to retry into — meaning the channel silently becomes unusable and the user is not re-spammed; preference and permission are both routing inputs feeding the decision to send or to fall back.

The attention model is the same shape, inverted: when the user entrusts a channel, the sender chooses not to interrupt. Quiet hours and batching windows are explicit, and the highest-cost decision is not to send. The design that respects attention gets granted more of it; the design that spends it, gets the permission revoked. The safety net is the criterion: security-critical notifications have their own urgency class that can override quiet hours only within a policy that says what qualifies, because sending everything at 3am and sending nothing at 3am are both policy failures.

Primary sources: <https://developer.apple.com/documentation/usernotifications> and <https://developer.mozilla.org/en-US/docs/Web/API/Push_API>.

## Decision rules

- Model permission state per channel per user, refreshed whenever the vendor reports a loss, and never assumed permanent.
- Treat permission loss as a routing input: fall back to the policy's next channel, never retry into the denied one.
- Model quiet hours and user-specified do-not-interrupt windows explicitly, including the timezone they live in.
- Record how each urgency class interacts with quiet hours, and require a policy — not a caller's judgment — to override.
- Give recipients a per-category control, not a single mute for everything.
- Measure the rate of setting changes as a signal, not a good-outcome statistic: an increase in mutes is an attention-budget default, not a growth metric.

## Procedure

1. Design the per-user, per-channel preference and permission schema, including the timezone.
2. Wire vendor permission-loss events to update the routing inputs in real time.
3. Define the quiet-hours and urgency override policy in writing with the document owner.
4. Read the preference upgrade gate — fall back to the next policy-allowed channel, with no retries into the denied channel.
5. Expose per-category controls to the user, and record their mapping to the event categories.
6. Audit the gating logic for each category: it checks all of permission, preference, quiet hours, and urgency class before any send.

## Anti-patterns

- A lost push permission retried into for months, silently generating zero-delivered inventory.
- The user's timezone missing from the model, so quiet hours fire at the wrong local time.
- Overrides decided at the send site by the closest engineer, not by a written policy.
- A single mute-all switch because per-category controls are harder to build.
- Measuring enablement alone and calling it user satisfaction.

## Done checklist

- [ ] Per-user, per-channel preference and permission schema live.
- [ ] Vendor permission-loss events wired in the same pipeline.
- [ ] Quiet hours policy written with urgency override rules.
- [ ] Timezone and category-control design live.
- [ ] Per-send gating audit includes permission, preference, quiet hours, and urgency.
- [ ] Mute and setting-change rates tracked as attention signals.

## Sources

- Apple notification permissions: <https://developer.apple.com/documentation/usernotifications>
- Web push permissions: <https://developer.mozilla.org/en-US/docs/Web/API/Push_API>
- Cross-platform push: <https://firebase.google.com/docs/cloud-messaging>
