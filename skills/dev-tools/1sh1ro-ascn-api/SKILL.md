---
name: ascn-api
description: "Use when tasks require ASCN API integration planning, paid-credit capability tracking, and endpoint probes once API credentials are available."
---

# ASCN API

Use this skill for ASCN API integration once credentials and endpoint docs are available.

## When to use

- The task requires ASCN AI agent outputs via API.
- You need a controlled probe tool with custom headers.

## Quick start

```bash
export ASCN_API_KEY="..."
python3 scripts/ascn_request.py /health --pretty
```

## Workflow

1. Set `ASCN_API_KEY` and `ASCN_BASE_URL`.
2. Set `ASCN_API_KEY_HEADER` based on account docs.
3. Probe endpoints and save confirmed templates.

## References

- `references/access.md`
