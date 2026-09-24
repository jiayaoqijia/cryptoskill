---
name: alternative-me-api
description: "Use when tasks need the Alternative.me Fear & Greed Index API (free/no-key) for sentiment sections in daily CEX reports."
---

# Alternative.me API

Use this skill for Fear & Greed Index pulls.

## When to use

- The task needs sentiment index values from Alternative.me.
- You need a free, no-key sentiment feed for daily/monthly reports.

## Quick start

```bash
python3 scripts/alternative_me_get.py fng --param limit=30 --pretty
```

## Workflow

1. Call base URL `https://api.alternative.me`.
2. Pull `/fng/` with required window.
3. Convert timestamp to report timezone.
4. Keep fallback note if endpoint is unavailable.

## References

- `references/endpoints.md`
