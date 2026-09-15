---
name: navigation
description: >-
  App navigation with named routes. Use when adding or changing a screen,
  navigating from a component or a non-UI caller (saga, Engine, deeplink
  handler), or writing tests that assert navigation.
maturity: stable
base: true
---

# Navigation

Use this skill for moving between screens.

## When to use

- Adding or changing a screen or navigator registration
- Navigating from a component
- Navigating from a saga, Engine, or other non-UI caller
- Writing tests that assert navigation
- Reviewing a PR that introduces or changes navigation

## Workflow

1. Pick the route name from the shared route map. Do not invent a string.
2. From a screen, navigate with the navigation hook. From a non-UI caller, use the navigation service.
3. Pass typed params. Register the screen on an existing navigator tree.
4. In tests, mock the navigation hook or the navigation service the same way nearby tests already do.
