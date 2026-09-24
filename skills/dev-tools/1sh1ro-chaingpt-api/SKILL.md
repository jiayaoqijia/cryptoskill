---
name: chaingpt-api
description: "Use when tasks need ChainGPT API/SDK calls (chat/news/trading assistant) with bearer-token auth and endpoint capability checks."
---

# ChainGPT API

Use this skill for ChainGPT HTTP API calls.

## When to use

- The task needs ChainGPT chat/news style endpoints.
- You have an API key/token.
- You need to log endpoint access restrictions by plan.

## Quick start

```bash
export CHAINGPT_API_KEY="..."
python3 scripts/chaingpt_request.py /api/v1/news --pretty
```

## Workflow

1. Set `CHAINGPT_API_KEY`.
2. Use bearer auth by default.
3. On permission errors, record as capability blocks.

## References

- `references/access.md`
