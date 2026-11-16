---
repo: metamask-extension
parent: visual-testing
metadata:
  location: test/e2e/playwright/llm-workflow/
  type: browser-testing
---

# MetaMask Visual Testing — Extension

## When to Use

- Visually validate MetaMask UI changes in a real browser
- Capture screenshots as evidence
- Verify onboarding, unlock, transaction, swap, or dapp-confirmation flows
- Debug unexpected UI state in the extension or sidepanel
- Inject test data into features that read from in-memory streams or data channels (not Redux) when fixtures and WebSocket mocks can't reach the data source

For architecture details, see `test/e2e/playwright/llm-workflow/README.md`.

## Gotchas

- `a11yRef`s (`e1`, `e2`, ...) are **ephemeral**. Always take refs from the latest response (`mm describe-screen` or the `observations` of your last action).
- A browser ref is tied to its DOM node: a live value in its name (a price such as `$2.42`, `3.92%` or `00:59`) does not break it. It fails at once with `MM_TARGET_NOT_FOUND` when the element was removed or re-mounted, or when a short name now says something else (a "Next" button became "Confirm"; plain integers such as `Account 1` count). Take a new `mm describe-screen` when that happens.
- After a call with `--observe none`, refs are **not** refreshed. Target by `--testid`, or run `mm describe-screen` before you use refs again. A browser ref that fell back to `role=`/`text=` (an element that could not be stamped) or that points to an icon button can click a different element; a ref whose element is gone fails with `MM_TARGET_NOT_FOUND`.
- Each ref resolves to exactly one element. A strict mode violation can only come from a fallback `role=`/`text=` ref or an explicit `--selector`/`--testid`; target the element by `--testid` or `--selector`, and scope it with `--within` when it matches several elements (for example two stacked modals with a Close button).
- Output is one line of JSON when stdout is not a terminal. Parse it as JSON. Add `--pretty` (or set `MM_PRETTY=1`) only when a human reads the output.
- A failed command prints **one JSON line on stdout** (`{"ok":false,"error":{"code","message","hint"?,"retryable"}}`) and exits non-zero. Branch on `error.code` or the exit code; success has no `ok` field. `mm stop` prints plain text, and `mm launch` warns about an unknown flag on stderr and ignores it (see [Output and Errors](references/cli-reference.md#output-and-errors)).
- Observations carry no app state. Use `mm get-state` for the account, network or balance. On `home.html#settings` (the route `mm navigate-settings` opens) it returns `isUnlocked: false` and `currentScreen: "unknown"`; use the URL and testIds from `mm describe-screen` there. Settings sub-pages such as `#/settings/about-us` report correctly.
- Do **not** sleep. A browser observation after a mutating or batch call has `animationsSettled`; when it is `false`, or you wait for data that loads, `mm wait-for` the element you expect (`mm wait-for --selector "text=Copied"`).
- A click, type or request timeout says "state unknown" and has `retryable: false`. The action can have happened: run `mm describe-screen` before you retry.
- `mm type` uses Playwright `fill()` and **clears the field first**. On the browser it fails at once with `MM_ELEMENT_NOT_EDITABLE` on a read-only or disabled field.
- After confirm or reject in the side panel, the page does **not** close. It stays open and navigates back to the home route.
- Headless, `mm wait-for-notification` waits for a confirmation route in `sidepanel.html`; headed, it waits for a `notification.html` popup. See [Confirmation pages](#confirmation-pages).
- `mm run-steps` expects a JSON **object** with a `steps` key, not a bare array.
- You cannot switch context during an active session. Run `mm cleanup` first, or use `mm launch --context ...`.
- The default password for built-in fixtures is `correct horse battery staple`.
- Network mocks are session-scoped. In the e2e fixture Basic functionality is off, and the home screen made no request to the MetaMask API origins, so a mock there can get no request at all. Check with `mm mock-network requests` before you rely on a mock; see [Mock Network](references/mock-network.md).
- An element below the fold is not a scroll problem for a click: Playwright's `click` already scrolls its target into view. To bring an element into view for a screenshot, use `mm scroll-to-element --testid <id>`; do not scroll with `mm cdp` scripts.
- In the e2e fixture, the Activity tab opens "Basic functionality is off" with no bottom navigation, so `mm click --testid bottom-nav-home` fails after 2 s with `MM_TARGET_NOT_FOUND`. Use `mm navigate-home` instead.
- Right after `mm reload` the observation can be empty. Run `mm wait-for` or `mm describe-screen` before you act on it.

## Prerequisites

**CLI invocation** — `mm` is a project-local dependency:

```bash
yarn mm <command>        # or: npx mm <command>
```

**Build validation** before `mm launch`:

- Build output is in `dist/chrome/`. If missing, build first.
- If a build exists and the user explicitly asked to rebuild, rebuild it.
- If a build exists and the user explicitly asked not to rebuild, reuse it.
- `mm launch` validates the build and returns an actionable error if missing.

```bash
yarn install && yarn build:test        # fresh worktree: run `yarn webpack:tsc` first
```

**Port conflicts** — if ports are stuck from a previous run, check `.mm-server` for active ports:

```bash
cat .mm-server   # look under subPorts for anvil and fixture ports
```

## Core Workflow

### 1. Launch

```bash
mm launch                                    # pre-onboarded wallet, 25 ETH on local Anvil
mm launch --state onboarding                 # fresh wallet
mm launch --context prod --state onboarding  # production-like mode
MM_HEADLESS=true mm launch                   # headless Chrome
```

Chrome is headed by default. `MM_HEADLESS=true` makes it headless; without `MM_HEADLESS`, `PLAYWRIGHT_HEADLESS`, `HEADLESS` or `CI` also do. The daemon reads it when it starts, so pass it on the `mm launch` that starts the daemon.

`mm launch` has no flag for a fixture preset: `--state custom` fails with `MM_LAUNCH_FAILED` (`stateMode 'custom' requires either 'fixturePreset' or 'fixture'`). Start from the default wallet and change state with [State Manipulation](references/state-manipulation.md).

Two contexts: **e2e** (default — local Anvil, fixtures, seeding) and **prod** (no fixtures, no local chain). Use `mm get-context` / `mm set-context` to switch. Cannot switch during active session.

Screenshots and session metadata default to `<repo>/test-artifacts/`. `MM_ARTIFACTS_DIR=/tmp/mm-artifacts mm launch` writes them to `/tmp/mm-artifacts/screenshots/` and `/tmp/mm-artifacts/<sessionId>/session.json`. Pass it on the `mm launch` that starts the daemon; `mm stop` a running daemon first.

### 2. Describe Screen

```bash
mm describe-screen
```

Returns current screen, active tab, visible testIds, and accessibility tree with refs.

**Observation efficiency:** Mutating actions (`click`, `type`, `navigate`) and `mm run-steps` return compact diff-based observations after the first observation. Use these for quick next-step targeting. Reads, discovery commands and `mm cdp` return no observation. Call `mm describe-screen` when you need the full a11y tree or to reset the baseline. It returns `screenshot: null`; use `mm screenshot` for an image.

Use the global `--observe <none|diff|full>` flag to change the observation of one call:

```bash
mm click --testid unlock-submit --observe none   # chain known actions: skip the observation
mm navigate-home --observe full                  # after navigation: get the whole screen
```

Only mutating and batch calls wait for animations before they observe. To get a settled screen after an action, let the action observe (`--observe full`) instead of running a read afterwards.

The observation then has `animationsSettled`: `true` when the page loaded and its finite animations ended within the 1 s wait, `false` when some were still running. It does not cover infinite spinners or data loaded from the network. When it is `false`, or you wait for data, `mm wait-for` the element you expect instead of sleeping:

```bash
mm wait-for --testid activity-list
mm wait-for --selector "text=Copied"
```

### 3. Interact

Use exactly **one targeting method** per call. Priority: `testId` (stable) > `a11yRef` (discovery) > `selector` (fallback).

```bash
# By testId — preferred for known flows and batching
mm click --testid unlock-submit
mm type --testid unlock-password "correct horse battery staple"
mm wait-for --testid account-menu-icon --timeout 10000
mm get-text --testid balance-display

# By a11yRef — from describe-screen, during discovery
mm click e5
mm type e2 "correct horse battery staple"

# By CSS selector — fallback when testIds or a11y refs are unavailable
mm click --selector "text=Rename"
mm click --selector "role=button[name='Submit']"
```

**Scoped targeting** with `--within` when duplicate names or testIds exist:

```bash
mm click --testid end-accessory --within "testid:account-list-item/0"
mm click e3 --within "testid:dialog-container"
mm click --selector ".popover-menu-item" --within "selector:.account-list-item:first-child"
```

`--within` accepts an a11yRef, `testid:<id>`, or `selector:<css>`.

**List views (account list, token list, network list):** These screens contain many elements with identical names and testIds. The a11y tree will show dozens of entries like `"Open multichain account address menu"` with no distinguishing context. You must scope with `--within` to target the correct item:

```bash
# Target the 3-dot menu on the first account in the account list
mm click --testid account-list-item-menu-button --within "testid:account-list-item/0"

# Target an element inside a specific dialog or popover
mm click --selector "text=Rename" --within "testid:popover-content"
```

If `--within` isn't working or you can't identify the right parent testId, use a CSS selector with `:nth-child()` or other structural selectors as a fallback.

#### Inspect, hover and viewport

Check styling and disabled states with values instead of by eye:

```bash
mm inspect --testid eth-overview-swap                 # disabled, attributes, styles
mm inspect --testid eth-overview-send --styles color,opacity,cursor,display
```

`mm inspect` returns `attributes`, `disabled`, `readOnly`, `styles` (default `color`, `background-color`, `opacity`, `cursor`) and `effectiveOpacity`. A faded, disabled Swap button reads `"disabled": true`, `"effectiveOpacity": 0.5`, `"cursor": "not-allowed"`. Compare two elements with the same `--styles`; do not compare one against unrelated text.

For hover-only UI and layout widths:

```bash
mm hover --testid account-menu-icon
mm screenshot --name account-menu-hovered
mm unhover
mm set-viewport 400 600
mm screenshot --name narrow
mm reset-viewport
```

To bring a row further down a list into view for a screenshot, use `mm scroll-to-element --testid <id>`. A click already scrolls its target, so you do not need it before `mm click`.

#### Timeouts

All interaction commands accept `--timeout <ms>` (default 15000). This is a **single deadline budget** covering visibility wait + action combined.

Phase-specific error codes on timeout:
- `MM_WAIT_TIMEOUT` — element never became visible. `retryable: true`.
- `MM_TARGET_NOT_FOUND` — `mm click` without `--timeout`: nothing matched after 2 s (a wrong testId shows up here, for example `eth-overview-receive`; Receive is `eth-overview-default`). Pass `--timeout` to wait for a target that appears late.
- `MM_CLICK_TIMEOUT` — click hung; state unknown. The message ends with Playwright's last step, for example `element is not enabled` (disabled Swap in the fixture) or `… intercepts pointer events` (a modal covers the target). Run `mm describe-screen` before retrying.
- `MM_TYPE_TIMEOUT` — the field did not appear or `fill()` hung; state unknown.
- `MM_GETTEXT_TIMEOUT` — the element did not appear or `textContent()` hung. `retryable: true`.
- `MM_PAGE_CLOSED` — page closed during action (expected for some confirmation flows); exits 3.

For the full error code and exit code tables, see [references/error-recovery.md](references/error-recovery.md).

### 4. Verify-Fix Loop

After any interaction sequence:

1. `mm describe-screen` to verify expected state
2. If wrong: `mm screenshot --name "debug-<action>"`, then retry
3. Continue only when expected state is confirmed

### 4b. Edge Case: Component Not Responding to State Changes

If you change Redux state via CDP but the target component doesn't update:

1. **The component reads from a different data source** — an in-memory stream, data channel, or React context that is NOT backed by Redux.
2. Read the component's source to identify the hook it uses (`useSelector` = Redux; anything else = likely in-memory).
3. Use the [React Fiber Data Injection](references/state-manipulation.md#5-inject-into-in-memory-data-sources-react-fiber-walk) pattern from the State Manipulation reference.
4. Disconnect the live data feed first (prevents overwrite), then push your test data.
5. Re-verify with `mm describe-screen`.

### 5. Confirmations (Dapp Flows)

```bash
mm navigate https://test-dapp.io     # navigate to dapp
mm click e1                           # trigger dapp action
mm wait-for-notification              # wait for the confirmation page
mm describe-screen                    # see the confirmation
mm click e2                           # confirm or reject
mm describe-screen                    # verify return to home
mm switch-to-tab dapp                 # back to dapp
```

Tab roles: `extension`, `notification`, `dapp`, `other`. To close a tab, pass `--role` or `--url` (`mm close-tab --role dapp`); `mm close-tab dapp` is a usage error. When several tabs share a role, use `--url`.

### 6. Navigate

```bash
mm navigate-home
mm navigate-settings
mm navigate https://test-dapp.io
mm reload     # reload the page, keep the route
```

`mm navigate-home` and `mm navigate-settings` load the page again (`home.html`, `home.html#settings`), which drops state injected with `mm cdp`. `mm reload` also loads the page again but keeps the current route.

### 7. Screenshots

```bash
mm screenshot --name "after-unlock"
```

Capture before and after meaningful state changes for visual validation evidence.

`mm screenshot` accepts only `--name` and captures the full page. For one element or the viewport, use a `run-steps` screenshot step with `selector` or `"fullPage": false`. See [Element and viewport screenshots](references/cli-reference.md#element-and-viewport-screenshots).

### 8. Cleanup (Always Required)

```bash
mm cleanup                 # stop browser and services
mm cleanup --shutdown      # also stop the daemon
mm stop                    # stop the daemon only (plain-text output)
```

## Confirmation pages

The session drives `home.html`, the full-page UI. Wallet-initiated confirmations (Send) render there, at `#/confirm-transaction/…`.

For dapp confirmations, `mm wait-for-notification` finds the confirmation page and makes it the active page:
- Headless: `sidepanel.html` (tab role `notification`), once its URL hash is a confirmation route
- Headed: the `notification.html` popup
- After confirm/reject, the side panel stays open and navigates back to home; use `mm describe-screen` to verify
- Confirmation routes: `/connect`, `/confirm-transaction`, `/confirmation`, `/confirm-import-token`, `/confirm-add-suggested-token`, `/confirm-add-suggested-nft`

### Send recipe (e2e fixture)

After `mm launch` and unlock (see [Batching](#batching-with-mm-run-steps)):

```bash
mm click --testid eth-overview-send
mm click --testid token-asset-0x539-ETH       # "All networks" lists several ETH rows; 0x539 is the local chain
mm type --testid recipient-address-input 0x2f318C334780961FB129D2a6c30D0763d9a5C970
mm type --testid send-amount-input 0.01
mm click --testid send-continue-button
mm wait-for --testid confirm-footer-button    # the review page shows skeletons first
mm click --testid confirm-footer-cancel-button   # or confirm-footer-button to send
```

The review page shows `confirm-send-amount` and `recipient-address`.

## Batching with mm run-steps

Use for known, deterministic sequences. Use individual commands for discovery or when intermediate state changes the next action.

```bash
mm run-steps '{"steps":[
  {"tool":"type","args":{"testId":"unlock-password","text":"correct horse battery staple"}},
  {"tool":"click","args":{"testId":"unlock-submit"}},
  {"tool":"wait_for","args":{"testId":"account-menu-icon","timeoutMs":10000}}
]}'
```

Details:
- Prefer `testId`, `a11yRef`, or `selector` in args (not `ref`)
- Use `within` in args to scope targeting within a parent element
- Add `batchTimeoutMs` (1000–30000 ms) for an overall deadline. The whole call stops after 30 s, so use a lower value (for example 20000) to get partial results, and split longer flows into several batches
- Add a top-level `observe` (`none` / `diff` / `full`, default `diff`) to set the observation collected after the batch. `includeObservations` was removed; check `summary.ok` to react to failures
- A failed step does not stop the batch: later steps still run. Add `"stopOnError": true` to stop at the first failed step
- Tool aliases like `navigate_home` and `navigate-home` are supported

Pattern: discover with `mm describe-screen` → batch known steps with `mm run-steps` → re-verify with `mm describe-screen`.

## Default Credentials

| Property | Value                          |
| -------- | ------------------------------ |
| Password | `correct horse battery staple` |
| Chain ID | `1337`                         |
| Balance  | 25 ETH                         |

## Capabilities

- **Anvil**: Local blockchain on port 8545
- **Fixture Server**: Wallet state management
- **Contract Seeding**: Deploy test contracts with `mm seed-contract`

## Reference Guides

Load these on demand — not required for standard visual testing:

- **[CLI Command Reference](references/cli-reference.md)** — full command tables for all `mm` commands
- **[State Manipulation](references/state-manipulation.md)** — read/write Redux and persisted state via CDP when fixtures don't cover your scenario
- **[Mock Network](references/mock-network.md)** — stub network requests for deterministic API responses
- **[Error Recovery](references/error-recovery.md)** — error codes, common failures, and troubleshooting
