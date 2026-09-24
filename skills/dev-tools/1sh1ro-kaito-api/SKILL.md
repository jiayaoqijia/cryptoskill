---
name: kaito-api
description: "Use when tasks require Kaito API integration planning for enterprise access, with placeholder request tooling and account-gated endpoint discovery."
---

# Kaito API

Use this skill when Kaito API access is approved.

## When to use

- The task needs Kaito InfoFi data/API outputs.
- Access is enterprise/contact-sales gated.

## Quick start

```bash
export KAITO_API_KEY="..."
python3 scripts/kaito_request.py /health --pretty
```

## Workflow

1. Set `KAITO_API_KEY` and `KAITO_BASE_URL`.
2. Set `KAITO_API_KEY_HEADER` as required by your account docs.
3. Probe endpoints and persist confirmed templates.

## References

- `references/access.md`
