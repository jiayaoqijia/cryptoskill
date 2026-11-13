---
name: api-versioning
domain: software-engineering/api-versioning
trigger: "\"Is this a breaking change\", \"do we need v2\", \"how do we version this API\", \"add a Sunset header\", \"deprecate this endpoint\", \"check the OpenAPI diff\"."
anti_trigger: "First design of a new contract (subskills/api-design.md); retiring a whole feature or system; library release numbers."
scope: "Versioning, breaking-change rules, Hyrum's law, sunset and deprecation headers"
status: "seedling"
---

# API Versioning

## Standard

- **SemVer 2.0.0** (https://semver.org): MAJOR for incompatible changes, MINOR for compatible additions, PATCH for fixes.
- **Breaking-change definition**: Google AIP-180 (compatibility) and AIP-185 (versioning) (https://google.aip.dev/180, https://google.aip.dev/185); Microsoft REST Guidelines §12.
- **Hyrum's law**: with enough users, every observable behaviour of an API will be depended on by somebody. (https://www.hyrumslaw.com/)
- **Signals**: `Deprecation` header, RFC 9745; `Sunset` header, RFC 8594 (https://www.rfc-editor.org/info/rfc8594). Sunset gives the date the API stops responding; Deprecation says it still works but is not preferred.
- **Diff gates**: `oasdiff breaking` for OpenAPI; `buf breaking` for Protobuf.
- **Notice**: Google Cloud GA norm is at least one year before a breaking change. ⚠️ Notice-length effect sizes come from one preprint (arXiv 2609.31288).

## Decision rules

1. Breaking = removing or renaming a field, endpoint or enum value; adding a required input; tightening validation; changing a type, default, status code, error `type` or relied-on ordering.
2. Not breaking = a new optional field, endpoint or parameter with old-behaviour default. ⚠️ A new enum value breaks strict-switch clients; document that clients must tolerate unknown values.
3. Prefer additive change. Never change behaviour inside a published major.
4. Scheme: major in the path (`/v1/`). Date-pinned header versions (Stripe-style) only with server-side translation layers (⚠️ secondary sources).
5. A break needs: a new major or date version, a migration guide, a Deprecation header on the old version, a Sunset date, and usage telemetry per version.
6. Remove the old version only when telemetry shows traffic near zero or the Sunset date passes. Removal is **human-gated**.
7. Exceptions with shorter notice: endpoints marked alpha/beta, security-driven removals.

## Procedure

1. Keep the last released spec as `openapi.base.yaml` (or the main-branch copy).
2. In CI run:
   ```bash
   oasdiff breaking openapi.base.yaml openapi.yaml --fail-on ERR
   buf breaking --against '.git#branch=main'
   ```
3. If the gate fails, first try an additive redesign.
4. If the break is required, write an ADR with the reason.
5. Ship the new version alongside the old one.
6. On old responses add:
   ```http
   Deprecation: @1767225600
   Sunset: Thu, 31 Dec 2026 23:59:59 GMT
   Link: <https://example.com/docs/migrate-v2>; rel="deprecation"
   ```
 ⚠️ Check the exact `Deprecation` value syntax against RFC 9745 before shipping.
7. Log calls per version and client ID. Publish a migration guide. Contact top remaining callers before the Sunset date.
8. After the Sunset date and human approval, remove the old version.

## Anti-patterns

- A "small" break shipped inside v1; removal with no telemetry check.
- URI version bumped for every additive change; Sunset with no Deprecation phase.
- An agent deprecating its own API without a human decision.

## Done checklist

- [ ] Diff gate runs in CI against the released baseline.
- [ ] Every break has an ADR, new version, migration guide.
- [ ] Deprecation and Sunset headers set on the old version.
- [ ] Per-version usage telemetry live.
- [ ] Removal approved by a human.

## Sources

- <https://google.aip.dev>
- <https://arxiv.org/pdf/2507.05316v1>
- https://semver.org · https://www.rfc-editor.org/info/rfc8594 · https://github.com/tufin/oasdiff
