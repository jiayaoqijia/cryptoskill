---
repo: metamask-mobile
parent: mobile-visual-testing
metadata:
  location: tests/llm-workflow/
  type: mobile-testing
---

# MetaMask Mobile Visual Testing — iOS & Android

Use this skill to visually validate MetaMask Mobile through the project-local `mm` CLI on **both iOS (Simulator) and Android (emulator)**. The same commands work on both platforms — pick the target with `mm launch --platform ios|android`.

> Nearly everything below is platform-agnostic. The differences are the **prerequisites** (idb/simctl on iOS vs. adb and an emulator on Android), the app install (`--app-bundle` is iOS only), and a few Android-only capabilities (WebView CDP, the Android snapshot helper). Those are called out where they apply.

## Architecture

The `mm` CLI and a persistent local HTTP daemon come from `@metamask/client-mcp-core`. The device backend is `@metamask/device-mcp`, which drives the **iOS Simulator through `idb`** (`idb-companion` + `fb-idb`) and **Android through `adb`** (`uiautomator` + an instrumentation helper). Accessibility trees, taps, typing, and screenshots all flow through that backend — there is no XCUITest runner in this workflow. The `mm cdp` / `hermes_targets` commands reach the React Native Hermes JS runtime via Metro on both platforms.

For full architecture, component locations, and safety details, see the on-demand references below and the in-repo doc `tests/llm-workflow/README.md`.

## Scope

- iOS Simulator or Android emulator (`emulator-*` serials only; physical Android devices are not supported), driven by the same `mm` CLI (`mm launch --platform ios|android`).
- Prod-only; preserves installed app/wallet state by default; reuses an installed MetaMask app on the target device.
- The workflow does not build the app, discover local build outputs, or initialize test state — install a build separately first. On iOS you can also pass `--app-bundle <path>` on launch. Android always reuses the installed `io.metamask`.

## Prerequisites

```bash
# iOS: verify the toolchain (Xcode, idb, idb_companion, a booted simulator)
yarn mm:doctor
# iOS: install idb if MM_DEPENDENCIES_MISSING is reported
brew tap facebook/fb && brew install idb-companion && pip3 install fb-idb
# iOS: boot a simulator when needed
xcrun simctl boot <UDID>

# Android: adb on PATH (Android SDK platform-tools) and exactly one emulator in state `device`
adb devices
adb -s emulator-5554 shell getprop sys.boot_completed   # must print 1

# Build/install MetaMask separately if it is not already installed
yarn setup && yarn start:ios     # or: yarn start:android
```

`yarn mm:doctor` checks the **iOS** toolchain only: it prints a PASS/FAIL report with install commands and exits non-zero when a prerequisite is absent, so it fails on an Android-only machine. For Android, use the `adb` checks above. If MetaMask is not installed, install it on the target device before launching (on iOS you can also pass `--app-bundle`).

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

# iOS only: install a specific .app build before launching
yarn mm launch --platform ios --app-bundle ios/build/MetaMask.app

# Force-replace an existing active session (runs cleanup first)
yarn mm launch --force
```

There is only one supported environment: prod. Do not request or switch launch contexts. Supplying `--context e2e` is rejected.

When a session is already active, `mm launch` rejects with `MM_SESSION_ALREADY_RUNNING` unless `--force` is passed (which cleans up the existing session then launches a new one).

`--reinstall`, `--reset-app-data`, and `--allow-fox-code-mismatch` are destructive to the installed wallet state and are guarded (a destructive flag requires `--app-bundle`). On Android, `--app-bundle` and these three flags are rejected with `MM_INVALID_CONFIG` (`Android reuses the installed io.metamask app`). See [references/cli-reference.md](references/cli-reference.md#destructive-launch-flags).

When attaching to Metro (`--metro-port`), the workflow is **attach-only** — it never spawns Metro. If the app is already running and healthily attached to Metro (Hermes target found at `/json`), `mm launch` connects without relaunching. If the app is not healthily attached, it terminates and re-launches via the deep link. On a fresh-booted simulator, a one-time relaunch ensures the accessibility tree is valid. Release/prod builds have no Hermes inspector; Metro attach requires a dev build.

Session metadata is written to `test-artifacts/<sessionId>/session.json`. Set `MM_ARTIFACTS_DIR=<dir>` before the daemon starts to write it to `<dir>/<sessionId>/session.json` instead. On mobile that moves `session.json` only: `mm screenshot` still writes into device-mcp's temporary directory (see Gotchas).

### 2. Observe Before Acting

```bash
yarn mm describe-screen
```

Use fresh output after navigation. Accessibility refs (`e1`, `e2`, ...) are ephemeral: always take refs from the latest response (`describe-screen` or the `observations` of your last action). A node with no test ID, name or value can be listed with a ref that is not targetable (`MM_TARGET_NOT_FOUND`, `Unknown a11yRef: e6. Available refs: …`): use a named child or sibling from the `Available refs` list.

**Observation efficiency:** mutating actions (`click`, `type`, ...) and `run-steps` return a compact diff of what changed. Reads, discovery commands and `mm cdp` return no observation. Use the global `--observe <none|diff|full>` flag to change the observation of one call:

```bash
yarn mm click --testid log-in-button --observe none   # chain known actions: skip the observation
yarn mm click e5 --observe full                        # after navigation: get the whole screen
```

Only mutating and batch calls wait for animations before they observe. To get a settled screen after an action, let the action observe (`--observe full`) instead of running a read afterwards.

A **failed** command prints one JSON line on stdout and exits non-zero; stderr carries only human logs. A success has no `ok` field:

```bash
yarn mm click --testid does-not-exist --timeout 2000
# {"ok":false,"error":{"code":"MM_CLICK_FAILED","message":"Operation failed: Timed out waiting for element: {\"identifier\":\"does-not-exist\"} (2000ms)","retryable":false},"meta":{…}}
# exit code 4
```

Read `error.code` and `error.retryable` (never the message text). Exit codes: 1 other, 2 usage, 3 no session or daemon, 4 target not found or not actionable, 5 timeout (click/type/request: state unknown), 6 platform or device. See [references/error-recovery.md](references/error-recovery.md#reading-a-failure).

### 3. Interact

Two targeting methods work on both iOS and Android: **test IDs** and **accessibility refs**. Use one per command; prefer a stable test ID, fall back to a fresh a11y ref from `describe-screen`. A test ID is matched against the element's identifier — `resource-id` on Android, the accessibility identifier (`AXUniqueId`) on iOS. A match on the exact identifier wins over a case-insensitive substring match.

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

If the keyboard covers the submit button, add `--dismiss-keyboard` to the click: the driver closes the keyboard and taps once more, and the result has `keyboardDismissed: true`:

```bash
yarn mm type --testid login-password-input "<wallet password>"
yarn mm click --testid log-in-button --dismiss-keyboard
# {"clicked":true,"target":"testId:log-in-button","keyboardDismissed":true,"screenChanged":true,"observations":{…}}
```

A `click` result (iOS and Android) also has `screenChanged` when an observation was collected: `false` means the screen looks the same as before the click, which is normal for some taps (the open tab) but a hint for a button that should navigate. `true` only means something changed, so check the new screen's test IDs. Before the tap, **iOS** hit-tests the tap point: a covered target fails with `MM_TARGET_OBSCURED` and nothing is tapped. Android does not hit-test, so an overlay on top of the target receives the tap silently.

**Scrolling.** React Native keeps off-screen rows in the accessibility tree, so "in the tree" does not mean the element can be tapped. `mm scroll-to-element` swipes until the element is inside the viewport:

```bash
yarn mm scroll-to-element --testid homepage-section-title-tokens
yarn mm scroll-to-element --testid import-token-button --direction down   # reveal content below
```

`--direction` is the **content** direction (`down` reveals content below) and defaults to `auto`, which picks it from the element's position; `--maxAttempts` (default 10) caps the swipes. A success returns `{"scrolled":true,"target":"testId:…","swipes":2,"inViewport":true,"bounds":{"width":402,"x":0,"y":401.66666666666663,"height":44},"observations":{…}}`. `MM_TARGET_NOT_VISIBLE` means the element was found but never brought into view; `MM_TARGET_NOT_FOUND` means it was never in the tree.

To tell whether an element is off screen: on iOS, `visible: false` in `list-testids` / `describe-screen`. On Android do not rely on `visible` (the 0.14.0 run reported `true` for every element, even `import-token-button` at y=6936 on a 2400 px screen). Read `bounds` instead (off screen when `y` is at or past the screen height, or `height` is 0), or call `scroll-to-element` before tapping.

### 4. Verify and Capture Evidence

After a mutating sequence:

1. Run `yarn mm describe-screen`.
2. Confirm the expected state.
3. Capture meaningful before/after evidence:

```bash
yarn mm screenshot --name "after-action"
```

On mobile the returned `path` is a file in device-mcp's temporary directory (`…/T/device-mcp-XXXX/screenshot-<hex>.png`); `--name` is not reflected in the file name and `MM_ARTIFACTS_DIR` does not move it. Record the returned `path` for the evidence.

If the state is wrong, capture a debug screenshot and retry from fresh refs.

### 5. Cleanup

```bash
yarn mm cleanup
yarn mm cleanup --shutdown   # also stops the daemon
```

Always clean up when testing is complete.

## Android specifics

Android runs the **same `mm` workflow** shown above (`mm launch --platform android`, `describe-screen`, `click`, `type`, `wait-for`, `screenshot`, `cleanup`). Under the hood the device backend uses `adb` (`uiautomator` + an instrumentation helper) instead of `idb`. Only these deltas matter:

- **Prerequisites:** `adb` on `PATH` (Android SDK platform-tools) and one booted, authorized emulator (`adb devices` shows `emulator-NNNN  device`), instead of idb/simctl. Without `--device-id`, launch needs exactly one online emulator; with it, the value must be an `emulator-<port>` serial. Otherwise launch fails with `MM_DEVICE_NOT_AVAILABLE`.
- **No APK lifecycle:** Android reuses the installed `io.metamask`. `--app-bundle`, `--reinstall`, `--reset-app-data` and `--allow-fox-code-mismatch` are rejected with `MM_INVALID_CONFIG`; install the APK outside the workflow.
- **Metro:** with `--metro-port`, launch creates `adb reverse tcp:<port> tcp:<port>` when it is missing (and removes only that mapping on cleanup), reuses an identical one, and fails on a conflicting one.
- **Default package:** `io.metamask` (vs. `io.metamask.MetaMask` on iOS) — relevant for `mm open-app` / `mm close-app` and the `--app-id` on `mm cdp`.
- **Back button:** Android has a real hardware back button — `mm press-button back` navigates back (on iOS `back` maps to home).
- **Off-screen taps are refused.** `@metamask/device-mcp` 0.8.0 refuses an Android tap on an element that does not intersect the screen, so the click fails with `MM_TARGET_NOT_VISIBLE` (exit 4, `Element is outside the 1080x2400 viewport … Scroll it into view first`) and nothing is tapped. Verified on `Medium_Phone_API_36.1` with `click --testid homepage-section-title-defi` on the wallet home; the failure took about 6 s. Run `mm scroll-to-element` first.
- **In-app browser / dapp web content (Android only, not validated with this workflow):** the web-page DOM inside MetaMask's in-app browser `WebView` is not reliably targetable by accessibility position. The core CLI can send CDP to a debuggable WebView with `mm cdp <method> [params] --target android-webview [--url-filter <substr>]` (full `Runtime`/`DOM`/`Page`/`Input` surface), while MetaMask's connection and signature sheets stay native. `mm device-context switch` does not change the target on Android, and `tests/llm-workflow/README.md` lists WebView switching as unsupported, so treat this path as untested. There is no iOS equivalent.
- **Snapshots on churny screens:** see the next section — Android needs the bundled snapshot helper where iOS does not.

## Android snapshots & the bundled snapshot helper

The Android device backend captures the hierarchy with `uiautomator dump`. But `uiautomator dump` internally calls `UiAutomation.waitForIdle`, which **never returns** on a continuously-redrawing screen (a React Native screen with polling, an animating skeleton, a spinner). Those snapshots fail with:

```
ERROR: could not get idle state.
```

To handle this, `@metamask/device-mcp` (the version pinned by the workflow) **ships a small self-instrumenting snapshot-helper APK** (`node_modules/@metamask/device-mcp/dist/android/device-mcp-android-snapshot-helper-<version>.apk`, package `io.metamask.devicemcp.snapshothelper`). The helper captures the hierarchy **without** waiting for idle and streams it back over `am instrument`. It is a `testOnly` APK installed on demand with `adb install -t`, reused across the session, and its signing certificate is cryptographically verified before use (fails **closed** on a signer mismatch rather than silently falling back). The helper is a **separate app** from MetaMask: it shares the `io.metamask` prefix but is a distinct package, and the backend resolves it by exact package name (`pm list packages`/`pm path` on the full `io.metamask.devicemcp.snapshothelper`), so it never collides with the wallet's `io.metamask` package or with `mm open-app`/`close-app`/`cdp --app-id`.

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
- **The `--testid` flag is lowercase.** `--testId` is not recognized as a flag; the value is treated as a positional target and silently hits the wrong element (usually timing out).
- **Element matching is exact first, then a case-insensitive substring.** `@metamask/device-mcp` 0.8.0 looks for an element whose identifier `equals` the value somewhere in the tree before it falls back to a substring match (iOS: the accessibility identifier, `AXUniqueId`; Android: `resource-id`), so `--testid account-picker` no longer resolves to `account-picker-avatar`. When no exact match exists the substring fallback still applies: `--testid Confirm` can match `Confirm Transaction`. Prefer exact, unique test IDs. If the screen after a tap is not the expected one, check `list-testids` for longer IDs that contain your value, and use `mm tap-coordinates` at the center of the element's `bounds` from `describe-screen` (Android: pixels).
- **`mm type` clears first** on both platforms, so there is no need to clear the field manually. There is no trailing-newline submit trick; to submit, tap the on-screen keyboard action button (a fresh a11y ref) or the form's submit control.
- No `mm build`; build/install separately.
- Browser-only commands are gated off mobile sessions and fail with `MM_TOOL_NOT_SUPPORTED_ON_PLATFORM` (exit 6): `navigate` (so also `navigate-home` and `navigate-settings`), `reload`, `inspect`, `hover` / `unhover`, `set-viewport` / `reset-viewport`, the tab commands, `wait-for-notification`, `clipboard`, `mock-network` and `build`. Navigate through visible UI elements; use `mm device-clipboard` for the device clipboard.
- `mm cdp` requires Metro. It does not reuse the launch's `--metro-port`, so pass `--metro-port <port>` on each `cdp` / `hermes-targets` call when Metro is not on 8081; otherwise `cdp` fails with `MM_CDP_FAILED` (`[HERMES_CONNECTION_FAILED] … fetch failed`).
- One Metro process per worktree is recommended.
- Mutating commands return compact diff observations; request a full `describe-screen` whenever refs or state are uncertain.
- **After a call with `--observe none`, refs are not refreshed.** Target by `--testid`, or run `describe-screen` before you use refs again: a stale ref can tap a different element.
- **Output is one line of JSON** when stdout is not a terminal. Parse it as JSON. A success has no `ok` field; a failure is `{"ok":false,"error":{"code","message","hint"?,"retryable"}}` with a class exit code. Add `--pretty` (or set `MM_PRETTY=1`) only when a human reads the output.
- **Observations carry no app state**, and `mm get-state` on mobile only reports whether the app is loaded (`source: "stub"`). Identify the screen from `describe-screen` test IDs (`login-password-input` = unlock, `wallet-screen` = wallet home). Read wallet state (account, network, balance) from the screen or through `mm cdp`. The `launch` result's `state` can also carry `isUnlocked` and a generic `prerequisites` list written for the extension; do not rely on either.
- **The keyboard can cover the submit button.** Add `--dismiss-keyboard` to the click: the driver closes the covering keyboard and taps once more, and the result has `keyboardDismissed: true`. Verified on iOS for unlock (`mm type --testid login-password-input …` then `mm click --testid log-in-button --dismiss-keyboard`); it replaces the old iOS `mm click --testid Done` workaround. A bare `mm dismiss-keyboard` was not re-tested on iOS with `@metamask/device-mcp` 0.8.0 (its changelog, #48, says iOS key presses were fixed). On Android, `mm press-button back` hides the keyboard, then `mm click --testid log-in-button`. While the Android keyboard is open, `list-testids` and observations include over 100 `com.google.android.inputmethod.latin:id/*` IDs; their presence means the keyboard is open.
- **Dev builds: the Expo dev-menu button can take taps.** In a Metro-attached dev build, the Expo floating "Tools" button is drawn over the app but is not in the accessibility tree. On Android it sat over `navbar-hamburger-menu-button`, and `mm click` opened the Expo dev menu (Reload / Go home / Toggle performance monitor) while returning `clicked:true, screenChanged:true`. After a tap, check that the new screen's test IDs are the expected ones; the dev menu has no app test IDs. Close it with its **Close** item (a named ref), then tap a free part of the target with `mm tap-coordinates` from its `bounds`. Never tap **Reload** or **Go home** on a real-funds wallet.
- **A navigation can finish after the observation.** The mobile observation retries for at most about 2 s, so after a tap that opens a slow screen (for example the first **Send** of a session) `observations` can still show the previous screen. Confirm with `mm wait-for --testid <id on the new screen>` before the next step.
- **iOS wallet home actions are in the tree now.** `@metamask/device-mcp` 0.8.0 supplements the iOS `axbridge` snapshot with the identified elements the `ax` API reports (changelog #52), so `wallet-buy-button`, `wallet-swap-button`, `wallet-send-button` and `wallet-receive-button` appear in `list-testids` and `describe-screen` (verified on iPhone 17 Pro). Clicking them was not verified in the 0.14.0 run: if a click fails or times out, fall back to `mm tap-coordinates <x> <y>` (points) using the element's `bounds` or the `mm screenshot` image.
- **A test ID present in one snapshot can disappear later.** Sections that render conditionally are unmounted from the tree, not just moved off screen. On the iOS wallet home `homepage-section-title-nfts` and `homepage-section-title-defi` were in the first `describe-screen` (`visible: false`) and gone after scrolling, while `homepage-more-section` below them appeared. On `MM_TARGET_NOT_FOUND` after scrolling, re-check with `describe-screen` that the target still exists before retrying; `homepage-section-title-tokens` is a target that was verified.
- **Timed-out calls are cancelled, and the outcome is structured.** On `MM_CLICK_TIMEOUT`, `MM_TYPE_TIMEOUT` or `MM_REQUEST_TIMEOUT` (exit 5), or `TOOL_EXECUTION_FAILED` with `Tool execution timed out after <n>ms` (exit 1, the daemon's request limit), an action that already started can still have happened, so run `describe-screen` before you retry.
- Call `node_modules/.bin/mm` directly to skip the Yarn startup (about 0.4–0.5 s per call) when running many commands.
- Never assume wallet credentials, balances, networks, or onboarding state. Inspect the installed app and obtain needed credentials from the user/environment.

## Error Recovery

- `MM_DEPENDENCIES_MISSING`: a required toolchain is missing. iOS: run `yarn mm:doctor`, then `brew tap facebook/fb && brew install idb-companion && pip3 install fb-idb`. Android: install the Android SDK platform-tools so `adb` is on `PATH`.
- `MM_TARGET_NOT_FOUND`: the element is not in the tree, or a test ID left it (a conditionally rendered section); describe the screen and re-target.
- `MM_TARGET_NOT_VISIBLE`: the element was found but is outside the viewport; `mm scroll-to-element`, then tap.
- `MM_TARGET_OBSCURED`: iOS only; the keyboard, a sheet or an overlay covers the tap point and nothing was tapped. Use `--dismiss-keyboard` or close the overlay.
- `MM_CLICK_FAILED`: a mobile click whose target never appeared usually ends here; check `list-testids` and re-describe.
- `MM_WAIT_TIMEOUT`: target did not become visible (`retryable: true`); describe the screen and verify the test ID.
- `MM_CLICK_TIMEOUT` / `MM_TYPE_TIMEOUT` / `MM_REQUEST_TIMEOUT`: exit 5, action state unknown; describe before retrying.
- `MM_DEVICE_NOT_AVAILABLE`: no device is booted, the id does not exist, or the device tool failed. iOS: `xcrun simctl list devices`, boot one, and verify MetaMask is installed. Android: `adb devices` must show exactly one `emulator-*` in state `device` (or the `--device-id` one), booted, with `io.metamask` installed.
- `MM_INVALID_CONFIG`: the launch options are unusable — no app and no `--app-bundle`, a destructive flag without `--app-bundle`, a `fox_code` mismatch, an unreachable Metro port, or (Android) any APK lifecycle flag or a `.device-session` file. Read the remediation text; reuse the installed app or install a matching build.
- `MM_DAEMON_NOT_RUNNING`: no daemon, or it refused the connection; `yarn mm launch`.
- `MM_TOOL_NOT_SUPPORTED_ON_PLATFORM`: a browser-only command on a mobile session; use visible UI interactions.

Launch errors use core `ErrorCode`s (not `MM_IOS_*`/`MM_ANDROID_*`). `launch` preserves any consumer-thrown `MM_*` code; a code the CLI does not know reaches the caller and exits 1, so the platform-specific detail stays in the code and message.

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
