# Mobile bottleneck diagnosis

Use the task-locked harness and an owned device, iOS simulator or Android
emulator session. The same recipe, timing boundaries, CPU capture and elimination
method apply to each. Resolve the iOS simulator UDID through the runtime contract
and use the harness's simulator lifecycle/UI actions; bind Android to its exact
adb serial, including an emulator serial. Resolve the
current app, Metro endpoint, device serial and recipe commands from its runtime
contract/help. Preparation stays outside the measured window. A dev client with
Metro can compare JS changes without a native build; record its native revision,
served bundle SHA and dev mode. Do not call dev-bundle numbers release timings.

Follow the real-device diagnosis and final-confirmation rule in the skill's
How to use section. Emulator CPU allocation, host load,
debug mode and virtual rendering can distort frame rates. Record the target,
OS/runtime, host and build mode; keep target and host allocation fixed within
each comparison. Simulator results apply to that environment and do not establish
physical-device latency or native GPU performance.

## Verify the requested source first

Before source attribution or a timed open, resolve the requested baseline to an
exact commit. For "main", fetch and resolve `origin/main`; a branch name or an
idle checkout is not evidence of that state. Compare it with the task checkout's
HEAD before creating the task branch. If preparation was skipped or the slot is
warm, this check is still required. Preserve unrelated work and use the approved
workspace/prepare path to select the requested commit. Verify the served bundle
after reload and retain its source receipt. If dependencies or native
compatibility prevent that state from running, report BLOCKED instead of
measuring an older release and calling it main.

Use the product's production trace sampler during diagnosis as well as paired
proof, including custom sampler overrides. Record the effective rate and its
source. Dev builds that sample every span can add synchronous CPU work and send
the investigation toward a development-only cost.

## Classify the delay

Measure the UI gesture, JS handler entry, first following JS rAF callback, first
layout, and the actual ready/transition boundary separately. Use one monotonic
JS clock. JS handler timing excludes any wait before that handler executes.

| Observation during the same action | Next evidence |
| --- | --- |
| JS rAF stops, long JS tasks, tap handler/layout delayed | JS CPU sampling and React commit attribution |
| JS continues but native frames miss deadlines | Android frame timeline/Perfetto or iOS native profiler for UI/render work |
| Both stall | Correlate both timelines; do not force a single-thread explanation |
| Idle JS/native threads while readiness waits | Request/dependency and lifecycle trace |

Use the RN performance monitor for triage, then save repeatable evidence. JS rAF
cadence is not compositor FPS. On Android, collect package-scoped `dumpsys gfxinfo`
frame stats or Perfetto around the recipe action, with timestamps and support
limits. A screenshot, delayed timer, or total render count alone cannot classify
the bottleneck.

## Automate a CPU profile

Profile a separate open from the timing series. Navigate and settle first, start
Hermes/JS sampling immediately before the same recipe-driven gesture, stop after
the declared ready boundary, and retain the recipe trace alongside the profile.

The native bridge already exposes `profiler-start` and `profiler-stop --out`.
Find the installed bridge through the task harness's help/runtime and confirm
these commands exist. They send CDP `Profiler.start`/`Profiler.stop`; Hermes may
reject `Profiler.enable` even when start/stop work. For example, in a tracked
shell job with `set -e` and the task's resolved command paths:

```bash
# BRIDGE is the resolved mobile bridge; FLOW_RECIPE performs one measured open.
# Preparation, warm-up and navigation have already completed.
OUT=<new-task-artifacts-directory>
mkdir -p "$OUT"
node "$BRIDGE" profiler-start > "$OUT/profile-start.json"
trap 'node "$BRIDGE" profiler-stop --out "$OUT/interrupted.cpuprofile"' EXIT
"$HARNESS" run "$FLOW_RECIPE" --artifacts-dir "$OUT/recipe" --json
node "$BRIDGE" profiler-stop --out "$OUT/open.cpuprofile" > "$OUT/profile-stop.json"
trap - EXIT
python3 "$PERF_SKILL_DIR/scripts/profile-flame.py" \
  "$OUT/open.cpuprofile" "$OUT/flame.html"
```

Bind the bridge to the same slot endpoint as the harness using its documented
runtime options. Do not guess a default port. If its wrapper lacks these
commands, use one CDP connection to the exact Metro `/json/list` app target:
`Profiler.start`, execute the recipe, `Profiler.stop`, save `result.profile`.
Always stop sampling on failure; retain the failure rather than presenting a
partial run as a success.

Open `flame.html` and inspect its sample-weighted caller graph and self-time
ranking. Also import `.cpuprofile` into RN DevTools if source maps are needed.
Record sample count, sample gaps, window length and whether the slow action is
actually represented. Zero samples, root/idle-only samples, or a sampler starved
during the stall are missing CPU attribution. Keep that evidence and diagnose
the profiler path; a React trace or wrapper timer does not become a CPU profile.
Correlate sampled functions with current source and React commits before naming
a component as the cause. Profiling overhead belongs outside the paired proof.

## Keep inspector messages small

Large CDP replies can stall the app themselves. In a prior Android investigation,
a full fiber-tree reply never completed, left a zero-byte output and caused an
ANR. The Android main-thread stack was in inspector `send`, large-object
allocation and GC. A reduced collect of about 125 KB completed; about 23 MB of
trace data delivered as many `Tracing.dataCollected` events also completed.
The failed single-message size was not measured. These observations establish
neither a universal safe cap nor the exact failure threshold.

Start with a short action-only sampling window. Read small summaries instead of
serializing an entire fiber tree. For custom probes, keep bounded records on the
runtime and retrieve bounded slices. Where the installed runtime supports native
sampling to a device file, stop there and `adb pull` the file. Chunked tracing
also avoids one giant reply. `Profiler.stop` itself may return one large message;
splitting its JSON on the host after receipt cannot prevent that stall.

Record actual serialized bytes per message or chunk, total bytes, elapsed
transfer time and the largest successful payload. If a transfer fails, record
the attempted size only if known, its timeout/error, app responsiveness and
package-scoped ANR stack. State the threshold as an observed bound, or unknown.
Do not repeatedly grow payloads until the phone ANRs. Shorten the window or use
a supported file/stream path before repeating the user interaction.

## Eliminate causes

Use reversible probes and retain each diagnostic patch. Before choosing a fix,
measure how much of the delay comes from mounting the content: compare the normal
flow with a temporary blank shell that preserves the route, gesture, transition
and ready observations. Put the switch above the tested subtree so its hooks do
not run while omitted. Returning null after those hooks ran does not remove their
mount cost; keep the surrounding component's hook order stable.

Add sections back progressively, or halve the expensive subtree. If omitting
content barely helps, investigate work before navigation, surrounding providers
or native rendering instead. Runtime/library frames still count when this
screen causes them; attribute them to the app's mounted work. If a candidate
explains only a small part of a large JS gap, continue this coarse elimination
before settling on that micro-optimization. Choose the largest proven removable
cost, not the first small positive result. Keep fixture and state unchanged.

Read runtime switches at mount so one session can rotate conditions between
opens. Record each condition, first JS frame, readiness, long gaps and relevant
CPU/React evidence. Confirm with an on/off/on reversal. A missing view that moves
work elsewhere is an attribution experiment, not a shippable fix. Do not hide
errors, remove required functionality, or claim several switches prove each
one's contribution. A valid fix may reduce work or defer it past first response;
retain all controls and measure full readiness and deferred work separately.
Trace the causal chain from gesture through scheduled work
and layout/transition, including hidden mounted children and pre-existing screen
work when the evidence points there.

Propose the smallest fix to the proven chain. For an authorised fix, prove the code
states with [paired device measurement](paired-device-measurement.md), including
adjacent-screen/deferred-work checks. For a requested PR comparison, use that
reference directly; no new fix or approval cycle is needed.

## Existing guides

Use the installed `mms-performance/references/` copies when available, or these
source guides. Keep their detailed tool instructions in one place:

- [React/JS profiling](https://github.com/MetaMask/skills/blob/main/domains/performance/skills/performance/references/js-profile-react.md)
- [JS and UI frame rates](https://github.com/MetaMask/skills/blob/main/domains/performance/skills/performance/references/js-measure-fps.md)
- [Performance timeline](https://github.com/MetaMask/skills/blob/main/domains/performance/skills/performance/references/js-performance-panel.md)
- [MetaMask tools](https://github.com/MetaMask/skills/blob/main/domains/performance/skills/performance/references/mm-tools.md)
