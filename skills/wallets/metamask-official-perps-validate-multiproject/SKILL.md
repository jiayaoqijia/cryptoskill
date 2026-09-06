---
name: perps-validate-multiproject
description: Interactively validate perps changes across local MetaMask Core, Mobile, and Extension checkouts. Use when a Core @metamask/perps-controller change must be checked in Mobile/Extension, or when a Mobile/Extension perps change needs parity validation in the other client. Defaults to current checkout as owner, yalc for Core package transport, read-only validation targets, and the smallest meaningful proof; asks the user only when required folders or proof level cannot be resolved.
maturity: stable
---

# Validate Perps Multiproject

Validate one perps change across multiple local MetaMask repo checkouts.

**Canonical direction: a CLIENT validates a CORE controller change.** The
`@metamask/perps-controller` package lives in Core; Mobile and Extension consume
it. The owner is wherever the controller change is; the targets are the clients
that must not break. (Client↔client parity is a secondary mode — see below.)

## Deterministic layer — use `scripts/perps-validate.sh`

Do **not** re-derive the per-folder commands each run. `scripts/perps-validate.sh`
encodes them and is portable across machines and Node managers. Run it in order:

```bash
SC="$(dirname "$0")/scripts/perps-validate.sh"   # or the skill's scripts/ path

perps-validate.sh doctor   <core-dir> <client-dir>      # sanity: branches, yalc, links
perps-validate.sh prestate <client-dir> [client-dir...] # snapshot BEFORE touching anything
perps-validate.sh build    <core-dir> [--full]          # build pkg; freshness gate
perps-validate.sh push     <core-dir> <client-dir> [...] # yalc publish + push into clients
perps-validate.sh verify   <client-dir>                 # version + new symbols landed?
#   -> then run the client's own proof (type-check + the affected tests)
perps-validate.sh restore  <client-dir> [client-dir...] # pre-state-aware restore
```

The script makes no assumption about the Node manager and resolves `yalc`
robustly (see "yalc resolution" below). Everything else in this doc explains the
*why* so you can adapt when a step deviates.

## Defaults

- **Owner checkout**: current repo/cwd unless a path is provided.
- **Folder layout**: assume Core/controller, Mobile, and Extension are sibling folders under one workspace.
- **Targets**:
  - Core/controller owner -> validate in Mobile and Extension when available;
  - Mobile owner -> validate parity in Extension;
  - Extension owner -> validate parity in Mobile.
- **Transport**: `yalc` for `@metamask/perps-controller`; none for client parity.
- **Proof**: smallest meaningful proof. For a client validating a Core change,
  the high-value proof is the **client type-check** (catches removed/renamed/
  changed exports) plus **the client tests that exercise the changed surface**.
  Add recipe/e2e or real UI flow only when runtime behavior changes.
- **Target edits**: forbidden unless explicitly allowed.
- **Cleanup**: required, and **pre-state aware** — a client that was already on a
  yalc link must be restored to that exact link, not wiped to a registry baseline.

## Step 0 — resolve folders or ask

Do not guess missing folders. Discover likely local checkouts, then ask only for unresolved choices.

```bash
HERE=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
PARENT=$(dirname "$HERE")

# Prefer sibling folders in the same workspace.
for name in core metamask-core controller metamask-mobile mobile metamask-extension extension; do
  [ -d "$PARENT/$name" ] && echo "$PARENT/$name"
done

# Optional fallback if repos are not siblings.
ROOT="${METAMASK_REPOS_DIR:-$HOME/dev/metamask}"
find "$ROOT" -maxdepth 1 -type d \
  \( -name 'core*' -o -name 'controller*' -o -name 'metamask-mobile*' -o -name 'mobile*' -o -name 'metamask-extension*' -o -name 'extension*' \) -print 2>/dev/null
```

Note: a workspace may hold many numbered clones (`core-1..core-6`,
`metamask-mobile-1..6`). Confirm WHICH core holds the change and WHICH client to
validate — do not assume the first match.

If needed, ask one concise question using the runtime's interactive question tool when available:

```text
I need the validation folders:
- Owner checkout (Core with the change): <default/candidates>
- Validation target client(s): <default/candidates>
- Proof level: transport-only | type/import | recipe/e2e | real UI flow
- May validation targets be edited? default no
```

Echo the resolved contract before changing anything.

## Worker context to inject

```md
## Perps multiproject validation

Owner: <core|mobile|extension> `<path>` on `<branch>`
Targets:
- <project> `<path>` — <read-only|editable> — purpose: <integration/parity>

Rules:
1. Capture `git status --short --branch` in every checkout first (`prestate`).
2. Edit only the owner checkout unless a target is explicitly editable.
3. For Core package validation, build first, then publish via yalc; never publish stale `dist/`.
4. Prove the built `dist/` actually carries the change (version bump + new symbols) before publishing.
5. Run the smallest proof that reaches the changed perps behavior.
6. Restore each client to its snapshot; a pre-existing yalc link must come back byte-for-byte.
```

## Core -> clients via yalc

`scripts/perps-validate.sh` runs all of this. The manual equivalents below are
for when you must deviate.

### yalc resolution (do not assume asdf/nvm/brew)

`yalc` is the single most fragile dependency across machines. A version-manager
**shim can exit 0 yet do nothing** — e.g. asdf prints `No version is set for
command yalc` and returns success, so `yalc publish` silently no-ops. Never trust
the exit code alone: a working `yalc` prints a semver to stdout.

Resolution order (what the script does):
1. `YALC_BIN` env override, if set.
2. `command yalc --version` — accept only if it prints a semver.
3. Otherwise locate yalc's own `yalc.js` and run it through any working `node`.
   Searched layouts: `$(npm root -g)/yalc`, `~/.asdf/installs/nodejs/*/lib/...`,
   `~/.nvm/versions/node/*/lib/...`, `~/.volta/...`, `/opt/homebrew/lib/...`,
   `/usr/local/lib/...`.

If all else fails: `npm i -g yalc`, or pass an explicit
`YALC_BIN="node /abs/path/to/yalc/src/yalc.js"`.

```bash
# Pre-state for every checkout (the script's `prestate` does this + a byte-for-byte
# backup of any existing .yalc link).
for repo in /path/to/core /path/to/client; do
  echo "--- $repo"; git -C "$repo" status --short --branch
  (cd "$repo" && printf 'node=%s yarn=%s\n' "$(node -v)" "$(yarn -v)")
done
```

### Building the package — expect a full monorepo build

The perps-controller package **cannot build standalone in a fresh Core checkout.**
Its `tsconfig.build.json` uses project references, so `yarn workspace
@metamask/perps-controller build` fails with `TS6305: Output file ... has not been
built from source file` for every dependency package whose `dist/` is missing
(network-controller, transaction-controller, controller-utils,
profile-sync-controller, remote-feature-flag-controller, messenger, …). This is
the normal state of a fresh checkout, **not** a perps-controller bug.

The supported fix is a full monorepo build first:

```bash
cd /path/to/core
nice -n 10 yarn build          # builds all referenced dists in dependency order
```

This takes several minutes (40+ packages) but is clean and leaves the checkout
buildable for later runs. Do **not** use `yarn workspaces foreach --from
@metamask/perps-controller -R ...` — it can fail on the
account-tree/multichain/perps/snap cycle and delete `dist/` on the way out.
`perps-validate.sh build <core> --full` wraps `nice -n 10 yarn build`; the
plain `build` form detects TS6305 and tells you to re-run with `--full`.

### Freshness gate

`yalc publish` success is meaningful only when the **current** run produced a
fresh `packages/perps-controller/dist`, and that dist carries the change. Verify
before trusting it:

```bash
D=/path/to/core/packages/perps-controller
node -p "require('$D/package.json').version"        # expected bump
ls "$D"/dist/index.cjs                               # dist exists
grep -l "<new export symbol>" "$D"/dist/index.d.cts  # new surface present
```

### Publish + push (advancing an existing link)

A client may **already** be on a yalc link (e.g. mid-feature dev). In that case
`yalc add` is wrong — use `yalc update` to advance the existing link in place.
`perps-validate.sh push` picks the right one automatically.

```bash
cd /path/to/core/packages/perps-controller && yalc publish --private --push
# `--push` propagates to every linked project. WATCH THE OUTPUT: it will touch
# *other* repos that link the same package (e.g. a sibling clone), not just your
# target. That is a side effect to note, not a failure.
```

### Run the proof, then restore

Client proof for "controller won't break":

```bash
cd /path/to/client
# 1. type-check — the strongest signal for export/type regressions.
NODE_OPTIONS='--max-old-space-size=8192' npx tsc --noEmit --incremental \
  --tsBuildInfoFile .tsbuildinfo --project ./tsconfig.json
# 2. the client tests that exercise the changed surface (NOT the whole suite,
#    NOT --findRelatedTests).
yarn jest <files that import the changed symbols> --no-coverage
```

### Cleanup — pre-state aware (critical)

The old "rm -rf .yalc yalc.lock && git checkout package.json yarn.lock" recipe is
**destructive** when the client was already on a yalc link before you started: it
wipes the user's active dev setup. Restore to the snapshot taken by `prestate`:

- **Client was already yalc-linked** → restore the backed-up `.yalc/<pkg>`
  byte-for-byte, restore `yalc.lock`/`package.json`, re-run
  `yarn install --mode=skip-build` if node_modules must match.
- **Client had no prior link (registry baseline)** → `yalc remove <pkg>`,
  `git checkout -- package.json yarn.lock`, `rm -rf .yalc yalc.lock`.

`perps-validate.sh restore <client>` does the right one based on the recorded
mode. If you advanced a client deliberately and the user wants to keep the new
version, say so explicitly and keep the snapshot for a later restore.

## Client parity

For Mobile <-> Extension checks:

1. Load relevant installed perps knowledge from `knowledge/`: `mobile-extension-map`, `screens`, `shared-package-analysis`, architecture docs as needed.
2. Find the equivalent screen/hook/flow in the other client.
3. Validate with real flow evidence; do not inject UI state.
4. Report semantic differences separately from regressions.

## Stop conditions

Stop and report when the owner package cannot build (after `--full`), a target
checkout has unexpected dirt, cleanup would delete user work, target source edits
are needed but not allowed, or required device/browser/credential context is
missing.

## Final answer

```md
Validated <change> against <targets>.
- Owner: <path>@<branch>, status <clean/expected dirty>
- Targets: <path/status>
- Transport: <yalc package/version or none>  (built via full monorepo build / package build)
- Proof: <type-check + tests/recipes> => <pass/fail>
- Artifacts: <paths>
- Cleanup: <restored to snapshot | left on new version by request + snapshot kept>
- Follow-ups/blockers: <if any>
```
