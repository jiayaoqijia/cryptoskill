---
name: key-pools
domain: software-engineering/key-pools
trigger: "Operating multiple keys legitimately: where entitlement exists and how to rotate."
anti_trigger: "Not for dodging a provider's limits, and not for secret handling in general."
scope: "Multiple keys and rotation for deployments entitled to them."
status: seedling
---

# Key pools

## Standard

Some deployments are legitimately entitled to multiple keys: an organisation with several paid accounts across teams, a platform acting for distinct customers each with their own provisioned key, a test environment separated from production by contract rather than by chance. For these, a key pool is ordinary credential management at a larger scale — each key with its owner, its entitlement, its documented limit, and the pool with a rotation schedule that treats each key as the secret it is.

The line this skill does not cross: a pool multiplied to circumvent a single deployment's limit — one application, many free-tier keys, rotating to dodge the daily cap — is abuse of the provider's regime. It breaches the contract the pool operator signed, invites enforcement that arrives as sudden termination, and this skill neither teaches it nor troubleshoots it. The test is entitlement: each key must correspond to a genuine, separately-provisioned right to serve the traffic it receives.

Primary sources: <https://docs.anthropic.com/en/api/rate-limits> and <https://12factor.net/>.

## Decision rules

- Record each key's entitlement: owner, tier, documented limit, and the traffic it may serve.
- Verify that the pool's total reflects genuine separate entitlements, not multiplied trial accounts.
- Route traffic to keys by entitlement class, not by round-robin opportunism.
- Rotate keys on a schedule and on any exposure signal; rotation is a security operation.
- Keep the per-key budget accounting so any single key's exhaustion is visible.
- Review the pool when the provider's contract changes; entitlement recalculation is part of the re-read.

## Procedure

1. Inventory the keys and their entitlements, owners, and documented limits.
2. Configure routing by entitlement class.
3. Attach the per-key budget accounting to the shared budgeting layer.
4. Set the rotation schedule and the exposure-trigger rotation.
5. Define the entitlement review: when a key's right to serve is re-verified.
6. Record pool operations — additions, rotations, revocations — in the operational log.

## Anti-patterns

- Multiplying keys to exceed one deployment's limit; this is abuse, not scaling.
- Free-tier keys aggregated into what is functionally a paid workload.
- Rotating keys without the security discipline rotation implies.
- A pool whose total budget exceeds the sum of documented entitlements.
- Adding a key during an outage without recording its origin and entitlement.

## Done checklist

- [ ] Entitlement per key documented.
- [ ] Routing by entitlement class.
- [ ] Per-key budget accounting attached.
- [ ] Rotation schedule and exposure triggers set.
- [ ] Entitlement review scheduled with the contract re-read.
- [ ] Pool operations logged.

## Sources

- Provider rate-limit documentation, Anthropic: <https://docs.anthropic.com/en/api/rate-limits>
- The twelve-factor app: <https://12factor.net/>
- Handling overload, Google SRE: <https://sre.google/sre-book/handling-overload/>
