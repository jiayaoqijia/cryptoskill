---
name: secrets-hygiene
description: >-
  Never commit, print, or paste live API keys, passphrases, or JWT secrets.
  Use when editing .env, debugging auth, writing skills/docs, or reviewing diffs.
license: MIT
compatibility: Policy skill; applies to all DUP Labs repos.
metadata:
  author: dup-labs
  version: "0.1.6"
  product: dup-labs
---

# Secrets hygiene

## When to Use

- `.env`, KuCoin keys, `RADAR_API_KEY`, JWT, Vault, Telegram tokens
- Logs, screenshots, skill text, MCP config

## Rules

1. Secrets live in env / SecretManager — never in git.
2. Prefer presence checks (`set` / `empty`) over printing values.
3. Redact in logs: show length or last4 only if required.
4. MCP: `RADAR_API_KEY` from process env only — never hardcode in `mcp.json`.
5. Rotate if a key was pasted into chat.

## Refuse

- Committing `.env` or key files.
- Embedding live keys in SKILL.md examples.
- Disabling TLS verify to “make auth work”.
