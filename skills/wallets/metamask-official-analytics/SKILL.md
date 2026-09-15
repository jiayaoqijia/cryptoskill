---
name: analytics
description: >-
  Product analytics and event tracking. Use when adding, migrating, or
  reviewing tracked events, or when writing tests for analytics call sites.
maturity: stable
base: true
---

# Analytics

Use this skill for product event tracking.

## When to use

- Adding or migrating event tracking in UI or non-UI code
- Writing or updating tests for analytics call sites
- Reviewing a PR that introduces or changes tracked events

## Workflow

1. Register this interaction in the catalog (`EVENT_NAME` + `generateOpt` in catalog modules). Reuse an existing catalog name only when this control is another instance of that same interaction (same dashboard event, same owners).
2. Attach properties on the event builder.
3. Send the built event through the tracking entry point.
4. In UI tests, wrap `useAnalytics` with the test factory (including files that already mock the hook). In non-React tests, assert the builder and the helper or Engine tracking util.
