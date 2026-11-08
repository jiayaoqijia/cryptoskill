---
name: mexc-futures-rest
description: MEXC Futures REST workflows for public contract data, signed account requests, positions, orders, and secure OPEN-API signing without exposing API keys.
---

# MEXC Futures REST

## Workflow

Resolve bundled helper paths from the skill root. In Claude Code, use `${CLAUDE_SKILL_DIR}/scripts/...`; do not assume the skill is installed under `~/.claude/skills` or any fixed repository path.

Use `${CLAUDE_SKILL_DIR}/scripts/mexc_futures_request.py` for request construction and signing. Never ask the user to paste API keys into chat, command arguments, source files, logs, or screenshots.

1. Use the quick commands below first for common tasks. Do not open references or run broad text searches until a quick command or lookup slice is insufficient.
2. Use `MEXC_API_KEY` and `MEXC_API_SECRET` env vars only; the helper enforces credential loading, signed-param placement, redacted dry-runs, method/path/base-url validation, and live-write confirmation.
3. Use `GET /api/v1/contract/detail` to confirm contract metadata, precision, leverage limits, and availability before trading.
4. MEXC is live-only: use tiny sizes and `--execute --confirm-live` only when clearly requested.
5. Prefer `python "${CLAUDE_SKILL_DIR}/scripts/lookup.py" <topic>` over opening full references; for balance/account questions, start with `python "${CLAUDE_SKILL_DIR}/scripts/lookup.py" balance`.

## Quick Commands

```bash
python "${CLAUDE_SKILL_DIR}/scripts/mexc_futures_request.py" GET /api/v1/contract/ping
python "${CLAUDE_SKILL_DIR}/scripts/mexc_futures_request.py" GET /api/v1/private/account/assets --signed
python "${CLAUDE_SKILL_DIR}/scripts/mexc_futures_request.py" GET /api/v1/private/account/assets --signed --execute
```

## Rules

- Use `GET /api/v1/private/account/assets --signed --execute` for the current Futures balance snapshot.
- Use `python "${CLAUDE_SKILL_DIR}/scripts/lookup.py" balance` to retrieve compact balance/account commands without loading references.
- Futures order placement requires KYC and account-side permission; prefer `externalOid`.
- Back off on rate limits and honor retry guidance when returned.

## Verification

After helper edits, run `python "${CLAUDE_SKILL_DIR}/scripts/mexc_futures_request.py" --self-test`.
