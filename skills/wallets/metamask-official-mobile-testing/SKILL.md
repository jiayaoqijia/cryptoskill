---
name: mobile-testing
description: >
  Single MetaMask Mobile testing entrypoint. Routes unit, component-view,
  integration, Appium E2E, and test-layer placement work to the right
  references. Use when writing, fixing, reviewing, or placing Mobile tests;
  when the user mentions Jest layers, *.view.test.tsx, *.integration.test.ts,
  Appium smoke, MMQA test-layer tickets, or asks which testing skill to install.
maturity: stable
base: true
---

# Mobile testing

One skill for MetaMask Mobile functional testing. Classify the task, pick the
layer, then open **only** the matching reference.

**Out of scope:** performance, visual, A/B, i18n, and flakiness skills — keep
those separate.

## First step — choose the layer

Read installed `knowledge/testing-layers.md` (source:
[`../../knowledge/testing-layers.md`](../../knowledge/testing-layers.md))
before writing any test. `references/layers.md` is only a redirect stub.

## Open next

| If the work is… | Open |
| --- | --- |
| Pure logic / helpers / selectors / CV fallback | [`references/unit.md`](references/unit.md) |
| Screen UI via real Redux / `*.view.test.tsx` | [`references/component-view.md`](references/component-view.md) |
| App↔controller seam / `*.integration.test.ts` | [`references/integration.md`](references/integration.md) |
| Justified device/native journey / run Appium locally (after layer gate) | [`references/appium-e2e.md`](references/appium-e2e.md) → mobile `docs/testing/appium-smoke-testing.md` |
| Area / Jira / PR coverage audit across layers | [`references/placement.md`](references/placement.md) |

Do not read every reference up front. Follow the decision tree in installed
`knowledge/testing-layers.md`, then open nested files only when that doc sends
you there.

## Hard rules

1. **Layer gate first.** Prefer **CV → integration → unit fallback → E2E**. Do not
   propose E2E until CV and integration have been ruled out in writing (why CV
   fails, why integration fails, required device/native boundary).
2. **If and only if E2E is justified**, implement device E2E in **Appium**.
3. For E2E, inspect existing Appium specs, POMs, fixtures, flows, and nearby
   feature examples in the mobile repo before proposing code.
4. E2E POM methods must not use `try/catch`.
5. Placement work defaults to **ANALYZE** — implement only when the user asks.

## Examples

```
User: Add tests for the new Predict screen visibility toggles
Agent: layers → CV → references/component-view.md → writing-tests.md
```

```
User: Cover HyperLiquid placeOrder through the real provider
Agent: layers → integration → references/integration.md
```

```
User: Add an Appium smoke for account rename
Agent: layers gate first — if only UI/nav, prefer CV; if device boundary required → appium-e2e.md
```

```
User: Cover a multi-screen filter journey on Predict
Agent: layers → CV (cross-screen routes) → references/component-view.md — not E2E
```

```
User: Analyze Perps for unit/CV/integration/e2e — MMQA-2102
Agent: references/placement.md (ANALYZE mode)
```
