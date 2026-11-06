---
repo: metamask-mobile
parent: mobile-visual-testing
metadata:
  location: test/llm-workflow/
  type: mobile-testing
---

# MetaMask Mobile Visual Testing — iOS & Android

Use this skill to visually validate MetaMask Mobile through the project-local `mm` CLI on **both iOS (Simulator) and Android (emulator/device)**. The same commands work on both platforms — pick the target with `mm launch --platform ios|android`.

> Nearly everything below is platform-agnostic. The only differences are the **prerequisites** (idb/simctl on iOS vs. adb/emulator on Android), the `--app-bundle` artifact (`.app` vs. `.apk`), and a couple of Android-only capabilities (WebView DOM access, the Android snapshot helper). Those are called out where they apply.

## Architecture

The `mm` CLI and a persistent local HTTP daemon come from `@metamask/client-mcp-core`. The device backend is `@metamask/device-mcp`, which drives the **iOS Simulator through `idb`** (`idb-companion` + `fb-idb`) and **Android through `adb`** (`uiautomator` + an instrumentation helper). Accessibility trees, taps, typing, and screenshots all flow through that backend — there is no XCUITest runner in this workflow. The `mm cdp` / `hermes_targets` commands reach the React Native Hermes JS runtime via Metro on both platforms.

For full architecture, component locations, and safety details, see the on-demand references below and the in-repo doc `tests/llm-workflow/README.md`.

## Scope

- iOS Simulator or Android emulator/device, driven by the same `mm` CLI (`mm launch --platform ios|android`).
- Prod-only; preserves installed app/wallet state by default; reuses an installed MetaMask app on the target device.
- The workflow does not build the app, discover local build outputs, or initialize test state — install a build separately first (`--app-bundle <path>` on launch, or a manual `adb install` / simulator install).

## Prerequisites

```bash
# Verify the toolchain (Xcode/idb for iOS, adb/emulator for Android, a booted device)
yarn mm:doctor

# iOS: install idb if MM_DEPENDENCIES_MISSING is reported
brew tap facebook/fb && brew install idb-companion && pip3 install fb-idb
# iOS: boot a simulator when needed
xcrun simctl boot <UDID>

# Android: ensure adb is on PATH (Android SDK platform-tools) and a device is up
adb devices                 # confirm an emulator/device is attached
adb install -r /path/to/metamask.apk   # install a build if one isn't present

# Build/install MetaMask separately if it is not already installed
yarn setup && yarn start:ios     # or: yarn start:android
```

Run `yarn mm:doctor` before launching; it prints a PASS/FAIL report with install commands for anything missing and exits non-zero when a prerequisite is absent. If an app is not installed, install it separately on the target device/simulator before launching (or pass `--app-bundle` on launch).

## Required Workflow

### 1. Launch

```bash
# Reuse the installed app and its current state (pick the platform)
yarn mm launch --platform ios
yarn mm launch --platform android

# Pin a specific device/emulator (same --device-id flag on both platforms;
# value differs: iOS = simulator UDID, Android = adb serial e.g. emulator-5554)
yarn mm launch --platform ios --device-id <UDID>
yarn mm launch --platform android --device-id emulator-5554

# Install a specific build before launching (iOS .app / Android .apk)
yarn mm launch --platform ios --app-bundle ios/build/MetaMask.app
yarn mm launch --platform android --app-bundle /path/to/metamask.apk

# Force-replace an existing active session (runs cleanup first)
yarn mm launch --force
```

There is only one supported environment: prod. Do not request or switch launch contexts. Supplying `--context e2e` is rejected.

When a session is already active, `mm launch` rejects with `MM_SESSION_ALREADY_RUNNING` unless `--force` is passed (which cleans up the existing session then launches a new one).

`--reinstall`, `--reset-app-data`, and `--allow-fox-code-mismatch` are destructive to the installed wallet state and are guarded (a destructive flag requires `--app-bundle`). See [references/cli-reference.md](references/cli-reference.md#destructive-launch-flags).

When attaching to Metro (`--metro-port`), the workflow is **attach-only** — it never spawns Metro. If the app is already running and healthily attached to Metro (Hermes target found at `/json`), `mm launch` connects without relaunching. If the app is not healthily attached, it terminates and re-launches via the deep link. On a fresh-booted simulator, a one-time relaunch ensures the accessibility tree is valid. Release/prod builds have no Hermes inspector; Metro attach requires a dev build.

### 2. Observe Before Acting

```bash
yarn mm describe-screen
```

Use fresh output after navigation. Accessibility refs (`e1`, `e2`, ...) are ephemeral: always take refs from the latest response (`describe-screen` or the `observations` of your last action).

**Observation efficiency:** mutating actions (`click`, `type`, ...) and `run-steps` return a compact diff of what changed. Reads, discovery commands and `mm cdp` return no observation. Use the global `--observe <none|diff|full>` flag to change the observation of one call:

```bash
yarn mm click --testid log-in-button --observe none   # chain known actions: skip the observation
yarn mm click e5 --observe full                        # after navigation: get the whole screen
```

Only mutating and batch calls wait for animations before they observe. To get a settled screen after an action, let the action observe (`--observe full`) instead of running a read afterwards.

### 3. Interact

Two targeting methods work on both iOS and Android: **test IDs** and **accessibility refs**. Use one per command; prefer a stable test ID, fall back to a fresh a11y ref from `describe-screen`. On Android, a test ID matches the element's `resource-id` / content-description / text (fuzzy, case-insensitive); on iOS it matches the accessibility identifier/label.

```bash
yarn mm click --testid unlock-submit
yarn mm type --testid unlock-password "<password supplied for this wallet>"
yarn mm wait-for --testid account-overview --timeout 15000
yarn mm get-text --testid balance-display

yarn mm click e5
yarn mm type e2 "text"
```

`--selector` (CSS) and `--within` (scoped search) are **rejected by the mobile driver** on both platforms even though the shared CLI accepts the flags — see Gotchas. To disambiguate duplicate targets, use a unique test ID or the exact element's fresh a11y ref.

The CLI flag is `--testid` (all lowercase); `--testId` is silently mis-parsed as a positional target and hits the wrong element. `mm type` clears the field before typing (iOS: idb `cmd+a` → delete → type; Android: the backend clears via adb before `input text`).

### 4. Verify and Capture Evidence

After a mutating sequence:

1. Run `yarn mm describe-screen`.
2. Confirm the expected state.
3. Capture meaningful before/after evidence:

```bash
yarn mm screenshot --name "after-action"
```

If the state is wrong, capture a debug screenshot and retry from fresh refs.

### 5. Cleanup

```bash
yarn mm cleanup
yarn mm cleanup --shutdown
```

Always clean up when testing is complete.

## Android specifics

Android runs the **same `mm` workflow** shown above (`mm launch --platform android`, `describe-screen`, `click`, `type`, `wait-for`, `screenshot`, `cleanup`). Under the hood the device backend uses `adb` (`uiautomator` + an instrumentation helper) instead of `idb`. Only these deltas matter:

- **Prerequisites:** `adb` on `PATH` (Android SDK platform-tools) and a booted emulator/attached device (`adb devices`), instead of idb/simctl.
- **Install artifact:** `--app-bundle` takes a `.apk`. You can also `adb install -r /path/to/metamask.apk` beforehand and just `mm launch --platform android`.
- **Default package:** `io.metamask` (vs. `io.metamask.MetaMask` on iOS) — relevant for `mm open-app` / `mm close-app` and the `--app-id` on `mm cdp`.
- **Back button:** Android has a real hardware back button — `mm press-button back` navigates back (on iOS `back` maps to home).
- **In-app browser / dapp web content (Android-only capability):** MetaMask's in-app browser is an Android `WebView` whose **web-page DOM is not reliably targetable by accessibility position**. Drive the page via the WebView CDP path (`mm device-context switch WEBVIEW`, or the `webview_cdp` MCP tool: full `Runtime`/`DOM`/`Page`/`Input` surface) and switch back to native for MetaMask's connection/signature sheets. A typical dapp flow alternates between the two. `mm device-context list` shows a `WEBVIEW` context when a debuggable WebView is open. There is no iOS equivalent in this workflow.
- **Snapshots on churny screens:** see the next section — Android needs the bundled snapshot helper where iOS does not.

## Android snapshots & the bundled snapshot helper

The Android device backend captures the hierarchy with `uiautomator dump`. But `uiautomator dump` internally calls `UiAutomation.waitForIdle`, which **never returns** on a continuously-redrawing screen (a React Native screen with polling, an animating skeleton, a spinner). Those snapshots fail with:

```
ERROR: could not get idle state.
```

To handle this, `@metamask/device-mcp` (0.7.0 in MetaMask Mobile) **ships a small self-instrumenting snapshot-helper APK** (`node_modules/@metamask/device-mcp/dist/android/device-mcp-android-snapshot-helper-<version>.apk`, package `io.metamask.devicemcp.snapshothelper`). The helper captures the hierarchy **without** waiting for idle and streams it back over `am instrument`. It is a `testOnly` APK installed on demand with `adb install -t`, reused across the session, and its signing certificate is cryptographically verified before use (fails **closed** on a signer mismatch rather than silently falling back). The helper is a **separate app** from MetaMask: it shares the `io.metamask` prefix but is a distinct package, and the backend resolves it by exact package name (`pm list packages`/`pm path` on the full `io.metamask.devicemcp.snapshothelper`), so it never collides with the wallet's `io.metamask` package or with `mm open-app`/`close-app`/`cdp --app-id`.

Behavior is controlled by the `DEVICE_MCP_ADB_SNAPSHOT` env var on the device backend (`@metamask/device-mcp`, which the `mm` CLI drives on Android):

- **`helper-first`** (default since `@metamask/device-mcp` 0.6.0) — the bundled helper first (fast on busy screens, and a fuller tree than the dump, including WebView content), then one `uiautomator dump` attempt (three if the helper never ran) for non-trust helper failures only.
- **`auto`** — fast `uiautomator dump` first, then the bundled helper, then remaining dump retries. Sticky per session: once the helper wins, later snapshots skip the quick dump.
- **`instrument`** — use the bundled helper only, with no dump fallback (fully fail-closed).
- **`dump`** — stock `uiautomator dump` only; the helper APK is never installed.

The first helper snapshot of a session can take longer, because it can install the helper (its own timeout, up to 60 s).

Operational guidance when a snapshot fails to capture:

1. If you see `could not get idle state` or `Capture did not stabilize within 500ms`, the screen is redrawing or in transition — retry; the backend already retries the helper before any dump fallback.
2. If it still fails, restart the session with `DEVICE_MCP_ADB_SNAPSHOT=instrument` in the environment to force the helper path.
3. If snapshots fail **closed with a trust/signer error**, a different app is squatting the helper's package name — uninstall it (`adb uninstall io.metamask.devicemcp.snapshothelper`) so the bundled, correctly-signed helper can install, or fall back to `DEVICE_MCP_ADB_SNAPSHOT=dump`.
4. As a last resort, use `mm screenshot` (always works) plus `mm tap-coordinates` from the image, or drive web content via the WebView CDP path.

The helper does not exist for iOS — idb's `describe-all` does not require an idle wait.

## Metro and Runtime Inspection

For JS development, attach the installed development app to Metro. The workflow is attach-only — start Metro separately:

```bash
yarn watch:clean
yarn mm launch --metro-port 8081

# Equivalent, still supported (the flag wins when both are set)
MM_METRO_PORT=8081 yarn mm launch
```

If Metro is not reachable on the given port, launch fails with `MM_INVALID_CONFIG`. If the app is already running and healthily attached to Metro, `mm launch` connects without relaunching (pure-attach). Release/prod builds have no Hermes inspector; Metro attach requires a dev build.

Node 20 may require `NODE_OPTIONS="--experimental-websocket"` for `mm cdp`; Node 22+ includes WebSocket support.

`mm cdp` evaluates JavaScript in the Hermes runtime through Metro's inspector proxy:

```bash
yarn mm cdp Runtime.evaluate '{"expression":"JSON.stringify(globalThis.__DEV__)"}'
```

Prefer controller methods over raw Redux mutation when inspecting or changing runtime state. Runtime modifications affect the current installed app state; restore any state changed during testing.

## Batching

Use `run-steps` only for known deterministic sequences:

```bash
yarn mm run-steps '{"steps":[
  {"tool":"type","args":{"testId":"login-password-input","text":"<password>"}},
  {"tool":"click","args":{"testId":"log-in-button"}},
  {"tool":"wait_for","args":{"testId":"wallet-screen","timeoutMs":15000}}
]}'
```

The input must be an object containing `steps`, not a bare array.

- Add `batchTimeoutMs` (1000–30000 ms) for an overall deadline. The whole call stops after 30 s, so use a lower value (for example 20000) to get partial results, and split longer flows into several batches.
- Add a top-level `observe` (`none` / `diff` / `full`, default `diff`) to set the observation collected after the batch. `includeObservations` was removed; check `summary.ok` to react to failures.

Pattern: discover with `yarn mm describe-screen` → batch known steps with `yarn mm run-steps` → re-verify with `yarn mm describe-screen`.

## Mobile Limitations and Gotchas

- **Only `--testid` and a11y refs target elements.** `--selector` throws (`CSS selectors are not supported on mobile`) and `--within` throws (`Scoped element search (within) is not supported on mobile`) at the driver on both iOS and Android, even though the shared CLI parses both flags. Do not use them.
- **`--testid` is case-sensitive and lowercase.** `--testId` is not recognized as a flag; the value is treated as a positional target and silently hits the wrong element (usually timing out).
- **Element matching is fuzzy and case-insensitive.** The backend matches on accessibility attributes by substring (iOS: label/identifier; Android: content-description/resource-id/text), so `--testid Confirm` can match `Confirm Transaction`. Prefer exact, unique test IDs to avoid hitting the wrong element.
- **`mm type` clears first** on both platforms, so there is no need to clear the field manually. There is no trailing-newline submit trick; to submit, tap the on-screen keyboard action button (a fresh a11y ref) or the form's submit control.
- No `mm build`; build/install separately.
- No URL navigation, tab switching, browser notification pages, or browser clipboard APIs.
- `navigate-home` and `navigate-settings` are not implemented; navigate through visible UI elements.
- `mm cdp` requires Metro. It does not reuse the launch's `--metro-port`, so pass `--metro-port <port>` on each `cdp` / `hermes-targets` call when Metro is not on 8081.
- One Metro process per worktree is recommended.
- Mutating commands return compact diff observations; request a full `describe-screen` whenever refs or state are uncertain.
- **After a call with `--observe none`, refs are not refreshed.** Target by `--testid`, or run `describe-screen` before you use refs again: a stale ref can tap a different element.
- **Output is one line of JSON** when stdout is not a terminal. Parse it as JSON. Add `--pretty` (or set `MM_PRETTY=1`) only when a human reads the output.
- **Observations carry no app state**, and `mm get-state` on mobile only reports whether the app is loaded (`source: "stub"`). Identify the screen from `describe-screen` test IDs (`login-password-input` = unlock, `wallet-screen` = wallet home). Read wallet state (account, network, balance) from the screen or through `mm cdp`.
- **The keyboard can cover the submit button.** After `mm type` into the unlock field, the iOS keyboard covers **Unlock**. On iOS, `mm dismiss-keyboard` fails (`idb ui key RETURN` is rejected by idb), so tap the keyboard's return key instead: `mm click --testid Done` (it also submits the unlock form). On Android, `mm press-button back` hides the keyboard, then `mm click --testid log-in-button`.
- **A navigation can finish after the observation.** The mobile observation retries for at most about 2 s, so after a tap that opens a slow screen (for example the first **Send** of a session) `observations` can still show the previous screen. Confirm with `mm wait-for --testid <id on the new screen>` before the next step.
- **iOS wallet home actions (Buy / Swap / Send / Receive) are not in the tree.** On iOS 18+ the snapshot reads the `axbridge` tree, where the balance hero and the action row are one unlabelled container, so `wallet-send-button` and the other action test IDs are missing and `click --testid wallet-send-button` times out. Take the button position from `mm screenshot` and use `mm tap-coordinates <x> <y>` (points). The next screens (for example Send, with `send-navbar-back-button`) are in the tree again.
- **`--testid` matches a substring, not the exact ID.** The tap goes to the first element in tree order whose test ID *contains* the value, and an a11y ref resolves to the same test ID query. On the Android wallet home, `click --testid account-picker` (or its ref) taps `account-picker-avatar` inside `profile-button` and opens the profile screen ("Create profile"). If the screen after a tap is not the expected one, check `list-testids` for longer IDs that contain your value, and use `mm tap-coordinates` at the center of the element's `bounds` from `describe-screen` (Android: pixels; for `account-picker`, `384 136`).
- **Timed-out calls are cancelled.** On `Tool execution timed out`, an action that already started can still have happened, so run `describe-screen` before you retry.
- Call `node_modules/.bin/mm` directly to skip the Yarn startup (about 0.4–0.5 s per call) when running many commands.
- Never assume wallet credentials, balances, networks, or onboarding state. Inspect the installed app and obtain needed credentials from the user/environment.

## Error Recovery

- `MM_DEPENDENCIES_MISSING`: a required toolchain is missing. Run `yarn mm:doctor`. iOS: `brew tap facebook/fb && brew install idb-companion && pip3 install fb-idb`. Android: install the Android SDK platform-tools so `adb` is on `PATH`.
- `MM_WAIT_TIMEOUT`: target did not become visible; describe the screen and verify scope/test ID.
- `MM_CLICK_TIMEOUT`: click may have completed; describe before retrying.
- `MM_TYPE_TIMEOUT`: field interaction stalled; inspect focus and use a fresh target.
- `MM_DEVICE_NOT_AVAILABLE`: no device is booted, the id does not exist, or the device tool failed. iOS: `xcrun simctl list devices` and boot one. Android: `adb devices` and start an emulator. Verify MetaMask is installed.
- `MM_INVALID_CONFIG`: the launch options are unusable — no app and no `--app-bundle`, a destructive flag without `--app-bundle`, a `fox_code` mismatch, or an unreachable Metro port. Read the remediation text; reuse the installed app or install a matching build.

Launch errors use core `ErrorCode`s (not `MM_IOS_*`/`MM_ANDROID_*`): `@metamask/client-mcp-core` collapses unknown consumer codes into `MM_LAUNCH_FAILED`, so platform-specific detail is carried in the message and remediation.

For the full error-code table and troubleshooting, see [references/error-recovery.md](references/error-recovery.md).

## Reference Guides

Load these on demand — not required for standard visual testing:

- **[references/cli-reference.md](references/cli-reference.md)** — full command tables, syntax rules, targeting details, and commands not available on mobile.
- **[references/error-recovery.md](references/error-recovery.md)** — error codes, common failures, and troubleshooting.
- **[references/state-manipulation.md](references/state-manipulation.md)** — read/write runtime state and call controller methods via `mm cdp` (Hermes runtime).
- **[references/runtime-monitoring.md](references/runtime-monitoring.md)** — capture network requests and console logs via Hermes runtime interceptors. Load when testing flows that involve API calls or debugging silent failures.

## References and Attribution

- **In-repo workflow doc:** `tests/llm-workflow/README.md` — daemon/session architecture, installed-app safety, and the canonical prerequisites (`idb`, `yarn mm:doctor`).
- **Upstream packages:** `@metamask/client-mcp-core` (the `mm` CLI + daemon, iOS and Android) and `@metamask/device-mcp` (device backend: idb for iOS, ADB for Android, plus the bundled Android snapshot-helper APK).
