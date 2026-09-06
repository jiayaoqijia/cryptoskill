---
repo: metamask-mobile
parent: coding-guidelines
---

# General Coding Guidelines

## Required Reading Before Development

**ALWAYS** check: `.github/guidelines/CODING_GUIDELINES.md` • `README.md` • Relevant `/docs` before coding

**Docs Structure**: `/docs/readme/` (core) • `/docs/` (features) • `README.md` (overview)

## Development Workflow

**Before Starting**: Read README.md → Check coding guidelines → Review relevant docs → Understand architecture

**Code Quality**:

- TypeScript guidelines from contributor docs • Functional components + hooks • PascalCase (components) / camelCase (functions)
- Reusable components/utilities • TSDoc format • Comprehensive tests following testing layers (below)

**Testing layers** (Mobile — canonical policy: testing domain `knowledge/testing-layers.md`, installed beside `mobile-testing`):

1. **Component-view** (`*.view.test.tsx`) — **default** for screen/view UI behavior via real app state
2. **Integration** (`*.integration.test.ts`) — app-to-controller flows with real controllers/providers/services and only the I/O boundary mocked
3. **Unit** (`*.test.ts(x)`) — pure helpers, narrow contracts, or cases CV cannot cover yet
4. **E2E** — justified device/native **Appium** journeys only (after CV + integration)

Do **not** default to broad RTL unit tests that render a whole screen and mock hooks/selectors. Install **`mobile-testing`** and let it route to the matching reference by layer.

**File Organization**:

```
ComponentName/
├── ComponentName.{constants,stories,styles,types}.ts(x)
├── ComponentName.tsx
├── ComponentName.view.test.tsx   # preferred for screen/view behavior
├── ComponentName.integration.test.ts # app-to-controller flow (see testing-layers)
├── ComponentName.test.ts(x)      # focused unit only (see testing-layers)
├── README.md
└── index.ts
```

## Documentation Quick Reference

**Core**: `/docs/readme/` (architecture, testing, debugging, performance, environment, expo-environment, storybook, troubleshooting, expo-e2e-testing, reassure, release-build-profiler)

**Features**: `/docs/` (deeplinks, animations, tailwind, confirmations, confirmation-refactoring) • `app/component-library/README.md` • `tests/MOCKING.md` • `CHANGELOG.md` • `app/core/{Analytics,Engine}/README.md`

**External**: [MetaMask Contributor Docs](https://github.com/MetaMask/contributor-docs) • [TypeScript Guidelines](https://github.com/MetaMask/contributor-docs/blob/main/docs/typescript.md)

**Testing (Mobile)**:

- Entrypoint: `mobile-testing` skill
- Layers policy: testing domain `knowledge/testing-layers.md` (beside `mobile-testing` when installed)
- Component-view / integration / unit / Appium E2E / placement: references inside `mobile-testing`
- Contributor unit docs: [Unit testing](https://github.com/MetaMask/contributor-docs/blob/main/docs/testing/unit-testing.md)

## Enforcement (MANDATORY)

**Documentation**: Read `.github/guidelines/`, `README.md`, and relevant `/docs` before implementing

**Commands**: ONLY use `.claude/commands/` + yarn command

**Testing**: CV default for views → integration for app-to-controller flows → unit for allowed fallback → Appium for justified device journeys. Install `mobile-testing` and follow testing domain `knowledge/testing-layers.md`.

**Forbidden**: ❌ npm/npx commands
