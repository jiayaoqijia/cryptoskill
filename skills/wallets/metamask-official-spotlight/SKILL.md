---
maturity: stable
name: spotlight
description: Set up and use Sentry Spotlight, the local trace and error viewer, for a MetaMask Mobile dev build. Use when the user asks to "open Spotlight", "connect Spotlight", or "see my traces locally"; to check a trace() change or inspect trace shape without the Sentry dashboard; or when Spotlight is not connecting, shows "multiple root transactions", or shows every event twice. Starts a pinned local sidecar, sets SENTRY_SPOTLIGHT in .js.env, opens the browser UI at http://localhost:8969, restarts Metro (stops this checkout's Metro and runs yarn watch:clean) when .js.env changed, and queries traces and errors over its HTTP MCP endpoint
---

# Sentry Spotlight

Spotlight is a local sidecar that receives the same envelopes the app sends to Sentry and shows them live: transactions, spans, errors, logs. It is part of the standard developer setup for seeing what a dev build emits, not an optional extra.

## When To Use

- The user asks to "open Spotlight", "connect Spotlight", or "see my traces locally".
- Verifying a `trace()` change or inspecting trace shape without waiting for the Sentry dashboard.
- Spotlight is not connecting, shows "(multiple root transactions)" on one trace, or shows every event twice.

## Do Not Use When

- Writing or reviewing span and event instrumentation itself — use `instrumentation` (and `sentry-quota` for span volume).
- Querying production or staging data — use `sentry-mcp-queries` or `grafana-tempo-queries`.
- The build is a release build. Spotlight only receives events from `__DEV__` builds.

## Workflow

1. Do not ask the user to read the Spotlight docs. Run `scripts/spotlight.sh on` (resolution and details in [references/mm-spotlight.md](references/mm-spotlight.md)).
2. `on` resets Metro itself when `.js.env` changed: it stops this checkout's Metro on its port, then runs `yarn watch:clean` detached (the developer loses that terminal's `r`/`j` keys; `on --no-metro` skips the reset). Do the steps it cannot: turn metrics consent on and fully relaunch the app.
3. Run `scripts/spotlight.sh status` to confirm events are arriving, then tell the user the UI is open at `http://localhost:8969`.
4. Query with `scripts/spotlight.sh mcp <tool> [json]` (`search_traces`, `get_traces`, `search_errors`, `search_logs`).
5. Use the gotchas section of the guide for multiple roots, duplicate events and noise spans. `scripts/spotlight.sh off` stops the sidecar and reports a supervisor (such as a launchd job) that restarts it.
