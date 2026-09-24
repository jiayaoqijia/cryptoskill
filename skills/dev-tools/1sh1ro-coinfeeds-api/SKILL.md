---
name: coinfeeds-api
description: "Use when tasks require Coinfeeds news/market API pulls with key auth and fallback handling for demo-only account access."
---

# Coinfeeds API

Use this skill for Coinfeeds endpoint calls.

## When to use

- The task needs Coinfeeds news/price feed APIs.
- You have a Coinfeeds API key or demo credentials.

## Quick start

```bash
export COINFEEDS_API_KEY="..."
python3 scripts/coinfeeds_request.py /v1/news --pretty
```

## Workflow

1. Set `COINFEEDS_API_KEY`.
2. Probe a simple endpoint first.
3. Treat unavailable AI/chat endpoints as plan-gated.

## References

- `references/access.md`
