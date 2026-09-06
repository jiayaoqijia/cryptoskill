---
repo: metamask-mobile
parent: swaps-cpu-profile-audit
---

# Swaps CPU Profile Audit — MetaMask Mobile

Audits a `.cpuprofile` already captured via
[`docs/readme/release-build-profiler.md`](../../../../../../docs/readme/release-build-profiler.md).
Nothing here touches a device, a simulator, Metro, or an `mm` session — it is
pure file analysis. Subject: the swaps/bridge experience — swaps-owned code
(`app/components/UI/Bridge/**` plus the swaps redux/selector/controller/util
paths listed in `DEFAULT_SCOPE_ROOTS`) **and** the non-swaps code that burned
JS-thread time in the same capture, each row tagged with whether swaps owns
it.

## Recording (human, not this skill)

Recording a fresh profile is manual, on-device work the user does themselves,
per `docs/readme/release-build-profiler.md`:

1. Build/install an **RC build** (dev builds are not representative).
2. On the device, **shake** → the **Performance Profiler** menu appears.
3. **Start**, reproduce the swaps/bridge flow, **Stop**.
4. iOS: **Export** the file (Share sheet). Android: it lands in Downloads
   automatically.

This skill's job starts once that `.cpuprofile` exists somewhere on disk. If
the user has not recorded one yet, point them at that doc rather than trying
to drive a device yourself.

## Step 1 — Locate the profile and the source maps

Ask for (or find) the `.cpuprofile` path — typically named
`sampling-profiler-trace*.cpuprofile` or similar. Source maps are optional but
the entire point of this skill is attributing time to real files — deciding
what is swaps-owned, what area it belongs to, and how it relates to the swaps
call stacks — which needs original file paths. Without a source map, frames
stay at the minified-bundle level, nothing matches an ownership root, and
every row collapses to "unknown". If the user doesn't have sourcemaps yet,
get them one of two ways:

**From a local RC build (matches the profile exactly, and is what the
Performance Profiler UI itself requires — `METAMASK_ENVIRONMENT=rc`):**

```bash
# iOS — the "Bundle JS Code & Upload Sentry Files" Xcode phase always writes this
yarn build:ios:main:rc
ls -la sourcemaps/ios/index.js.map

# Android — the RN Gradle plugin's Hermes compose step always writes this
# (variant is prodRelease for the `main` flavor)
yarn build:android:main:rc
ls -la android/app/build/generated/sourcemaps/react/prodRelease/index.android.bundle.map
```

**From CI, if the profile came from a CI-built RC instead:** GitHub Actions
artifacts from the `Build Mobile App` (`build.yml`) workflow —
`ios-sourcemaps-main-rc` (contains `index.js.map`) or
`android-sourcemaps-main-rc` (contains `index.android.bundle.map`). Download
and unzip.

Four traps, each of which silently produces an unusable, mismatched or missing
map:

- **A `yarn watch` / Metro dev-server map does not work here.** Metro's
  `/index.map` endpoint serves a **dev** bundle map, which does not correctly
  symbolicate a **release** Hermes profile — different minification, different
  module IDs. Always use the Release/RC-build map above, not a running
  watcher.
- **Omitting `--sourcemap-path` does not mean "no source map".** The CLI then
  calls its own `findSourcemap()`: it looks for an Android **debug** build map
  under `android/app/build/**`, and otherwise downloads `/index.map` from
  whatever Metro is listening on `--port` (default `8081`). So if you have
  `yarn watch` running, an innocent-looking mapless conversion quietly feeds
  the transformer a dev map — which crashes it
  (`TypeError: Cannot read properties of undefined (reading 'map')` from
  `source-map-consumer`) or, worse, succeeds with wrong attributions. To
  convert genuinely without a map, stop Metro or pass a dead port
  (`--port 0`), which is exactly what `scripts/run.sh` does.
- **`yarn gen-bundle:ios` / `gen-bundle:android` do not pass
  `--sourcemap-output`** (as of this writing) — running them produces a
  bundle with no map at all. Don't use them for this.
- **The map has to come from the build that produced the capture.** A map
  built from a different commit still "works" — every position resolves to
  *something* — but the names and lines belong to different code. The tell is a
  report where function names don't match what's at that `file:line`, or where
  frames that clearly ran resolve with no self time while `[root]` swallows the
  capture. Check the two files' dates and the commit each came from; if they
  disagree, say so in the report's caveat line and treat all `file:line`
  attribution as unreliable rather than reasoning from it.

If no source maps exist at all, proceed anyway (Step 2 is skippable) but say
so explicitly in the final report — the audit becomes best-effort, and the
ownership column in particular cannot be trusted.

## Step 2 — Symbolicate (skip only if already converted, or no sourcemaps)

```bash
cd <metamask-mobile>
yarn react-native-release-profiler \
  --local /path/to/profile.cpuprofile \
  --sourcemap-path /path/to/sourcemaps/index.js.map
```

Three things about this CLI, all of which bite:

- **`--sourcemap-path` takes the `.map` file, not a directory or a zip.** The
  transformer behind it does `readFile()` + `JSON.parse()` on that path, so a
  directory fails with `EISDIR` and a zip fails to parse. Unzip a CI
  sourcemaps artifact first and point at `index.js.map` (iOS) or
  `index.android.bundle.map` (Android) inside it.
- **There is no output-path flag.** `--output` / `--dstPath` do not exist
  (passing one makes Commander exit with `unknown option`); the destination is
  hardcoded to `.`, so the file always lands in the **current working
  directory**. `cd` to where you want it, and expect the name
  `<profile-basename-without-.cpuprofile>-converted.json`.
- **Omitting `--sourcemap-path` makes it look for a map on its own** — see the
  second trap in Step 1. Add `--port 0` (or stop Metro) when you deliberately
  want a mapless conversion.

The full option list, for reference: `--local`, `--filename`,
`--sourcemap-path`, `--generate-sourcemap`, `--port`, `--appId`,
`--appIdSuffix`, `--fromDownload`, `--raw`.

The result is a JSON **array** of Chrome-trace Begin/End duration events,
each carrying `args.url` / `args.line` / `args.column` resolved to original
`app/...` source when the source map covers that frame. Without a source map
you still get a converted JSON, but `args.url` holds the raw Hermes frame
*name* rather than a path, so ownership and area attribution degrade to
whatever the minified names happen to reveal.

## Step 3 — Aggregate with the bundled analyzer

The script ships inside this skill, installed under whichever harness
directory `yarn skills` wrote to. Probe for it rather than hardcoding one
path — which of these exists depends on which harnesses were synced, and
that can differ per directory:

```bash
cd <metamask-mobile>

for AC in \
  .claude/skills/mms-swaps-cpu-profile-audit/scripts/analyze-cpuprofile.cjs \
  .cursor/rules/mms-swaps-cpu-profile-audit/scripts/analyze-cpuprofile.cjs \
  .agents/skills/mms-swaps-cpu-profile-audit/scripts/analyze-cpuprofile.cjs
do
  [ -f "$AC" ] && break
done
if [ ! -f "${AC:-}" ]; then
  echo "analyze-cpuprofile.cjs not found under .claude, .cursor, or .agents." >&2
  echo "Run 'yarn skills' to (re)sync it, then retry." >&2
  exit 1
fi

node "$AC" --profile /path/to/profile-converted.json
```

It is **read-only** — plain Node, no dependencies, no network, no repo
writes — so it needs no sandbox permission beyond reading the profile file
and this repo. It auto-detects the input shape (converted JSON array, or a
raw un-converted `.cpuprofile` object as a fallback) and prints a Markdown
report to stdout with four parts:

1. **Metrics** — format detected, capture duration, distinct frames,
   attributable JS work, the runtime/idle total that was excluded from it,
   then the JS work split three ways: swaps-owned (with the widest inclusive
   swaps span underneath it), non-swaps on the swaps path, non-swaps running
   concurrently.
2. **Swaps-owned areas (self time)** — `Area | Time | % of swaps time |
   Inclusive | # of hot spots`. The inclusive column is what saves you when
   swaps self time is ~0: it shows the work swaps code set in motion.
3. **Non-swaps areas on the swaps path** and **Non-swaps areas running
   concurrently** — separate tables, so swaps detail is never diluted by
   context. Reuse all three tables in the final report.
4. **Runtime & idle** — `[root]` (wall time with no JS running) and GC, kept
   visible but out of every percentage. Never a fix-table row.
5. **Top swaps-owned frames** and **Top non-swaps frames** — ranked by self
   time, with `file:line`, for the code reading in Step 5.

Areas that neither did work nor triggered any are dropped entirely, so an
empty row is a real signal rather than a formatting artefact.

Useful flags:

| Flag | Default | Purpose |
|---|---|---|
| `--scope <substring>` | the swaps-owned path list (`DEFAULT_SCOPE_ROOTS`) | Comma-separated substrings that define swaps ownership. Rarely needs changing; widen it only if swaps has taken over new paths not yet in the script. |
| `--top <n>` | `40` | How many ranked frames to list per section. |
| `--context-min-pct <n>` | `0.5` | Noise floor for non-swaps rows, as a % of attributable JS work (idle/GC excluded). Raise it on a noisy capture; drop to `0` to see everything. |
| `--trigger-min-pct <n>` | `5` | How much work a *zero-self-time* swaps area must have triggered (inclusive, as a % of JS work) to earn a row. Stops screens whose module merely got evaluated — a batch-sell modal the user never opened — from appearing at `0.00 ms`. |
| `--swaps-only` | off | Suppress the non-swaps and runtime tables (the aggregate metrics still show how much time they took). Only for a deliberately narrow swaps-only pass. |
| `--json` | off | Emit the aggregated JSON instead of Markdown (for further scripting). |
| `--out <path>` | stdout | Write the report to a file instead of printing it. |

### Why swaps self time can read `0.00 ms`

Self time is credited to the stack's leaf, and a React screen is rarely the
leaf — it calls the reconciler, selectors and dependencies, which do the work.
So `Swaps-owned code: 0.00 ms` alongside a large `Inclusive (ms)` means *swaps
triggered the cost without spending it*, which is still a swaps finding: look
at the `Called by swaps` rows and at the swaps call sites. Genuine "swaps did
nothing" looks different — no swaps area rows at all, because nothing swaps
owns even appeared on the stacks.

Three other things produce a misleadingly small swaps number, all worth ruling
out before writing the report:

- **Most of the capture was idle.** Check the `Runtime & idle` row; if `[root]`
  dominates, the user recorded mostly sitting still, and only the JS-work
  numbers mean anything.
- **The source map did not match the build.** See Step 1's fourth trap.
- **The interesting interaction happened outside the capture window.** Compare
  the capture length against the journey being audited.

The report header prints the capture's actual duration as a plain value in
the "Metric | Value" table — no ideal/minimum comparison for now, just the
raw timing:

```
| Metric | Value |
|---|---|
| Capture length | ~10s |
```

Use judgment on whether that duration looks long enough to cover the full
swaps/bridge journey (quote fetch, screen transitions, animations) and say
so in Step 6 (confidence) if it looks short.

Read the Markdown report yourself before writing the final audit — it is raw
aggregated data, not the finished analysis. Step 4 below is where the actual
audit work happens.

### Optional: one-shot wrapper (`scripts/run.sh`)

If the input is an archive (a zipped sourcemaps CI artifact, or a bundle
containing the `.cpuprofile` alongside other files) or you'd simply rather
not run Steps 2–3 by hand, `scripts/run.sh` (next to `analyze-cpuprofile.cjs`
in this skill) does the whole staging → convert → aggregate pipeline in one
call. Every file it extracts, converts, or writes (staged input, extracted
archives, the `*-converted.json`, the final report) goes under a throwaway
run folder created **inside the metamask-mobile repo itself**
(`<repo>/.mms-swaps-cpu-audit-run.XXXXXX/`), which is deleted automatically
when the script exits — success, failure, or interrupted — so nothing is
left on disk afterwards and there is no manual cleanup step. (An earlier
version of this script staged everything under the OS tmp directory instead;
that made `yarn --cwd <repo> react-native-release-profiler` resolve
Corepack's pinned Yarn version inconsistently, since Corepack determines the
version from the `packageManager` field by walking up from the shell's
actual cwd, not from `--cwd`. Anchoring the run folder inside the repo, and
always invoking `yarn` with the repo as cwd, avoids that.)

```bash
for RC in \
  .claude/skills/mms-swaps-cpu-profile-audit/scripts/run.sh \
  .cursor/rules/mms-swaps-cpu-profile-audit/scripts/run.sh \
  .agents/skills/mms-swaps-cpu-profile-audit/scripts/run.sh
do
  [ -f "$RC" ] && break
done

bash "$RC" \
  --repo <metamask-mobile> \
  --profile /path/to/profile.cpuprofile-or-converted.json-or-archive.zip \
  --sourcemaps /path/to/sourcemaps-dir-or.zip   # optional
```

It forwards `--scope`, `--top`, `--context-min-pct`, `--trigger-min-pct` and
`--swaps-only` to the
analyzer, and omits any you don't pass so the analyzer's own defaults apply.

It prints the same Markdown report `analyze-cpuprofile.cjs` would produce
directly, so Step 4 below still applies unchanged — by the time it returns,
its run folder has already been removed.

## Step 4 — Area map (how self time attributes to a surface)

### Swaps-owned areas

The analyzer buckets any swaps-owned frame by matching its resolved source
path against `app/components/UI/Bridge/**` subfolders, most-specific first.
This mirrors the directory as of the time this was written — re-run
`find app/components/UI/Bridge -maxdepth 2 -type d` if it looks stale, and
update `AREA_MAP` in the script if the tree has been restructured:

| Path fragment | Reported area | User-facing surface |
|---|---|---|
| `Views/BridgeView` | Swaps/Bridge screen (BridgeView) | Main swaps screen |
| `components/BridgeTokenSelector` | Asset picker (token selector modal) | Asset picker |
| `components/QuoteSelectorView` | Quote select screen | Quote select screen |
| `components/QuoteDetailsCard`, `QuoteDetailsRecipientKeyValueRow` | Quote details card | Quote select screen |
| `components/QuoteCountdownTimer` | Quote countdown timer | Quote select screen |
| `components/PostTradeBottomSheet`, `components/TransactionDetails` | Post-trade modal | Post-trade modal |
| `Views/BatchSellReview` | Batch sell — review | Batch sell |
| `Views/BatchSellTokenSelect` | Batch sell — token select | Batch sell |
| `components/BatchSell*Modal` | Batch sell — \<modal\> | Batch sell |
| `components/TokenInputArea` | Token input area | Main swaps screen |
| `components/SwapsKeypad` | Keypad | Main swaps screen |
| `components/SlippageModal` | Slippage modal | Slippage modal |
| `components/BlockaidModal`, `HighRateAlertModal`, `PriceImpactModal`, `MissingPriceModal`, `TokenWarningModal`, `MarketClosedBottomSheets` | \<respective\> modal | Warning/alert modals |
| `hooks/` | Bridge hooks | (cross-cutting — attribute to whichever screen calls the hook) |
| `utils/` | Bridge utils | (cross-cutting) |
| anywhere else under `Bridge/` | Bridge (other / unmapped subfolder) | Unmapped — read the file to place it |

Frames under `hooks/` or `utils/` are cross-cutting: the analyzer buckets
them into "Bridge hooks"/"Bridge utils" rather than a specific screen, so
when one shows up hot, check its call sites (`grep -rn "useTheHookName("
app/components/UI/Bridge`) to say which screen actually pays for it in the
report.

### Non-swaps context areas

Everything the swaps roots don't match is bucketed by `CONTEXT_AREA_MAP` —
also substring-matched, most-specific first — into readable areas rather than
one "other" pile. It covers the surfaces that realistically show up in a
capture recorded on a swaps screen:

| Path fragment (examples) | Reported area |
|---|---|
| `react-native/Libraries/Renderer`, `node_modules/react/`, `node_modules/scheduler` | React Native renderer / React runtime / React scheduler |
| `react-native-reanimated`, `react-native-gesture-handler` | Reanimated (animations) / Gesture handler |
| `@react-navigation`, `app/components/Nav`, `app/core/NavigationService` | React Navigation (library) / Navigation (app nav stack) / Navigation service |
| `react-redux`, `@reduxjs/toolkit`, `redux`, `reselect`, `redux-persist`, `app/store`, `app/selectors` | react-redux / Redux Toolkit / Redux runtime / Reselect / redux-persist / Redux store (app) / App selectors |
| `controllers/token-detection`, `token-balances`, `token-rates`, `currency-rate`, `account-tracker` | \<respective\> (polling) — the usual source of `Concurrent` time |
| `app/core/Engine`, `@metamask/*-controller(s)` | Engine / controller wiring, or the named controller |
| `app/component-library` | Design system (component-library) |
| `app/components/UI/Tokens`, `AssetOverview`, `Views/confirmations`, `components/hooks` | Token list UI / Asset overview / Confirmations / Shared app hooks |
| `app/core/Analytics`, `app/util/metrics`, `app/util` | Analytics / metrics, App utils |
| anything else under `node_modules/<pkg>` | `<pkg> (dependency)` |
| any other app path | first three path segments (e.g. `app/components/Views/Settings`) |
| no resolved path | Unknown (unsymbolicated) |

Add an entry to `CONTEXT_AREA_MAP` when a real audit produces a fallback
label that reads poorly — the fallbacks are deliberately generic, not a
statement that the code doesn't matter.

### Relation to swaps

Independently of the area, each frame carries how it related to the swaps
call stacks during the capture (`Swaps-owned`, `Called by swaps`,
`Hosts swaps screen`, `Concurrent (off swaps path)` — defined in `skill.md`).
Computed from the stacks themselves: self time accrued with a swaps frame
below it on the stack makes a frame `Called by swaps`; being on the stack when
swaps code was entered makes it `Hosts swaps screen`; never sharing a stack
with swaps code makes it `Concurrent`. When an area mixes relations, the
by-area table shows whichever relation holds the most self time, and the
per-frame table keeps the exact split.

If the user needs to route a non-swaps finding, `.github/CODEOWNERS` maps the
file path to the owning team (last matching pattern wins), e.g.
`app/components/Nav/NavigationProvider @MetaMask/mobile-platform`.

## Step 5 — Diagnose and propose fixes

For every hot frame, read the actual source at `file:line` (and its immediate
call site) before writing a finding — self/total time tells you *where*, not
*why*. Match what you read against the `performance` skill's verified
anti-pattern catalogue and cite its fix recipe rather than improvising:

| Symptom in the code | Guide |
|---|---|
| Selector returns a new array/object/identity, or mutates | `mm-selector-memoization.md` |
| Hook builds a fresh array/object/function and returns it without `useMemo`/`useCallback` | `mm-unstable-hook-return.md` |
| `useSelector(x, isEqual)` band-aid, inline `useSelector(state => state.x)` | `mm-redux-antipatterns.md` |
| `Context.Provider value={{...}}` inline object | `mm-context-performance.md` |
| `JSON.stringify` in a `useEffect`/`useMemo` dependency array | `mm-hook-dependency-arrays.md` |
| Screen/modal fetches everything on mount instead of what's visible | `mm-eager-work-on-mount.md` |
| `FlatList`/`ScrollView` rendering a growing list without perf props | `js-lists-flatlist-flashlist.md` |
| `useNativeDriver: false` animating layout properties | `mm-layout-animations.md` |

These guides live in the `performance` skill
(`domains/performance/skills/performance/references/`) — read the specific
guide before proposing the fix in your report, don't just cite the filename.

How far to go depends on ownership:

- **Swaps-owned (`Owned by swaps = Yes`)** — full diagnosis and a concrete
  fix, citing the guide.
- **`Called by swaps`** — read the swaps call site first. If swaps calls it
  too often, or with an unstable argument/dependency, the fix is a swaps fix
  even though the hot frame isn't swaps code; say so. Only when the callee
  itself is simply slow does it become the other team's.
- **`Hosts swaps screen`** — describe what the swaps screen makes the host do
  (mount cost, prop churn, provider re-render). Fix cell stays a pointer.
- **`Concurrent (off swaps path)`** — name the mechanism (poll interval,
  subscription, animation) and leave it as context for the user to route. Do
  not write a patch plan for it.

## Worked example

```bash
$ yarn react-native-release-profiler --local ~/Downloads/sampling-profiler-trace-1699999999.cpuprofile \
    --sourcemap-path ~/Downloads/ios-sourcemaps-main-rc/index.js.map
Successfully converted to Chrome tracing format and pulled the file to ./sampling-profiler-trace-1699999999-converted.json

$ node .agents/skills/mms-swaps-cpu-profile-audit/scripts/analyze-cpuprofile.cjs \
    --profile ./sampling-profiler-trace-1699999999-converted.json
# CPU profile audit — swaps/bridge + on-screen context

| Metric | Value |
|---|---|
| Format detected | converted |
| Capture length | ~5s |
| Distinct frames sampled | 42 |
| JS work sampled (attributable) | 1500.00 ms |
| Runtime & idle (root span, GC) | 2100.00 ms (58.3% of capture) — excluded from the splits below |
| Swaps-owned code | 1010.50 ms (67.4% of JS work) |
| ↳ widest swaps-owned span (inclusive) | 1402.00 ms — work swaps code set in motion, including callees |
| Non-swaps code on the swaps path | 401.20 ms (26.7% of JS work) |
| Non-swaps code running concurrently | 88.30 ms (5.9% of JS work) |

## Swaps-owned areas (self time)
| Area | Time (ms) | % of swaps time | Inclusive (ms) | # of hot spots |
|---|---|---|---|---|
| Quote select screen | 612.40 | 60.6% | 1402.00 | 6 |
| Asset picker (token selector modal) | 398.10 | 39.4% | 611.00 | 4 |

## Non-swaps areas on the swaps path (self time)
| Area | Relation to swaps | Time (ms) | % of JS work | # of hot spots |
|---|---|---|---|---|
| Navigation (app nav stack) | Hosts swaps screen | 260.00 | 17.3% | 3 |
...
```

These raw tables are aggregated data, not the finished audit — read them,
then open the top frame in each meaningful area (say
`app/components/UI/Bridge/components/QuoteSelectorView/index.tsx:88` and
`app/components/Nav/Main/MainNavigator.js:210`), read what each is actually
doing, and turn them into plain-language rows in the final report's
probable-cause/fix table (see `skill.md`'s Output format; the `Metric`/`By
area` tables above are reused as-is in the final report):

| Screen / area | Owned by swaps | Probable cause | Fix |
|---|---|---|---|
| Quote select screen | Yes | Re-sorts the entire quote list every time the screen re-renders — sort comparator is inline and not memoized — 612ms, 6x, `QuoteSelectorView/index.tsx:88` | Wrap in `useMemo` keyed on the quote list identity (see `mm-unstable-hook-return.md` if the list itself has no stable reference either) |
| Navigation (app nav stack) | No | The tab navigator re-renders its whole screen tree while the swaps screen mounts, so opening swaps pays for every sibling screen — 260ms, 3x, `Main/MainNavigator.js:210` | Not swaps-owned; owned by the navigation/platform area — raise it with them |
