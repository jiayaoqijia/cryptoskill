# MM CLI Command Reference

Complete command reference for the `mm` CLI. For core workflow and getting started, see the main skill.

## Contents

- [Syntax Rules](#syntax-rules)
- [Global Options](#global-options)
- [Output and Errors](#output-and-errors)
- [Lifecycle](#lifecycle)
- [Interaction](#interaction)
- [Navigation & Tabs](#navigation--tabs)
- [Context](#context)
- [State & Seeding](#state--seeding)
- [Session Events](#session-events)
- [Advanced](#advanced)

## Syntax Rules

The CLI is strict about flag names and argument positions. A mistyped flag is read as the element target, so the command fails on a target that does not exist.

### Flag spelling is exact — lowercase, no variants

```bash
# CORRECT
mm click --testid unlock-submit
mm type --testid unlock-password "correct horse battery staple"

# WRONG — each flag becomes the testId: MM_TARGET_NOT_FOUND after 2 s (with --timeout: MM_CLICK_TIMEOUT)
mm click --testId unlock-submit     # capital I — treated as testId "--testId"
mm click --test-id unlock-submit    # hyphenated — treated as testId "--test-id"
mm click --TestId unlock-submit     # PascalCase — same problem
```

The only recognized flags are `--testid`, `--selector`, `--within`, `--frame` and `--timeout`; `mm inspect` adds `--styles`, and `mm scroll-to-element` adds `--direction` and `--maxAttempts` (and rejects `--frame`). Anything else (including `--testId` with a capital I) is parsed as a positional argument and used as a literal testId value, producing a locator like `[data-testid="--testId"]` that matches nothing.

### a11yRefs are positional arguments — no `--ref` flag

```bash
# CORRECT — ref is the first positional arg
mm click e5
mm type e2 "correct horse battery staple"

# WRONG — no --ref flag exists; "--ref" becomes the testId value
mm click --ref e5
```

### One targeting method per call

Each interaction command accepts exactly one of: positional a11yRef, `--testid`, or `--selector`. Do not combine them.

```bash
mm click e5                             # a11yRef (positional)
mm click --testid unlock-submit         # testId (flag)
mm click --selector "#connectButton"    # CSS selector (flag)
```

### Quick reference

| What you want | Correct syntax | Common mistake |
|---|---|---|
| Click by testId | `mm click --testid X` | `mm click --testId X` (capital I) |
| Click by a11y ref | `mm click e5` | `mm click --ref e5` (no such flag) |
| Click by CSS | `mm click --selector ".btn"` | `mm click --css ".btn"` (no such flag) |
| Type by testId | `mm type --testid X "text"` | `mm type --testId X "text"` |
| Type by a11y ref | `mm type e2 "text"` | `mm type --ref e2 "text"` |

## Global Options

These flags work with every command and can appear anywhere in the command line.

| Flag | Description |
|---|---|
| `--project <path>` | Target a specific project directory. Overrides `MM_PROJECT` and git-based discovery |
| `--observe <none\|diff\|full>` | Observation returned after the call. Default: `diff` for mutating commands and `run-steps`, `none` for reads, discovery and `cdp` |
| `--pretty` | Indent JSON output. Default: one line per result when stdout is not a terminal, indented on a terminal. `MM_PRETTY=1` / `0` sets the default |

| `--observe` level | Response |
|---|---|
| `none` | No `observations`. Fastest. Refs are **not** refreshed: run `mm describe-screen` before you use refs again |
| `diff` | Only what changed since the previous observation |
| `full` | The whole compacted screen (`a11y` + `testIds`). Becomes the new diff baseline |

Observations contain `testIds`, `a11y` and, on the browser after a mutating or batch call, `animationsSettled` — no app state. Use `mm get-state` for state.

Every tool, `launch` and `cleanup` response includes `meta.timing` (`queueMs`, `toolMs`, `observationMs`, `totalMs`).

## Output and Errors

A successful command prints one JSON line on stdout and exits 0. The response has no `ok` field: the result is at the top level, with `observations` and `meta.timing` when collected.

A failed command prints **one JSON line on stdout** and exits non-zero. When stderr is a terminal, a human also gets `Error: <message>` there. `mm launch` writes `Warning: unknown launch flag '<flag>'` to stderr and ignores the flag.

```json
{"ok":false,"error":{"code":"MM_TARGET_NOT_FOUND","message":"Selector [data-testid=\"does-not-exist\"] (testId:does-not-exist) matched 0 elements after 2000ms","hint":"Run `mm describe-screen` to get fresh refs.","retryable":false},"meta":{"timing":{"queueMs":0,"toolMs":2010,"observationMs":40,"totalMs":2050}}}
```

| Field | Meaning |
|---|---|
| `error.code` | Branch on this. |
| `error.message` | Detail for a human. A browser timeout carries Playwright's message and can contain ANSI escapes. |
| `error.hint` | What to do next, when the code has a default hint. |
| `error.retryable` | `true` only when the same command can run again unchanged. It is `false` for click, type and request timeouts: the action state is unknown. |
| `meta` | Request timing. Missing on CLI usage errors (`MM_INVALID_INPUT`) and when the daemon did not answer; schema errors (`VALIDATION_ERROR`) have it. |

| Exit | Meaning |
|---|---|
| 0 | Success |
| 1 | Anything else (internal error, unknown code) |
| 2 | Usage or validation error; nothing ran |
| 3 | No session, daemon not running, or daemon connection lost |
| 4 | Target not found or not actionable |
| 5 | Timeout |
| 6 | Platform, device, Metro or Hermes unavailable |
| 7 | Daemon version mismatch (reserved) |

With no daemon running, an unknown command or a bad flag returns exit 3 (`MM_DAEMON_NOT_RUNNING`), not 2.

`mm stop` is the exception: it prints plain text (`Daemon stopped (was PID … on port …).`) and exits 0. With no daemon it prints `No daemon is running.` on stderr and exits 0.

## Lifecycle

| Command                 | Description                            |
| ----------------------- | -------------------------------------- |
| `mm launch`             | Launch MetaMask in Chrome              |
| `mm cleanup`            | Stop browser and services              |
| `mm cleanup --shutdown` | Stop browser, services, and the daemon |
| `mm stop [--force]`     | Stop the daemon (plain-text output)    |
| `mm status`             | Show current daemon and session status |

`mm launch` starts the daemon if it is not running. `mm cleanup` leaves it up for the next launch; `mm cleanup --shutdown` and `mm stop` end it.

**Artifacts directory.** `MM_ARTIFACTS_DIR=<dir> mm launch` writes screenshots to `<dir>/screenshots/` and session metadata to `<dir>/<sessionId>/session.json`, instead of `<repo>/test-artifacts/`. The value comes from the environment of the daemon process, so pass it on the `mm launch` that starts the daemon; if a daemon is already running, `mm stop` first.

## Interaction

| Command                      | Description                                            |
| ---------------------------- | ------------------------------------------------------ |
| `mm click <ref>`             | Click element by a11y ref, testId, or selector         |
| `mm type <ref> <text>`       | Type text into element (uses `fill()`, clears first)   |
| `mm get-text <ref>`          | Read text content of element                           |
| `mm inspect <ref>`           | Attributes, disabled/read-only flags, computed styles  |
| `mm hover <ref>`             | Move the pointer over an element                       |
| `mm unhover`                 | Move the pointer off the page                          |
| `mm set-viewport <w> <h>`    | Resize the active page's viewport                      |
| `mm reset-viewport`          | Restore the size from before `set-viewport`            |
| `mm describe-screen`         | Combined state + activeTab + testIds + a11y snapshot   |
| `mm screenshot [--name <n>] [--selector <css>] [--frame <f>]` | Full page, one element, or an iframe |
| `mm wait-for <ref>`          | Wait for element to be visible                         |
| `mm scroll-to-element <ref>` | Scroll the element into view                           |
| `mm wait-for-notification`   | Wait for the confirmation page, set it as active       |
| `mm accessibility-snapshot`  | Get trimmed a11y tree with refs                        |
| `mm list-testids`            | List visible `data-testid` attributes                  |
| `mm clipboard <action>`      | Read from or write to browser clipboard                |

All interaction commands accept `--timeout <ms>` (default 15000). This is a **single deadline budget** covering visibility wait + action combined — not a per-phase timeout. The daemon queue and the CLI derive their own limits from it, so a long `--timeout` is not cut off by a 30 s request limit, and the command answers with the action's own error code (`MM_WAIT_TIMEOUT`, `MM_CLICK_TIMEOUT`, …). Commands without an action timeout (`navigate`, `describe-screen`, `screenshot`, `run-steps` without `batchTimeoutMs`, …) use the daemon queue limit, 30 s (`requestTimeoutMs` in `.mm-server`); past it they fail with `MM_QUEUE_TIMEOUT` (exit 5, state unknown).

`mm inspect` is read-only and returns no observation. `mm hover`, `mm unhover`, `mm set-viewport`, `mm reset-viewport` and `mm scroll-to-element` are mutating and observe by default.

### Why a click failed

| Case | Result |
| --- | --- |
| No `--timeout`, the target matches **0 elements** after 2 s | Fails at once: `MM_TARGET_NOT_FOUND`, exit 4, `Selector [data-testid="x"] (testId:x) matched 0 elements after 2000ms` (with `--within`, the message names the parent: `… inside testId:<parent> matched 0 elements …`) |
| `--timeout <ms>` given | Waits that long for the target to appear, then `MM_CLICK_TIMEOUT`, exit 5. Pass one when the screen is still loading |
| Target found but not clickable | `MM_CLICK_TIMEOUT`, exit 5, after the full timeout (15 s by default). The message ends with Playwright's last step |
| Target matches several elements | `MM_CLICK_FAILED`, exit 4, at once: `strict mode violation … resolved to <n> elements`. Scope it with `--within` or use a ref |

Only `mm click` fails fast. `wait-for`, `type`, `hover`, `inspect` and `scroll-to-element` wait the full timeout. A missing `--within` parent also waits the full timeout.

A `MM_CLICK_TIMEOUT` message ends with `(last Playwright step: …)`, which says why:

| Last step | Do |
| --- | --- |
| `element is not enabled` | The button is disabled; check the form state (`mm inspect` shows `disabled`) |
| `<div …> from <div class="mm-modal" data-testid="home-network-filter-modal">…</div> subtree intercepts pointer events` | Another element covers the target; close it first |
| `locator resolved to hidden <input …/>` | The element is hidden and has no single plain label; click its visible wrapper |
| `waiting for locator('[data-testid="x"]') to be visible` | The target never appeared within `--timeout`, or it is in the DOM but hidden; click its visible wrapper |

On a click or type timeout the message says "state unknown" and `retryable` is `false`. The action can have happened: run `mm describe-screen` before you retry.

**Hidden checkbox or radio.** Toggles keep the real `<input type="checkbox">` (and its testId) at 1×1 px under a styled switch, for example `basic-functionality-toggle` in Settings > Privacy. When such an input has one label (a wrapping `<label>` or `<label for>`), `mm click` clicks the label instead and the result has `"clickedLabel": true`; the input toggles. Check the new value with `mm inspect --testid <id>` (`attributes.value`). An input without a label, or whose label holds a link or button, is clicked as before.

### Waiting for the screen

Do not add `sleep`. A browser observation after a mutating or batch call has `animationsSettled`: `true` when the page loaded and its finite animations ended within the 1 s wait, `false` when some were still running. It does not cover infinite spinners or data loaded from the network. When it is `false`, or you wait for data (a new screen, a list, a toast), `mm wait-for` the element you expect and continue as soon as it is visible:

```bash
mm wait-for e7 [--timeout <ms>]
mm wait-for --testid activity-list
mm wait-for --selector "text=Copied"
```

`--selector` takes any Playwright selector, so `text=<text>` waits for visible text. The match is case-insensitive and a substring; use `text="<text>"` with quotes for an exact match.

### Element, iframe and viewport screenshots

`mm screenshot` captures the full page. `--selector <css>` captures one element, and `--frame <iframe>` captures an iframe (with `--selector`, the element inside it). `--testid` is ignored without an error: use `--selector '[data-testid="x"]'`.

```bash
mm screenshot --name send-btn --selector '[data-testid="eth-overview-send"]'   # 121x56
mm screenshot --name chart --frame e13                                          # the iframe's ref

# Viewport only
mm run-steps '{"steps":[{"tool":"screenshot","args":{"name":"viewport","fullPage":false}}],"observe":"none"}'
```

The result has the file `path`, `width` and `height`. A selector that matches nothing waits 30 s, then fails with `MM_SCREENSHOT_FAILED` (exit 1, `locator.screenshot: Timeout 30000ms exceeded`) or `MM_QUEUE_TIMEOUT` (exit 5), whichever ends first. Check that the element exists first.

### Iframes

`mm describe-screen` lists an iframe element as a node with role `iframe` (for example `{"ref":"e13","role":"iframe","name":"Advanced Chart"}`), and the accessibility nodes of up to 5 visible iframes after the page's nodes, with refs `f1e1`, `f1e2`, … (`f2e1` for the second). Use those refs like any ref. To target an element inside an iframe by testId or selector, add `--frame <iframe>` to `click`, `type`, `hover`, `wait-for`, `get-text`, `inspect` or `screenshot`. `<iframe>` is the iframe element: its ref (`e13`), `testid:<id>`, `selector:<css>` or a bare testId.

```bash
mm describe-screen --frame e13                                  # only that iframe's nodes (refs f6e1, …)
mm get-text --frame e13 --selector body
mm wait-for --frame 'selector:[data-testid="advanced-chart-iframe"] iframe' --selector body
```

- `--frame` must point at the `<iframe>` element. A testId on a wrapper fails at once: `MM_TARGET_NOT_FOUND`, `Frame not found: [data-testid="advanced-chart-iframe"] is not an iframe`. On the Extension asset page that testId is on a `<div>`; use the ref or `selector:[data-testid="advanced-chart-iframe"] iframe`.
- A missing frame on `describe-screen --frame` fails after 5 s with `MM_TARGET_NOT_FOUND` (`Frame not found: no element matches …`); on `get-text` / `wait-for` it waits for the full `--timeout`.
- `--frame` with a ref target is `MM_INVALID_INPUT` (exit 2): `f1e*` refs already point into their iframe. `scroll-to-element` and `long-press` reject `--frame`.
- A canvas-only iframe (the TradingView chart) has no accessibility nodes, so `describe-screen --frame` returns `nodes: []`. Use `mm screenshot --frame` and `get-text --frame … --selector body`.
- `mm inspect --frame` on the chart iframe failed with `MM_INSPECT_FAILED` (`Playwright did not report the element it resolved`). Use `get-text` or a screenshot there.
- `list-testids` and the `testIds` list cover the page only. Iframes inside iframes are not read.

### Several matches

When a selector or testId matches more than one element, the click fails with a strict mode violation. Scope it with `--within` (an a11yRef, `testid:<id>` or `selector:<css>`). For example, with a modal open over the page, `button[aria-label='Close']` can match two buttons:

```bash
mm click --selector "button[aria-label='Close']" --within "selector:[role=dialog]"
```

### Scroll to element

`mm scroll-to-element <ref>` scrolls the element into view, also inside a scrollable container. It waits for the element first (default 15 s) and accepts `--timeout` and `--within`.

```bash
mm scroll-to-element --testid settings-tab-item-about-us
mm scroll-to-element --testid row --within "testid:token-list"
```

On the browser:

- Success is `{"scrolled":true,"target":"testId:<id>"}`. There is no `swipes`, `inViewport` or `bounds` (those are mobile-only).
- `--direction` (and the mobile-only `--maxAttempts`) is accepted and has no effect.
- A target that never appears fails with `MM_WAIT_TIMEOUT`: exit 5, `retryable: true`. `message` is Playwright's raw `locator.waitFor` output and can contain ANSI escapes. `MM_TARGET_NOT_VISIBLE` is mobile-only. A stale or unknown a11y ref fails at once with `MM_TARGET_NOT_FOUND`.
- The element must be in the DOM. A virtualized list that renders rows only near the viewport cannot be scrolled to this way.

Playwright's `click` already scrolls its target into view, so you do not need this before `mm click`. Use it to bring an element into view for a screenshot, or to reach content further down a list.

### Element state and styles

`mm inspect <ref>` reads an element instead of judging it by eye. Browser only and read-only (no observation). Accepts `--styles <prop,prop>`, `--timeout <ms>` and `--within`.

```bash
mm inspect --testid send-continue-button
mm inspect --testid eth-overview-send --styles color,opacity,cursor,display
```

Returns `target`, `tagName`, `attributes` (every attribute, by name), `disabled` (native, `fieldset` or `aria-disabled`), `readOnly` (the `readonly` property or `aria-readonly="true"`), `styles` and `effectiveOpacity`.

`styles` has the computed value of each requested property, keyed as requested (default `color`, `background-color`, `opacity`, `cursor`); an unknown property is `""`. `effectiveOpacity` is the element's opacity times that of every ancestor, so a field faded by a parent shows it. On the e2e send page, before a recipient and amount are set, the faded Continue button (`send-continue-button`) reads `"disabled":true`, `"effectiveOpacity":0.5`, `"cursor":"not-allowed"`. To check that a field is not faded, inspect it and the field you compare it to with the same `--styles`. `mm type` into a read-only or disabled field fails at once with `MM_ELEMENT_NOT_EDITABLE` instead of waiting for the timeout.

### Hover and viewport

`mm hover <ref>` moves the pointer over an element so hover-only UI shows (a tooltip, a popover, a hover style). It waits for the element and checks that nothing covers it, like `mm click`. `mm unhover` moves the pointer off the page, so the hovered element loses its state and no other element gets one. Browser only.

```bash
mm hover --testid eth-overview-send
mm screenshot --name send-hovered
mm unhover
mm screenshot --name send-idle
```

`mm inspect --testid eth-overview-send --styles background-color` shows the change: `rgba(180, 180, 181, 0.24)` while hovered, `rgba(180, 180, 181, 0.157)` after `mm unhover`. An element hidden with opacity 0 (`effectiveOpacity: 0` in `mm inspect`) cannot be hovered: the hover waits for the full timeout and fails with `MM_WAIT_TIMEOUT`.

The pointer stays where `mm hover` left it until the next hover, click or `mm unhover`, so take the screenshot right after the hover. Success is `{"hovered":true,"target":"testId:<id>"}`; `mm unhover` returns `{"unhovered":true}`. A target that does not appear, or stays covered, fails with `MM_WAIT_TIMEOUT`; other failures return `MM_HOVER_FAILED`.

`mm set-viewport <width> <height>` resizes the active page in CSS pixels (width 100–7680, height 100–4320); `mm reset-viewport` restores the size the page had before the first `set-viewport`.

```bash
mm set-viewport 400 600    # {"width":400,"height":600,"original":{"width":1280,"height":800}}
mm screenshot --name narrow
mm reset-viewport          # {"reset":true,"viewport":{"width":1280,"height":800}}
```

`set-viewport` returns `original` (the size before the first change). `reset-viewport` returns `reset: false` when `set-viewport` was not used. The size is per page and survives reload and navigation until reset. Do not drive hover, the pointer or the viewport with `mm cdp`.

### Keyboard keys

There is no browser key command (`mm press-button` is for mobile). Send a key with CDP. For example, Escape closes a component-library modal:

```bash
mm cdp Input.dispatchKeyEvent '{"type":"keyDown","key":"Escape","code":"Escape","windowsVirtualKeyCode":27}'
mm cdp Input.dispatchKeyEvent '{"type":"keyUp","key":"Escape","code":"Escape","windowsVirtualKeyCode":27}'
```

## Navigation & Tabs

| Command                                      | Description                                   |
| -------------------------------------------- | --------------------------------------------- |
| `mm navigate <url>`                          | Navigate to a specific URL                    |
| `mm navigate-home`                           | Navigate to the extension home                |
| `mm navigate-settings`                       | Navigate to the extension settings            |
| `mm reload`                                  | Reload the active page, keeping its URL       |
| `mm switch-to-tab <role>` / `--role <role>`  | Switch active page to a different tab by role |
| `mm switch-to-tab --url <url>`               | Switch to the tab with this URL               |
| `mm close-tab --role <role>` / `--url <url>` | Close a tab                                   |

Tab roles: `extension`, `notification`, `dapp`, `other`.

`mm reload` reloads the active page and keeps its URL, including the hash route. `mm navigate-home` and `mm navigate-settings` also load the page again, at `home.html` and `home.html#settings`. Both drop state injected with `mm cdp`. The observation right after the reload can be empty; run `mm wait-for` or `mm describe-screen` before you act.

`mm switch-to-tab dapp` is equivalent to `mm switch-to-tab --role dapp`. `mm close-tab` has no positional form: `mm close-tab dapp` prints a usage error, so pass `--role` or `--url`.

When several tabs share a role (for example two dapp tabs, or a new tab opened by a link), `--role` may pick the wrong one. Use `--url` to choose the exact tab.

## Context

| Command                      | Description                                    |
| ---------------------------- | ---------------------------------------------- |
| `mm get-context`             | Get current context and available capabilities |
| `mm set-context <e2e\|prod>` | Switch workflow context                        |

Two contexts: `e2e` (default — local Anvil, fixtures, seeding) and `prod` (no fixtures, no local chain). Cannot switch during active session — run `mm cleanup` first.

## State & Seeding

| Command                   | Description                                                 |
| ------------------------- | ----------------------------------------------------------- |
| `mm get-state`            | Get current extension state (the only source of app state) |
| `mm run-steps <json>`     | Execute multiple tools in sequence                          |
| `mm seed-contract <type>` | Deploy a test contract                                      |
| `mm seed-contracts`       | Deploy multiple test contracts                              |
| `mm get-contract-address` | Get deployed contract address                               |
| `mm list-contracts`       | List all deployed contracts                                 |

`mm run-steps` returns `summary` (`ok`, `total`, `succeeded`, `failed`, `skipped`, `durationMs`) and exits 0 even when steps fail, so check `summary.ok`. A failed step does not stop the batch unless `"stopOnError": true`. Step args take `ref` as shorthand for `a11yRef` in every target tool (`click`, `type`, `get_text`, `hover`, `inspect`, `wait_for`, `scroll_to_element`, …) and in `within`. Step args use the tool schema, not CLI flags: `inspect` takes `"styles":["cursor"]` (an array; a string is a `VALIDATION_ERROR` step). `batchTimeoutMs` is checked between steps: the step in progress finishes with its own timeout, then the remaining steps are skipped with `MM_BATCH_TIMEOUT`; the call itself still exits 0 with partial results. The daemon log adds `failed=<n>/<total>` and the first failed step's code (see [Daemon log](#daemon-log)).

## Session Events

Browser only. Console errors and network requests of every page, the service worker, the offscreen document and snaps iframes, recorded from `mm launch` on. See [logs-and-network.md](logs-and-network.md) for the per-flow recipe and the record shapes.

| Command | Description |
|---|---|
| `mm events mark` | Current `cursor` and `summary` (`startedAt`, `captureErrors`, …) |
| `mm events clear [--kind console\|network]` | Empty the buffer; the cursor keeps counting |
| `mm logs [--cursor <n> \| --since <t>] [--limit <n>] [--grep <re>]` | Console errors and uncaught exceptions |
| `mm logs configure --levels error,warning` | Record more levels from now on |
| `mm network [--cursor <n> \| --since <t>] [--url <glob>] [--errors] [--settled]` | HTTP(S) requests: status, ms, failure, `rpcMethods` |
| `mm network configure --rpc-errors` | Also record JSON-RPC `rpcError` |

## Advanced

| Command                                           | Description                                                 |
| ------------------------------------------------- | ----------------------------------------------------------- |
| `mm mock-network add '<json-rule-or-config>'`     | Add route mocks (pages, service worker, offscreen, snaps)   |
| `mm mock-network clear`                           | Clear network mocks and recorded requests                   |
| `mm mock-network list`                            | List rules, with `contexts` and `pending`                   |
| `mm mock-network requests [--limit <n>] [--url <text>] [--bodies]` | Recorded matched and missed requests, with bodies |
| `mm cdp <method> [params-json] [--timeout <ms>] [--target page\|sw] [--fresh]` | Raw Chrome DevTools Protocol command |

### mm cdp

`--target page` (default) sends to the active page, `--target sw` to the background service worker. Each target keeps one persistent CDP session, so a domain you enable stays enabled for the next calls. `--fresh` sends the command on a one-shot session that is detached afterwards. `--target hermes` / `android-webview` are mobile only (`MM_INVALID_INPUT`, exit 2).

```bash
mm cdp Runtime.evaluate '{"expression":"location.pathname","returnByValue":true}'                # "/home.html"
mm cdp Runtime.evaluate '{"expression":"Object.keys(stateHooks)","returnByValue":true}' --target sw
mm cdp Runtime.evaluate '{"expression":"1+1","returnByValue":true}' --fresh
```

The session records events with `Network` and `Runtime` enabled on every target, so `mm cdp Network.enable` (no params) returns `{}` without sending anything, while `Network.disable` or `Network.enable` with params fails at once with `MM_CDP_BLOCKED` (exit 2): `… refused while an event subscription holds the Network domain on this target … Use --fresh to send it on a one-shot session.` `--timeout` (max 30000) bounds the CDP call: `MM_CDP_FAILED` (exit 1), `CDP call "Runtime.evaluate" timed out after 1000ms`.

`mm cdp` returns no observation by default. If the call changed page state, add `--observe full` or run `mm describe-screen`.

### Daemon log

`.mm-daemon.log` at the project root records every request with its outcome:

```text
[2026-11-13T15:25:10.579Z] [INFO] POST /tool/click 200 ok=false code=MM_TARGET_NOT_FOUND 2050ms
[2026-11-13T13:54:23.290Z] [INFO] POST /tool/scroll_to_element 200 ok=false code=MM_WAIT_TIMEOUT 2063ms
[2026-11-25T12:29:49.478Z] [INFO] POST /tool/screenshot 200 ok=false code=MM_QUEUE_TIMEOUT 30000ms
```

A failed tool call still answers HTTP 200 and puts the failure in the body, so the status code is not the outcome (only a schema failure logs `400 ok=false code=VALIDATION_ERROR`); `grep ok=false .mm-daemon.log` lists the failed calls of a run. A `run_steps` line with failed steps adds `failed=<n>/<total>` and the first failed step's code: `POST /tool/run_steps 200 ok=true failed=1/3 code=MM_WAIT_TIMEOUT …`.

For mock network details, see [mock-network.md](mock-network.md).
For console errors and the request log, see [logs-and-network.md](logs-and-network.md).
For CDP state manipulation, see [state-manipulation.md](state-manipulation.md).
