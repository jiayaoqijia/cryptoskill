# MM CLI Command Reference for Mobile (iOS)

Command reference for the prod-only MetaMask Mobile consumer. The generic core CLI exposes commands for multiple consumers; availability here is determined by the iOS platform driver and mobile session manager.

## Contents

- [Syntax Rules](#syntax-rules)
- [Global Options](#global-options)
- [Lifecycle](#lifecycle)
- [Destructive Launch Flags](#destructive-launch-flags)
- [Installed State](#installed-state)
- [Interaction](#interaction)
- [Discovery](#discovery)
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

## Global Options

These flags work with every command and can appear anywhere in the command line.

| Flag | Description |
| --- | --- |
| `--project <path>` | Target a specific project directory. Overrides `MM_PROJECT` and git-based discovery |
| `--observe <none\|diff\|full>` | Observation returned after the call. Default: `diff` for mutating commands and `run-steps`, `none` for reads, discovery and `cdp` |
| `--pretty` | Indent JSON output. Default: one line per result when stdout is not a terminal, indented on a terminal. `MM_PRETTY=1` / `0` sets the default |

| `--observe` level | Response |
| --- | --- |
| `none` | No `observations`. Fastest. Refs are **not** refreshed: run `yarn mm describe-screen` before you use refs again |
| `diff` | Only what changed since the previous observation |
| `full` | The whole compacted screen (`a11y` + `testIds`). Becomes the new diff baseline |

Observations contain `testIds` and `a11y` only, no app state. The mobile a11y tree is flat: layout-only nodes, the status bar, the navigation bar and the React Native dev overlay are filtered out.

Every tool, `launch` and `cleanup` response includes `meta.timing` (`queueMs`, `toolMs`, `observationMs`, `totalMs`).

Agents that run many commands can call `node_modules/.bin/mm <command>` directly. It takes the same arguments as `yarn mm <command>` and skips the Yarn startup (about 0.4–0.5 s per call).

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
| `--force` | Replace an existing active session |

The `--goal` and `--flow-tags` launch flags were removed in `@metamask/client-mcp-core` 0.13.0. Session metadata is written to `test-artifacts/<sessionId>/session.json`.

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
| `yarn mm describe-screen` | Return the current screen, visible test IDs, and the accessibility tree with refs |
| `yarn mm screenshot [--name <name>]` | Capture the current simulator screen |
| `yarn mm accessibility-snapshot` | Return a trimmed accessibility tree (the shared `--root <selector>` flag is ignored on iOS; the full tree is always returned) |
| `yarn mm list-testids [--limit <n>]` | List visible test IDs |
| `yarn mm get-state` | Return a partial app-state snapshot: `isLoaded`, `extensionId` (the bundle ID / package) and `source: "stub"`. There is no `currentScreen`, and wallet fields (unlock, account, network, balance) are omitted, not guessed. Identify the screen from `describe-screen` test IDs (for example `login-password-input` = unlock, `wallet-screen` = wallet home) |
| `yarn mm get-context` | Report the static prod environment and available mobile capabilities |

Mutating tools (`click`, `type`, ...) and `run-steps` return observations with fresh references, as a compact diff from the prior observation by default. Reads, discovery commands and `cdp` return no observation. Use `describe-screen` whenever a complete tree or refreshed baseline is needed.

Only mutating and batch calls wait for animations before they observe. To get a settled screen after an action, let the action observe (`--observe full`) instead of running a read afterwards.

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
| `observe` | `none`, `diff` (default) or `full`: the observation collected after the batch. Replaces `includeObservations`, which was removed; check `summary.ok` to react to failures |
| `batchTimeoutMs` | Overall deadline, 1000–30000 ms; remaining steps are skipped after expiry. The whole call stops after 30 s, so use a lower value (for example 20000) to get partial results, and split longer flows into several batches |

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

`yarn mm cdp` and `yarn mm hermes-targets` do not reuse the launch's `--metro-port`: they use the daemon's `HERMES_METRO_PORT` or 8081. When Metro runs on another port, pass `--metro-port <port>` on every `cdp` / `hermes-targets` call, or the call fails with `HERMES_CONNECTION_FAILED`.

On Node 20, add `NODE_OPTIONS="--experimental-websocket"` when launching. `yarn mm cdp` returns no observation by default. After runtime mutation, add `--observe full` or run `yarn mm describe-screen` to resynchronize observations.

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
| `yarn mm seed-contract` | Contract seeding needs the e2e chain, which this consumer does not run |
| `yarn mm seed-contracts` | Contract seeding needs the e2e chain, which this consumer does not run |
| `yarn mm get-contract-address` | Depends on seeded e2e contracts that do not exist here |
| `yarn mm list-contracts` | Depends on seeded e2e contracts that do not exist here |

`yarn mm get-context` is available and always reports the static `prod` environment plus the mobile capabilities on offer.

`yarn mm cdp` and `yarn mm hermes-targets` are available for Metro-attached mobile development sessions.
