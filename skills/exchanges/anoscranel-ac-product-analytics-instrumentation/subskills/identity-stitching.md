---
name: identity-stitching
domain: software-engineering/identity-stitching
trigger: "Connecting anonymous to logged-in and counting users rather than devices."
anti_trigger: "Not for authentication itself, and not for privacy obligations on identifiers."
scope: "Anonymous-to-logged-in, device graphs, and the counts that depend on them."
status: seedling
---

# Identity stitching

## Standard

Before login, the best an event stream carries is a device identifier: a cookie, a platform ID, a random device token. After login, the stream can carry a user identifier. The stitching problem is connecting the pre-login device set to the post-login user — with the standard approach being that at login, the client emits an identity event linking the anonymous ID to the now-known ID, and the analysis layer merges the histories going forward.

The stitching determines what "unique users" means. The count is per-device by default; stitch to per-person and the number changes. A consistent stitching policy — stated in the plan, not implied — is what keeps reports comparable over time. Identities that re-link on every login step remain stable; IDs that silently leak — a device reset creating a new anonymous ID — remain part of the data quality report /// the event stream will not tell you its own gaps unless the plan asks it to.

Primary sources: <https://developer.apple.com/documentation/appstoreconnectapi> and <https://en.wikipedia.org/wiki/Customer_data_platform>.

## Decision rules

- Device ID and user ID are separate declared properties, never conflated.
- The identity event linking them fires at every transition from anonymous to known.
- Password-reset and re-login cases are included in the stitching test, not edge cases.
- The choice of primary identifier (person or device) is stated once in the plan.
- Counts derived from stitched identity state their stitching policy in the analysis themselves.
- Session boundaries — how one session is detected from the stream — are part of the identity policy and written down.

## Procedure

1. Choose where the persistent anonymous ID lives on each platform.
2. Declare the identity event schema.
3. Emit it at every login and re-login.
4. Write the stitching policy (person-primary or device-primary) into the plan.
5. Add session-boundary rules to the plan beside the stitching policy.
6. Verify the stitching on a sample: pick a user, confirm all their pre-login history lands with them.

## Anti-patterns

- Counting unique devices and reporting them as users.
- A stitch performed only after the first login and never on password resets.
- Session-end rules that are never defined — the session table does not exist.
- New anonymous IDs (a device app update appearing as a churn event) with no protection.
- Mixing person and device IDs in one metric without saying which.

## Done checklist

- [ ] Anonymous-ID placement defined per platform.
- [ ] Identity event declared and emitted at every transition.
- [ ] Stitching policy stated once in the plan.
- [ ] Session-boundary rules written beside it.
- [ ] Sample verification run on a real known user.
- [ ] Metrics state their identity basis.

## Sources

- Platform identifier interfaces: <https://developer.apple.com/documentation/appstoreconnectapi>
- Data aggregation layer background: <https://en.wikipedia.org/wiki/Customer_data_platform>
- Storage considerations for identifiers: <https://developer.mozilla.org/en-US/docs/Web/API/Beacon_API>
