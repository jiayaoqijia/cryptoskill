# Error Recovery & Troubleshooting

## Contents

- [On Failure](#on-failure)
- [Exit Codes](#exit-codes)
- [Error Codes](#error-codes)
- [Common Failures & Solutions](#common-failures--solutions)
- [Daemon Log](#daemon-log)

## On Failure

1. Read the JSON line on stdout (not stderr): `error.code` says what failed, `error.hint` what to do next, `error.retryable` whether the same command can run again unchanged.
2. Act on the exit code and `error.code` (tables below). A click, type or request timeout has `retryable: false` and says "state unknown": the action can have happened.
3. Run `mm describe-screen` (or `mm wait-for`) to see the state before you retry.
4. Capture `mm screenshot --name "debug"` for diagnosis.
5. If the cause is not in the app, read the [daemon log](#daemon-log).

Success has no `ok` field, and `mm stop` prints plain text. For the exact JSON shape, see [Output and Errors](cli-reference.md#output-and-errors).

## Exit Codes

| Exit | Meaning                                                | Do                                                                    |
| ---- | ------------------------------------------------------ | --------------------------------------------------------------------- |
| 0    | ok                                                     |                                                                       |
| 1    | anything else (internal, tool failure, unknown code)   | Read `error.message`                                                  |
| 2    | usage or validation; nothing ran                       | Fix the command                                                       |
| 3    | no session, daemon not running, daemon connection lost | `mm launch`; after `MM_DAEMON_CONNECTION_LOST` check the screen first |
| 4    | target not found or not actionable                     | `mm describe-screen`, then re-target, scroll or dismiss the keyboard  |
| 5    | timeout (click, type or request: action state unknown) | `mm describe-screen` before any retry                                 |
| 6    | platform, device, Metro or Hermes not available        | Check the device, Metro and the build                                 |
| 7    | daemon version mismatch (reserved)                     |                                                                       |

## Error Codes

| Code                         | Meaning                                                                                      |
| ---------------------------- | -------------------------------------------------------------------------------------------- |
| `MM_SESSION_ALREADY_RUNNING` | Session exists — `mm cleanup` first, or launch with `--force`                                |
| `MM_NO_ACTIVE_SESSION`       | No session — `mm launch` first                                                               |
| `MM_LAUNCH_FAILED`           | Browser launch failed                                                                        |
| `MM_INVALID_INPUT`           | Invalid parameters or flag; nothing ran                                                      |
| `MM_TARGET_NOT_FOUND`        | Element not found; a click without `--timeout` fails after 2 s, a stale ref at once — `mm describe-screen` |
| `MM_TAB_NOT_FOUND`           | Tab not found                                                                                |
| `MM_CLICK_FAILED`            | Click failed (post-find)                                                                     |
| `MM_CLICK_TIMEOUT`           | Click timed out; state unknown; the message ends with Playwright's last step — `mm describe-screen` before retrying |
| `MM_TYPE_FAILED`             | Type failed (post-find); also when the target is not an input, textarea, select or contenteditable, e.g. a button: `locator.isEditable: Element is not an <input>…`, not `MM_ELEMENT_NOT_EDITABLE` |
| `MM_TYPE_TIMEOUT`            | The field did not appear or `fill()` hung; state unknown                                     |
| `MM_ELEMENT_NOT_EDITABLE`    | Type target is read-only or disabled (browser, fails at once)                                |
| `MM_GETTEXT_FAILED`          | `get-text` failed (element detached) — re-target                                             |
| `MM_GETTEXT_TIMEOUT`         | The element did not appear or `textContent()` hung; `retryable: true`                        |
| `MM_INSPECT_FAILED`          | `mm inspect` could not read the element (non-timeout)                                        |
| `MM_HOVER_FAILED`            | `mm hover` / `mm unhover` failed (non-timeout)                                               |
| `MM_VIEWPORT_FAILED`         | `mm set-viewport` / `mm reset-viewport` could not resize the page                            |
| `MM_WAIT_TIMEOUT`            | `wait-for`, `hover`, `inspect` or `scroll-to-element` timed out                              |
| `MM_NOTIFICATION_TIMEOUT`    | `wait-for-notification` timed out                                                            |
| `MM_PAGE_CLOSED`             | Page closed during interaction — normal after some confirmations; exits 3                    |
| `MM_SCREENSHOT_FAILED`       | Screenshot capture failed                                                                    |
| `MM_BATCH_TIMEOUT`           | `batchTimeoutMs` deadline exceeded                                                           |
| `MM_CONTEXT_SWITCH_BLOCKED`  | Cannot switch context during active session                                                  |
| `MM_SET_CONTEXT_FAILED`      | Context switch failed                                                                        |
| `MM_CDP_BLOCKED`             | CDP method is in the destructive-blocklist                                                   |
| `MM_CDP_FAILED`              | CDP command execution failed or timed out                                                    |
| `MM_DAEMON_NOT_RUNNING`      | No daemon, or it refused the connection — `mm launch`                                        |
| `MM_DAEMON_CONNECTION_LOST`  | Connection failed after the request was sent; the action may have run — `mm describe-screen` |
| `MM_REQUEST_TIMEOUT`         | The CLI stopped waiting for the daemon; state unknown                                        |
| `VALIDATION_ERROR`           | Input failed the tool schema; nothing ran                                                    |

## Common Failures & Solutions

| Symptom                                                 | Likely Cause                                                           | Solution                                                           |
| ------------------------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `MM_SESSION_ALREADY_RUNNING`                            | Previous session not cleaned                                           | `mm cleanup`, or `mm launch --force`                               |
| `MM_NO_ACTIVE_SESSION` / `MM_DAEMON_NOT_RUNNING`        | No browser or no daemon                                                | `mm launch`                                                        |
| Extension not loading                                   | Extension not built                                                    | `yarn build:test` then `mm launch`                                 |
| `EADDRINUSE` port error                                 | Orphan processes                                                       | Check `.mm-server` for ports, kill the orphaned process            |
| `MM_TARGET_NOT_FOUND` on a ref                          | Removed, re-mounted or other text since the snapshot                   | `mm describe-screen`; target by `--testid` when stable             |
| `MM_WAIT_TIMEOUT`                                       | Element did not appear                                                 | `mm describe-screen`, check the screen, increase `--timeout`       |
| `MM_TARGET_NOT_FOUND` after 2 s on a click (exit 4)      | No element matches the testId or selector (wrong or not rendered yet)  | Check `mm describe-screen`; if the screen is still loading, retry with `--timeout <ms>` |
| `MM_CLICK_TIMEOUT` / `MM_TYPE_TIMEOUT`                  | Action hung; state unknown                                             | Read `(last Playwright step: …)` in the click message: `element is not enabled`, `… intercepts pointer events` (close the overlay), `resolved to hidden` (click the label); `mm describe-screen` before retrying |
| `MM_ELEMENT_NOT_EDITABLE`                               | Field is read-only or disabled                                         | Expected when verifying a read-only field; check with `mm inspect` |
| `MM_GETTEXT_TIMEOUT`                                    | Element missing (wrong testId or not rendered yet)                     | `mm describe-screen` and re-target                                 |
| `MM_GETTEXT_FAILED`                                     | Element detached                                                       | `mm describe-screen` and re-target                                 |
| `MM_PAGE_CLOSED`                                        | Confirmation auto-closed                                               | Expected — `mm describe-screen` to find the active page            |
| `MM_CDP_BLOCKED`                                        | Destructive CDP method                                                 | Use a non-blocked method                                           |
| `MM_CDP_FAILED`                                         | Invalid CDP params                                                     | Check method & params; retry with `--timeout` (max 30000)          |
| `MM_CONTEXT_SWITCH_BLOCKED`                             | Active session                                                         | `mm cleanup` before `mm set-context`                               |
| Fixtures not available                                  | Running in prod context                                                | `mm set-context e2e`                                               |
| Stale a11yRefs after navigate or reload                 | Refs not refreshed                                                     | `mm describe-screen` for fresh refs                                |
| A ref clicks the wrong element                          | After `--observe none`: a fallback `role=`/`text=` or icon-button ref  | `mm describe-screen`, or target by `--testid`                      |
| Ref click fails at once with `MM_TARGET_NOT_FOUND`      | Removed, re-mounted or changed text after the snapshot                 | Expected; `mm describe-screen` and re-target                       |
| `MM_CLICK_FAILED`: strict mode violation (exit 4)       | A fallback ref or an explicit selector/testId matches several elements | Target by `--testid`/`--selector`; scope it with `--within`        |
| `TOOL_EXECUTION_FAILED`: `Tool execution timed out after <n>ms` (exit 1) | Call cancelled at the daemon's request limit | `mm describe-screen` before retry; the action can have happened |
| `MM_REQUEST_TIMEOUT`: `request timed out after <n>ms; state unknown` (exit 5) | The daemon did not answer before the CLI's limit | `mm describe-screen` before retry; the action can have happened |
| `Error: unknown command 'knowledge-...'`                | Knowledge store removed                                                | No replacement. Discover with `mm describe-screen`                 |

## Daemon Log

`.mm-daemon.log` at the project root records every request with its outcome:

```text
[2026-11-13T15:25:10.579Z] [INFO] POST /tool/click 200 ok=false code=MM_TARGET_NOT_FOUND 2050ms
[2026-11-13T13:54:23.290Z] [INFO] POST /tool/scroll_to_element 200 ok=false code=MM_WAIT_TIMEOUT 2063ms
```

A failed tool call still answers HTTP 200 and puts the failure in the body, so the status code is not the outcome (only a schema failure logs `400 ok=false code=VALIDATION_ERROR`). Run `grep ok=false .mm-daemon.log` to list the failed calls of a run. A `run_steps` line with failed steps adds `failed=<n>/<total>` and the first failed step's code: `POST /tool/run_steps 200 ok=true failed=1/3 code=MM_WAIT_TIMEOUT …`.
