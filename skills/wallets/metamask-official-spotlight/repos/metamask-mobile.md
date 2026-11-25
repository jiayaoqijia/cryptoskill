---
repo: metamask-mobile
parent: spotlight
---

## MetaMask Mobile specifics

| Content | Path |
|---------|------|
| Spotlight gate (`__DEV__` and `SENTRY_SPOTLIGHT === 'true'`) | `app/util/sentry/utils.ts` → `setupSentry` |
| Env file the script edits (gitignored) | `.js.env`, created from `.js.env.example` when missing |
| Metro port | `WATCHER_PORT` in `.js.env` (default 8081); `yarn watch:clean` is `scripts/build.sh watcher --clean` |
| Trace wrapper and consent buffering | `app/util/trace.ts` → `trace()`, `getCachedConsent()` |

| You are... | Go to |
|---|---|
| Verifying a `trace()` change or inspecting trace shape | [references/mm-spotlight.md](references/mm-spotlight.md) → `scripts/spotlight.sh mcp search_traces` |
| Spotlight not connecting; "(multiple root transactions)" on one trace; every event appears twice | [references/mm-spotlight.md](references/mm-spotlight.md) → gotchas |
