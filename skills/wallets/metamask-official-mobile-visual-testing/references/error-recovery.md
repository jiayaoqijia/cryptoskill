# Error Recovery and Troubleshooting for Mobile (iOS)

## Contents

- [On Failure](#on-failure)
- [Error Codes](#error-codes)
- [Common Failures and Solutions](#common-failures-and-solutions)
- [Safe App Resolution](#safe-app-resolution)
- [Daemon Issues](#daemon-issues)
- [Metro and Hermes Failures](#metro-and-hermes-failures)

## On Failure

If launch or the iOS toolchain is the problem (not an in-app screen issue), run the environment doctor first:

```bash
yarn mm:doctor
```

It prints a PASS/FAIL report for Xcode, `idb`, `idb_companion`, and a booted simulator, with install commands for anything missing, and exits non-zero when a prerequisite is absent. This is the fastest way to resolve `MM_DEPENDENCIES_MISSING` and `MM_DEVICE_NOT_AVAILABLE`.

For in-app failures:

1. Run `yarn mm describe-screen`.
2. Identify the current screen and visible blockers. If the screen is unknown, capture a screenshot.
3. Query prior successful runs:

   ```bash
   yarn mm knowledge-search "<flow name>"
   yarn mm knowledge-sessions
   yarn mm knowledge-last
   ```

4. Capture evidence with `yarn mm screenshot --name "debug"`.
5. Retry only after obtaining fresh accessibility references.

## Error Codes

Launch errors use the core `ErrorCode` set. `@metamask/client-mcp-core` only preserves a consumer-thrown code when it is a known core code and otherwise collapses it into `MM_LAUNCH_FAILED`, so the iOS driver reports launch and prerequisite failures with core codes (`MM_DEPENDENCIES_MISSING`, `MM_DEVICE_NOT_AVAILABLE`, `MM_INVALID_CONFIG`, `MM_LAUNCH_FAILED`). The iOS-specific detail is carried in the message and remediation text, not in a dedicated `MM_IOS_*` code.

### Interaction Errors

| Code | Meaning and recovery |
| --- | --- |
| `MM_TARGET_NOT_FOUND` | The element is not visible or the reference is stale. Run `yarn mm describe-screen` and target again. |
| `MM_WAIT_TIMEOUT` | The element did not appear before the deadline. Verify the screen and increase `--timeout` if the app is still transitioning. |
| `MM_CLICK_FAILED` | The element was found but could not be clicked. Check for overlays, alerts, or disabled state. |
| `MM_CLICK_TIMEOUT` | The click stalled and may have completed. Describe the screen before retrying. |
| `MM_TYPE_FAILED` | The target may not be editable. Verify the selected element and keyboard state. |
| `MM_TYPE_TIMEOUT` | Input stalled. Describe the screen, obtain a fresh target, and retry. |
| `MM_GETTEXT_FAILED` | The target detached or does not expose text. Re-describe and re-target. |
| `MM_GETTEXT_TIMEOUT` | Text retrieval exceeded the deadline. Retry with a fresh target or larger `--timeout`. |
| `MM_PAGE_CLOSED` | The target closed during the action. This can be expected for transitions; inspect current state. |
| `MM_BATCH_TIMEOUT` | `run-steps` exceeded `batchTimeoutMs`. Reduce the batch or increase its deadline. |

### Session and Launch Errors

| Code | Meaning and recovery |
| --- | --- |
| `MM_SESSION_ALREADY_RUNNING` | A session or launch already exists. Run `yarn mm cleanup`, then launch again. |
| `MM_NO_ACTIVE_SESSION` | No app session exists. Run `yarn mm launch`. |
| `MM_LAUNCH_FAILED` | The app or platform driver failed to start. Run `yarn mm cleanup` and retry; inspect the simulator, installed app, and `.mm-daemon.log`. |
| `MM_DEPENDENCIES_MISSING` | Xcode command-line tools or `idb` (Facebook iOS Debug Bridge) are missing. Run `yarn mm:doctor`, then install `idb` with `brew tap facebook/fb && brew install idb-companion && pip3 install fb-idb`. |
| `MM_DEVICE_NOT_AVAILABLE` | No simulator is booted, the given UDID does not exist, or `simctl` failed. Run `xcrun simctl list devices` and boot one; verify `--device-id`. |
| `MM_INVALID_CONFIG` | The launch options are not usable: no app installed and no `--app-bundle`, a destructive flag without `--app-bundle`, a `fox_code` mismatch, an unreachable Metro port, or an e2e-only option in this prod-only workflow. Read the remediation text in the error. |
| `MM_PORT_IN_USE` | The daemon port is already bound by stale state. Run `yarn mm stop --force`, then launch again. |
| `MM_INVALID_INPUT` | A command or flag value is malformed. Correct it before retrying. |

### Discovery and Capture Errors

| Code | Meaning and recovery |
| --- | --- |
| `MM_DISCOVERY_FAILED` | A `describe-screen` / accessibility snapshot failed. Wait for transitions to settle, capture a screenshot, and verify the app has not crashed, then retry. |
| `MM_SCREENSHOT_FAILED` | The simulator screen capture failed. Verify the simulator is booted and the session is active. |

### Hermes and Platform Errors

`cdp` and `hermes-targets` run against the Hermes runtime through Metro. The idb workflow surfaces a small set of codes here — do not expect granular per-phase Hermes codes.

| Code | Meaning and recovery |
| --- | --- |
| `MM_HERMES_NOT_AVAILABLE` | `hermes-targets` was run on a session with no mobile driver, or Metro is not attached. Launch with `--metro-port <port>` (or `MM_METRO_PORT`) set and retry. |
| `MM_HERMES_FAILED` | Hermes target discovery failed. Verify Metro is running, the app is a development build, and one simulator/one Metro process per worktree. |
| `MM_CDP_BLOCKED` | The requested `cdp` method is blocked as destructive. Use a safe inspection method instead. |
| `MM_CDP_FAILED` | `cdp` execution failed or timed out. On Node 20 confirm `--experimental-websocket` was set at launch; inspect Metro and `.mm-daemon.log`. |
| `MM_TOOL_NOT_SUPPORTED_ON_PLATFORM` | The command is browser-only (or a mobile-only command was run without a mobile session). Use visible mobile UI interactions instead. |

## Common Failures and Solutions

| Symptom | Likely cause | Safe solution |
| --- | --- | --- |
| Previous session blocks launch | Session was not cleaned up | `yarn mm cleanup`, then `yarn mm launch` |
| No active session | The app has not been launched through the daemon | `yarn mm launch` |
| Launch cannot locate MetaMask | MetaMask is not installed on the selected simulator | Install the intended app build on that simulator, then launch again |
| Simulator is unavailable | No booted simulator or incorrect UDID | Check `xcrun simctl list devices`, boot the intended device, and use `--device-id <UDID>` |
| App identity mismatch (`MM_INVALID_CONFIG`, `different fox_code`) | Installed and requested builds have different `fox_code` values | Reuse the existing installed app, or install a matching build with `--app-bundle` plus `--reinstall` / `--allow-fox-code-mismatch` (destructive to wallet state) |
| `idb` not installed | Missing iOS Debug Bridge dependency (`MM_DEPENDENCIES_MISSING`) | Run `yarn mm:doctor`, then `brew tap facebook/fb && brew install idb-companion && pip3 install fb-idb` |
| Empty or failed screen snapshot | Splash screen, animation, app transition, or crash | Wait briefly, describe again, and capture a screenshot |
| Stale accessibility references | Screen changed after the references were generated | Run `yarn mm describe-screen` and use fresh references |
| Interaction timeout | Animation, overlay, or stale/ambiguous target | Re-`describe-screen`, target by a unique test ID or fresh a11y ref (no `--within` on mobile), and increase `--timeout` only when appropriate |
| `--testId` times out | Incorrect capitalization | Use `--testid` in lowercase |
| Daemon address already in use | Stale daemon state (`MM_PORT_IN_USE`) | Run `yarn mm stop --force`, then `yarn mm launch` |

## Safe App Resolution

The mobile workflow preserves the installed app and its wallet state by default.

For a `fox_code` mismatch (`MM_INVALID_CONFIG`, message contains `different fox_code`):

1. Prefer launching the already-installed app.
2. If replacing it, build and install a matching app outside of the `mm` workflow (such as through Xcode or standard repository setup scripts), or install it through the guarded `mm` path with `--app-bundle <path> --reinstall`. Both `--reinstall` and `--allow-fox-code-mismatch` are destructive to existing wallet state.

## Daemon Issues

If the CLI hangs or returns connection errors:

1. Check status: `yarn mm status`.
2. Stop stale state: `yarn mm stop --force`.
3. Inspect `.mm-daemon.log`.
4. Restart with `yarn mm launch`.

The daemon shuts down after 30 minutes of inactivity. Its state is stored in `.mm-server` at the project root, isolated per worktree.

## Metro and Hermes Failures

If Metro attachment or Hermes inspection fails:

1. Start Metro with `yarn watch:clean`.
2. Verify its status endpoint, normally `http://localhost:8081/status`.
3. Ensure `--metro-port <port>` (or `MM_METRO_PORT`) matches the running Metro process.
4. Confirm the installed app is a compatible development build and belongs to the selected simulator.
5. Use one Metro process and one active simulator per worktree to avoid target ambiguity.
6. Inspect `.mm-daemon.log` for attachment and target-selection details.
7. Restart safely:

   ```bash
   yarn mm cleanup
   yarn mm launch --metro-port 8081
   ```

On Node 20, launch the daemon with `NODE_OPTIONS="--experimental-websocket"` when Hermes WebSocket support is required. Node 22 and later provide WebSocket support directly.
