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

- `a11yRef`s (`e1`, `e2`, ...) are **ephemeral**. After `mm describe-screen`, `mm accessibility-snapshot`, or major navigation, re-describe before reusing refs.
- `mm type` uses Playwright `fill()` and **clears the field first**.
- After confirm or reject in sidepanel mode, the page does **not** close. It stays open and navigates back to the home route.
- `mm wait-for-notification` waits for the sidepanel confirmation route, not a legacy popup window.
- `mm run-steps` expects a JSON **object** with a `steps` key, not a bare array.
- You cannot switch context during an active session. Run `mm cleanup` first, or use `mm launch --context ...`.
- The default password for built-in fixtures is `correct horse battery staple`.
- Network mocks are session-scoped. Add rules after `mm launch` and before the triggering UI action; `mm cleanup` removes them.
- `mm mock-network` **cannot** intercept requests during extension startup before the session is fully active.
- There is **no `mm scroll` command**. If an element is below the viewport and `mm click` times out, scroll it into view via CDP before retrying:
  ```bash
  mm cdp Runtime.evaluate '{"expression":"document.querySelector(\"[data-testid=import-token-button]\").scrollIntoView({block:\"center\"})"}'
  mm click --testid import-token-button
  ```

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
yarn install && yarn build:test:webpack
```

**Port conflicts** — if ports are stuck from a previous run, check `.mm-server` for active ports:

```bash
cat .mm-server   # look under subPorts for anvil and fixture ports
```

## Core Workflow

### 1. Launch

```bash
mm launch                                          # pre-onboarded wallet, 25 ETH on local Anvil
mm launch --state onboarding                       # fresh wallet
mm launch --state custom --preset withERC20Tokens  # custom fixture
mm launch --context prod --state onboarding        # production-like mode
```

Available presets: `withMultipleAccounts`, `withERC20Tokens`, `withConnectedDapp`, `withPopularNetworks`, `withMainnet`, `withNFTs`, `withFiatDisabled`, `withHSTToken`.

Two contexts: **e2e** (default — local Anvil, fixtures, seeding) and **prod** (no fixtures, no local chain). Use `mm get-context` / `mm set-context` to switch. Cannot switch during active session.

### 2. Reuse Knowledge (Mandatory)

```bash
mm knowledge-search "<flow name>"
mm knowledge-sessions
```

Reuse discovered sequences when they exist. If none exist, proceed with discovery and let this session record the new steps.

### 3. Describe Screen

```bash
mm describe-screen
```

Returns current screen, active tab, visible testIds, and accessibility tree with refs.

**Observation efficiency:** Mutating actions (`click`, `type`, `navigate`) return compact diff-based observations after the first mutation. Use these for quick next-step targeting. Call `mm describe-screen` when you need the full a11y tree, screenshots, or to reset the baseline.

### 4. Interact

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

#### Timeouts

All interaction commands accept `--timeout <ms>` (default 15000). This is a **single deadline budget** covering visibility wait + action combined.

Phase-specific error codes on timeout:
- `MM_WAIT_TIMEOUT` — element never became visible.
- `MM_CLICK_TIMEOUT` — element found, click hung. May have completed; run `mm describe-screen`.
- `MM_TYPE_TIMEOUT` — element found, `fill()` hung.
- `MM_GETTEXT_TIMEOUT` — element found, `textContent()` hung.
- `MM_PAGE_CLOSED` — page closed during action (expected for some confirmation flows).

For the full error code table, see [references/error-recovery.md](references/error-recovery.md).

### 5. Verify-Fix Loop

After any interaction sequence:

1. `mm describe-screen` to verify expected state
2. If wrong: `mm screenshot --name "debug-<action>"`, check `mm knowledge-search "<flow>"`, retry
3. Continue only when expected state is confirmed

### 5b. Edge Case: Component Not Responding to State Changes

If you change Redux state via CDP but the target component doesn't update:

1. **The component reads from a different data source** — an in-memory stream, data channel, or React context that is NOT backed by Redux.
2. Read the component's source to identify the hook it uses (`useSelector` = Redux; anything else = likely in-memory).
3. Use the [React Fiber Data Injection](references/state-manipulation.md#5-inject-into-in-memory-data-sources-react-fiber-walk) pattern from the State Manipulation reference.
4. Disconnect the live data feed first (prevents overwrite), then push your test data.
5. Re-verify with `mm describe-screen`.

### 6. Confirmations (Dapp Flows)

```bash
mm navigate https://test-dapp.io     # navigate to dapp
mm click e1                           # trigger dapp action
mm wait-for-notification              # wait for sidepanel confirmation
mm describe-screen                    # see the confirmation
mm click e2                           # confirm or reject
mm describe-screen                    # verify return to home
mm switch-to-tab dapp                 # back to dapp
```

Tab roles: `extension`, `notification`, `dapp`, `other`.

### 7. Navigate

```bash
mm navigate-home
mm navigate-settings
mm navigate https://test-dapp.io
```

### 8. Screenshots

```bash
mm screenshot --name "after-unlock"
```

Capture before and after meaningful state changes for visual validation evidence.

### 9. Cleanup (Always Required)

```bash
mm cleanup                 # stop browser and services
mm cleanup --shutdown      # also stop the daemon
```

## Sidepanel Mode

The extension runs in sidepanel mode by default (`sidepanel.html`).

Key behavior:
- After confirm/reject, the sidepanel stays open and navigates back to home
- `mm wait-for-notification` waits for a confirmation route in the URL hash
- After a confirmation action, use `mm describe-screen` to verify the return to home state
- Confirmation routes: `/connect`, `/confirm-transaction`, `/confirmation`, `/confirm-import-token`, `/confirm-add-suggested-token`, `/confirm-add-suggested-nft`

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
- Add `batchTimeoutMs` for overall timeout
- Tool aliases like `navigate_home` and `navigate-home` are supported

Pattern: discover with `mm describe-screen` → reuse from `mm knowledge-search` → batch with `mm run-steps` → re-verify with `mm describe-screen`.

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
