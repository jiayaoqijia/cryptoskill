---
name: tokenmetrics-api
description: "Use when tasks require Token Metrics API integration (indices, AI/trader grades) with key-based auth and paid-plan gating."
---

# Token Metrics API

Use this skill for Token Metrics REST calls when API credentials are available.

## When to use

- The task needs Token Metrics market/AI signals.
- You need a key-authenticated request runner.
- You need paid-plan capability checks.

## Quick start

```bash
export TOKENMETRICS_API_KEY="..."
python3 scripts/tokenmetrics_request.py /v2/indices --pretty
```

## Workflow

1. Set `TOKENMETRICS_API_KEY`.
2. Start with a lightweight endpoint probe.
3. Persist blocked endpoints as `data_gaps` instead of failing the whole report.

## References

- `references/access.md`
