---
name: feature-flags
description: >-
  Version-gated remote feature flags. Use when adding, migrating, or
  reviewing a remote or version-gated feature flag, writing a flag
  selector, or gating UI on a flag boolean.
maturity: stable
base: true
---

# Feature flags

Use this skill for remote and version-gated feature flags.

## When to use

- Adding or migrating a remote / version-gated feature flag
- Writing or updating a flag selector
- Gating UI or hooks on a flag boolean
- Reviewing a PR that introduces or changes flag evaluation

## Workflow

1. Evaluate the flag in a selector. Return a boolean.
2. Map a non-standard remote shape to `{ enabled, minimumVersion }` before the shared helper.
3. Consume that boolean in UI or hooks. Do not re-run version math there.
4. Cover the selector with collocated tests (enabled, disabled, invalid, fallback).
