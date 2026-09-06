---
repo: metamask-extension
parent: extension-testing
---

# MetaMask Extension

This skill installs for **metamask-extension**.

Follow the router in the skill body. Layer policy: installed
`knowledge/extension-testing-layers.md` (canonical; `references/layers.md` is a stub).

## In-repo docs (source of truth for paths)

- Unit philosophy: `docs/testing.md`
- UI integration: `test/integration/**/*.test.tsx` with
  `test/lib/render-helpers.js`
- Composed-background integration:
  `app/scripts/metamask-controller.test.js` and
  `app/scripts/metamask-controller.actions.test.js`
- E2E agent index: `test/e2e/AGENTS.md`
- Driver API: `test/e2e/webdriver/README.md`
- Visual (`mm` CLI): `test/e2e/playwright/llm-workflow/README.md` — use
  separate `visual-testing` skill, not this skill
- Bugbot / POM review rules: `.cursor/BUGBOT.md` sections 3.1–3.9 (**local**
  review only — CODEBOT / `/review` / local Bugbot run; see
  `references/e2e/pom-antipatterns.md`)

## Common commands

```bash
yarn test:unit path/to/file.test.ts
yarn test:integration
yarn test:unit app/scripts/metamask-controller.test.js
yarn build:test   # or yarn start:test while iterating
yarn test:e2e:single test/e2e/tests/.../foo.spec.ts --browser=chrome
yarn lint:changed:fix
```

## Skill references

- Unit: [`../references/unit.md`](../references/unit.md)
- Integration: [`../references/integration.md`](../references/integration.md)
- E2E router: [`../references/e2e.md`](../references/e2e.md)
