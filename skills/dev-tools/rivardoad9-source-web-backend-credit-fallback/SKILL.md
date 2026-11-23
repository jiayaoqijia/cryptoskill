---
name: web-backend-credit-fallback
description: "Guard paid web-search API credits with auto-flip cron."
---

# Web backend credit fallback

Use when a paid web-search/extract API (Exa, Firecrawl, Parallel) may run out of credits and search must keep working. Builds a silent cron guard that flips the Hermes web backend to a free provider and back.

Hermes does NOT auto-fall back to another configured vendor when a paid key hits 402. The only built-in rescue is the keyless ring (`exa, parallel, firecrawl, keenable` in `plugins/web/keyless_mcp.py`); TinyFish is not in it. So build the guard.

## Facts worth knowing first

- Backend selection is per call from `web.backend` / `web.search_backend` / `web.extract_backend`, so `hermes config set` takes effect immediately, cron included. Set all three.
- Hermes refuses agent writes to `config.yaml`; use `hermes config set <key> <value>`.
- TinyFish (plugin `~/.hermes/plugins/tinyfish`) is genuinely free: search 30/min + 500/hr, fetch 150/min + 1,000/day, keeps working at $0 wallet. Free tier to use as the fallback.
- Exa charges per call (lite $4/1k, auto $7/1k, contents $1/1k pages), so a monitoring probe costs real money — probe at most daily, and use free log scanning for immediacy.
- `/search` with `type: lite, numResults: 1` is the cheapest auth probe (~$0.004).

## Pattern (proven, see ~/.hermes/scripts/exa_guard.py)

1. Free detection: tail `~/.hermes/logs/agent.log` from a stored byte offset, match provider error lines containing `exa` and `(402|401|payment required|insufficient|quota)`. On log rotation (offset > size) set offset = size and skip the chunk — otherwise old errors cause a false flip.
2. Billed detection: daily probe gated on a `last_probe` timestamp (default 20h). Treat network errors as alive; only HTTP 401/402 may flip.
3. Flip with `hermes config set` for all three backend keys, then re-read them to verify; persist state (`active`, `changed_at`) so it never flip-flops.
4. Recovery: when on fallback and the probe returns 200, flip back (free credits reset on the 1st).
5. Print nothing when nothing changed. Register as `no_agent` cron every 30m with `deliver='telegram:<chat_id>'` — empty stdout sends nothing.

## Test before scheduling

Monkeypatch the module in a temp dir (`LOG_DIR`, `STATE`, `HERMES` -> shell stub recording `config set/get`) and assert: silent when clean, flips on a 402 log line, flips back on probe 200, does NOT flip on network error, no double flip when already in target state.

## Cost discipline

Guarding costs ~1 lite probe/day (~$0.12/mo). Do not probe every 30 minutes. Split by volume: interactive searches on the paid index, high-frequency cron collectors on the free one.
