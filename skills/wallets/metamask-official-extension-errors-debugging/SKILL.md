---
maturity: experimental
name: extension-errors-debugging
description: Diagnose browser extension errors — MV3 vs MV2, background/UI context, error tagging
---

# Extension Errors Debugging

## When To Use

- Errors appear in one manifest version but not the other
- Background connection or keepalive failures
- Errors that are hard to reproduce in development (only manifest in prod)
- Diagnosing Sentry errors before attributing root cause

## Do Not Use When

- Local development errors with full stack traces and reliable repro
- Build/compile errors (TypeScript, ESLint, bundler)
- Test failures unrelated to extension runtime behavior

## Workflow

1. **Check distribution** — Filter by `dist` tag. Is the error 99%+ MV3, MV2, or split? Tag splits count errors, not users, so compare the split against how users divide across the same tag before reading a skew as a cause.
2. **Classify root cause** — MV3-only → service worker lifecycle (specifically cold-start cascade; ongoing idle termination is mitigated — see `mv3-service-worker` knowledge). Split → application logic. MV2-only → Firefox behavior.
3. **Identify context** — Is the error from background (`app/scripts/`) or UI (`ui/`)? Stack trace file paths reveal this.
4. **Check error tags** — Verify `environment`, `installType`, and `dist` are what you expect (these are independent dimensions).
5. **Reproduce** — Use `dist` tag filter to reproduce in the right manifest version.

## Context Identification from Stack Traces

| Path prefix in trace | Context |
|---------------------|---------|
| `app/scripts/controllers/` | Background controller |
| `app/scripts/metamask-controller.js` | Background aggregator |
| `ui/components/` or `ui/pages/` | UI (React) |
| `shared/` | Either — shared module |

## Background-Specific Error Types

| Error | MV3 Root Cause | Mitigated? |
|-------|---------------|------------|
| Background connection unresponsive (cold-start cascade) | `service-worker.ts` → `background.js` listener race on worker cold start | No |
| Background connection unresponsive (first-flush latency) | Cold start + background state aggregation before `startUiSync` | No |
| Background connection unresponsive (idle termination) | Worker idle-killed mid-session | Yes — 2s `chrome.storage.session` keepalive |
| Port disconnected (wake/termination race) | Port closed during worker lifecycle transition; silent via try/catch | No |
| Keepalive timer missed (active session) | Would imply `chrome.storage.session.set` interval failed — rare; investigate as application bug, not platform behavior | N/A |
| In-memory state lost (cold start) | New worker instance re-reads persisted state | No |

## Common Pitfalls

| Mistake | Correct Approach |
|---------|-----------------|
| Attribute 99% MV3 error to application code | Check if error requires running background; MV3 SW lifecycle is the likely root cause |
| Default to "SW was terminated mid-session" for MV3 errors | Ongoing idle termination is mitigated by the 2s `chrome.storage.session` keepalive. The likely mechanism is cold-start cascade or first-flush latency — see `mv3-service-worker` knowledge |
| "Keepalive timer missed" ⇒ SW slept | The 2s keepalive prevents idle sleep while active. A missed keepalive during active session is a code bug, not platform behavior |
| Use `environment` to filter for dev builds | Use `installType: development` — a prod build can be sideloaded |
| Conflate `dist` and `environment` | They are independent; filter both when needed |
| Reproduce MV2-only error in Chrome | Use Firefox; `installType` doesn't replicate MV3/MV2 lifecycle difference |
