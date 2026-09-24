---
name: santiment-api
description: "Use when tasks require Santiment API/GraphQL metrics (social dominance, sentiment, on-chain series) with API-key auth and paid-plan endpoint gating."
---

# Santiment API

Use this skill for Santiment GraphQL API calls.

## When to use

- The task needs social/sentiment metrics from Santiment.
- You have a Santiment API key (or are preparing integration for future key usage).

## Quick start

```bash
export SANTIMENT_API_KEY="..."
python3 scripts/santiment_graphql.py \
  --query '{ projects(first: 3) { slug name } }' \
  --pretty
```

## Workflow

1. Send GraphQL requests to endpoint from env or default.
2. Use `Authorization: Apikey <key>` by default (override if docs/account differs).
3. Capture GraphQL errors as capability blocks.
4. Keep query templates in `references/` as they stabilize.

## References

- `references/permissions.md`
