# MM CLI Command Reference for Mobile (iOS)

Command reference for the prod-only MetaMask Mobile consumer. The generic core CLI exposes commands for multiple consumers; availability here is determined by the iOS platform driver and mobile session manager.

## Contents

- [Syntax Rules](#syntax-rules)
- [Lifecycle](#lifecycle)
- [Destructive Launch Flags](#destructive-launch-flags)
- [Installed State](#installed-state)
- [Interaction](#interaction)
- [Discovery](#discovery)
- [Knowledge Store](#knowledge-store)
- [Batching](#batching)
- [Hermes CDP](#hermes-cdp)
- [Simulator Selection](#simulator-selection)
- [Not Available on Mobile](#not-available-on-mobile)

## Syntax Rules

Flag names and argument positions are exact. Mistyped interaction flags may be parsed as literal targets and eventually time out.

### Use exact lowercase interaction flags

```bash
# Correct
yarn mm click --testid unlock-submit
yarn mm type --testid unlock-password "<wallet password>"

# Incorrect
yarn mm click --testId unlock-submit
yarn mm click --test-id unlock-submit
```

The shared CLI parses `--testid`, `--selector`, `--timeout`, and `--within`, but the iOS driver only supports `--testid` (and positional a11y refs). `--selector` and `--within` are accepted by the parser and then **rejected at runtime by the mobile driver** — see [Targeting on iOS](#targeting-on-ios).

### Accessibility references are positional

```bash
# Correct
yarn mm click e5
yarn mm type e2 "text"

# Incorrect: there is no --ref flag
yarn mm click --ref e5
```

Use exactly one targeting method per command: a positional accessibility reference or `--testid`.

| Goal | Correct syntax |
| --- | --- |
| Click by test ID | `yarn mm click --testid X` |
| Click by accessibility reference | `yarn mm click e5` |
| Type by test ID | `yarn mm type --testid X "text"` |
| Type by accessibility reference | `yarn mm type e2 "text"` |

### Targeting on iOS

- **Supported:** `--testid <id>` and positional a11y refs (`e1`, `e2`, ...).
- **Not supported:** `--selector <css>` throws `CSS selectors are not supported on mobile`. `--within <scope>` throws `Scoped element search (within) is not supported on mobile`. The parser accepts both flags, but the iOS driver rejects them at runtime.
- **Matching is fuzzy and case-insensitive.** idb matches accessibility label/identifier by substring, so `--testid Confirm` can match `Confirm Transaction`. Use exact, unique test IDs to disambiguate; there is no `--within` scoping fallback on mobile.
- **`--testid` is lowercase.** `--testId` is not recognized as a flag and its value is treated as a positional target.

## Lifecycle

| Command | Description |
| --- | --- |
| `yarn mm launch [options]` | Start the daemon and launch an iOS session using the installed app state |
| `yarn mm cleanup` | Close the app and clear the active session |
| `yarn mm cleanup --shutdown` | Clean up the session and stop the daemon |
| `yarn mm status` | Show daemon and session status |
| `yarn mm stop [--force]` | Stop the daemon; `--force` also clears stale daemon state |
| `yarn mm serve [--background]` | Start the daemon without launching a session |

### Supported launch flags

The locally installed core CLI parser exposes these launch flags that are meaningful for this consumer:

| Flag | Description |
| --- | --- |
| `--platform ios` | Explicitly select the iOS platform (plain launch is preferred, as the mobile consumer automatically handles it) |
| `--device-id <UDID>` | Select an iOS Simulator by UDID |
| `--app-bundle <path>` | Install a specific `.app` bundle before launching (for example `ios/build/MetaMask.app`). Required before any destructive flag |
| `--metro-port <port>` | Attach to a running Metro bundler on the given port. Equivalent to `MM_METRO_PORT`; the flag wins when both are set |
| `--goal <text>` | Record the session goal in knowledge metadata |
| `--flow-tags <tags>` | Record comma-separated flow tags |
| `--force` | Replace an existing active session |

Launch timeout is 120 seconds. The project CLI does not build MetaMask. Install the intended app on the simulator before launching, or pass `--app-bundle <path>` to install a specific build.

The destructive flags `--reinstall`, `--reset-app-data`, and `--allow-fox-code-mismatch` are also parsed but guarded — see [Destructive Launch Flags](#destructive-launch-flags). For command-line Metro attachment, use `--metro-port <port>` or the `MM_METRO_PORT` environment variable as documented below.

## Destructive Launch Flags

These flags replace the installed app and destroy the wallet state it holds, so this prod-only consumer guards them. Do not use them on a wallet you need to preserve.

| Flag | Description |
| --- | --- |
| `--reinstall` | Uninstall and reinstall the app before launching. Rejected unless `--app-bundle` is also supplied |
| `--reset-app-data` | Clear the app container/wallet state before launching. Rejected unless `--app-bundle` is also supplied |
| `--allow-fox-code-mismatch` | Bypass the app-identity guard so a bundle with a different `fox_code` can be installed. May make existing wallet/keychain data unreadable |

Guardrails enforced at launch:

- `--reinstall` and `--reset-app-data` are rejected unless `--app-bundle` is also supplied, because the installed app is otherwise the only copy and would be destroyed by the uninstall step. The rejection surfaces as `MM_INVALID_CONFIG`.
- Installing a bundle whose `fox_code` differs from the installed app is rejected (`MM_INVALID_CONFIG`) unless `--reinstall` or `--allow-fox-code-mismatch` is passed.
- A warning is printed to stderr whenever a destructive flag is honored.

```bash
# Replace the installed app with a local build, discarding wallet state
yarn mm launch --app-bundle ios/build/MetaMask.app --reinstall
```

## Installed State

`yarn mm launch` opens the MetaMask app already installed on the selected simulator and preserves its current wallet state. The workflow does not guarantee:

- an onboarding or unlocked screen
- a password
- a particular account, network, token, or balance

Always run `yarn mm describe-screen` and inspect the current app before interacting. Obtain credentials from the user or approved environment rather than assuming them.

The generic core package may display environment-selection and test-state commands because it supports other consumers. This mobile consumer always reports prod, cannot switch environments, and does not provide local test-state capabilities. Do not use those generic commands in a mobile visual-testing flow.

## Interaction

| Command | Description |
| --- | --- |
| `yarn mm click <ref>` | Click by accessibility reference or test ID |
| `yarn mm type <ref> <text>` | Clear and type into an editable element |
| `yarn mm get-text <ref>` | Read an element's text |
| `yarn mm wait-for <ref>` | Wait for an element to become visible |

All interaction commands accept on iOS:

- `--timeout <ms>`: one deadline for visibility and action
- `--testid <id>`: target by test ID

`--selector` and `--within` are parsed but rejected by the iOS driver (see [Targeting on iOS](#targeting-on-ios)). To disambiguate duplicate targets, use a unique test ID or the exact element's fresh a11y ref — there is no scoped-search fallback on mobile.

## Discovery

| Command | Description |
| --- | --- |
| `yarn mm describe-screen` | Return app state, visible test IDs, accessibility tree, and prior knowledge |
| `yarn mm screenshot [--name <name>]` | Capture the current simulator screen |
| `yarn mm accessibility-snapshot` | Return a trimmed accessibility tree (the shared `--root <selector>` flag is ignored on iOS; the full tree is always returned) |
| `yarn mm list-testids [--limit <n>]` | List visible test IDs |
| `yarn mm get-state` | Return the current app-state snapshot |
| `yarn mm get-context` | Report the static prod environment and available mobile capabilities |

Mutating tools return observations with fresh references. Later actions may return compact differences from the prior observation. Use `describe-screen` whenever a complete tree or refreshed baseline is needed.

## Knowledge Store

| Command | Description |
| --- | --- |
| `yarn mm knowledge-search <query>` | Search recorded steps |
| `yarn mm knowledge-last` | Return recent steps from the current session |
| `yarn mm knowledge-sessions` | List recorded sessions and metadata |
| `yarn mm knowledge-summarize [--session <id>]` | Generate a session recipe |

## Batching

### `yarn mm run-steps '<json>'`

The argument must be a JSON object containing a `steps` array:

```bash
yarn mm run-steps '{"steps":[
  {"tool":"click","args":{"a11yRef":"e3"}},
  {"tool":"wait_for","args":{"testId":"home-screen","timeoutMs":10000}}
]}'
```

| Parameter | Description |
| --- | --- |
| `steps` | Required array of `{tool, args}` objects |
| `stopOnError` | Stop after the first failure; defaults to `false` (remaining steps still run). Set `true` to abort on the first error |
| `includeObservations` | `'all'`, `'none'`, or `'failures'` |
| `batchTimeoutMs` | Overall deadline; remaining steps are skipped after expiry |

Each step is independently checked for mobile platform support. Do not put browser-only commands in a mobile batch.

## Hermes CDP

### `yarn mm cdp <method> [params-json] [flags]`

On mobile, `cdp` connects to the Hermes runtime through Metro's inspector proxy. It does not expose browser DOM, Page, or Network domains.

```bash
yarn mm cdp Runtime.evaluate '{"expression":"JSON.stringify(globalThis.__DEV__)"}'
yarn mm cdp Runtime.evaluate '{"expression":"1+1"}' --timeout 60000
```

| Flag | Description |
| --- | --- |
| `--timeout <ms>` | Per-command timeout |
| `--metro-port <port>` | Override the Metro inspector port for this command |
| `--app-id <id>` | Require a matching app identity for target selection |

### `yarn mm hermes-targets [flags]`

Read-only, mobile-only. Lists and diagnoses the debuggable React Native Hermes targets Metro exposes, reporting which target would be chosen or why selection is ambiguous. Use it to confirm Metro is running, the app is registered, and to discover the real app identity.

| Flag | Description |
| --- | --- |
| `--all` | List every discovered target instead of only the selected one |
| `--metro-port <port>` | Override the Metro inspector port |
| `--app-id <id>` | Require a matching app identity for target selection |

The driver verifies app identity and device pinning before executing commands.

Start Metro attachment before runtime inspection, using either the `--metro-port` flag or the `MM_METRO_PORT` environment variable (the flag wins when both are set):

```bash
yarn watch:clean
yarn mm launch --metro-port 8081

# Equivalent, still supported
MM_METRO_PORT=8081 yarn mm launch
```

On Node 20, add `NODE_OPTIONS="--experimental-websocket"` when launching. Run `yarn mm describe-screen` after runtime mutation to resynchronize observations.

## Simulator Selection

```bash
xcrun simctl list devices
xcrun simctl boot <UDID>
yarn mm launch --device-id <UDID>
```

Prefer one booted simulator and one Metro process per worktree, especially during Hermes inspection.

## Not Available on Mobile

The core CLI is shared across consumers, so its help lists commands that this prod-only mobile consumer does not support. Two groups are unavailable here: browser-only commands, and e2e-context commands (fixtures, seeding, environment switching). Do not use any of these in a mobile visual-testing flow.

### Browser-only

| Command | Mobile behavior or alternative |
| --- | --- |
| `yarn mm navigate <url>` | Browser-only; navigate through visible UI elements |
| `yarn mm navigate-home` | Not implemented; click the Wallet tab in the UI |
| `yarn mm navigate-settings` | Not implemented; click the Settings tab in the UI |
| `yarn mm switch-to-tab` | Browser tabs do not exist in the mobile session |
| `yarn mm close-tab` | Browser tabs do not exist in the mobile session |
| `yarn mm wait-for-notification` | Browser notification-page command |
| `yarn mm clipboard` | Browser command in the current CLI surface |
| `yarn mm mock-network` | Browser-only network interception |
| `yarn mm build` | No mobile build capability; build and install separately |

### E2E-context only (not applicable to prod-only mobile)

This consumer always reports the static `prod` environment and provides no local test infrastructure, so these commands are meaningless here even though the shared CLI still lists them.

| Command | Mobile behavior or alternative |
| --- | --- |
| `yarn mm set-context` | Environment switching is unavailable; the mobile consumer is always `prod` |
| `yarn mm get-state` | E2E fixture/state snapshot; use `yarn mm describe-screen` for live UI state |
| `yarn mm seed-contract` | Contract seeding needs the e2e chain, which this consumer does not run |
| `yarn mm seed-contracts` | Contract seeding needs the e2e chain, which this consumer does not run |
| `yarn mm get-contract-address` | Depends on seeded e2e contracts that do not exist here |
| `yarn mm list-contracts` | Depends on seeded e2e contracts that do not exist here |

`yarn mm get-context` is available and always reports the static `prod` environment plus the mobile capabilities on offer.

`yarn mm cdp` and `yarn mm hermes-targets` are available for Metro-attached mobile development sessions.
