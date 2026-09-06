---
repo: core
parent: perps-review-pr
---

## File Paths

| Area | Path |
|---|---|
| Package | `packages/perps-controller/` |
| Controller | `packages/perps-controller/src/PerpsController.ts` |
| Providers | `packages/perps-controller/src/providers/` |
| Services | `packages/perps-controller/src/services/` |
| Types | `packages/perps-controller/src/types/` |
| Utils | `packages/perps-controller/src/utils/` |
| Selectors | `packages/perps-controller/src/selectors.ts` |
| Tests | `packages/perps-controller/tests/` |
| Package metadata | `packages/perps-controller/package.json`, `packages/perps-controller/CHANGELOG.md` |

## Review Focus Areas

**Shared package source of truth** — Core hosts `@metamask/perps-controller`, which is consumed by Mobile and Extension. Review API, type, state-shape, selector, event-name, and export changes as cross-client contract changes, not Core-only implementation details.

**Platform-agnostic controller boundary** — controller code must not depend on Mobile or Extension UI/runtime concepts. Flag direct UI assumptions, browser/React Native APIs, test-only fixtures leaking into production, and client-specific behavior that belongs in consuming repos.

**Provider/service correctness** — changes in providers, services, routing, subscriptions, or caches must preserve provider isolation, cleanup/unsubscribe behavior, error handling, and deterministic state updates. Watch for stale subscriptions, duplicated polling, shared mutable provider state, and unbounded caches.

**Formatting and numeric contracts** — Core utilities such as `perpsFormatters`, `significantFigures`, order calculations, and market transforms feed both clients. Enforce the shared formatting rules; flag `.toFixed` display shortcuts, lossy number conversions, and inconsistent fallback display vs. true zero.

**Generated artifacts and exports** — when controller messenger actions, exports, constants, or package surfaces change, verify generated action types, package exports, and changelog requirements are handled. A PR that changes public package behavior should include tests and release notes/changelog where Core requires them.

**Client sync impact** — if a Core change requires Mobile or Extension adapter/UI changes, call that out explicitly. Do not approve a Core PR that silently changes contracts without naming the downstream migration or compatibility plan.

## Validation

1. `yarn workspace @metamask/perps-controller test` — package tests pass.
2. `yarn workspace @metamask/perps-controller build` — package builds and types emit.
3. `yarn workspace @metamask/perps-controller messenger-action-types:check` — when controller messenger actions/types changed.
4. Focused root lint/misc checks for touched files when practical, e.g. `yarn lint:eslint --quiet packages/perps-controller` if supported by the checkout.
5. If public API/package metadata changed, run the relevant changelog validation for `@metamask/perps-controller`.
