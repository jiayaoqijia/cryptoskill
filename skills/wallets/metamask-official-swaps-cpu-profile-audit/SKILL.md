---
name: swaps-cpu-profile-audit
description: >-
  Parse an already-recorded Hermes / React Native Release Profiler
  `.cpuprofile` (ideally symbolicated with source maps) and audit it for slow
  frames on the swaps/bridge screen and the modals or subpages it opens —
  quote select screen, post-trade modal, batch sell, asset picker/token
  selector. Use when a user hands you a `.cpuprofile` file (e.g. a
  `sampling-profiler-trace*.cpuprofile`, or its already-converted
  `*-converted.json`) recorded per `docs/readme/release-build-profiler.md` and
  asks to audit, analyze, explain, or find why the swaps/bridge flow is slow
  based on that trace. This is an offline, file-based analysis — no simulator,
  device, Metro, or `mm` session is required, unlike `swaps-perf-audit` (which
  measures live render counts on a running simulator). The audit accounts for
  ALL time in the capture, not just swaps-owned code: non-swaps frames that
  ran while the user sat on a swaps screen (navigation, redux, design system,
  polling controllers, React internals) are reported too, each labelled with
  whether the swaps team owns it and how it relates to the swaps call stacks.
  The report always leads with a timing table (capture metrics + by-area self
  time with an ownership column) and a short outcome line, and only adds a
  probable-cause/fix table when there is an actual issue — deep fixes are
  proposed for swaps-owned rows, while non-owned rows are named and routed.
  MetaMask Mobile only.
maturity: stable
---

# Swaps CPU Profile Audit

Turns a captured Hermes CPU profile into a performance audit of the
swaps/bridge experience: which frames actually burned time in the capture,
which surface they belong to (main screen, quote select, post-trade, batch
sell, asset picker, ...), **whether the swaps team owns them**, and what to
change. This skill owns the profile-parsing protocol, the swaps-tree area
map, and the ownership/relation classification; the fix recipes themselves
live in the `performance` skill, and the live on-device measurement
counterpart is `swaps-perf-audit`.

Auditing only swaps-owned files misses a whole class of real regressions: a
capture taken on the swaps screen can be dominated by a slow navigator
transition, a re-rendering provider, an unmemoized shared selector, or a
polling controller — none of it under `app/components/UI/Bridge/**`, all of
it felt by the user as "swaps is slow". So the analyzer classifies **every**
frame in the capture, and the report names the non-swaps contributors instead
of dropping them.

## When To Use

Use when the user:

- Hands you a `.cpuprofile` (or its converted JSON) and asks what's slow in
  swaps/bridge, or to audit/analyze/explain it.
- Asks "why is swaps slow" and already has a recorded trace, RC build
  profiling session, or Release Profiler capture in hand.
- Wants swaps performance fixes justified by trace evidence instead of a
  static code sweep.
- Needs to know whether the cost on a swaps screen is actually the swaps
  team's to fix, or belongs to another team's code.

Do not use for:

- Recording a *new* profile live on a simulator/device, or driving the app —
  that is manual, human-only work described in
  `docs/readme/release-build-profiler.md` (shake the device, Start, reproduce,
  Stop). This skill starts only once a `.cpuprofile` file already exists on
  disk.
- Live render-count / re-render measurement on a running simulator — use
  `swaps-perf-audit`.
- A capture that was not recorded on the swaps/bridge screens, or a general
  app-wide performance sweep — the whole model here assumes the user was
  sitting on a swaps surface while recording, which is what makes non-swaps
  frames in the trace attributable at all. Point them at the general
  `performance` skill instead.
- MetaMask Extension — Hermes/Release Profiler `.cpuprofile` capture doesn't
  exist there; this skill installs only for `metamask-mobile`.

## How ownership and relation are decided

Two independent axes, both computed by the analyzer:

**Owned by swaps** — the frame's resolved source path matches one of the
swaps-owned roots (`app/components/UI/Bridge/**` plus the swaps redux slice,
selectors, bridge controller/messenger wiring, bridge utils, and the
swaps/bridge confirmation rows). This is a path-list decision, so it is
stable and does not depend on the trace.

**Relation to swaps** — where the frame sat relative to swaps code in the
recorded call stacks:

| Relation | Meaning | Typical example |
|---|---|---|
| `Swaps-owned` | The frame is swaps code | `BridgeView`, `useQuotes` |
| `Called by swaps` | Non-swaps frame that ran with a swaps frame below it on the stack — swaps code invoked it | `useSelector`, a shared hook, a design-system component rendered by swaps |
| `Hosts swaps screen` | Non-swaps frame that was on the stack when swaps code was entered — it renders/hosts the screen | React reconciler, navigator, redux `Provider` |
| `Concurrent (off swaps path)` | Non-swaps frame that never shares a stack with swaps code — it competes for the JS thread anyway | Token detection / balance polling, analytics flush |
| `Runtime / idle` | Engine bookkeeping owned by nobody, excluded from every percentage | `[root]` (wall time with no JS running), `[GC young gen]` |

The distinction drives what you do with a finding: `Called by swaps` is often
still a swaps bug (swaps calls it too often, or with unstable arguments),
`Hosts swaps screen` usually means the screen makes the host do too much
work, and `Concurrent` is someone else's timer stealing frames while the user
is mid-swap.

### Self time vs inclusive time — read both

Self time answers "which frame was executing", so it lands on the *leaf* of
the stack. A React component that renders a heavy tree therefore often shows
**0 ms of self time** while the cost piles up in the reconciler, a selector,
or a dependency it called. `Swaps-owned code: 0.00 ms` never means "swaps did
nothing" on its own — check the inclusive column and the
`Called by swaps` rows before concluding anything, because "swaps triggers
expensive work" is a swaps finding even when no swaps frame is hot.

Two corollaries for reading the analyzer output honestly:

- **Idle is not work.** `[root]` owns all the wall time when no JS is running,
  which on a capture where the user paused can be most of it. The analyzer
  splits it (and GC) into `Runtime / idle` and excludes it from every
  percentage, so "% of JS work" means what it says. Never put an idle or GC
  row in the fix table.
- **A zero-self area with a trivial inclusive span means nothing.** Usually
  it is just a module getting evaluated (a screen the user never opened).
  The analyzer only keeps a zero-self swaps row when the work it triggered
  clears `--trigger-min-pct` (default 5% of JS work); do not reintroduce
  those rows by hand.

## Workflow

1. **Locate the inputs.** You need the `.cpuprofile` path. Source maps are
   optional but strongly preferred — without them, frames stay at the
   minified-bundle level, so nothing resolves to a real path and both the
   ownership and area columns collapse to "unknown". If the user has
   sourcemaps (from a local `--sourcemap-path` or a `*-sourcemaps-<build>` CI
   artifact) but hasn't converted yet, do that next.
2. **Symbolicate.** Convert the raw profile with the project's own tool,
   which resolves bundle positions back to original `app/...` source paths:
   ```bash
   # --sourcemap-path takes the .map FILE, not a directory or a zip.
   # The output lands in the CURRENT DIRECTORY — the CLI has no output flag.
   yarn react-native-release-profiler --local <profile.cpuprofile> \
     --sourcemap-path <sourcemaps>/index.js.map
   ```
   This writes `<profile-basename>-converted.json` into the directory you ran
   it from. Never omit `--sourcemap-path` just to "see what happens": without
   it the CLI silently substitutes a map of its own (an Android *debug* build
   map, or `/index.map` downloaded from a running Metro server), which cannot
   symbolicate a release Hermes capture — it either crashes the transformer or
   produces confidently wrong file attributions. See the repo overlay for the
   exact commands and traps. Skip this step only if the user already has a
   converted JSON, or has no sourcemaps at all (state clearly in the report
   that findings are then best-effort and file/line attribution is
   unreliable).
3. **Aggregate.** Run the bundled analyzer against the converted JSON (or the
   raw `.cpuprofile` as a fallback — see the repo overlay for exact usage).
   It reconstructs self time and total (inclusive) time per frame from the
   sampling data, then emits four separate tables: swaps-owned areas
   (`app/components/UI/Bridge/**` subfolder → BridgeView / QuoteSelectorView /
   PostTradeBottomSheet / BatchSell\* / BridgeTokenSelector / ... — see the
   repo overlay's area table), non-swaps areas on the swaps path, non-swaps
   areas running concurrently, and runtime/idle. Areas that did no work and
   triggered none are dropped, so every row you see earned its place.
4. **Read the code at the hot frames.** A `file:line` with high self time is
   a *symptom*, not a diagnosis — open the file, read the actual code at that
   location and its call sites, and identify the concrete anti-pattern (dead
   re-render, unmemoized sort/filter, unstable hook return, JSON.stringify in
   a dependency array, etc.). Cross-reference the `performance` skill's
   anti-pattern catalogue and per-pattern guides
   (`mm-selector-memoization.md`, `mm-unstable-hook-return.md`,
   `mm-redux-antipatterns.md`, `mm-hook-dependency-arrays.md`,
   `mm-context-performance.md`, `mm-eager-work-on-mount.md`, etc.) for the fix
   recipe rather than inventing one from scratch.
5. **For each hot non-swaps frame, work out what pulled it in.** Do not stop
   at the relation label — establish the concrete link before reporting it.
   For `Called by swaps`, find the swaps call site (`grep` the hook/component
   name under `app/components/UI/Bridge`) and say which swaps surface drives
   it, since the fix is frequently on the swaps side. For `Hosts swaps
   screen`, say what the screen makes the host do (mount cost, prop churn,
   provider re-render). For `Concurrent (off swaps path)`, name the mechanism
   (a poll, a subscription, an animation) — that row is context for the user,
   not a swaps task.
6. **Always report the timing tables; keep prose minimal.** Every report leads
   with the timing data — the analyzer's `Metric | Value` block, then the
   swaps-owned area table, then the two non-swaps tables — regardless of
   whether an issue was found. Follow it with exactly one short line stating
   the outcome: where the capture's JS work actually went, and whether the
   expensive part is swaps-owned. Do not add speculation, hedging, or
   suggestions about what to check/run next beyond what's in Step 7 — the
   report is data plus outcome, nothing else.
7. **If an issue was found, add a probable-cause/fix table — nothing more.**
   Each row carries an `Owned by swaps` cell so the reader sees at a glance
   what the swaps team can act on. Order rows by self time, swaps-owned first.
   Per row: the screen or area, the probable cause in plain language (what's
   happening and why — not "unmemoized selector" but e.g. "re-sorts the whole
   quote list every time you interact with the screen", with the relation,
   `file:line`, self-ms and calls folded into that same cell), and the fix.
   Depth differs by ownership: for `Owned by swaps = Yes`, give the concrete
   fix citing the relevant `performance` skill guide; for `No`, keep the fix
   cell to a short pointer plus who should take it (the owning area/team —
   `.github/CODEOWNERS` maps the file path to a team if the user needs to
   route it), and do not write a detailed patch plan for code another team
   maintains.

   Be ruthless about what earns a row — the table exists to be acted on, and
   every row that can't be is noise that buries the ones that can:
   - Every swaps-owned area with real self time, or with a large inclusive
     span, gets its own row. This detail is the point of the audit.
   - Non-swaps areas: only the few that genuinely matter (roughly ≥5% of JS
     work each, and rarely more than three rows). A dependency at 0.6% is not
     a finding.
   - Never a row for `Runtime / idle`, `[root]`, or GC. If GC volume looks
     symptomatic, it belongs in the cause cell of the row that caused it, not
     in a row of its own.
   - Never a row you cannot explain in plain language. If you couldn't read
     the code behind it (unsymbolicated, or a minified dependency internal),
     say so in the caveat line instead of inventing a row.

   Do not append anything after this table — no next-steps, no suggestion to
   re-run tests or capture a new profile, no broader speculation. The only
   exception is a single factual caveat line when something materially
   undermines the finding: no sourcemaps were available, the source map did
   not match the build that produced the capture (wrong function names,
   everything resolving to `[root]`), most of the capture was idle, or the
   capture looks too short to cover the full journey (quote fetch, screen
   transitions, animations). Skip that caveat whenever the capture and
   findings look adequate.

The exact commands, the swaps-tree area map, the context area map, and the
bundled analyzer's usage are in the repo overlay
(`repos/metamask-mobile.md`).

## Output format

Lead with the metrics table, then the swaps-owned area table, then the two
non-swaps tables (omit either if it has no rows), then exactly one short
outcome line. Keep the tables separate — swaps-owned detail is the subject of
the audit, and the non-swaps tables are context around it. Do not add anything
beyond what's specified below — no speculation, no assumptions, no suggestions
about what to check or run next.

**No issue found:**

```
# CPU Profile Audit — swaps/bridge

| Metric | Value |
|---|---|
| Capture length | ~<Xs> |
| JS work sampled | <Y>ms |
| Idle / GC (excluded from the splits) | <Y>ms (<Z>% of capture) |
| Swaps-owned code | <Y>ms (<Z>% of JS work) |
| Non-swaps code on the swaps path | <Y>ms (<Z>%) |
| Non-swaps code running concurrently | <Y>ms (<Z>%) |

**Swaps-owned areas**

| Area | Self time (ms) | % of swaps time | Inclusive (ms) |
|---|---|---|---|
| <Area> | <ms> | <%> | <ms> |

No meaningful performance issue in this capture — <one-line factual summary, e.g. "only <Y>ms of JS work in <Xs>, most of it <what>">.
```

**Issue(s) found** — same tables, plus a probable-cause/fix table. Keep it
skimmable (a non-engineer should get the gist without decoding jargon); fold
relation/`file:line`/self-ms/calls detail into the "Probable cause" cell
rather than adding separate columns:

```
# CPU Profile Audit — swaps/bridge

| Metric | Value |
|---|---|
| Capture length | ~<Xs> |
| JS work sampled | <Y>ms |
| Idle / GC (excluded from the splits) | <Y>ms (<Z>% of capture) |
| Swaps-owned code | <Y>ms (<Z>% of JS work) |
| Non-swaps code on the swaps path | <Y>ms (<Z>%) |
| Non-swaps code running concurrently | <Y>ms (<Z>%) |

**Swaps-owned areas**

| Area | Self time (ms) | % of swaps time | Inclusive (ms) |
|---|---|---|---|
| <Area> | <ms> | <%> | <ms> |

**Non-swaps areas on the swaps path**

| Area | Relation to swaps | Self time (ms) | % of JS work |
|---|---|---|---|
| <Area> | Called by swaps / Hosts swaps screen | <ms> | <%> |

**Non-swaps areas running concurrently**

| Area | Self time (ms) | % of JS work |
|---|---|---|
| <Area> | <ms> | <%> |

Found <N> issue(s) costing ~<Y>ms, of which <M> are swaps-owned.

| Screen / area | Owned by swaps | Probable cause | Fix |
|---|---|---|---|
| <Area, e.g. "Quote select screen"> | Yes | <plain-language root cause, e.g. "re-sorts the whole quote list every time you interact with the screen"> — <self>ms, <calls>x, `<file>:<line>` | <concrete fix> (see `<guide>.md`) |
| <Area, e.g. "Navigation (app nav stack)"> | No | <plain-language root cause + how it relates to swaps, e.g. "the navigator re-renders the whole tab stack while the swaps screen mounts"> — <self>ms, <calls>x, `<file>:<line>` | <short pointer>; owned by <area/team>, raise it with them |

<optional single factual caveat line — only if source maps were missing or mismatched, the capture was mostly idle, or it looked too short>
```
