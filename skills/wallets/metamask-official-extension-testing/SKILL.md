---
name: extension-testing
description: >
  Single MetaMask Extension testing entrypoint. Routes unit, UI and
  composed-background integration, and Selenium E2E create/maintain work
  (flakiness, POM anti-patterns) to the right references. Use when writing,
  fixing, reviewing, or placing Extension tests; when the user mentions
  MetaMaskController, FixtureBuilderV2, page objects, E2E flake, POM
  anti-patterns, or asks which Extension testing skill to install.
maturity: stable
base: true
---

# Extension testing

One skill for MetaMask Extension functional testing. Classify the task, pick the
layer, then open **only** the matching reference.

**Flakiness note:** Unlike Mobile (where Jest unit flakiness is a separate
skill), Extension **E2E** flakiness lives **inside** this skill under
`references/e2e/flakiness.md` — create and maintain share one tree.

## When To Use

- Writing, fixing, or reviewing MetaMask Extension unit, integration, or Selenium
  E2E tests
- Choosing the right Extension test layer (unit vs integration vs E2E)
- Creating or updating page objects, flows, or fixtures (`FixtureBuilderV2`)
- Fixing E2E flakes or auditing POM anti-patterns
- MMQA testing-skills work that targets Extension (for example MMQA-2274)

**Out of scope:** performance, visual (`visual-testing` / `mm` CLI), A/B, i18n,
Mobile layers, and cross-layer placement audits (phase 2). Keep those separate.

## Prerequisites

- Consumer repo: MetaMask Extension (`metamask-extension`)
- Skill installed via `yarn skills` / `@metamask/skills` for
  `testing/extension-testing`
- Familiarity with Extension test layout: colocated `*.test.ts(x)`,
  `test/integration/`, `app/scripts/metamask-controller*.test.js`, `test/e2e/`
- For E2E: a test build (`yarn build:test` or `yarn start:test`) and Chrome (or
  Firefox MV2) available

## Workflow

### 1. Choose the layer

Read installed `knowledge/extension-testing-layers.md` (source:
[`../../knowledge/extension-testing-layers.md`](../../knowledge/extension-testing-layers.md))
before writing any test. `references/layers.md` is only a redirect stub.

### 2. Open only the matching reference

| If the work is… | Open |
| --- | --- |
| Pure logic / helpers / selectors / isolated controller / narrow RTL unit | [`references/unit.md`](references/unit.md) |
| Full UI + real Redux under `test/integration/`, or real `MetaMaskController` composition under `app/scripts/` | [`references/integration.md`](references/integration.md) |
| Create or update Selenium E2E / POM / fixtures | [`references/e2e.md`](references/e2e.md) → writing-tests |
| Fix flaky E2E or POM bad practices / audit anti-patterns | [`references/e2e.md`](references/e2e.md) → maintain / flakiness / pom-antipatterns |

Do not read every reference up front. Follow the decision tree in installed
`knowledge/extension-testing-layers.md`, then open nested files only when that
doc sends you there.

### 3. Hard rules

1. **Layer gate first.** Prefer **unit → integration (only when justified) →
   E2E**. Document why unit is insufficient before proposing new E2E.
2. Integration has two existing homes. Use `test/integration/` for real UI +
   Redux with mocked background RPC; use `app/scripts/metamask-controller*.test.js`
   for real composed-background wiring with external I/O mocked. Do not
   duplicate every scenario across both homes or invent a new integration tree.
3. E2E is legitimate for real browser/extension/dapp/window boundaries — do not
   copy Mobile’s “almost never E2E” gate.
4. For E2E, inspect existing specs, page objects, flows, and fixtures in the
   feature folder before proposing code.
5. E2E POM methods must not use `try/catch`. Locators belong in page objects,
   not flows or specs. Specs must not call the driver for UI actions. Avoid
   hardcoded delays without a justifying comment.
6. Maintain mode: diagnose with `references/e2e/flakiness.md`, enforce structure
   with `references/e2e/pom-antipatterns.md`. Prefer waits and mocks over retries.
7. Bugbot is a **local** safety net only (`.cursor/BUGBOT.md`), never a PR merge
   gate — see `pom-antipatterns.md`. Get the code right in this skill first.

## Examples

```
User: Add a unit test for the deep-link parser helper
Agent: layers → unit → references/unit.md
```

```
User: Verify MetaMaskController routes watchAsset through the composed controllers
Agent: layers → integration (composed background) → references/integration.md
```

```
User: Verify a Redux-driven confirmation alert without a browser
Agent: layers → integration (UI + state) → references/integration.md
```

```
User: Add E2E for connecting the test dapp and confirming a tx
Agent: layers → e2e (dapp/window boundary) → references/e2e.md → writing-tests.md
```

```
User: This E2E flakes on window handle / stale element
Agent: references/e2e.md → maintain.md → flakiness.md
```

```
User: Audit this PR for POM anti-patterns / try/catch in page objects
Agent: references/e2e.md → pom-antipatterns.md
```

## Troubleshooting

### Agent opened every reference

**Problem:** Context bloat; conflicting guidance.

**Solution:** Stop after the layer decision. Open only the one row in the
Workflow table that matches the task.

### E2E proposed for pure logic

**Problem:** Slow, flake-prone coverage for something unit can own.

**Solution:** Re-read `knowledge/extension-testing-layers.md`. Document why unit
(and integration, if relevant) cannot cover the case before adding E2E.

### POM / Bugbot confusion

**Problem:** Expecting Bugbot CI on the PR to block POM anti-patterns.

**Solution:** Follow `references/e2e/pom-antipatterns.md` while writing. Use
local CODEBOT / `/review` / local Bugbot against `.cursor/BUGBOT.md` as a
backstop — not CI.

### Deprecated skill still selected

**Problem:** Agent loads old `e2e-testing`, `unit-testing`, or
`e2e-flakiness-patterns`.

**Solution:** Those are redirect stubs. Prefer this skill
(`testing/extension-testing`) and re-sync with `yarn skills`.

## Security considerations

- Do not put secrets, private keys, seed phrases, or API keys in skill files,
  fixtures committed for demos, or example snippets.
- E2E fixtures and mocks must not embed production credentials.
- This skill guides test generation only; it is not an enforcement layer. Pair
  with local review (`.cursor/BUGBOT.md`) and normal CI lint/tests for hard
  gates.
