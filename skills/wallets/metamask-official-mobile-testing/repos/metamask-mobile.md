---
repo: metamask-mobile
parent: mobile-testing
---

# MetaMask Mobile

This skill installs only for **metamask-mobile**.

Follow the router in the skill body. Layer policy: installed
`knowledge/testing-layers.md` (canonical; `references/layers.md` is a stub).

When writing Appium E2E, treat the live repo as source of truth:

- Appium smoke (write + run): `tests/smoke-appium/`,
  `docs/testing/appium-smoke-testing.md`, skill
  [`../references/appium-e2e.md`](../references/appium-e2e.md)
- Unified POM: `tests/docs/UNIFIED_E2E_ARCHITECTURE.md`, `docs/testing/e2e-testing.md`
- CV: `tests/component-view/`
- Integration: `tests/integration/AGENTS.md`
