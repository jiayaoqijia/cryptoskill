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

Use fresh output after navigation. Accessibility refs (`e1`, `e2`, ...) are ephemeral: always take refs from the latest response (`describe-screen` or the `observations` of your last action). Every observation renumbers the refs, so a ref from the call before last can now name another element. A node with no test ID, name or value can be listed with a ref that is not targetable (`MM_TARGET_NOT_FOUND`, `Unknown a11yRef: e6. Available refs: …`): use a named child or sibling from the `Available refs` list.

**A mobile ref is not tied to its node.** It is resolved again at tap time: by the node's test ID, or, without one, by its label and type. The tap goes to the **first** element in the tree that matches. So:

- A node with `"ambiguous": true` shares its test ID or label with other nodes, and its ref can tap another one. Do not tap it by ref.
- A label-only ref (a node with no `testId`) also matches an element with a test ID and the same text.

On a real-funds wallet, tap by a unique `--testid`. Use a ref only for a node with a unique name and no `ambiguous` flag, taken from the latest response. Check the result's `target` and the next screen.

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

The CLI flag is `--testid` (all lowercase); `--testId` is silently mis-parsed as a positional target and hits the wrong element. `mm type` clears the field before typing, so a retype replaces the text. To clear a field, run `mm type <field> ""`. It clears on both platforms: on Android it exits 0 (`textLength: 0`); on iOS it exits 4 with `MM_TYPE_FAILED` (`idb ui text` rejects empty text), but the field is already empty. On iOS, `get-text` of a text field returns its placeholder, not what you typed: read the field's `textContent` in `describe-screen`.

**Covered targets.** Before the tap, the device hit-tests the tap point on **iOS and Android**. A covered target fails with `MM_TARGET_OBSCURED` (exit 4) and nothing is tapped. The message names the cover, for example `… is covered at (937, 1903) by the keyboard: android.widget.TextView` or `… by android.view.View around android.widget.ImageView label="Tools"` (the Expo dev button, see Gotchas). When the keyboard is the cover, add `--dismiss-keyboard`: the driver closes the keyboard and taps once more, and the result has `keyboardDismissed: true`:

```bash
yarn mm type --testid login-password-input "<wallet password>"
yarn mm click --testid log-in-button --dismiss-keyboard
# {"clicked":true,"target":"testId:log-in-button","keyboardDismissed":true,"screenChanged":true,"observations":{…}}
```

`mm dismiss-keyboard` closes the keyboard on its own. On Android it checks that the keyboard is gone and fails with `MM_DEVICE_ACTION_FAILED` (exit 6) if it is still shown; with no keyboard it does nothing and returns `{"dismissed":true}`.

A `click` result (iOS and Android) also has `screenChanged` when an observation was collected and there is an earlier screen to compare with (it is left out for the first click after `launch` when the calls in between used `--observe none`). `false` means the screen looks the same as before the click, which is normal for some taps (the open tab) but a hint for a button that should navigate. `true` does not prove navigation: the tapped button's press feedback alone makes it `true`. Check the new screen's test ID (see [Slow first screens](#slow-first-screens-android)).

**Scrolling.** React Native keeps off-screen rows in the accessibility tree, so "in the tree" does not mean the element can be tapped. `mm scroll-to-element` swipes until the element is inside the viewport:

```bash
yarn mm scroll-to-element --testid homepage-section-title-tokens
yarn mm scroll-to-element --testid import-token-button --direction down   # reveal content below
```

`--direction` is the **content** direction (`down` reveals content below) and defaults to `auto`, which picks it from the element's position; `--maxAttempts` (default 10) caps the swipes. A success returns `{"scrolled":true,"target":"testId:…","swipes":2,"inViewport":true,"bounds":{"width":402,"x":0,"y":401.66666666666663,"height":44},"observations":{…}}`. `MM_TARGET_NOT_VISIBLE` means the element was found but never brought into view; `MM_TARGET_NOT_FOUND` means it was never in the tree.

`visible: false` in `list-testids` / `describe-screen` means the element is off screen, on both platforms: its frame does not overlap the screen, the same rule the tap uses. Android reports off-screen rows with a zero height, so they are `visible: false`. Run `scroll-to-element` before you tap one: a tap fails with `MM_TARGET_NOT_VISIBLE`. `scroll-to-element` can still fail with `MM_TARGET_NOT_VISIBLE` for a section that never comes into view.

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

### Slow first screens (Android)

On Android, a screen that mounts for the first time in the session (for example the Explore tab after launch) can take about 2 s. The tap works, but its observation can still show the old screen, and `screenChanged` can be `true` anyway. After a tap that should open a new screen:

1. Look for the new screen's test ID in the observation (Explore: `explore-safe-area`).
2. If it is missing, run `yarn mm wait-for --testid <that id>`. It returns as soon as the screen is there.
3. **Do not tap again**: the first tap worked, and a second tap can do the action twice.

```bash
yarn mm click --testid tab-bar-item-Trending      # observation still shows wallet-screen
yarn mm wait-for --testid explore-safe-area       # found after about 1.3 s
```

Later visits to the same tab show the new screen at once. The observation also retries once while the old screen is being torn down. If an observation still looks partial, run `describe-screen` before you act on it.

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
- **Off-screen and covered taps are refused.** A tap on an element outside the screen fails with `MM_TARGET_NOT_VISIBLE` (exit 4, `Element is outside the 1080x2400 viewport … Scroll it into view first`); run `mm scroll-to-element` first. A tap on a covered element fails with `MM_TARGET_OBSCURED` (see [Interact](#3-interact)). In both cases nothing is tapped.
- **The keyboard:** while it is open, `list-testids` and observations include about 100 `com.google.android.inputmethod.latin:id/*` IDs; their presence means the keyboard is open. Close it with `mm dismiss-keyboard` or `--dismiss-keyboard` on the click.
- **In-app browser / dapp web content (Android only, not validated with this workflow):** the web-page DOM inside MetaMask's in-app browser `WebView` is not reliably targetable by accessibility position. The core CLI can send CDP to a debuggable WebView with `mm cdp <method> [params] --target android-webview [--url-filter <substr>]` (full `Runtime`/`DOM`/`Page`/`Input` surface), while MetaMask's connection and signature sheets stay native. `mm device-context switch` does not change the target on Android, and `tests/llm-workflow/README.md` lists WebView switching as unsupported, so treat this path as untested. There is no iOS equivalent.
- **Snapshots on churny screens:** see the next section — Android needs the bundled snapshot helper where iOS does not.

## Android snapshots & the bundled snapshot helper

The Android device backend captures the hierarchy with `uiautomator dump`. But `uiautomator dump` internally calls `UiAutomation.waitForIdle`, which **never returns** on a continuously-redrawing screen (a React Native screen with polling, an animating skeleton, a spinner). Those snapshots fail with:

```
ERROR: could not get idle state.
```

To handle this, `@metamask/device-mcp` (the version pinned by the workflow) **ships a small self-instrumenting snapshot-helper APK** (`node_modules/@metamask/device-mcp/dist/android/device-mcp-android-snapshot-helper-<version>.apk`, package `io.metamask.devicemcp.snapshothelper`). The helper captures the hierarchy **without** waiting for idle and streams it back over `am instrument`. It is a `testOnly` APK installed on demand with `adb install -t`, reused across the session, and its signing certificate is cryptographically verified before use (fails **closed** on a signer mismatch rather than silently falling back). The helper is a **separate app** from MetaMask: it shares the `io.metamask` prefix but is a distinct package, and the backend resolves it by exact package name (`pm list packages`/`pm path` on the full `io.metamask.devicemcp.snapshothelper`), so it never collides with the wallet's `io.metamask` package or with `mm open-app`/`close-app`/`cdp --app-id`.

Behavior is controlled by the `DEVICE_MCP_ADB_SNAPSHOT` env var on the device backend (`@metamask/device-mcp`, which the `mm` CLI drives on Android):

- **`helper-first`** (default) — the bundled helper first (fast on busy screens, and a fuller tree than the dump, including WebView content), then one `uiautomator dump` attempt (three if the helper never ran) for non-trust helper failures only.
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

`mm cdp` evaluates JavaScript in the Hermes runtime through Metro's inspector proxy. It uses the Metro port the session was launched with (`--metro-port` or `MM_METRO_PORT`), so no flag is needed on each call:

```bash
yarn mm cdp Runtime.evaluate '{"expression":"JSON.stringify(globalThis.__DEV__)"}'
```

The session keeps one Hermes connection open and reuses it. The first call connects, so it can take a bit longer; later calls reuse the open connection. `mm hermes-targets` shows `sessionMetroPort`, `connected: true` and the pinned device after the first call. A per-call `--metro-port` or `--app-id` overrides the session values for that call only (one-shot connection). A failure names the port it tried: `[HERMES_CONNECTION_FAILED] Hermes CDP connection failed: fetch failed (Metro port 8099)` (`MM_CDP_FAILED`, exit 1).

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

- `ref` is shorthand for `a11yRef` in every step that takes a target (`click`, `type`, `wait_for`, `get_text`, `scroll_to_element`, `long_press`): `{"tool":"get_text","args":{"ref":"e14"}}`.
- Add `batchTimeoutMs` (1000–30000 ms) for an overall deadline. It is checked between steps: the step in progress finishes with its own timeout, then the remaining steps are skipped and partial results come back. The CLI and the daemon wait for the deadline plus the slowest step, so the batch is not cut off mid-step.
- Add a top-level `observe` (`none` / `diff` / `full`, default `diff`) to set the observation collected after the batch. Check `summary.ok` to react to failures.

Pattern: discover with `yarn mm describe-screen` → batch known steps with `yarn mm run-steps` → re-verify with `yarn mm describe-screen`.

## Mobile Limitations and Gotchas

- **Only `--testid` and a11y refs target elements.** `--selector` throws (`CSS selectors are not supported on mobile`) and `--within` throws (`Scoped element search (within) is not supported on mobile`) at the driver on both iOS and Android, even though the shared CLI parses both flags. Do not use them.
- **A non-numeric flag value is dropped without an error.** `click --testid x --timeout abc` runs with the default timeout and still taps. Check numeric flag values before you run the command.
- **The `--testid` flag is lowercase.** `--testId` is not recognized as a flag; the value is treated as a positional target and silently hits the wrong element (usually timing out).
- **Element matching is exact first, then a case-insensitive substring.** `@metamask/device-mcp` looks for an element whose identifier `equals` the value somewhere in the tree before it falls back to a substring match (iOS: the accessibility identifier, `AXUniqueId`; Android: `resource-id`), so `--testid account-picker` resolves to `account-picker`, not `account-picker-avatar`. When no exact match exists the substring fallback still applies: `--testid Confirm` can match `Confirm Transaction`. Prefer exact, unique test IDs. If the screen after a tap is not the expected one, check `list-testids` for longer IDs that contain your value, and use `mm tap-coordinates` at the center of the element's `bounds` from `describe-screen` (Android: pixels).
- **`mm type` clears first** on both platforms, so there is no need to clear the field manually (`mm type <field> ""` clears it, see [Interact](#3-interact)). There is no trailing-newline submit trick; to submit, tap the on-screen keyboard action button (a fresh a11y ref) or the form's submit control.
- No `mm build`; build/install separately.
- Browser-only commands are gated off mobile sessions and fail with `MM_TOOL_NOT_SUPPORTED_ON_PLATFORM` (exit 6): `navigate` (so also `navigate-home` and `navigate-settings`), `reload`, `inspect`, `hover` / `unhover`, `set-viewport` / `reset-viewport`, the tab commands, `wait-for-notification`, `clipboard`, `mock-network`, `events` / `logs` / `network` and `build`. Navigate through visible UI elements; use `mm device-clipboard` for the device clipboard.
- `mm cdp` requires Metro and a session launched with `--metro-port` (or `MM_METRO_PORT`); it then reuses that port (see [Metro and Runtime Inspection](#metro-and-runtime-inspection)).
- One Metro process per worktree is recommended.
- Mutating commands return compact diff observations; request a full `describe-screen` whenever refs or state are uncertain.
- **After a call with `--observe none`, refs are not refreshed.** Target by `--testid`, or run `describe-screen` before you use refs again: a stale ref can tap a different element.
- **Output is one line of JSON** when stdout is not a terminal. Parse it as JSON. A success has no `ok` field; a failure is `{"ok":false,"error":{"code","message","hint"?,"retryable"}}` with a class exit code. Add `--pretty` (or set `MM_PRETTY=1`) only when a human reads the output.
- **Observations carry no app state**, and `mm get-state` on mobile only reports whether the app is loaded (`source: "stub"`). Identify the screen from `describe-screen` test IDs: `login-password-input` = unlock; wallet home = `wallet-screen` on Android, `account-picker` on iOS (the iOS tree can have no `wallet-screen`, so `wait-for --testid wallet-screen` can time out after a good unlock). Read wallet state (account, network, balance) from the screen or through `mm cdp`. The `launch` result's `state` can also carry `isUnlocked` and a generic `prerequisites` list written for the extension; do not rely on either.
- **Dev builds: the Expo dev "Tools" button can cover a target.** A Metro-attached dev build can show a floating "Tools" button over the app. Not every setup shows it, and it can be dragged anywhere on the screen, so where it sits depends on the setup. It is not in `testIds` or `a11y`. A click on a target under it is refused with `MM_TARGET_OBSCURED`, and the message names the button (`… by android.view.View around android.widget.ImageView label="Tools"`). A `tap-coordinates` near the target can still hit the button and open the Expo dev menu (Reload / Go home / …). To clear the target, drag the button away with `mm device-swipe` from the button's position (take it from a screenshot), then click again. If the dev menu opens, close it with `mm tap-coordinates` at the center of its close (X) button: the `Close` ref is itself refused as covered by its button, and the button has no name, so it has no usable ref. Never tap **Reload** or **Go home** on a real-funds wallet.
- **A navigation can finish after the observation.** See [Slow first screens](#slow-first-screens-android): confirm with `mm wait-for --testid <id on the new screen>`, and do not tap again.
- **iOS: the tab bar items are not in the tree.** On the iPhone 17 Pro, `describe-screen` lists only the `Tab Bar` group (y 791–874 points), not `tab-bar-item-*`, so `click --testid tab-bar-item-Trending` fails with `MM_CLICK_FAILED` after 15 s. Tap the tab with `mm tap-coordinates` from a screenshot of the tab bar (Home, Explore, Money, Social, then the `+` Actions button: never tap `+` on a real-funds wallet). Android lists `tab-bar-item-Wallet`, `tab-bar-item-Trending`, `tab-bar-item-Money` and `tab-bar-item-Social`.
- **iOS wallet home actions are in the tree.** `@metamask/device-mcp` supplements the iOS `axbridge` snapshot with the identified elements the `ax` API reports, so `wallet-buy-button`, `wallet-swap-button`, `wallet-send-button` and `wallet-receive-button` appear in `list-testids` and `describe-screen` (verified on iPhone 17 Pro). Clicking them was not verified: if a click fails or times out, fall back to `mm tap-coordinates <x> <y>` (points) using the element's `bounds` or the `mm screenshot` image.
- **A test ID present in one snapshot can disappear later.** Sections that render conditionally are unmounted from the tree, not just moved off screen. On the iOS wallet home `homepage-section-title-nfts` and `homepage-section-title-defi` were in the first `describe-screen` (`visible: false`) and gone after scrolling, while `homepage-more-section` below them appeared. On `MM_TARGET_NOT_FOUND` after scrolling, re-check with `describe-screen` that the target still exists before retrying; `homepage-section-title-tokens` is a target that was verified.
- **Timed-out calls are cancelled, and the outcome is structured.** On `MM_CLICK_TIMEOUT`, `MM_TYPE_TIMEOUT`, `MM_QUEUE_TIMEOUT` (the daemon stopped the request) or `MM_REQUEST_TIMEOUT` (the CLI stopped waiting), all exit 5, an action that already started can still have happened, so run `describe-screen` before you retry. The CLI, the daemon queue and the action share one timeout budget, so the CLI never gives up before the daemon answers. An observation that takes longer than 8 s does not fail the call: the result has `observations: {"timedOut": true}`; run `describe-screen` before you use refs.
- Call `node_modules/.bin/mm` directly to skip the Yarn startup (about 0.4–0.5 s per call) when running many commands.
- Never assume wallet credentials, balances, networks, or onboarding state. Inspect the installed app and obtain needed credentials from the user/environment.

## Error Recovery

- `MM_DEPENDENCIES_MISSING`: a required toolchain is missing. iOS: run `yarn mm:doctor`, then `brew tap facebook/fb && brew install idb-companion && pip3 install fb-idb`. Android: install the Android SDK platform-tools so `adb` is on `PATH`.
- `MM_TARGET_NOT_FOUND`: the element is not in the tree, or a test ID left it (a conditionally rendered section); describe the screen and re-target.
- `MM_TARGET_NOT_VISIBLE`: the element was found but is outside the viewport; `mm scroll-to-element`, then tap.
- `MM_TARGET_OBSCURED`: the keyboard, a sheet or an overlay (dev builds: the Expo "Tools" button) covers the tap point and nothing was tapped. Use `--dismiss-keyboard` or close or move the overlay.
- `MM_CLICK_FAILED`: a mobile click whose target never appeared usually ends here; check `list-testids` and re-describe.
- `MM_WAIT_TIMEOUT`: target did not become visible (`retryable: true`); describe the screen and verify the test ID.
- `MM_CLICK_TIMEOUT` / `MM_TYPE_TIMEOUT` / `MM_QUEUE_TIMEOUT` / `MM_REQUEST_TIMEOUT`: exit 5, action state unknown; describe before retrying.
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
