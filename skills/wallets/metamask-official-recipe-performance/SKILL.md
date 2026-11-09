---
name: recipe-performance
description: Diagnose a specific MetaMask user flow's real-app performance and Sentry critical-user-flow telemetry with deterministic mm-harness recipes. Use for CUF boundaries, cold/warm/background-resume behavior, latency regressions, lifecycle tags, duplicate or blocking network requests, long tasks, layout/paint cost, screen redraws, React rerenders, or browser trace analysis where tests alone cannot prove the real app.
disable-model-invocation: true
maturity: experimental
---

# Recipe performance

Depends on the installed `mms-recipe-cook` and `mms-recipe-harness`; this is a dev flavour, not a standalone workflow.

Given a human user flow, automatically execute sibling skill `/mms-recipe-cook`; never ask the user to invoke both. Once Cook locks the task harness, run `mm-harness help --json` and follow its authoring, composition, quality, and drift method. `/mms-recipe-harness` owns the sandbox. This skill adds performance diagnosis and proof.

Read `references/performance-evidence.md` before planning proof. For Extension rendering or network optimization, also read `references/rendering-network.md`. For Mobile bottlenecks, read `references/mobile-device-measurement.md`; for an authorised before/after comparison, read `references/paired-device-measurement.md`. Resolve `PERF_SKILL_DIR` to the directory containing this loaded skill, including a branch-specific copy when supplied.

The result must be reproducible: retain the rerunnable root recipe and run-scoped evidence that proves the same flow and finding. Treat an uncorrelated profiler observation as a hypothesis, not proof.

## How to use

Start with a running Mobile app on an explicit simulator/emulator or device, a
repeatable fixture and the task-locked `mm-harness`. Record the build mode; a
compatible dev client with Metro supports JS diagnosis without a native rebuild.
Use Recipe Harness to discover and prepare missing prerequisites.
Find bottlenecks and report final numbers on a real mid- or low-range device.
Simulators and flagship phones hide JS-thread/layout cost: an iPhone simulator found an 18% win; a Pixel 6 exposed a 60% one in the same sheet.
Iterate on a simulator or emulator, then confirm the bottleneck and final gain on the device.

Example prompt:

> Using the recipe-performance skill, make the Perps order sheet (tap Long or Short on a market) open faster. Find the biggest bottleneck, fix it, and give before/after stats from the device.

Expect a bottleneck diagnosis backed by a CPU profile and viewable flame graph,
a focused code change when requested, and paired before/after evidence with n,
p50/p75, frame gaps and a noise verdict. The report records the target, source,
build/sampler configuration, raw artifacts and actual wall time.

For planning, budget about 5–15 minutes for a prepared four-block comparison per
flow. First-time fixture setup, instrumentation and bisection can take hours;
that capture budget is not an end-to-end time guarantee.

## Interactive checkpoints

Let Cook initialize and prepare the task before product discovery. Then present the proposed user journey, exact measured start/end boundary, client/lifecycle/environment, evidence authorities, failure verdict, and whether the run is baseline-only or may lead to a fix. A request to measure, diagnose, or compare a named flow authorizes its baseline/comparison measurement. Confirm only an unresolved scope or environment choice before measuring.

Choose the path the request needs. A diagnosis asks for bottleneck evidence and a proposed fix; an existing-PR or null comparison goes directly to paired measurement, without requiring a new fix.

After the baseline, present the verdict and evidence. Diagnosis may use reversible task-local timing probes and elimination variants, with their patches retained and restored. If the caller requested a fix or optimization, apply the smallest change supported by that baseline and rerun the identical recipe. For a diagnosis-only request, present the proposed fix for approval first.

## Contract first

Write one row per claim before editing:

| Claim | Real user action | Exact start/end boundary | Context/tags | Authority | Failure verdict |
|---|---|---|---|---|---|

Resolve names, routes, selectors, controller methods, and telemetry attributes from current source or live CLI discovery. Never reuse a historical name without confirming it exists.

## Workflow

1. Apply the task harness's `help --json` method to select, compose, or repair the smallest recipe for the claim. Keep reusable domain composition in a team library; do not grow `mm-harness` for one investigation.
2. Make preparation deterministic but outside the measured window. Use real lifecycle actions for cold, warm, and background-resume states. Use controller actions for state, assertions, and cleanup—not as substitutes for a claimed UI gesture.
3. Run one baseline recipe. Runtime claims require the real app and a run-scoped assertion. Focused tests corroborate; they never replace runtime proof.
4. Match evidence to the claim:
   - recipe `trace.json`: graph execution and orchestration duration;
   - exact product start/end markers: local CUF boundary and tags;
   - Sentry spans/dashboard query: indexed telemetry and aggregate latency;
   - Chrome DevTools/CDP trace: Extension JavaScript/render/network diagnosis;
   - Mobile JS CPU sampling profile plus rendered flame graph: function attribution around the recipe action; native frame evidence distinguishes UI rendering from JS stalls;
   - controller read: resulting application state.
5. For a Mobile diagnosis, correlate the CPU profile with JS frame gaps and source, then use blank-then-add elimination or mount-read runtime switches to test the cause. Follow the Mobile reference.
6. On an unexpected result, stop and classify `PROVEN`, `DISPROVEN`, `INCONCLUSIVE`, or `BLOCKED`. Do not broaden queries, change actions, or retry a nondeterministic path to manufacture a pass.
7. Fix only a proven defect within the authorised scope, then rerun the identical recipe and evidence query. Cleanup must leave the selected account/market deterministic even after failure.

## Efficiency gate

Add a reusable recipe or instruction only when it removes repeated inference, encodes a safety/evidence invariant, or has already served multiple proofs. Prefer direct, discoverable controller/CDP use for one-off diagnosis. Never add an action merely to hide a standard tool the agent can already use reliably.

## Output

Retain the contract matrix, root recipe, resolved dependency recipes and resolution graph, trace, diagnostics, exact marker excerpts, controller state, and redacted Sentry/trace summary. For Mobile, retain the raw CPU profile, viewable flame graph, elimination conditions and paired block table where applicable. Separate observations from inference; do not claim cross-platform parity unless equivalent boundaries are verified on each client.
