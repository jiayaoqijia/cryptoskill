# Performance evidence

## Choose the authority

| Question | Primary evidence | Common mistake |
|---|---|---|
| Did the real user journey execute? | Recipe UI action + state assertion | Calling the controller instead of the UI |
| Did the product CUF start/end correctly? | Fresh, correlated product markers or spans | Treating recipe node duration as CUF latency |
| Is indexed telemetry correct? | Exact Sentry span/query in the run window | Broadening the query until rows appear |
| Why is Extension slow? | DevTools Performance trace over the same action | Adding a harness wrapper before direct CDP is tried |
| Did state converge? | Controller read followed by teardown assertion | Inferring state from a screenshot |

## Lifecycle semantics

- `cold`: terminate and relaunch the installed app; prove readiness before the measured action.
- `warm`: keep the process and relevant runtime initialized.
- `background_resume`: background and foreground the same running process. A foreground action that reloads JavaScript is not valid background-resume evidence.

Record the observed lifecycle context at the product boundary. Do not infer it from the recipe mode or elapsed time.

## Secrets

Use Recipe Harness's fixture-selection flow through the task-locked CLI. If the fixture is missing or invalid, relay doctor's exact choices and wait for the operator. Reuse an approved canonical fixture when offered; do not assume a new wallet must be initialized. Only a human operator supplies missing SRPs and passwords.

The team 1Password vault (for human operators only) is:
https://consensys.1password.com/app#/m3mshk44tttveurtljcuwdj46m/AllItems

Never request or paste an SRP, private key, or password in chat or CLI arguments. Never hard-code these values in recipes, scripts, or evidence artifacts. Agents must not access the vault or any secret store directly.

## Sentry

Confirm the build can emit: DSN/config present, test overrides off, consent enabled where required, SDK initialized, and the environment sampled. Query the exact current span/transaction name and bounded run window. A zero-row query is `INCONCLUSIVE` until local emission and ingestion prerequisites are proven.

Prefer a scoped read token. If a human-authenticated browser is explicitly provided, keep access inside that browser session and retain only redacted response fields. Never extract cookies, storage, auth headers, session tokens, wallet secrets, or recovery phrases.

## Extension DevTools and CDP

Use `mm-harness debug` for a human Performance-panel recording attached to the slot-owned Extension page. Record only the action window and save the trace as an artifact.

For automated diagnosis, read the actual CDP endpoint from `mm-harness status --json` or the checkout runtime contract—never assume a port. Select the exact Extension target from `/json/list`, then attach to its reported `webSocketDebuggerUrl`.

- `Performance.enable` + `Performance.getMetrics` provides cumulative runtime counters. Capture before and after the same action and compare deltas.
- `Tracing.start` + `Tracing.end` provides event-level CPU/render/network evidence. Wait for `Tracing.tracingComplete` and persist the complete stream before analyzing it.

The DevTools protocol can change between Chromium versions. Use the target browser's `/json/protocol` contract when automating beyond these stable calls. These Chrome domains do not establish Mobile React Native performance; Mobile CUFs require product markers/spans and real lifecycle recipes.

## Cross-client claims

- Mobile: real UI, lifecycle, product CUF markers, Sentry, controller end state.
- Extension: real UI and Chrome trace; use product telemetry only when an equivalent boundary exists in current source.
- Core: controller/state and headless operation timing only; no UI render or lifecycle claim.

Reuse the journey across clients, but state each client's proof claim separately.

### Mobile: obtaining a build

A local build is always valid but takes significantly longer. As a faster alternative, download a pre-built arm64 APK from the scheduled CI workflow:

https://github.com/MetaMask/metamask-mobile/actions/workflows/build-android-arm64-scheduled.yml

Pick the latest successful run, download the arm64 APK artifact, and install it on the target device or emulator before running the recipe. For native changes, confirm the build SHA matches the source revision under investigation before recording evidence. For a JS-only dev-client comparison, keep the same compatible native client in both states and verify each served Metro bundle revision separately. Record both identities; do not claim release-build timings from a dev bundle.
