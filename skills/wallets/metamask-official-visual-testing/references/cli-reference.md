# MM CLI Command Reference

Complete command reference for the `mm` CLI. For core workflow and getting started, see the main skill.

## Contents

- [Syntax Rules](#syntax-rules)
- [Global Options](#global-options)
- [Lifecycle](#lifecycle)
- [Interaction](#interaction)
- [Navigation & Tabs](#navigation--tabs)
- [Context](#context)
- [State & Seeding](#state--seeding)
- [Advanced](#advanced)

## Syntax Rules

The CLI is strict about flag names and argument positions. Mistyped flags are silently treated as element targets, producing confusing timeout errors.

### Flag spelling is exact — lowercase, no variants

```bash
# CORRECT
mm click --testid unlock-submit
mm type --testid unlock-password "correct horse battery staple"

# WRONG — all of these silently fail with a timeout
mm click --testId unlock-submit     # capital I — treated as testId "--testId"
mm click --test-id unlock-submit    # hyphenated — treated as testId "--test-id"
mm click --TestId unlock-submit     # PascalCase — same problem
```

The only recognized interaction flags are: `--testid`, `--selector`, `--timeout`, `--within`. Anything else (including `--testId` with a capital I) is parsed as a positional argument and used as a literal testId value, producing a locator like `[data-testid="--testId"]` which always times out.

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

Observations contain `testIds` and `a11y` only, no app state. Use `mm get-state` for state.

Every tool, `launch` and `cleanup` response includes `meta.timing` (`queueMs`, `toolMs`, `observationMs`, `totalMs`).

## Lifecycle

| Command                 | Description                            |
| ----------------------- | -------------------------------------- |
| `mm launch`             | Launch MetaMask in headless Chrome     |
| `mm cleanup`            | Stop browser and services              |
| `mm cleanup --shutdown` | Stop browser, services, and the daemon |
| `mm status`             | Show current daemon and session status |

## Interaction

| Command                      | Description                                          |
| ---------------------------- | ---------------------------------------------------- |
| `mm click <ref>`             | Click element by a11y ref, testId, or selector       |
| `mm type <ref> <text>`       | Type text into element (uses `fill()`, clears first) |
| `mm get-text <ref>`          | Read text content of element                         |
| `mm describe-screen`         | Combined state + activeTab + testIds + a11y snapshot |
| `mm screenshot [--name <n>]` | Take and save a full-page screenshot                 |
| `mm wait-for <ref>`          | Wait for element to be visible                       |
| `mm wait-for-notification`   | Wait for sidepanel confirmation route, set as active |
| `mm accessibility-snapshot`  | Get trimmed a11y tree with refs                      |
| `mm list-testids`            | List visible `data-testid` attributes                |
| `mm clipboard <action>`      | Read from or write to browser clipboard              |

All interaction commands accept `--timeout <ms>` (default 15000). This is a **single deadline budget** covering visibility wait + action combined — not a per-phase timeout.

### Element and viewport screenshots

`mm screenshot` accepts only `--name` and always captures the full page. Other flags such as `--testid` or `--selector` are ignored without an error. To capture one element or only the viewport, use a `run-steps` screenshot step:

```bash
# One element (CSS selector; quote attribute values)
mm run-steps '{"steps":[{"tool":"screenshot","args":{"name":"side-nav","selector":"[data-testid=\"side-nav\"]"}}],"observe":"none"}'

# Viewport only
mm run-steps '{"steps":[{"tool":"screenshot","args":{"name":"viewport","fullPage":false}}],"observe":"none"}'
```

The result has the file `path`, `width` and `height`. A selector that matches nothing waits until the request times out (about 30 s), so check that the element exists first.

### Several matches

When a selector or testId matches more than one element, the click fails with a strict mode violation. Scope it with `--within` (an a11yRef, `testid:<id>` or `selector:<css>`). For example, with a modal open over the page, `button[aria-label='Close']` can match two buttons:

```bash
mm click --selector "button[aria-label='Close']" --within "selector:[role=dialog]"
```

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
| `mm switch-to-tab <role>` / `--role <role>`  | Switch active page to a different tab by role |
| `mm switch-to-tab --url <url>`               | Switch to the tab with this URL               |
| `mm close-tab --role <role>` / `--url <url>` | Close a tab                                   |

Tab roles: `extension`, `notification`, `dapp`, `other`.

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

## Advanced

| Command                                           | Description                                                 |
| ------------------------------------------------- | ----------------------------------------------------------- |
| `mm mock-network add '<json-rule-or-config>'`     | Add Playwright route mocks during active session            |
| `mm mock-network clear`                           | Clear network mocks and recorded requests                   |
| `mm mock-network list`                            | List active network mock rules                              |
| `mm mock-network requests [--limit <n>]`          | Show recorded matched and missed mocked-origin requests     |
| `mm cdp <method> [params-json] [--timeout <ms>]`  | Send raw Chrome DevTools Protocol command against active page|

`mm cdp` returns no observation by default. If the call changed page state, add `--observe full` or run `mm describe-screen`.

For mock network details, see [mock-network.md](mock-network.md).
For CDP state manipulation, see [state-manipulation.md](state-manipulation.md).
