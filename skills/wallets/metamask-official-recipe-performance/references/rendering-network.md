# Extension rendering and network optimization

Use a deterministic recipe to create the measured action. Keep profiler collection outside the recipe protocol unless repeated use proves a generic action is needed.

## Capture contract

1. Name one user action and its start/end observation.
2. Reuse the closest working recipe; move preparation, fixture convergence, and navigation before the measured window.
3. Resolve the slot-owned Extension target and CDP endpoint. Confirm available commands from that browser's `/json/protocol`; never assume a port or protocol version.
4. Capture only the action window:
   - `Network.enable` and request/response/finish events;
   - `Performance.enable` plus before/after `Performance.getMetrics` deltas;
   - `Tracing.start`/`Tracing.end`, retaining events through `Tracing.tracingComplete`.
5. Preserve normal cache/service-worker behavior unless the claim explicitly concerns cold-cache behavior. Record any override.
6. Save the raw trace and a redacted summary beside the recipe artifacts.

`mm-harness debug` is the human path to the slot-owned DevTools Performance panel. Direct CDP is the agent path. Neither requires a new recipe action. For a repeatable agent capture around one explicit command, run:

```bash
.agents/skills/mms-recipe-performance/scripts/capture-extension-window.mjs \
  --boundary '<verified-selector>' \
  --out-dir <task>/artifacts/baseline -- \
  mm-harness call <action> <key=value...>
```

The helper resolves the CDP port from the checkout's runtime contract (an explicit `--cdp-port`, `RECIPE_CDP_PORT`, or `CDP_PORT` overrides it), then retains redacted CDP events and a summary. The caller supplies domain routes, selectors, and action parameters from its team library or live discovery.

## Analyze

### Network

Report total requests, transferred bytes, duration, initiator, and dependency ordering for the measured window. Group duplicate candidates by method plus normalized URL and, when safe, a non-secret body digest. Strip query values, headers, bodies, credentials, and wallet data from retained evidence.

A repeated request is not automatically a bug. Classify retry, polling, cache validation, batching, and distinct request bodies before declaring duplication. Prove an avoidable duplicate from its initiator and current source.

Rank slow or blocking requests by their effect on the claimed UI boundary, not duration alone. A long background request that does not gate rendering is a side finding.

### Main thread and rendering

Report long tasks and the measured window's scripting, style, layout, paint, and composite work. Use trace events and screenshots to connect expensive work to the claimed screen; do not infer user impact from a global process total.

### React

Use a verified React Profiler channel to report commit count, commit duration, and repeatedly expensive components. DOM mutations, paint events, and function-call counts do not prove a React rerender. If the running build exposes no verified React profiler channel, record React commit analysis as `N/A` and retain the browser trace.

## Prove the optimization

Treat duplicate requests, long tasks, and expensive commits as hypotheses until source and trace evidence identify a causal path. Apply one minimal fix, then rerun the identical recipe with the same lifecycle, fixture, cache policy, target surface, and profiler settings.

Compare before/after request inventory, blocking chain, main-thread/rendering breakdown, React commits when available, product boundary markers, and final controller state. If normal run variance can reverse the result, repeat the unchanged pair or report `INCONCLUSIVE`; never select only the fastest run.
