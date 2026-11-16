# Error Recovery and Troubleshooting for Mobile (iOS and Android)

## Contents

- [On Failure](#on-failure)
- [Reading a Failure](#reading-a-failure)
- [Error Codes](#error-codes)
- [Common Failures and Solutions](#common-failures-and-solutions)
- [Safe App Resolution](#safe-app-resolution)
- [Daemon Issues](#daemon-issues)
- [Metro and Hermes Failures](#metro-and-hermes-failures)

## On Failure

If launch or the toolchain is the problem (not an in-app screen issue), check the environment first.

iOS: run the environment doctor:

```bash
yarn mm:doctor
```

It prints a PASS/FAIL report for Xcode, `idb`, `idb_companion`, and a booted simulator, with install commands for anything missing, and exits non-zero when a prerequisite is absent. It checks iOS only, so it fails on an Android-only machine.

Android: `adb devices` must list exactly one `emulator-*` in state `device` (or the `--device-id` one), and `adb -s <serial> shell getprop sys.boot_completed` must print `1`.

For in-app failures:

1. Run `yarn mm describe-screen`.
2. Identify the current screen and visible blockers. If the screen is unknown, capture a screenshot.
3. Capture evidence with `yarn mm screenshot --name "debug"`.
4. Retry only after obtaining fresh accessibility references.

## Reading a Failure

With `@metamask/client-mcp-core` 0.14.0 a failed command prints **one JSON line on stdout** and exits non-zero:

```json
{"ok":false,"error":{"code":"MM_CLICK_FAILED","message":"Operation failed: Timed out waiting for element: {\"identifier\":\"does-not-exist\"} (2000ms)","retryable":false},"meta":{"timing":{…}}}
```

- Decide with `error.code` or the exit code. Do not grep stderr or match `Error:` text: stderr is for human logs only.
- `error.hint` is optional. `error.retryable` is always present and is `true` only when running the same command again, unchanged, is safe (reads and waits). It is `false` for click, type and request timeouts, because the action state is unknown.
- `meta` is present when the daemon answered. A usage error the CLI rejects before sending (exit 2) and a missing daemon (exit 3) have none; a daemon-side schema `VALIDATION_ERROR` does.
- A successful result has **no** `ok` field. `mm stop` still prints plain text (`Daemon stopped (was PID <pid> on port <port>).`, or `No daemon is running.` on stderr with exit 0).
- Without a daemon, an unknown command exits 3 (`MM_DAEMON_NOT_RUNNING`), not 2: the daemon check runs first.

| Exit | Meaning | Codes (examples) |
| --- | --- | --- |
| 0 | ok | |
| 1 | anything else (internal error, tool failure, unknown code) | `MM_LAUNCH_FAILED`, `MM_INTERNAL_ERROR`, `TOOL_EXECUTION_FAILED` (includes `Tool execution timed out`), an `MM_*` code the CLI does not know |
| 2 | usage or validation; nothing ran | `MM_INVALID_INPUT`, `MM_INVALID_CONFIG`, `VALIDATION_ERROR` |
| 3 | no session, daemon not running, daemon connection lost | `MM_NO_ACTIVE_SESSION`, `MM_DAEMON_NOT_RUNNING`, `MM_DAEMON_CONNECTION_LOST` |
| 4 | target not found or not actionable | `MM_TARGET_NOT_FOUND`, `MM_TARGET_NOT_VISIBLE`, `MM_TARGET_OBSCURED`, `MM_CLICK_FAILED` |
| 5 | timeout (click, type and request timeouts: state unknown) | `MM_WAIT_TIMEOUT`, `MM_CLICK_TIMEOUT`, `MM_REQUEST_TIMEOUT`, `MM_BATCH_TIMEOUT` |
| 6 | platform, device, Metro or Hermes not available | `MM_DEVICE_NOT_AVAILABLE`, `MM_HERMES_FAILED`, `MM_TOOL_NOT_SUPPORTED_ON_PLATFORM` |
| 7 | daemon version mismatch (reserved) | |

## Error Codes

Launch errors use the core `ErrorCode` set. `launch` preserves any consumer-thrown `MM_*` code (known or not); a code the CLI does not know reaches the caller and exits 1. The iOS and Android adapters report launch and prerequisite failures with core codes (`MM_DEPENDENCIES_MISSING`, `MM_DEVICE_NOT_AVAILABLE`, `MM_INVALID_CONFIG`, `MM_LAUNCH_FAILED`), with the platform detail in the message and remediation text, not in a dedicated `MM_IOS_*` / `MM_ANDROID_*` code.

### Interaction Errors

| Code | Exit | Meaning and recovery |
| --- | --- | --- |
| `MM_TARGET_NOT_FOUND` | 4 | The element is not in the UI tree, or the reference is stale or not targetable (`Unknown a11yRef`; for `scroll-to-element`: never found). Run `yarn mm describe-screen` and target again; a conditionally rendered section can unmount a test ID that an earlier snapshot had. A message that says `Use device_snapshot` names an MCP tool; the CLI equivalent is `mm describe-screen`. |
| `MM_TARGET_NOT_VISIBLE` | 4 | The element was found but is outside the viewport: a tap on an off-screen element, or `scroll-to-element` that could not bring it into view. Run `yarn mm scroll-to-element`, then tap. When the failing command **is** `scroll-to-element`, its hint is not useful: run `describe-screen`, check the element still exists and its `bounds`, try the other `--direction`, or tap the center of `bounds` with `mm tap-coordinates`. |
| `MM_WAIT_TIMEOUT` | 5 | The element did not appear before the deadline. `retryable: true`. Verify the screen and increase `--timeout` if the app is still transitioning. |
| `MM_TARGET_OBSCURED` | 4 | iOS: another element (keyboard, sheet, overlay) covers the tap point, so nothing was tapped. Close the keyboard with `mm click … --dismiss-keyboard`, or close the overlay first. |
| `MM_CLICK_FAILED` | 4 | The click failed for another reason. On mobile a `--testid` that never appeared usually ends here (the driver's wait timed out) rather than in `MM_TARGET_NOT_FOUND` / `MM_CLICK_TIMEOUT`. Check the test ID with `list-testids`, then re-describe. |
| `MM_CLICK_TIMEOUT` | 5 | The click hung after the element was found; the state is unknown. Describe the screen before retrying. |
| `MM_TYPE_FAILED` | 4 | The target may not be editable. Verify the selected element and keyboard state. |
| `MM_TYPE_TIMEOUT` | 5 | Input stalled; the state is unknown. Describe the screen, obtain a fresh target, and retry. |
| `MM_GETTEXT_FAILED` | 4 | The target detached or does not expose text. Re-describe and re-target. |
| `MM_GETTEXT_TIMEOUT` | 5 | Text retrieval exceeded the deadline. Retry with a fresh target or larger `--timeout`. |
| `MM_PAGE_CLOSED` | 3 | The target closed during the action. This can be expected for transitions; inspect current state. |
| `MM_BATCH_TIMEOUT` | 5 | `run-steps` exceeded `batchTimeoutMs`. Split the batch; the deadline is capped at 30000 ms. |

### Session and Launch Errors

| Code | Exit | Meaning and recovery |
| --- | --- | --- |
| `MM_SESSION_ALREADY_RUNNING` | 1 | A session or launch already exists. Run `yarn mm cleanup`, then launch again, or use `--force`. |
| `MM_NO_ACTIVE_SESSION` | 3 | No app session exists. Run `yarn mm launch`. |
| `MM_DAEMON_NOT_RUNNING` | 3 | No daemon is running, or it refused the connection. Run `yarn mm launch` (or `yarn mm serve`) to start it. |
| `MM_DAEMON_CONNECTION_LOST` | 3 | The connection failed after the request was sent. The CLI does not resend it: the action may have run, so run `describe-screen` before retrying. |
| `MM_REQUEST_TIMEOUT` | 5 | The CLI stopped waiting for the daemon. The action state is unknown: run `yarn mm describe-screen` before retrying. |
| `MM_LAUNCH_FAILED` | 1 | The app or platform driver failed to start (Android: `io.metamask did not become ready`). Run `yarn mm cleanup` and retry; inspect the device, installed app, and `.mm-daemon.log`. |
| `MM_DEPENDENCIES_MISSING` | 6 | iOS: Xcode command-line tools or `idb` (Facebook iOS Debug Bridge) are missing. Run `yarn mm:doctor`, then install `idb` with `brew tap facebook/fb && brew install idb-companion && pip3 install fb-idb`. Android: `adb` is unavailable; install Android SDK Platform-Tools and put `adb` on `PATH`. |
| `MM_DEVICE_NOT_AVAILABLE` | 6 | iOS: no simulator is booted, the given UDID does not exist, or `simctl` failed; run `xcrun simctl list devices` and boot one. Android: no or several online emulators, a `--device-id` that is not an online `emulator-<port>`, boot not completed, `io.metamask` not installed, an `adb` command failed, or an `adb reverse` conflict; check `adb devices`. Verify `--device-id`. |
| `MM_INVALID_CONFIG` | 2 | The launch options are not usable: no app installed and no `--app-bundle`, a destructive flag without `--app-bundle`, a `fox_code` mismatch, an unreachable Metro port, or an e2e-only option in this prod-only workflow. Android also rejects `--app-bundle`, `--reinstall`, `--reset-app-data` and `--allow-fox-code-mismatch` (`Android reuses the installed io.metamask app`) and a `.device-session` file. Read the remediation text in the error. |
| `MM_PORT_IN_USE` | 1 | The daemon port is already bound by stale state. Run `yarn mm stop --force`, then launch again. |
| `MM_INVALID_INPUT` | 2 | A command or flag value is malformed. Correct it before retrying. A `mm click` with no target is this case: `error.message` is the usage line. |

### Discovery and Capture Errors

| Code | Exit | Meaning and recovery |
| --- | --- | --- |
| `MM_DISCOVERY_FAILED` | 1 | A `describe-screen` / accessibility snapshot failed. Wait for transitions to settle, capture a screenshot, and verify the app has not crashed, then retry. |
| `MM_SCREENSHOT_FAILED` | 1 | The device screen capture failed. Verify the simulator or emulator is booted and the session is active. |

On mobile the screenshot is written to device-mcp's own temporary directory (`…/T/device-mcp-XXXX/screenshot-<hex>.png`), not to `MM_ARTIFACTS_DIR`, and `--name` does not change the file name. Use the `path` from the response.

### Hermes and Platform Errors

`cdp` and `hermes-targets` run against the Hermes runtime through Metro. The idb workflow surfaces a small set of codes here — do not expect granular per-phase Hermes codes.

| Code | Exit | Meaning and recovery |
| --- | --- | --- |
| `MM_HERMES_NOT_AVAILABLE` | 6 | `hermes-targets` was run on a session with no mobile driver, or Metro is not attached. Launch with `--metro-port <port>` (or `MM_METRO_PORT`) set and retry. |
| `MM_HERMES_FAILED` | 6 | Hermes target discovery failed. Verify Metro is running, the app is a development build, and one device/one Metro process per worktree. |
| `MM_CDP_BLOCKED` | 2 | The requested `cdp` method is blocked as destructive. Use a safe inspection method instead. |
| `MM_CDP_FAILED` | 1 | `cdp` execution failed or timed out. `[HERMES_CONNECTION_FAILED] … fetch failed` means Metro is not on the port used: pass `--metro-port <port>`. On Node 20 confirm `--experimental-websocket` was set at launch; inspect Metro and `.mm-daemon.log`. |
| `MM_TOOL_NOT_SUPPORTED_ON_PLATFORM` | 6 | The command is browser-only on this mobile session (`inspect`, `hover` / `unhover`, `set-viewport` / `reset-viewport`, `reload`, `navigate`, the tab commands, `clipboard`, `mock-network`, `build`), or a mobile-only command ran without a mobile driver. The message names the tool and platform, for example `Tool "inspect" is not supported on ios platform`. Use visible mobile UI interactions instead. |

## Common Failures and Solutions

| Symptom | Likely cause | Safe solution |
| --- | --- | --- |
| Previous session blocks launch | Session was not cleaned up | `yarn mm cleanup`, then `yarn mm launch` |
| No active session | The app has not been launched through the daemon | `yarn mm launch` |
| Launch cannot locate MetaMask | MetaMask is not installed on the selected device | Install the intended app build on that device, then launch again |
| Simulator is unavailable | No booted simulator or incorrect UDID | Check `xcrun simctl list devices`, boot the intended device, and use `--device-id <UDID>` |
| Emulator is unavailable | No or several online emulators, or a non-emulator serial | Check `adb devices`, leave one `emulator-*` in state `device`, and use `--device-id emulator-<port>` |
| App identity mismatch (`MM_INVALID_CONFIG`, `different fox_code`) | iOS: installed and requested builds have different `fox_code` values | Reuse the existing installed app, or install a matching build with `--app-bundle` plus `--reinstall` / `--allow-fox-code-mismatch` (destructive to wallet state) |
| `idb` not installed | Missing iOS Debug Bridge dependency (`MM_DEPENDENCIES_MISSING`) | Run `yarn mm:doctor`, then `brew tap facebook/fb && brew install idb-companion && pip3 install fb-idb` |
| Empty or failed screen snapshot | Splash screen, animation, app transition, or crash | Wait briefly, describe again, and capture a screenshot |
| Stale accessibility references | Screen changed after the references were generated | Run `yarn mm describe-screen` and use fresh references |
| Ref taps the wrong element | Ref used after a call with `--observe none` | Run `yarn mm describe-screen`, or target by `--testid` |
| `MM_REQUEST_TIMEOUT` / `MM_CLICK_TIMEOUT` / `MM_TYPE_TIMEOUT` (exit 5) | The call was cancelled or the action hung; the action state is unknown | Run `yarn mm describe-screen` before retrying; the action can have happened |
| Click on a test ID that does not exist (exit 4, `MM_CLICK_FAILED`) | On mobile the driver's wait for the target timed out and the failure is classified as a click failure | Check the ID with `yarn mm list-testids`, re-describe, then retry. Do not retry blindly if the tap may have run |
| `MM_TARGET_NOT_VISIBLE` from `scroll-to-element` (exit 4) | The element is in the tree but never came into the viewport | `describe-screen`, check its `bounds`, try the other `--direction`, raise `--maxAttempts`, or tap the center of `bounds` with `mm tap-coordinates` |
| `MM_TARGET_NOT_FOUND` from `scroll-to-element` (exit 4) | The element left the tree (conditionally rendered section) or the ID is wrong | `describe-screen` to confirm it still exists; re-open the screen that renders it |
| `MM_TARGET_OBSCURED` (exit 4) | iOS: the keyboard, a sheet or an overlay covers the tap point; nothing was tapped | `mm click … --dismiss-keyboard`, or close the overlay first |
| `MM_TOOL_NOT_SUPPORTED_ON_PLATFORM` (exit 6) | A browser-only command on a mobile session | Use visible mobile UI interactions; see [cli-reference.md](cli-reference.md#browser-only) |
| Interaction timeout | Animation, overlay, or stale/ambiguous target | Re-`describe-screen`, target by a unique test ID or fresh a11y ref (no `--within` on mobile), and increase `--timeout` only when appropriate |
| `--testId` times out | Incorrect capitalization | Use `--testid` in lowercase |
| Daemon address already in use | Stale daemon state (`MM_PORT_IN_USE`) | Run `yarn mm stop --force`, then `yarn mm launch` |

A call that runs past the daemon's request limit is cancelled and fails with `TOOL_EXECUTION_FAILED` and the message `Tool execution timed out after <n>ms` (exit 1). `MM_REQUEST_TIMEOUT` (exit 5) means the CLI stopped waiting because the daemon did not answer at all. In both cases the action state is unknown: run `yarn mm describe-screen` before retrying.

## Safe App Resolution

The mobile workflow preserves the installed app and its wallet state by default.

For a `fox_code` mismatch (`MM_INVALID_CONFIG`, message contains `different fox_code`):

1. Prefer launching the already-installed app.
2. If replacing it, build and install a matching app outside of the `mm` workflow (such as through Xcode or standard repository setup scripts), or install it through the guarded `mm` path with `--app-bundle <path> --reinstall`. Both `--reinstall` and `--allow-fox-code-mismatch` are destructive to existing wallet state.

## Daemon Issues

If the CLI hangs or returns connection errors:

1. Check status: `yarn mm status`.
2. Stop stale state: `yarn mm stop --force`.
3. Inspect `.mm-daemon.log`. Every request line ends with the outcome, for example `POST /tool/scroll_to_element 200 ok=false code=MM_TARGET_NOT_VISIBLE 15957ms`; `grep ok=false .mm-daemon.log` lists the failed calls of a run.
4. Restart with `yarn mm launch`.

The daemon shuts down after 30 minutes of inactivity. Its state is stored in `.mm-server` at the project root, isolated per worktree.

## Metro and Hermes Failures

If Metro attachment or Hermes inspection fails:

1. Start Metro with `yarn watch:clean`.
2. Verify its status endpoint, normally `http://localhost:8081/status`.
3. Ensure `--metro-port <port>` (or `MM_METRO_PORT`) matches the running Metro process.
4. Confirm the installed app is a compatible development build and belongs to the selected device.
5. Use one Metro process and one active device per worktree to avoid target ambiguity.
6. Inspect `.mm-daemon.log` for attachment and target-selection details.
7. Restart safely:

   ```bash
   yarn mm cleanup
   yarn mm launch --metro-port 8081
   ```

On Node 20, launch the daemon with `NODE_OPTIONS="--experimental-websocket"` when Hermes WebSocket support is required. Node 22 and later provide WebSocket support directly.
