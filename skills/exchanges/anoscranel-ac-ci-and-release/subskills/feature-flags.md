---
name: feature-flags
domain: software-engineering/feature-flags
trigger: "\"Put it behind a flag\", \"add a kill switch\", \"dark launch this\", \"roll out to 10% of users\", \"clean up old flags\", \"use OpenFeature\"."
anti_trigger: "Traffic-level canary and blue-green rollout (subskills/deployment.md); A/B experiment statistics are out of scope for this tree; cutting a version (subskills/release-launch.md)."
scope: "Decoupling deploy from release; flag types, owner, expiry, cleanup"
status: "seedling"
---

# Feature Flags

## Standard

- **Deploy ≠ release**: flags let code reach production switched off; release becomes a config change.
- **Toggle categories** (Pete Hodgson, "Feature Toggles", martinfowler.com): release, experiment, ops, permission toggles, differing in lifespan and dynamism (https://martinfowler.com/articles/feature-toggles.html).
- **Flag debt**: every flag needs an owner, an expiry date and a cleanup plan.
- **OpenFeature spec v0.9.0** (29 July 2026), vendor-neutral API. Typed evaluation takes a flag key and a required default value. Req 1.4.10: evaluation "MUST NOT throw"; abnormal execution returns the default value (https://openfeature.dev/specification/sections/flag-evaluation). ⚠️ Pre-1.0; stability is set per section.

## Decision rules

1. Flag a change when it needs staged exposure, a kill switch or an off-by-default merge to trunk. Do not flag trivial changes.
2. Pick the type first:
 - release toggle: days to weeks, then removed;
 - ops toggle (kill switch): long-lived, owned by on-call;
 - permission toggle: long-lived, tied to plans or roles;
 - experiment toggle: lives for the experiment only.
3. Every flag records: key, type, owner, created date, expiry date, default.
4. Release toggles expire within 30 days of full rollout. ⚠️ House number.
5. The default value is the safe state: usually off for new features, on for a kill switch guarding an existing path.
6. Evaluation must never throw or block. Wrap the call; fall back to the default.
7. Test both paths of every flag in CI.
8. Keep flag checks at one point per feature, not scattered through the code.
9. Turning a flag on for 100% of production users is a release: **human-gated**.

## Procedure

1. Register the flag:
   ```yaml
   key: new-checkout
   type: release
   owner: payments-team
   created: 2026-10-17
   expires: 2026-11-30
   default: false
   ```
2. Evaluate through a neutral API:
   ```ts
   import { OpenFeature } from '@openfeature/server-sdk';
   const client = OpenFeature.getClient();
   const on = await client.getBooleanValue('new-checkout', false, { targetingKey: user.id });
   return on ? newCheckout(req) : oldCheckout(req);
   ```
3. Write tests for flag on and flag off.
4. Deploy with the flag off. Verify nothing changed.
5. Ramp: internal users → 1% → 10% → 50% → 100%, watching errors and key metrics at each step. ⚠️ Steps are house defaults.
6. Problem → flip off. Confirm recovery in metrics.
7. At 100% and stable: open a cleanup PR. Delete the flag check, the old path and its tests. Remove the flag from the registry.
8. Weekly: list flags past expiry and assign cleanup.

## Anti-patterns

- Flags with no owner or expiry.
- Release toggles left in code for months.
- Nested flags that make paths impossible to test.
- Flag evaluation that throws or calls the network on every request without a cache.
- Reusing an old flag key for a new feature.

## Done checklist

- [ ] Flag registered with type, owner, expiry, default.
- [ ] Safe default; evaluation cannot throw.
- [ ] Both paths tested.
- [ ] Ramp watched; kill path proven.
- [ ] Flag removed after full rollout.

## Sources

- https://martinfowler.com/articles/feature-toggles.html · https://openfeature.dev/specification/
- <https://launchdarkly.com/blog/what-are-feature-flags>
- <https://www.ainformat.com/detail/2777>
