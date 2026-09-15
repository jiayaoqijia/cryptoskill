---
repo: metamask-extension
parent: sentry-quota
---

## File Paths

| Path | Role |
|---|---|
| `shared/lib/trace.ts` | `TraceName` / `TraceOperation` enums = the custom-span registry; `trace({ name, op, data }, cb)` API |
| `shared/lib/wrapper-sampling.ts` | `shouldSampleWrappers(traceId)` — the Tier-2 deterministic sub-sample gate |
| `shared/lib/messenger-tracing.ts` | `wrapMessengerWithTracing` + `isReadOnlyAction` read-only denylist (~90% volume cut before sampling) |
| `app/scripts/lib/createMetaRPCHandler.ts` | `rpc.handler` span — gated behind `shouldSampleWrappers` |
| `app/scripts/lib/setupSentry.js` | global `tracesSampleRate` fallback (`0.005` = 0.5%) |
| `app/scripts/lib/sentry-traces-sampler.ts` | `tracesSampler`: per-name rates (`DEFAULT_TRANSACTION_SAMPLE_RATES`) and the remote-rate ceiling. It takes precedence over `tracesSampleRate` |

Core controller instrumentation lives in the **`MetaMask/core`** monorepo: per-package `TraceName` in `packages/<pkg>/src/**/{constants/traces,utils/trace}.ts` (e.g. `bridge-controller/src/constants/traces.ts`). Controllers don't import Sentry — they call an injected `trace` callback (`traceAsControllerCallback` in the extension).

## Commands

```bash
EXT=<metamask-extension checkout>
CORE=<core monorepo checkout>

# Span registries (the inventory)
rg -n 'enum TraceName' "$EXT/shared/lib/trace.ts"
rg -n -g '**/{traces,trace}.ts' 'enum TraceName' "$CORE/packages"

# Locate a culprit's emit site
rg -n '<SpanName>|TraceName.<SpanName>' "$EXT" "$CORE/packages"

# All span creation sites — then read each enclosing scope for loop/poller (fan-out)
rg -n 'trace\(' "$EXT/app" "$EXT/shared" "$CORE/packages/<pkg>/src"

# Gate present before the span? (absence = always-on)
rg -n 'shouldSample|tracesSampleRate|hashBucket|Math.random' <call-site-file>

# Kill-switch present?
rg -n 'SENTRY_[A-Z_]*DISABLED' "$EXT" "$CORE/packages/<pkg>/src"

# PR review — added instrumentation lines only
gh pr diff <n> --repo MetaMask/metamask-extension \
  | rg '^\+' | rg 'TraceName|trace\(|shouldSampleWrappers|SENTRY_.*DISABLED|op:'
```

## Architectural Notes

- **Gate location differs by repo.** Extension spans go through `trace()` — gate at the call site or in the wrapper. Core controller spans go through the injected callback — gate in the package's trace util or the callback so every consumer (extension, mobile) inherits the cap.
- **`BackgroundRpc` / `MessengerCall`** (the `TraceName` tail) are the already-gated wrapper spans from [PR #39891](https://github.com/MetaMask/metamask-extension/pull/39891) — the reference implementation of the Tier-2 sub-sample pattern and the `SENTRY_DISTRIBUTED_TRACING_DISABLED` kill-switch.
- **Tier-0 fix path is a core PR + a patch on the extension release branch.** Controller instrumentation originates in `MetaMask/core`; the release branch is where the cherry-pick lands. The sev-1 blocker goes on the in-flight release milestone — e.g. [issue #43211](https://github.com/MetaMask/metamask-extension/issues/43211) ("Assets Controller Sentry Instrumentation exceeding quota").
- **Spotting the culprit first:** `sentry-mcp-queries` → Volume Estimation (`span.op` aggregate `count()`) ranks span contributors by span count; this skill takes over once you have the offending span name. A span-count ranking is not a ranking by billed volume: retention differs per name, so no single factor rescales it, and on a plan metered in transactions it can invert.
