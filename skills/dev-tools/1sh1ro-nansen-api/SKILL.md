---
name: nansen-api
description: "Use when tasks require Nansen API integration with enterprise/paid access, key-header configuration, and endpoint-specific request templates once credentials are available."
---

# Nansen API

Use this skill when you have Nansen API credentials.

## When to use

- The task needs Nansen smart-money or on-chain analytics endpoints.
- A paid/enterprise key is expected.
- You need a configurable request runner before endpoint templates are finalized.

## Quick start

```bash
export NANSEN_API_KEY="..."
export NANSEN_BASE_URL="https://api.nansen.ai"
python3 scripts/nansen_request.py /health --method GET --pretty
```

## Workflow

1. Set `NANSEN_API_KEY` and `NANSEN_BASE_URL`.
2. Default auth header is `apikey`; set `NANSEN_API_KEY_HEADER` if your account expects another header.
3. Start with a capability probe endpoint.
4. Store endpoint-specific payload templates under `references/` as they are confirmed.

## References

- `references/permissions.md`
