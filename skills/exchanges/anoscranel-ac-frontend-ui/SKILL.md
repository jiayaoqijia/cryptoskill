---
name: ac-frontend-ui
description: "Building web interfaces and making them accessible: component structure and state placement, responsive layout, design systems and design tokens, plus WCAG 2.2 AA conformance — semantics, keyboard paths, contrast, screen-reader checks. Use when asking \"build this UI\", \"make this component\", \"where should this state live\", \"make it responsive\", \"use our design tokens\", \"is this accessible\", \"keyboard users can't reach this\", \"fix contrast\", \"meet WCAG 2.2 AA\". Not for browser automation tests, Core Web Vitals and bundle size, or native mobile UI; those sit outside this skill."
license: MIT
metadata:
  domain: software-engineering
---

# Frontend UI

## Overview

Two leaves build the interface. One covers structure: component trees, where state lives, responsive layout, token-only styling. The other covers the WCAG 2.2 AA pass: semantics, keyboard, contrast, screen reader, and where the automation ceiling sits. Build it, then make it usable by everyone.

## When to use

- Components and screens: state placement, derived values, loading/empty/error states.
- Responsive layout at set widths; design-system and token-only styling.
- Accessibility checks: axe scans, keyboard-only passes, screen-reader passes.
- Fixing contrast, target size, focus visibility; meeting WCAG 2.2 AA.

## When not to use

- Browser-driven end-to-end test suites — outside this skill.
- Core Web Vitals, bundles and render cost — outside this skill.
- Native mobile UI — outside this skill.

## Precedence

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by an ancestor — leaves narrow, never override upward.

## Subskill index

| Leaf | Task | Trigger |
|---|---|---|
| `subskills/frontend-ui.md` | Components, state, layout | "build this UI" |
| `subskills/accessibility.md` | WCAG 2.2 AA checks and fixes | "is this accessible" |

## See also

- `subskills/frontend-ui.md` — build the interface.
- `subskills/accessibility.md` — open it to everyone.
