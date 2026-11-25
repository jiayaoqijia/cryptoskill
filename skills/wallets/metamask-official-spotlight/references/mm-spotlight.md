# Sentry Spotlight — see Sentry events locally

[Spotlight](https://spotlightjs.com/docs/about/) is a local sidecar (default `http://localhost:8969`) that receives the same envelopes the app sends to Sentry and shows them live: transactions, spans, errors, logs. Use it to check a `trace()` change, see why a flow is slow, or debug trace shape **without waiting for the Sentry dashboard**. Dev builds only.

**When the user asks to "open Spotlight", "connect Spotlight", or "see my traces locally" — follow the fast path below. Do not ask them to read the Spotlight docs.**

## Fast path (agent runbook)

The helper script ships next to this skill. Resolve it from whichever install dir exists:

```bash
S=$(ls .claude/skills/mms-spotlight/scripts/spotlight.sh \
       .agents/skills/mms-spotlight/scripts/spotlight.sh \
       .cursor/rules/mms-spotlight/scripts/spotlight.sh 2>/dev/null | head -n 1)
"$S" on          # idempotent; run from anywhere inside the metamask-mobile checkout
```

`on` does all of this and is safe to re-run:

1. Starts the sidecar if `:8969/health` is not answering (`yarn dlx @spotlightjs/spotlight@<pinned>`, in its own session so it survives the tool call). Reuses a running one.
2. Edits `.js.env` (gitignored): creates it from `.js.env.example` if missing, sets `SENTRY_SPOTLIGHT="true"`, and if `MM_SENTRY_DSN` is empty sets a **localhost-only throwaway DSN** so nothing leaves the machine. A real DSN is left alone.
3. Opens `http://localhost:8969` in the **system** browser. This browser UI is the only viewer: there is no desktop app to install.
4. **Resets Metro when `.js.env` changed** (it created the file or set a value). Env vars are inlined by Babel at bundle time, so a reload is not enough. The script stops the Metro already listening on its port (`WATCHER_PORT` from `.js.env`, else `8081`; a second `yarn watch:clean` aborts on a busy port), then runs `yarn watch:clean` from the repo root in its own session and waits until Metro reports `packager-status:running` (log: `${TMPDIR}/spotlight-metro.log`).
   - It only kills **this checkout's** Metro: the listener's command must contain the repo root and `expo`, `metro` or `react-native`. Anything else on the port (another checkout's Metro, an unrelated server) makes it exit 5 and kill nothing.
   - A re-run that changes nothing leaves Metro alone, so it never kills a healthy session.
   - **The replacement Metro is detached**, so its terminal is gone: the `r` reload and `j` DevTools keys no longer work, and output goes to the log file. Developers who want to keep their own Metro terminal should run `on --no-metro` and restart Metro themselves.
   - Flags: `--restart-metro` forces the reset, `--no-metro` skips it and prints the manual steps instead. Passing both, or an unknown flag, is a usage error.
5. Prints what is still needed on the app side.

Then do the steps the script cannot:

| Step | When | How |
|---|---|---|
| Fully relaunch the app | After `on` printed `metro: up` (it reset Metro) | The running app holds the old bundle. Relaunch it so it loads the fresh one. If you ran `on --no-metro` and it printed "Restart Metro", do that by hand first: stop any Metro on the dev port (`WATCHER_PORT`, default 8081), then `yarn watch:clean`. |
| Metrics consent ON | Always, once per install | Settings → Security and privacy → **Participate in MetaMetrics**. Sentry reads consent at launch, so **relaunch the app after toggling** (the app says so itself). If you have simulator UI automation, drive it; otherwise ask the user to tap it. |
| `__DEV__` build | Always | Spotlight forwarding is gated on `__DEV__`; release builds never send. |

Finish with `"$S" status`. It queries the sidecar for traces and errors in the last 5 minutes (`SPOTLIGHT_STATUS_WINDOW` seconds overrides) and prints one of:
- `Connected: the app is sending events to Spotlight.` when traces arrived in that window.
- `No traces yet. App not connected: …` when there are none at all in the last hour.
- `No traces in the last 300s, but earlier ones exist …` when the app connected before and has gone quiet.
- If the sidecar is up but its MCP endpoint errors, it exits 3 and prints the reason (HTTP status or MCP error) with the sidecar log path, instead of guessing.

Tell the user the UI is open at `http://localhost:8969`. `"$S" off` stops the sidecar (not Metro). It waits for the process to exit, then checks the port again, and exits 7 with the new pid, its parent and any non-Apple launchd job whose label contains `spotlight` if something restarts it. It never removes a job it did not create.

## Querying data as the agent

Prefer the Spotlight MCP tools if a `spotlight` MCP server is connected: `search_traces`, `get_traces`, `search_errors`, `search_logs`. If not, the script calls the same tools over HTTP, no MCP setup needed:

```bash
"$S" mcp search_traces '{"filters":{"timeWindow":3600,"limit":10}}'   # recent traces, 8-char ids
"$S" mcp get_traces '{"traceId":"26aae995"}'                          # full span tree for one trace
"$S" mcp search_errors '{"filters":{"timeWindow":300}}'               # errors in the last 5 min
```

Raw form, if the script is unavailable (the `Accept` header is required):

```bash
curl -sS -X POST http://127.0.0.1:8969/mcp \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_traces","arguments":{"filters":{"timeWindow":3600}}}}'
```

To make the tools native in the user's agent (optional, user-level, never commit): Cursor `.cursor/mcp.json` → `{"mcpServers":{"spotlight":{"url":"http://127.0.0.1:8969/mcp"}}}`; Claude Code → `claude mcp add --transport http spotlight http://127.0.0.1:8969/mcp`. The sidecar must be running first.

Live stream in a terminal: `yarn dlx @spotlightjs/spotlight@<pinned> tail traces -f md` (types: `traces`, `logs`, `errors`).

## How it is wired in the app (verify, this drifts)

```bash
rg -n "SENTRY_SPOTLIGHT|spotlight" app/util/sentry/utils.ts .js.env.example
```

Events reach Spotlight only when **all** of these hold in `setupSentry` (`app/util/sentry/utils.ts`):

- `__DEV__` is true and `SENTRY_SPOTLIGHT === 'true'`. Use the string `true`. The generic Spotlight getting-started docs say `1`, but this app's check is an exact match, so `1` silently does nothing. `on` already writes `true`.
- `MM_SENTRY_DSN` is non-empty. `setupSentry` returns early without it, so Spotlight stays silent. Spotlight does not need the DSN to be reachable: the SDK emits `beforeEnvelope` to Spotlight before it tries the transport.
- Metrics consent is on **for the app's own `trace()` calls**: `app/util/trace.ts` buffers traces while `getCachedConsent() !== true`, so a flow started with `trace()` does not reach Spotlight without consent. At the SDK level consent does not matter for Spotlight: the SDK hands every envelope to Spotlight (`beforeEnvelope`) before it checks `enabled`, and sets up the Spotlight integration even when the client is disabled. `enabled: forceEnabled || hasConsent` only gates the send to Sentry's servers.

The SDK finds the sidecar from the Metro dev-server host on port 8969 (`getDefaultSidecarUrl` in `@sentry/react-native`), and the sidecar listens on all interfaces. iOS simulators and devices on the Metro host therefore need nothing extra. If Android shows nothing, try `adb reverse tcp:8969 tcp:8969` and check the host firewall for 8969.

## Reading what you see (gotchas seen on this app)

- **"(multiple root transactions)" on one trace.** The React Navigation idle span sets the trace id on the current scope, so any independent, parentless transaction started while a screen is active inherits it. The trace view groups by `trace_id`, hence several roots. Not a Spotlight bug. If the work is genuinely independent, `trace({ ..., forceTransaction: true })` starts a root with a fresh trace id (see the `forceTransaction` doc in `app/util/trace.ts`). If it belongs to the flow, pass a `parentContext` instead.
- **Inflated span counts in the Spotlight UI.** `profilesSampleRate` is 1.0 and profile samples are counted as spans. Only the entries in a transaction's `spans` are real spans.
- **Nothing after turning metrics on.** Consent is read when Sentry initialises and a runtime toggle does not re-init it. Relaunch the app.
- **`ERROR: port 8969 is held by pid …`.** Another process owns the port and is not a healthy sidecar. Stop it or set `SPOTLIGHT_PORT`.
- **`off` exits 7: "listening again as pid …".** Something restarts the sidecar, typically a launchd job submitted by an earlier setup (`launchctl list | grep -i spotlight`, usually running `npx -y @spotlightjs/spotlight`). The script prints the label but will not remove it: `launchctl remove <label>`, then run `off` again. Note `npx` is not the sanctioned path here; `on` uses the pinned `yarn dlx`.
- **`ERROR: pid … on :8081 is not this checkout's Metro` (exit 5).** The Metro on the port belongs to another checkout, or is not Metro. Stop it yourself, or run `on --no-metro`.
- **`off` refuses a pid.** It only stops a process whose command contains `@spotlightjs/` or is a `.bin/spotlight` binary, so it never kills an unrelated process that merely has "spotlight" in a path.

## Guardrails

- Never commit `.js.env` or a real DSN. Both stay local.
- Repo rule: `yarn` only, never `npx`. The sidecar is not a project dependency, so use `yarn dlx` with a pinned version (`SPOTLIGHT_VERSION` overrides the script's pin). Do not float to `latest`.
- With a **real** DSN set, events go to that Sentry project as well as Spotlight, subject to the user's consent. If the user only wants local viewing, use the throwaway DSN.
- Spotlight data can include wallet addresses and request URLs. It stays on `localhost`; do not paste raw envelopes into PRs or tickets.
- Spotlight is for inspection. It does not replace measurement discipline: record the numbers you read from it, and for performance work follow the `performance` skill's Measure → Optimize → Re-measure → Validate loop.
