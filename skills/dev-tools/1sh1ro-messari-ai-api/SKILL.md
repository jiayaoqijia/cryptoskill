---
name: messari-ai-api
description: "Use when tasks require Messari AI/OpenAI-compatible endpoint calls with bearer auth and account-level capability checks."
---

# Messari AI API

Use this skill for Messari AI/OpenAI-compatible requests.

## When to use

- The task needs Messari AI endpoints.
- You have a Messari API key.

## Quick start

```bash
export MESSARI_API_KEY="..."
python3 scripts/messari_request.py /ai/post-openai-chat-completions   --method POST --json '{"model":"gpt-4o-mini","messages":[{"role":"user","content":"hi"}]}' --pretty
```

## Workflow

1. Set `MESSARI_API_KEY`.
2. Send bearer-auth requests.
3. Capture plan/auth errors as capability blocks.

## References

- `references/access.md`
