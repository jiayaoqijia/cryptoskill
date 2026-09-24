---
name: altfins-api
description: "Use when tasks require altFINS API integration planning, key-auth endpoint probes, and premium-access fallback handling."
---

# altFINS API

Use this skill for altFINS API integration once account access is enabled.

## When to use

- The task needs altFINS analytics/signal APIs.
- You need key-auth request tooling with endpoint probes.

## Quick start

```bash
export ALTFINS_API_KEY="..."
python3 scripts/altfins_request.py /health --pretty
```

## Workflow

1. Set `ALTFINS_API_KEY` and `ALTFINS_BASE_URL`.
2. Set `ALTFINS_API_KEY_HEADER` based on your account docs.
3. Probe endpoints and map plan restrictions before production use.

## References

- `references/access.md`
