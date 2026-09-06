---
name: deploy-to-cloud-engine
description: "Deploys a built Internet Computer project to a cloud engine (OpenCloud): link the console identity with `icp identity link web` (defaults to https://opencloud.org; a delegation handoff covers sandboxes the browser cannot reach), run `icp deploy` on the engine's subnet, tag canisters with `__META_*` for a named console app, bake version metadata (service:git:sha) into the wasm, and deploy the proxy an app needs for Bitcoin/Ethereum signing, VetKeys or exchange rates, card-funded from the console or self-deployed via `icp new --subfolder proxy`. Use when shipping to a cloud engine; on mention of OpenCloud, an engine subnet id, or linking the icp CLI; when sign-in never completes from a sandbox; when naming, versioning or giving an icon to a console app; when a proxy must be deployed, funded or topped up (failing proxied calls: cloud-engine-canisters); or which balance to top up (subscription, reserve, proxy). Do NOT use for a mainnet deploy with no engine (icp-cli) or canister logic (cloud-engine-canisters)."
license: Apache-2.0
compatibility: "icp-cli >= 0.3.0 (deploy/identity commands verified against 0.3.0 and 1.0.2, proxy and cycles commands against 1.0.2 and 1.3.0; the delegation handoff needs `icp identity delegation`, present in 1.0.x; the `proxy` project template needs `icp new --subfolder`), a cloud engine console account, a browser for the Internet Identity sign-in, and a saved payment method for the console-funded proxy"
metadata:
  title: Deploy to Cloud Engine
  category: CloudEngine
---

# Deploy to Cloud Engine

## What This Is

A **cloud engine** is a user-owned slice of Internet Computer capacity, administered from a web console (by default `https://opencloud.org`). Each engine runs on a single **subnet**. This skill takes a project that already builds and gets it deployed onto that engine, from a coding agent.

This skill only covers the cloud-engine-specific steps: linking the CLI to the engine's console identity, and a subnet-targeted deploy. For everything else about the CLI (`icp.yaml`, recipes, environments, bindings, identities), load the **`icp-cli`** skill.

Before running any `icp` command you are unsure of, run `icp <subcommand> --help` (e.g. `icp identity link --help`, `icp deploy --help`) to confirm the command and flags exist. Do not infer flags. Authoritative reference: https://cli.internetcomputer.org/llms.txt

## What You Need

Two values. Look for them first in `icp.yaml` or earlier in the conversation. One has a default; the other you must ask for:

1. **Console origin** — the URL the user signs in to their cloud engine console with. **Defaults to `https://opencloud.org`** (the main OpenCloud console). It is used as the `--auth` origin in Step 1 so the linked CLI identity derives the **same principal that administers the engine**. Use the default, but say so and give the user a chance to override before linking:
   - Say: "I'll link the CLI against `https://opencloud.org`, the default console. If you sign in to your engine console at a different URL, tell me now."
   - Only use a different origin when the user names one — never substitute another URL on your own; the `--auth` origin determines the derived principal (see Pitfall 2).
2. **Subnet id**: the subnet the engine deploys to, required by `icp deploy --subnet`. There is **no default**; never guess it. The user finds it on the engine's **Settings** page in the console (under the engine's identifiers), or copies it from the console's command palette. If absent, **ask and do not proceed without it**:
   - Ask: "What is your engine's subnet id? It is on your engine's Settings page in the console."

Record both so you do not re-ask within the session.

## Prerequisites

- `icp` on `$PATH` — see the **`icp-cli`** skill to install. Verify with `icp --version` (this skill's commands are verified against 0.3.0 and 1.0.2). If the installed version differs, confirm the flag set with `icp <cmd> --help` before running — flags have changed across major versions.
- A project that already builds. If it does not build or package yet, set that up first (see the `icp-cli` skill), then return here.
- macOS: `icp` stores its data under `~/Library/Application Support/org.dfinity.icp-cli/`. If the shell cannot write there (`Operation not permitted` from macOS TCC, e.g. when commands run through a bridge), redirect the data to an unprotected path for the session — `HOME=/tmp/icp-home icp …` — and keep that same `HOME` on **every** subsequent `icp` command, or the later commands will not see the linked identity.

## Step 1 — Link the CLI to your engine identity (once per machine)

The CLI must sign as the **same identity that administers the engine** — that is the principal you log in to the console with.

### Step 1.0 — First determine WHERE the CLI runs relative to the browser

`icp identity link web` completes the sign-in via a redirect to `http://127.0.0.1:<port>` **on the machine where the CLI runs**. The browser in which the user completes the Internet Identity sign-in must be able to reach that loopback address. Determine the environment before linking:

- **CLI and browser on the same machine, with network** (local development, or a terminal-integrated agent on the user's own machine) → use the normal link flow below.
- **CLI in a remote or isolated sandbox, with network** (the agent runs in the cloud; the user's browser is on a different machine) → the normal flow **cannot** work: the sign-in URL carries a `callback=http://127.0.0.1:<port>` bound to the sandbox, the user's browser resolves `127.0.0.1` to its *own* machine, and the delegation never reaches the CLI. Later commands then fail with authorization errors. Use the **delegation handoff** below instead.
- **CLI shell with no network at all** (e.g. a sandboxed device bridge on the user's own machine: DNS blocked, HTTPS requests fail, writes limited to `/tmp`) → **no** `icp` network command can run there — not the link, and not `icp deploy` either. The delegation handoff does not help: it only moves signing authority, not network access. Do not retry, tunnel, or proxy. Prepare the project and hand the user **one script** to run in their real terminal — see "No-network CLI host" below.

When in doubt, probe before linking: `curl -sI https://<console-origin>` failing (or DNS not resolving) from the CLI shell means the no-network case.

**Never** present a sandbox `127.0.0.1` URL to the user as something to open in their browser — it is unreachable from their machine. And do not invent a headless flag on `icp identity link web`: as of icp-cli 1.0.2 it has none (confirm with `icp identity link web --help`).

### Delegation handoff (CLI host and browser on different machines)

`icp identity delegation` transfers signing authority from an identity linked on the **user's** machine to a session key on the **CLI host**, without the browser ever reaching the CLI host. It requires `icp` installed on the user's machine too, and exists in icp-cli 1.0.x — verify with `icp identity delegation --help` on both machines. If the user's machine has `icp` and you can run commands there, the simplest path is to run this whole skill there instead; otherwise:

1. **On the CLI host (sandbox)** — create a pending identity with a fresh session key:

   ```bash
   icp identity delegation request <your-identity-name>
   ```

   It prints the session **public** key as a PEM to stdout. Give that PEM block to the user. (If the default `--storage keyring` fails in a headless sandbox, retry with `--storage plaintext`.)

2. **On the user's machine** — the user links there if not already linked (`icp identity link web <local-name> --auth <console-origin>` — the normal flow works locally), saves the PEM to a file, and signs a delegation to it:

   ```bash
   icp identity delegation sign --identity <local-name> --key-pem session-key.pem --duration 8h > delegation.json
   ```

   `--duration` takes e.g. `30m`, `8h`, `1d`; optionally `--canisters <ids>` restricts the delegation. The user sends `delegation.json` back. If `sign` fails with `delegation for identity <name> has expired or will expire within 5 minutes`, the local web session has lapsed — run `icp identity reauth <local-name>` (the normal browser flow, which works locally) and retry.

3. **On the CLI host** — complete the pending identity and activate it:

   ```bash
   icp identity delegation use <your-identity-name> --from-json delegation.json
   icp identity default <your-identity-name>
   icp identity principal   # must print the user's console principal
   ```

Treat `delegation.json` as a **time-limited credential**: whoever holds the sandbox's session key can sign as the user's console principal until it expires. Keep the duration short and re-run the handoff when it lapses.

### No-network CLI host — hand the user one script

If the CLI shell cannot reach the network, the user's real terminal is the deploy machine — and because their terminal and browser share a loopback there, the **normal** link flow works; no delegation handoff is needed. Your job shifts to preparation:

1. Get the built project into a directory the user's terminal can reach.
2. Write one script at the project root that does the whole network-bound sequence — adapt this template (fill in the real identity name, console origin, and subnet id; do not leave placeholders):

   ```bash
   #!/usr/bin/env bash
   set -euo pipefail
   icp --version
   icp identity list | grep -E '^\*? *<your-identity-name> ' >/dev/null || icp identity link web <your-identity-name> --auth <console-origin>
   icp identity default <your-identity-name>
   icp deploy -e ic --subnet <subnet-id>
   ```

3. Ask the user to run it in their terminal, complete the Internet Identity sign-in when the browser opens, and paste the output back.
4. Verify from the pasted output (canister ids, frontend URL) and continue — a re-deploy for the Step 2 `__META_*` variables goes through the same script.

### Normal link flow (CLI and browser share a loopback)

First check what already exists:

```bash
icp identity list      # names + principals; * marks the active identity
```

The list does **not** show which console (if any) an identity was linked against — that cannot be determined from the CLI. Decide like this:

- **Only `anonymous` (or plain local identities) listed** — no web-linked identity exists; run the link command below.
- **An identity the user recognizes as their engine identity** (by name or principal) — set it active (below) and skip to Step 2.
- **Unsure** — ask the user, or simply relink under a new name; linking again is cheap and safe.

To link, run this, substituting a name the user picks — `<your-identity-name>` is any local label, not a fixed value (do not hardcode something like `my-engine-admin`); reuse the **same** name in every command below:

```bash
icp identity link web <your-identity-name> --auth <console-origin>
```

- Use `https://opencloud.org` as `<console-origin>` unless the user named a different console. Never omit `--auth`: the flag has a built-in default (`https://id.ai`) that is **not** your console and silently derives the wrong principal.
- The command first waits at a **"Press Enter to log in"** prompt before anything happens. Run it interactively when you can; in a non-interactive shell (e.g. a background process) pipe a real newline:

  ```bash
  printf '\n' | icp identity link web <your-identity-name> --auth <console-origin>
  ```

  Do **not** redirect stdin from `/dev/null` — the bare EOF does not satisfy the prompt, and the command sits on "Press Enter to log in" indefinitely with no browser ever opening.
- After Enter it opens a **browser tab**. The **user** completes the Internet Identity sign-in there. Wait for them to confirm before continuing — you cannot complete the sign-in for them.
- `--auth` must be the **exact** console origin (scheme + host), e.g. `https://opencloud.org`. A mismatched origin derives a *different* principal, and the engine will reject the deploy as unauthorized.
- This is a **one-time, per-machine** step.

Then make it the active identity and verify:

```bash
icp identity default <your-identity-name>
icp identity default     # prints the active identity name
icp identity principal   # prints the principal the deploy will sign as
```

## Step 2 — Name the app (and give it an icon) in the console (recommended)

By default, CLI-deployed canisters appear on the engine console's Applications page as bare rows labelled only by their principal id. A set of **canister environment variables** makes the console group them into a single named application with readable per-canister labels, an "Open" button, and an icon. Set them once in your project config:

- `__META_PROJECT` — the application name. Canisters that share the **same** value are grouped into one named app, so set an identical value on every canister of the app.
- `__META_NAME` — the per-canister display label (e.g. `Backend`, `Frontend`).
- `__META_MAIN_CANISTER` — the literal string `"true"` on exactly one canister (the entry point, usually the frontend/asset canister). This marks the app's **main canister**: the console reads `__META_BASE_URL` and `__META_ICON_PATH` only from it, and the "Open" button targets it.
- `__META_BASE_URL` — an **absolute `https://` URL**, set on the main canister (e.g. the frontend canister's URL `https://<frontend-canister-id>.icp.net`, or a custom domain). When present and valid, it is the URL the "Open" button opens; when absent or not `https`, the "Open" button falls back to the main canister's gateway URL. It is also the base that `__META_ICON_PATH` resolves against.
- `__META_ICON_PATH` — the path to the app icon, resolved against `__META_BASE_URL` to form the icon the console renders (e.g. `/favicon.svg` → `https://<base>/favicon.svg`). Set it on the **main** canister, alongside `__META_BASE_URL`.

The icon and "Open" link are read **only from the main canister** (the one marked `__META_MAIN_CANISTER: "true"`) — `__META_BASE_URL` / `__META_ICON_PATH` on any other canister are ignored.

Set them under each canister's `settings.environment_variables` — this is valid alongside a recipe. With per-canister `canister.yaml` files:

```yaml
# frontend/canister.yaml
name: frontend
recipe:
  type: "@dfinity/static-site@v0.3.3"
  configuration:
    build:
      - npm install
      - npm run build
    dir: dist
settings:
  environment_variables:
    __META_PROJECT: "My App"
    __META_NAME: "Frontend"
    __META_MAIN_CANISTER: "true"
    __META_BASE_URL: "https://<frontend-canister-id>.icp.net"
    __META_ICON_PATH: "/favicon.svg"
```

```yaml
# backend/canister.yaml
name: backend
recipe:
  type: "@dfinity/motoko@v5.0.0"   # v5 reads main/candid from mops.toml ([canisters.backend]) — see the icp-cli skill
settings:
  environment_variables:
    __META_PROJECT: "My App"
    __META_NAME: "Backend"
```

For a single inline `icp.yaml` (canisters defined there directly), put the same `settings.environment_variables` block under each canister entry. Note the inline form: `canisters` is an **array** of `{name, recipe, settings}` items, not a map keyed by canister name:

```yaml
# icp.yaml — canisters defined inline
canisters:
  - name: frontend
    recipe: # … as in the canister.yaml example above
    settings:
      environment_variables:
        __META_PROJECT: "My App"
        __META_NAME: "Frontend"
        __META_MAIN_CANISTER: "true"
        __META_BASE_URL: "https://<frontend-canister-id>.icp.net"
        __META_ICON_PATH: "/favicon.svg"
  - name: backend
    recipe: # … as in the canister.yaml example above
    settings:
      environment_variables:
        __META_PROJECT: "My App"
        __META_NAME: "Backend"
```

Notes:
- icp-cli **merges** these with the `PUBLIC_CANISTER_ID:<name>` variables it injects automatically at deploy time — the asset canister keeps serving and the app keeps working. (Verified against icp-cli 0.3.0.)
- All values are strings; `__META_MAIN_CANISTER` must be the exact string `"true"`.
- They are applied during `icp deploy` (the "Setting environment variables" step). After deploy, confirm with `icp canister settings show <name> -e ic`.

Icon specifics (the console builds the icon as `__META_BASE_URL` + `__META_ICON_PATH`):
- **Both** must be present and **on the main canister** for an icon to appear — there is no fallback. `__META_ICON_PATH` alone does nothing.
- `__META_BASE_URL` must parse as an absolute **`https://`** URL. A bare host, an `http://` URL, or a `data:` / `javascript:` value is rejected: the icon then does not render, and the "Open" button falls back to the main canister's gateway URL (it does not disappear). (The console validates the scheme before using it.)
- `__META_ICON_PATH` is a **path to an asset your frontend actually serves** (e.g. `/favicon.svg`), not an inline image. The resolved URL is rendered as an `<img>` `src`, so it must return an image. Do **not** put a `data:` URI here: engine env values are length-capped (≤128 chars observed), so it would not fit, and the field is a path by design.
- The frontend canister's id is only known **after** the first deploy. The usual flow is: deploy once, read the frontend canister id from the output, set `__META_BASE_URL` to `https://<that-id>.icp.net` (and `__META_ICON_PATH`), then re-deploy to apply. If you control a custom domain for the app, you can set it up front instead.

### Pin the Internet Identity derivation origin (if the app signs users in)

Internet Identity derives a principal **per origin**. An app reached at both its canister address and a custom domain signs the same person in as two different users.

The engine console names the app's **canister address** as the origin to derive from. It cannot be renamed or removed, so it survives adding, changing, or dropping a custom domain. It is the address of the canister that **serves your frontend** (the asset/static-site canister the browser loads the app from), built from that canister's id:

```
https://<frontend-canister-id>.icp.net
```

That is usually the canister you marked `__META_MAIN_CANISTER: "true"`, but that flag is a console display setting, not a guarantee. If you marked a backend canister, still derive from the frontend canister. A backend canister cannot be a derivation origin: the browser is never on it, and it cannot serve the `.well-known/ii-alternative-origins` file Internet Identity fetches from that origin to validate the claim.

Build the value from the canister id, **not** from `__META_BASE_URL`. The two match only while `__META_BASE_URL` still points at the canister address. Pointing it at a custom domain is normal and supported (see the icon notes above), and the two then differ. A custom domain is the one value that must never become the derivation origin.

**Do this before the app has users, not after.** A domain that has already collected sign-ins cannot be repointed at a derivation origin without orphaning every account created under it. If the app might ever get a custom domain, set `derivationOrigin` on the first deploy even while the canister address is the only origin — it costs nothing then and cannot be applied retroactively without losing accounts.

For the mechanics — the `derivationOrigin` option and the `.well-known/ii-alternative-origins` file, including the `_headers` entry the `@dfinity/static-site` recipe needs — load the **`internet-identity`** skill.

Caffeine apps are the exception: Caffeine owns their address, so it is not the app's to derive from. The console withholds the canister-address row for them.

### Version metadata (recommended)

Embed build provenance into each canister's wasm so tooling and the console can show what version is running (console support is rolling out; the metadata is already readable — see the verify note below). Add this **by default on every deploy** — do not wait for the user to ask. All official recipes (motoko, rust, static-site, asset-canister, prebuilt) accept a `metadata` list under the recipe `configuration`; each entry is baked into the wasm as a custom section. Values are interpolated into a shell command at build time, so `$(…)` command substitution works. (Verified by live builds against `@dfinity/motoko` v4.1.0 and v5.0.0 on icp-cli 1.0.2.)

**Git project** (check first: `git rev-parse HEAD` succeeds):

```yaml
recipe:
  type: "@dfinity/motoko@v5.0.0"
  configuration:
    metadata:
      - name: service:git:sha
        value: $(git rev-parse HEAD)$(git diff --quiet HEAD 2>/dev/null || echo +dirty)
      - name: service:git:origin
        value: $(git remote get-url origin)
      - name: service:git:updated_at
        value: $(git log -1 --format=%cI)
      - name: service:version
        value: $(node -p "require('./package.json').version" 2>/dev/null || echo 1.0.0)
```

**Non-git project** — the git substitutions above do **not** fail the build; they silently bake garbage (`service:git:sha` becomes the literal `+dirty`, `service:git:origin` comes out empty). Use only an explicit version, and bump it on each subsequent deploy:

```yaml
metadata:
  - name: service:version
    value: "1.0.0"
```

Notes:

- Use these exact names (`service:git:sha`, `service:git:origin`, `service:git:updated_at`, `service:version`) — they are the agreed convention the console will read; differently named entries will not be picked up.
- Prefer command results over literals where possible: `+dirty` on the sha flags uncommitted changes, so a deploy is traceable to its exact source state.
- Values must be **deterministic** for a given source tree: sha, origin, the last commit's date, a version string. Never embed a build time (`$(date)`) or other build-time-varying values. The commit date (`%cI`) is allowed because it is a property of the commit, not of the build — but note it means "code last changed", not "last deployed": deploying an old commit shows the old date. The deploy time itself comes from the canister history the network records automatically.
- If the project has no `package.json` (or no version field), the fallback `1.0.0` applies; replace it with the project's real versioning scheme when one exists.
- The sections are injected as `icp:private`, readable by the canister's controllers (you, and the console acting as you) via read_state — no canister call needed. Verify after deploy, with the linked identity active: `icp canister metadata <canister-name> service:git:sha -e ic`.

## Step 3 — Deploy to the engine's subnet

From the project root:

```bash
icp deploy -e ic --subnet <subnet-id>
```

- `-e ic` targets mainnet (the engine runs on an IC subnet); `--subnet <subnet-id>` pins the deploy to **your engine's** subnet. Confirm the exact flags with `icp deploy --help` before running if unsure.
- Deploying consumes capacity on the engine; make sure the engine has room.

**Alternative: packaged upload.** If the project is distributed as a built `.icp` package and a direct `icp deploy` is not available, the user can upload the bundle instead: engine → **Applications** → **Build and deploy app**, which walks through selecting the engine and uploading the `.icp` bundle. The same menu ("More ways to deploy") offers the App Store for ready-made apps and the CLI instructions this skill automates.

## Step 4 — Verify

- The `icp deploy` output reports the deployed canister ids.
- The canisters appear on the engine's **Applications** page in the console; each canister's detail view offers an "Open in browser" link.
- If you set the metadata in Step 2, the canisters are grouped under your `__META_PROJECT` name with their `__META_NAME` labels, and the main canister shows an "Open" button — instead of bare principal rows. With `__META_BASE_URL` + `__META_ICON_PATH` set, the app also shows its icon (allow for a short console cache delay).
- A frontend (asset) canister is served at `https://<frontend-canister-id>.icp.net`.

Report the deployed canister ids (and the frontend URL, if any) back to the user.

## Step 5: Deploy a proxy canister (only if the app needs chain-key services)

Skip this step unless the app calls **threshold ECDSA or Schnorr** (Bitcoin, Ethereum), **vetKD / VetKeys**, the **exchange-rate canister** (XRC), or any other canister that must be paid in cycles across a subnet boundary. Everything else (the app's own execution, storage, messaging, and HTTPS outcalls) is free on an engine and needs no proxy at all.

Those services live on other subnets and charge cycles per call, and an engine canister can neither hold cycles nor send a cycle-bearing message across the engine boundary. A **proxy canister** on a normal Application subnet makes the call on its behalf and pays from its own balance.

### Which proxy

Two different canisters can play this role, and picking the wrong one produces a working-looking setup that fails at the first call:

| | **Console proxy** | **Self-deployed proxy** |
|---|---|---|
| Deployed by | The console, per engine | You, with `icp` |
| Authorized callers | The engine's **canister-id ranges**, plus controllers | **Controllers only** |
| Your engine canisters may call it | Yes, automatically | Only after you add each one as a controller |
| Your CLI identity may call it | **No** (rejected as `UnauthorizedUser`) | Yes: you are a controller |
| Threshold-key derivation | Isolated per calling canister | No isolation |
| Funded with | A card, in USD | Cycles you hold (`icp cycles mint`) |

- **App code calling chain-key services → the console proxy.** It is the one that admits your engine's canisters without per-canister configuration.
- **You calling something from the CLI** (`icp canister call --proxy`, `icp deploy --proxy`, canister-only management methods like `canister_info` or `raw_rand`) **→ your own proxy.** The console proxy cannot serve this: it rejects ingress from any non-controller principal, and your CLI identity is not one.

They are not substitutes, and they derive **different keys**: see the derivation warning in `cloud-engine-canisters` before switching an app from one to the other.

### Console proxy: deploy and fund it (a console action, not a CLI one)

There is no `icp` command and no agent-drivable API for this: the console endpoints behind it authenticate with a browser session cookie minted by the Internet Identity login. Hand the user these steps and wait for the proxy canister id:

1. Open the engine in the console → **Canisters** in the engine's sidebar (not **Applications**, which lists deployed apps) → the **Proxy canisters** section.
2. **Deploy a proxy**: choose the initial balance (**minimum $5**, maximum $1000 per spend). The saved card is charged for that amount and the proxy is provisioned in under a minute; if no card is saved yet, the console opens a hosted Stripe Checkout to capture one first.
3. Optionally turn on **Automatic top-up** and pick a recharge amount. The console then charges the card and refills the proxy whenever its balance falls below a low threshold (500 G cycles by default), so a signing app does not stall at 3am. Without it the proxy is **Manual**: its balance is still refreshed and shown, but it is never charged.
4. Copy the **proxy canister id** from the table. That id is what the app calls.

Also on that table: **Refresh balance** (a live read, since the displayed figure is cached), **Top up** (charge the card and deliver cycles now), and **Delete proxy** (stops and deletes the canister and refunds the remaining balance to the payment method).

An engine may have **more than one** proxy ("Deploy another proxy"). They are independent balances and, for a signing app, independent key namespaces.

### Wire the proxy id into the app

The app needs the id at runtime. Pass it as a canister environment variable rather than hardcoding it in source, so the same code can run against a local mock and against the engine:

```yaml
settings:
  environment_variables:
    PROXY_CANISTER_ID: "<proxy-canister-id>"
```

Read it in the canister the same way as any other environment variable, and treat it as **permanent configuration**: for an app that derives threshold keys, changing this value changes every address the app owns.

### Self-deployed proxy: the CLI path

For proxying *your own* calls. This one is the upstream `dfinity/proxy-canister`, deployed from a template:

```bash
icp new my-proxy --subfolder proxy       # pre-built wasm, no init args
cd my-proxy
icp deploy -e ic                         # NOT --subnet <engine-subnet>: see below
export PROXY_ID=$(icp canister status -e ic --id-only proxy)
```

Fund it, and check on it, with the cycles ledger:

```bash
icp cycles balance -e ic                 # what you hold
icp cycles mint --icp 1 -e ic            # ICP -> cycles, if you need more
icp canister top-up "$PROXY_ID" --amount 5t -e ic
icp canister status "$PROXY_ID" -e ic    # the proxy's own balance
```

Then pass it to any command that needs cycles or a canister-only management method:

```bash
icp canister call my-canister charge_me '()' -e ic --proxy "$PROXY_ID" --cycles 1_000_000_000_000
icp deploy -e ic --proxy "$PROXY_ID"
```

Three things to get right:

- **Do not deploy it onto the engine's subnet.** A proxy on a `CloudEngine` subnet is useless: it holds 0 cycles and cannot send a cycle-bearing message either. Omit `--subnet` (Step 3's engine-subnet flag is for your app, not for this) so it lands on a normal Application subnet.
- **It authorizes controllers only.** For an *engine canister* to call it, that canister's principal must be added as a controller (`icp canister settings update "$PROXY_ID" --add-controller <canister-id> -e ic`), one call per canister, repeated whenever a canister is added. This is the maintenance burden the console proxy exists to remove.
- **It does not isolate key derivation.** Any authorized caller can request any derivation path, and the keys it produces differ from the console proxy's. Do not point a signing app at one casually.

## Paying for an engine: the three balances

Three separate balances exist, they are funded differently, and running one dry has nothing to do with the others. Do not "top up the canister" on an engine without first establishing which of these is meant:

| Balance | What it pays for | How it is funded | What happens when it empties |
|---|---|---|---|
| **Engine operating budget** | The engine itself: node payments, compute, bandwidth | The engine's subscription: a recurring card charge set up at checkout | The engine **freezes**: the console describes this as canisters paused with code and data preserved. Recovered by paying the outstanding renewal from the engine's billing page, possible only while the failed invoice is still payable, so treat a freeze as urgent, not parked |
| **Engine emergency reserve** | Holding a frozen engine open long enough to recover it | A prepaid window chosen at checkout (capped at **4 weeks**), extendable later by the engine **owner** from the console | The engine is **permanently deleted**: this is the one that is not reversible |
| **Proxy cycle balance** | Only the calls the proxy relays (signing, vetKD, XRC) | Card, per the console flow above, or `icp canister top-up` for a self-deployed one | Relayed calls fail with `InsufficientCycles`; the proxy freezes rather than being deleted, and recovers on a later top-up |

The app's own canisters have **none** of these: they hold 0 cycles by design and cannot be topped up. A "0 cycles" reading on an engine canister is normal (see `cloud-engine-canisters`, pitfall 5).

## Code that runs on the engine

A cloud engine runs on a **`CloudEngine` subnet** with protocol-level call rules that differ from normal Application subnets: engine canisters hold 0 cycles and must **never attach cycles** to any call, **cross-subnet calls must be bounded-wait**, HTTPS outcalls are made directly and free, and cycle-bearing cross-subnet targets (exchange-rate XRC, threshold ECDSA/Schnorr, vetKD) go through the engine's funded **console proxy canister**. Before writing or debugging any canister code that will run on the engine, load the **`cloud-engine-canisters`** skill — it has the rules, the proxy interface, and the pitfalls.

## Common Pitfalls

1. **Sign-in not completed.** Running `icp identity link web …` but not finishing the Internet Identity sign-in in the browser leaves the CLI unlinked; later commands fail with authorization errors. Re-run and wait for the user to confirm the browser flow finished. If no browser ever opened, the command is stalled at the "Press Enter to log in" prompt — relaunch with a piped newline, `printf '\n' | icp identity link web …`, never `< /dev/null` (see Step 1). If the CLI runs in a remote sandbox, re-running can never complete — see Pitfall 10 and the delegation handoff in Step 1.0.
2. **Wrong `--auth` origin.** Using any URL other than the console origin the user signs in with derives a different principal, and the engine rejects the deploy as not authorized. Relink with the exact console URL. If the deploy is rejected as unauthorized after linking against the default `https://opencloud.org`, ask the user for the exact URL they sign in with and relink.
3. **Guessing the subnet id.** Never invent it: the deploy fails or targets the wrong subnet. It is on the engine's **Settings** page in the console; ask the user.
4. **Deploying with the anonymous identity.** The default local identity is anonymous and is not the engine admin. You must link and `icp identity default <your-identity-name>` first.
5. **Using `dfx`.** This ecosystem uses `icp`, never `dfx`. The correct sequence is `icp identity link web <name> --auth <console-origin>` (Step 1), then `icp deploy -e ic --subnet <subnet-id>` (Step 3). See the `icp-cli` skill.
6. **Skipping the app metadata.** Without `__META_PROJECT` (Step 2), the canisters still deploy and work but render as bare, unnamed principal rows in the console. Setting `__META_*` is what produces a named app with labelled canisters and an "Open" button.
7. **Wrong `__META_MAIN_CANISTER` value.** It is matched as the exact string `"true"`. A boolean, `"True"`, or marking more than one canister means no (or the wrong) "Open" button. Mark exactly one entry-point canister.
8. **Inventing an icon variable.** The icon variable is `__META_ICON_PATH` (a path resolved against `__META_BASE_URL`). Do not guess `__META_ICON`, `__META_LOGO`, or `__META_ICON_LINK` — they are ignored, so the icon silently never appears.
9. **Icon set on the wrong canister, or without a base URL.** The icon is read only from the **main** canister and needs **both** `__META_BASE_URL` (a valid absolute `https://` URL) and `__META_ICON_PATH`. Setting the icon path on a side canister, omitting the base URL, or giving a non-https / `data:` base means no icon renders. (The "Open" button still works — it falls back to the main canister's gateway URL — so a bad base URL costs the icon and the custom Open URL, not the button.)
10. **Assuming the browser and CLI share localhost.** `icp identity link web` returns the delegation to `127.0.0.1:<port>` on the CLI host. If the CLI runs in a remote sandbox while the user's browser is on a different machine, the sign-in never completes and later commands fail with authorization errors — no amount of re-running the link fixes it. See Step 1.0: use the delegation handoff (`icp identity delegation request` / `sign` / `use`), or run the link and deploy where the browser and CLI share a loopback.
11. **Expecting the delegation handoff to fix a missing network.** The handoff moves signing authority, not connectivity — `icp deploy` still needs the network from the shell that runs it. If the CLI shell has no network at all (a sandboxed device bridge: DNS blocked, HTTPS fails), no `icp` network command can run there, link or deploy. Do not offer to "do the rest" from that shell and do not tunnel — hand the user one script for their real terminal (see "No-network CLI host" in Step 1.0), where the normal link flow works because terminal and browser share a loopback.
12. **Build timestamps in wasm metadata.** Metadata is baked into the wasm and must be deterministic — a build time (`$(date)`) changes every build even with identical source, breaking reproducibility and changing the module hash on every deploy. The deterministic alternative is the last commit's date, `service:git:updated_at` = `$(git log -1 --format=%cI)` — a property of the source tree, not the build. The deploy time itself comes from the canister history recorded by the network, never from metadata.
13. **Git metadata substitutions in a non-git project.** Outside a git repository, `$(git rev-parse HEAD)` does not fail the build — it silently bakes garbage: `service:git:sha` becomes the literal `+dirty` and `service:git:origin` comes out empty. Check for a git repo first (`git rev-parse HEAD` succeeds); if there is none, set only `service:version` with an explicit value (or `git init` and commit before deploying, if version control is wanted anyway).
14. **Letting an engine app collect sign-ins before pinning a derivation origin.** Internet Identity principals are per-origin, so adding a custom domain later turns every existing user into a stranger at the new address — and the fix cannot be applied retroactively without orphaning the accounts already made under the old origin. On the first deploy of any app that uses II, set `derivationOrigin` to the address of the canister that serves the frontend, built from its canister id (`https://<frontend-canister-id>.icp.net`), even when that is currently the app's only origin. Do **not** copy `__META_BASE_URL`: it is allowed to point at a custom domain, and a custom domain is exactly what must not become the derivation origin. See the `internet-identity` skill for the `.well-known/ii-alternative-origins` half.
15. **Trying to deploy or fund the console proxy from the CLI or an API.** There is no `icp` command for it, and the console endpoints behind the buttons authenticate with a browser-session cookie from the Internet Identity login (no token auth), so an agent cannot drive them. Hand the user the console steps (engine → **Canisters** → **Proxy canisters**) and wait for the proxy canister id. An agent *can* do the whole self-deployed-proxy path unattended, but that is a different canister with different authorization (Step 5).
16. **Deploying a self-deployed proxy onto the engine's subnet.** Reusing Step 3's `--subnet <engine-subnet-id>` puts the proxy on the `CloudEngine` subnet, where it holds 0 cycles and may not send cycle-bearing messages either, so it cannot do the one thing a proxy is for. Omit `--subnet` so it lands on a normal Application subnet.
17. **Expecting a self-deployed proxy to accept calls from engine canisters.** It authorizes **controllers only**. An engine canister calling it gets `UnauthorizedUser` until that canister's principal is added with `icp canister settings update <proxy> --add-controller <canister-id> -e ic`, and again for every canister added later. The console proxy authorizes the engine's whole canister-id range instead, which is why it is the right one for app code.
18. **Deleting a proxy that a signing app derives keys from.** The delete button refunds the remaining cycles, which makes it look like a tidy-up. It is not: threshold keys are derived from the proxy's own principal, so deleting it (or repointing the app at another proxy) changes every Bitcoin/Ethereum address the app owns and strands any funds at the old ones. See `cloud-engine-canisters` for the derivation rules before touching a proxy that an app already signs with.
19. **Confusing the three balances.** "The canister is out of cycles" means something different for each: an engine canister holds 0 cycles by design and cannot be topped up, a frozen *engine* is a subscription/emergency-reserve problem, and `InsufficientCycles` from a relayed call is the *proxy's* balance. Establish which one before topping anything up, and note that only the engine's emergency reserve running out is irreversible.

## Additional References

- Load `cloud-engine-canisters` for the call rules for code that runs on the engine: never attach cycles, bounded-wait cross-subnet calls, direct HTTPS outcalls, and the console proxy for cycle-bearing cross-subnet targets (XRC, threshold signing, vetKD). Load it before writing or debugging engine canister code.
- Load `icp-cli` for general icp CLI usage (`icp.yaml`, recipes, environments, bindings, identities). Load it for anything beyond this cloud-engine deploy flow — in particular when the project does not build or package yet.
- Load `internet-identity` for details of the Internet Identity sign-in that Step 1 triggers in the browser.
- Load `vetkeys` for what vetKD is and how VetKeys are used, once a proxy is in place: its call code targets a normal subnet, so see `cloud-engine-canisters` for the proxied form an engine needs.
- Load `cycles-management` for cycles on ordinary (non-engine) canisters: balances, freezing thresholds, and ICP-to-cycles conversion via the CMC.
