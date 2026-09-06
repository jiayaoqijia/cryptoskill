---
name: icp-cli
description: "Guides use of the icp command-line tool for building and deploying Internet Computer applications. Covers project configuration (icp.yaml), recipes, environments, canister lifecycle, identity management, and bundling a project into a self-contained .icp package (icp project bundle). Use when building, deploying, or managing any IC project. Use when the user mentions icp, dfx, canister deployment, local network, project setup, or bundling/packaging an app as an .icp file. Do NOT use for canister-level programming patterns like access control, inter-canister calls, or stable memory — use domain-specific skills instead."
license: Apache-2.0
metadata:
  title: ICP CLI
  category: Infrastructure
---

# ICP CLI

## What This Is

The `icp` command-line tool builds and deploys applications on the Internet Computer. It replaces the legacy `dfx` tool with YAML configuration, a recipe system for reusable build templates, and an environment model that separates deployment targets from network connections. Never use `dfx` — always use `icp`.

Before generating any `icp` command not explicitly documented here, run `icp --help` or `icp <subcommand> --help` to verify the command and its flags exist. Do not infer flags from `dfx` equivalents — the CLIs are not flag-compatible.

## Installation

```bash
npm install -g @icp-sdk/icp-cli @icp-sdk/ic-wasm
```

`ic-wasm` is required when using official recipes (`@dfinity/rust`, `@dfinity/motoko`, `@dfinity/static-site`, `@dfinity/asset-canister`) — they depend on it for optimization and metadata embedding. Requires [Node.js](https://nodejs.org/) >= 22. Also available via Homebrew and shell script installer — see the [icp-cli releases](https://github.com/dfinity/icp-cli/releases).

**Linux note:** On minimal installs, you may need system libraries: `sudo apt-get install -y libdbus-1-3 libssl3 ca-certificates` (Ubuntu/Debian) or `sudo dnf install -y dbus-libs openssl ca-certificates` (Fedora/RHEL).

## Prerequisites

- For Rust canisters: `rustup target add wasm32-unknown-unknown`
- For Motoko canisters: `npm i -g ic-mops` and a `mops.toml` at the project root with the Motoko compiler version and a `[canisters]` entry:
  ```toml
  [toolchain]
  moc = "1.9.0"

  [canisters.backend]
  main = "src/backend/main.mo"
  ```
  The `@dfinity/motoko@v5+` recipe compiles via `mops build <canister-name>`. The canister name in `icp.yaml` must exactly match a key in `[canisters]` — a missing or mismatched key causes `mops build` to fail with `No Motoko canisters found in mops.toml configuration` (see Pitfall 17). Without `mops.toml`, the recipe fails because `mops` is not found. Templates include `mops.toml` automatically; for manual projects, create it before running `icp build`. Load `mops-cli` for `[canisters]` configuration options, dependency management, and `mops build` details.

## Common Pitfalls

1. **Using `dfx` instead of `icp`.** The `dfx` tool is legacy. All commands have `icp` equivalents — see `references/dfx-migration.md` for the full command mapping. Never generate `dfx` commands or reference `dfx` documentation. Configuration uses `icp.yaml`, not `dfx.json` — and the structure differs: canisters are an array of objects, not a keyed object.

2. **Using `--network ic` to deploy to mainnet.** icp-cli uses environments, not direct network targeting. The correct flag is `-e ic` (short for `--environment ic`).
   ```bash
   # Wrong
   icp deploy --network ic
   # Correct
   icp deploy -e ic
   ```
   Note: `-n` / `--network` targets a network directly and works with canister IDs (principals). Use `-e` / `--environment` when referencing canisters by name. For token and cycles operations, use `-n` since they don't reference project canisters.

3. **Using a recipe without a version pin.** icp-cli rejects unpinned recipe references. Always include an explicit version. Official recipes are hosted at [dfinity/icp-cli-recipes](https://github.com/dfinity/icp-cli-recipes).
   ```yaml
   # Wrong — rejected by icp-cli
   recipe:
     type: "@dfinity/rust"

   # Correct — pinned version
   recipe:
     type: "@dfinity/rust@v3.3.0"
   ```

4. **Writing manual build steps when a recipe exists.** Official recipes handle Rust, Motoko, and asset canister builds. Use `recipe: { type: "@dfinity/rust@v3.3.0" }` instead of writing shell commands in `build.steps` — the Rust recipe defaults the Cargo `package` to the canister name, so no configuration is needed when they match (see Pitfall 21).

5. **Not committing `.icp/data/` to version control.** Mainnet canister IDs are stored in `.icp/data/mappings/<environment>.ids.json`. Losing this file means losing the mapping between canister names and on-chain IDs. Always commit `.icp/data/` — never delete it. Add `.icp/cache/` to `.gitignore` (it is ephemeral and rebuilt automatically). If you have environments using a connected network that gets reset frequently you can add those specific environment mapping files to .gitignore. **Never** add the entire `.icp` or `.icp/data` directory to gitignore.

6. **Using `icp identity use` instead of `icp identity default`.** The dfx command `dfx identity use <name>` became `icp identity default <name>` (setter). `icp identity default` with no argument is the getter — it prints the current default identity, equivalent to `dfx identity whoami`. The command `icp identity use` does not exist. Similarly, `dfx identity get-principal` became `icp identity principal`, and `dfx identity remove` became `icp identity delete`.

7. **Confusing networks and environments.** A network is a connection endpoint (URL). An environment combines a network + canisters + settings. You deploy to environments (`-e`), not networks. Multiple environments can target the same network with different settings (e.g., staging and production both on `ic`).

8. **Writing `networks` or `environments` as a YAML map instead of an array.** Both `networks` and `environments` are arrays of objects in `icp.yaml`, not maps:
   ```yaml
   # Wrong — map syntax
   networks:
     local:
       mode: managed
   environments:
     staging:
       network: ic

   # Correct — array syntax
   networks:
     - name: local
       mode: managed
   environments:
     - name: staging
       network: ic
       canisters: [backend, frontend]
   ```

9. **Forgetting that local networks are project-local.** Unlike dfx which runs one shared global network, icp-cli runs a local network per project. You must run `icp network start -d` in your project directory before deploying locally. The local network auto-starts with system canisters and seeds accounts with ICP and cycles. Stop it when done:
   ```bash
   icp network start -d  # start background network
   icp deploy            # build + deploy + sync
   icp network stop      # stop when done
   ```

10. **Not specifying build commands for a frontend canister.** dfx automatically runs `npm run build` for asset canisters. icp-cli requires explicit build commands in the recipe configuration:
    ```yaml
    canisters:
      - name: frontend
        recipe:
          type: "@dfinity/static-site@v0.3.3"   # recommended frontend recipe (certified-assets)
          configuration:
            dir: dist
            build:
              - npm install
              - npm run build
    ```

11. **Expecting `output_env_file` or `.env` with canister IDs.** dfx writes canister IDs to a `.env` file (`CANISTER_ID_BACKEND=...`) via `output_env_file`. icp-cli does not generate `.env` files. Instead, it injects canister IDs as environment variables (`PUBLIC_CANISTER_ID:<name>`) directly into canisters during `icp deploy`. Frontends read these from the `ic_env` cookie set by the frontend canister (static-site or the legacy asset canister). Remove `output_env_file` from your config and any code that reads `CANISTER_ID_*` from `.env` — frontends use the `ic_env` cookie, and canister code reads the same variables at runtime (see Canister Environment Variables below and Pitfall 22).

12. **Expecting `dfx generate` for TypeScript bindings.** icp-cli does not have a `dfx generate` equivalent. Use `@icp-sdk/bindgen` (>= 0.3.0) with `@icp-sdk/core` (>= 5.0.0 — there is no 0.x or 1.x release) to generate TypeScript bindings from `.did` files at build time. Use `outDir: "./src/bindings"` so imports are clean (e.g., `./bindings/backend`). The `.did` file must exist on disk — either commit it to the repo, or generate it with `icp build` first (recipes auto-generate it when `candid` is not specified). See `references/binding-generation.md` for the full Vite plugin setup.

13. **Passing `{ agent }` to `createActor` from `@icp-sdk/bindgen`.** The old `@dfinity/agent` pattern was `createActor(canisterId, { agent })`. The `@icp-sdk/bindgen` pattern is `createActor(canisterId, { agentOptions: { host, rootKey } })` — the binding creates the agent internally. Passing `{ agent }` to the new API **silently creates an anonymous identity** — no error is thrown, but calls return empty data or access denied. See `references/binding-generation.md` for the correct pattern.

14. **Mixing canister-level fields across config styles.** When using a recipe, the only valid canister-level fields are `name`, `recipe`, `sync`, `settings`, and `init_args`. Fields like `candid`, `build`, or `wasm` are **not** valid at canister level alongside a recipe — recipe-specific options go inside `recipe.configuration`. When using bare `build` (no recipe), valid canister-level fields are `name`, `build`, `sync`, `settings`, and `init_args`. The field `init_arg_file` does not exist — use `init_args.path` instead (e.g., `init_args: { path: ./args.bin, format: bin }`). For the authoritative field reference, consult the [icp-cli configuration reference](https://cli.internetcomputer.org/1.2/reference/configuration.md).
    ```yaml
    # Wrong — candid is not a canister-level field when using a recipe
    canisters:
      - name: backend
        candid: backend/backend.did
        recipe:
          type: "@dfinity/rust@v3.3.0"

    # Correct — candid goes inside recipe.configuration
    canisters:
      - name: backend
        recipe:
          type: "@dfinity/rust@v3.3.0"
          configuration:
            candid: backend/backend.did
    ```

15. **Placing `mops.toml` where `mops` cannot find it.** `mops` searches upward from the build working directory. Where to place `mops.toml` depends on how the canister is defined:
    - **Inline canisters** (defined directly in `icp.yaml`): build cwd is the project root. Place `mops.toml` at the project root next to `icp.yaml`. A `mops.toml` in `src/backend/` will not be found.
    - **Path-based canisters** (referenced via `canisters/*` or `./my-canister`, each with its own `canister.yaml`): build cwd is the canister directory. Place `mops.toml` in each canister's directory for per-canister dependencies and compiler versions, or omit it to fall back to a shared `mops.toml` in a parent directory.

    When `mops.toml` is not found, `mops build` fails because it cannot locate the project configuration. When `mops.toml` exists but is missing the matching `[canisters.<name>]` entry, see Pitfall 17.

16. **Misunderstanding Candid file generation with recipes.** Binding generation tools (e.g. `@icp-sdk/bindgen`) require a `.did` file at a known path on disk. Where to configure it depends on the recipe:

    **Rust** — `candid` goes inside `recipe.configuration` in `icp.yaml`:
    - If **specified**: the file must already exist. The recipe uses it as-is and does not generate one.
    - If **omitted**: the recipe auto-generates the `.did` via `candid-extractor` into the build cache (no predictable project path).

    To generate and commit it, then add `candid: backend/backend.did` inside `recipe.configuration`:
    ```bash
    cargo install candid-extractor  # one-time setup
    icp build backend
    candid-extractor target/wasm32-unknown-unknown/release/backend.wasm > backend/backend.did
    ```

    **Motoko (v5 recipe)** — `mops build` auto-generates the `.did` to `.mops/.build/<name>.did`.

    - **No binding generation needed** — nothing to do. The generated `.did` in `.mops/.build/` is sufficient; do not commit it.
    - **Binding generation needed** — generate a curated `.did` at a stable path with `mops generate candid`:
      ```bash
      mops generate candid backend
      ```
      This extracts the Candid interface directly from Motoko source **without compiling WASM**. With `[canisters.backend].candid` set in `mops.toml`, it overwrites that file; otherwise it writes `<name>.did` next to `main` (e.g. `main = "src/backend/main.mo"` → `src/backend/backend.did`) and records the path in `mops.toml`. Point the binding tool's config (e.g. `@icp-sdk/bindgen`'s `didFile`) at that `.did`. **Re-run after any interface change**, and commit the `.did` and `mops.toml` together. Load `mops-cli` for details. (The older `mops build backend` + `cp .mops/.build/backend.did …` two-step still works but builds the full WASM just to extract the interface.)

17. **Missing or mismatched `[canisters]` key in `mops.toml`.** The `@dfinity/motoko@v5+` recipe calls `mops build <canister-name>`, where the name comes from the `name` field in `icp.yaml`. `mops build` requires a matching `[canisters.<name>]` entry in `mops.toml`. If the entry is absent or the key does not exactly match (including casing), the build fails with:
    ```
    No Motoko canisters found in mops.toml configuration
    ```
    Add the matching entry — the key must equal the `name:` value in `icp.yaml`:
    ```toml
    [canisters.backend]
    main = "src/backend/main.mo"
    ```

18. **Port 8000 already in use when starting the local network.** Two scenarios:

    **Scenario A — another icp-cli project holds the port.** Stop that project's network using `--project-root-override` (a global flag available on all commands):
    ```bash
    icp network stop --project-root-override /path/to/other-project
    ```
    To run both networks at once instead of stopping one — e.g. parallel git worktrees — set `gateway.port: 0` so each gets a free port. See "Parallel local networks (git worktrees)" under How It Works.

    **Scenario B — a non-icp service holds the port.** Configure an alternate port in `icp.yaml` and read the actual URLs dynamically via `icp network status --json` rather than hardcoding localhost:8000:
    ```yaml
    networks:
      - name: local
        mode: managed
        gateway:
          port: 8001
    ```
    ```bash
    icp network status --json  # returns gateway URL, replica URL, etc.
    ```

19. **`icp new` hangs in CI without `--silent`.** Without `--define` flags, `icp new` launches an interactive prompt that blocks indefinitely in non-interactive environments. Always pass `--subfolder`, `--define`, and `--silent` for scripted use:
    ```bash
    icp new my-project --subfolder rust --define project_name=my-project --silent
    ```

20. **Using the anonymous identity on mainnet.** The local network seeds all managed identities — including the anonymous identity, which is the default — with ICP and cycles on start, so local development works out of the box with no identity or cycles setup required. On mainnet this does not apply, and the anonymous identity should never be used: it is shared by anyone, meaning ICP sent to it is publicly accessible and canisters deployed under it are uncontrolled.

    Before deploying to mainnet, switch to a named identity:
    ```bash
    icp identity list                                          # check available identities (`identity`, never `identities`)
    icp identity default my-identity                           # switch to an existing one
    # or: icp identity new my-identity && icp identity default my-identity
    ```
    Then verify it has funds — a new identity will need to be funded with ICP or cycles before proceeding:
    ```bash
    icp token balance -n ic    # check ICP balance on mainnet
    icp cycles balance -n ic   # check cycles balance on mainnet
    icp identity account-id    # get account ID to fund if needed
    ```

21. **Over-specifying (or wrongly omitting) `package` in the Rust recipe.** As of `@dfinity/rust@v3.3.0` the `package` config is **optional** and defaults to the canister `name` in `icp.yaml`. By convention, keep the canister `name` equal to the `[package] name` in `Cargo.toml` and omit `package` entirely:
    ```yaml
    # Preferred — name matches the Cargo package, so no package config
    canisters:
      - name: backend        # matches [package] name = "backend" in Cargo.toml
        recipe:
          type: "@dfinity/rust@v3.3.0"

    # Required only when the names differ (e.g. a workspace crate)
    canisters:
      - name: backend
        recipe:
          type: "@dfinity/rust@v3.3.0"
          configuration:
            package: my-project-backend   # actual [package] name in Cargo.toml
    ```
    Omitting `package` when the names **differ** causes `cargo build` to fail with a package-not-found error — set it to the exact `[package] name`. On recipe versions before `v3.3.0`, `package` was required in all cases.

22. **Hand-wiring canister IDs with setter methods or deploy scripts.** Controller-only setters (`setBridge(principal)`) called by a post-deploy script — or sibling IDs hardcoded in `settings.environment_variables` or init args — are unnecessary: `icp deploy` injects every canister's ID into every canister's settings as `PUBLIC_CANISTER_ID:<canister-name>`, readable by canister code at runtime with the correct per-environment value (see Canister Environment Variables). Setter wiring is also more fragile: a `--mode reinstall` silently wipes the stored pointer, while the automatic variables are re-stamped on every deploy.

## How It Works

### Project Creation

`icp new` scaffolds projects from templates. Pass `--subfolder`, `--define`, and `--silent` for non-interactive use:
```bash
icp new my-project --subfolder rust --define project_name=my-project --silent
```
Available templates and options: [dfinity/icp-cli-templates](https://github.com/dfinity/icp-cli-templates).

### Build → Deploy → Sync

```text
Source Code → [Build] → WASM → [Deploy] → Running Canister → [Sync] → Configured State
```

`icp deploy` runs all three phases in sequence:
1. **Build** — Compile canisters to WASM (via recipes or explicit build steps)
2. **Deploy** — Create canisters (if new), apply settings, install WASM
3. **Sync** — Post-deployment operations via `script` or `plugin` steps (e.g., uploading assets). Asset uploading is not built into the CLI: a frontend recipe supplies a `plugin` sync step that uploads the `dir` contents — the recommended `@dfinity/static-site@v0.3.3` (certified-assets) or the legacy `@dfinity/asset-canister@v2.2.1`. The legacy built-in `type: assets` step is removed in icp-cli 0.3.0 — see the `static-site` skill.

Run phases separately for more control:
```bash
icp build                     # Build only
icp deploy                    # Full pipeline (build + deploy + sync)
icp sync my-canister          # Sync only (e.g., re-upload assets)
```

### Environments and Networks

Two implicit environments are always available:

| Environment | Network | Purpose |
|-------------|---------|---------|
| `local` | `local` (managed, localhost:8000) | Local development |
| `ic` | `ic` (connected, https://icp-api.io) | Mainnet production |

The `ic` network is protected and cannot be overridden.

Custom environments enable multiple deployment targets on the same network:

```yaml
environments:
  - name: staging
    network: ic
    canisters: [frontend, backend]
    settings:
      backend:
        compute_allocation: 5

  - name: production
    network: ic
    canisters: [frontend, backend]
    settings:
      backend:
        compute_allocation: 20
        freezing_threshold: 7776000
```

### Parallel local networks (git worktrees)

Local networks are project-local — keyed by project root (Pitfall 9). Separate git worktrees of the same repo are separate project roots, so each worktree can run its own independent local network. This lets multiple agents or branches build and deploy in parallel without interfering. The only obstacle is the gateway port: every worktree defaults to `8000`, so the second `icp network start` fails with a port conflict.

Set the managed network's gateway port to `0` so the OS assigns a free ephemeral port per worktree:

```yaml
networks:
  - name: local
    mode: managed
    gateway:
      port: 0   # 0 = OS picks a free port — avoids collisions across worktrees
```

`icp network start -d` prints the chosen port (`Network started on port 58157`). To recover it afterward — for tests, scripts, or another agent — query the running network and read `gateway_url`:

```bash
icp network start -d
icp network status --json
# -> { "managed": true, "api_url": "http://localhost:58157/", "gateway_url": "http://localhost:58157/", ... }

icp network status --json | jq -r '.gateway_url'   # http://localhost:58157/
```

Never hardcode `localhost:8000` when using `port: 0` — the port changes on every start, so read `gateway_url` (or `api_url`) from `icp network status --json` each time. To target a specific worktree's network from outside its directory, pass the global `--project-root-override <path>` flag (e.g. `icp network status --json --project-root-override /path/to/worktree`).

### Install Modes

```bash
icp deploy                    # Auto: install new, upgrade existing (default)
icp deploy --mode upgrade     # Preserve state, run upgrade hooks
icp deploy --mode reinstall   # Clear all state (dangerous)
```

### Bundling a project into an `.icp` package (experimental)

`icp project bundle` (icp-cli >= 0.3.0) packages a project into a self-contained deployable archive. **This is an experimental feature, intentionally hidden from help output** — `icp --help` and `icp project --help` do not list it, but the command exists and works. Do not conclude it doesn't exist because help omits it, and do not suggest it proactively — use it only when the user explicitly asks to bundle an app or produce an `.icp` package.

```bash
icp project bundle --output my-app.icp
```

The output is a gzipped tar archive; `--output` accepts any path (`my-app.icp` and `bundle.tar.gz` are both common). The bundle contains the built WASMs and a rewritten `icp.yaml`:

- All canisters are built first; each canister's build steps are replaced with a prebuilt step referencing the bundled WASM (`canisters/<name>.wasm`), pinned by sha256.
- Plugin sync steps (e.g. the asset canister's upload plugin) are preserved — the plugin WASM and its `dirs`/`files` inputs are copied into the archive.
- Network and environment manifests referenced by path are inlined; `init_args` files are copied into the archive.
- An optional `icp_appmanifest.yaml` (app metadata) is included, with its `screenshots` paths relocated into the archive.

To deploy from a bundle, extract it and run `icp deploy` from the extracted directory — no build toolchain (Rust, mops, npm) is required because every build step is prebuilt:

```bash
mkdir app && tar -xzf my-app.icp -C app
cd app && icp deploy -e <environment>
```

An `.icp` package can also be uploaded to a Caffeine cloud engine via the console's App Center ("Upload a custom app") — see the `deploy-to-cloud-engine` skill.

Bundling fails when:

- A canister has a `script` sync step — only `plugin` sync steps can be replayed from a bundle (`canister 'X' has a script sync step, which is not supported in bundles`).
- Any synced directory, plugin file, `init_args` file, or screenshot resolves outside the project directory.
- The `--output` path is inside a directory the bundle would sync (the partial archive would include itself).
- A managed network defines a bind mount with an absolute host path — bundles require relative paths for portability.

## Configuration

### Rust canister

```yaml
canisters:
  - name: backend
    recipe:
      type: "@dfinity/rust@v3.3.0"
      configuration:
        candid: backend.did  # optional — if specified, file must exist (auto-generated when omitted)
        # package: my-crate  # optional — only when the Cargo [package] name differs from the canister name
```

By convention the canister `name` must match the `[package] name` in `Cargo.toml`. When they match, `package` is optional (recipe >= v3.3.0 defaults it to the canister name). Set `package` explicitly only when the Cargo package name differs — e.g. a workspace with a differently named crate (see Pitfall 21).

### Motoko canister

The v5 recipe delegates compilation to `mops build`. Canister configuration (`main`, `candid`, `args`) moves from `icp.yaml` to `mops.toml`:

```yaml
# icp.yaml
canisters:
  - name: backend
    recipe:
      type: "@dfinity/motoko@v5.0.0"
```
```toml
# mops.toml
[toolchain]
moc = "1.9.0"

[canisters.backend]
main = "src/backend/main.mo"
candid = "backend.did"  # optional — auto-generated to .mops/.build/ when omitted
```

The canister name (`backend`) must exactly match between `icp.yaml` and `mops.toml`. No `recipe.configuration` block is needed in `icp.yaml`.

### Static site (frontend)

```yaml
canisters:
  - name: frontend
    recipe:
      type: "@dfinity/static-site@v0.3.3"
      configuration:
        dir: dist
        build:
          - npm install
          - npm run build
```

`@dfinity/static-site` (the certified-assets canister) is the recommended frontend recipe. The legacy `@dfinity/asset-canister@v2.2.1` recipe is still supported for existing projects — see the `static-site` skill for both and for migration.

For multi-canister projects, list all canisters in the same `canisters` array. icp-cli builds them in parallel. There is no `dependencies` field — use Canister Environment Variables for inter-canister communication.

### Custom build steps (no recipe)

When not using a recipe, only `name`, `build`, `sync`, `settings`, and `init_args` are valid canister-level fields. There are no `wasm`, `candid`, or `metadata` fields — handle these in the build script instead:

- **WASM output**: copy the final WASM to `$ICP_WASM_OUTPUT_PATH`
- **Candid metadata**: use `ic-wasm` to embed `candid:service` metadata
- **Candid file**: the `.did` file is referenced only in the `ic-wasm` command, not as a YAML field

```yaml
canisters:
  - name: backend
    build:
      steps:
        - type: script
          commands:
            - cargo build --target wasm32-unknown-unknown --release
            - cp target/wasm32-unknown-unknown/release/backend.wasm "$ICP_WASM_OUTPUT_PATH"
            - ic-wasm "$ICP_WASM_OUTPUT_PATH" -o "$ICP_WASM_OUTPUT_PATH" metadata candid:service -f backend/backend.did -v public --keep-name-section
```

### Available recipes

| Recipe | Type string | Required config | Optional config |
|--------|------------|-----------------|-----------------|
| Rust | `@dfinity/rust@v3.3.0` | — | `package` (defaults to canister name), `candid`, `locked`, `shrink`, `compress`, `metadata` |
| Motoko | `@dfinity/motoko@v5.0.0` | — | `shrink`, `compress`, `metadata` |
| Static site (frontend) | `@dfinity/static-site@v0.3.3` | `dir` | `build`, `presync`, `metadata` |
| Asset (legacy frontend) | `@dfinity/asset-canister@v2.2.1` | `dir` | `build`, `version` |
| Prebuilt | `@dfinity/prebuilt@v2.1.0` | `path` | `sha256`, `shrink`, `compress`, `metadata` |

`@dfinity/static-site` is the recommended way to host a frontend; `@dfinity/asset-canister` is the legacy asset canister (see the `static-site` skill).

Verify latest recipe versions at [dfinity/icp-cli-recipes releases](https://github.com/dfinity/icp-cli-recipes/releases). Use `icp project show` to see the effective configuration after recipe expansion.

### Canister Environment Variables

During `icp deploy`, icp-cli injects the ID of **every canister in the environment** into **every canister's settings** as `PUBLIC_CANISTER_ID:<canister-name>` (the principal in text form). These are canister *settings* env vars, readable **at runtime by canister code**, with per-environment values refreshed on every deploy — the same code is correct on local, staging, and mainnet with zero configuration.

**Use these for inter-canister wiring** instead of setter methods, init args, or post-deploy scripts (Pitfall 22). Read them lazily at call time — Motoko: `Runtime.envVar<system>(...)` (motoko-core v2.1.0+), Rust: `ic_cdk::api::env_var_value(...)` — see `references/canister-env-vars.md` for code and the first-install/reinstall behavior.

**Frontend** (JavaScript): the frontend canister (static-site or the legacy asset canister) exposes the variables through the `ic_env` cookie, set on all HTML responses. Read it with `@icp-sdk/core`:
```js
import { safeGetCanisterEnv } from "@icp-sdk/core/agent/canister-env";

const backendId = safeGetCanisterEnv()?.["PUBLIC_CANISTER_ID:backend"];
```

**Caveats:**

- Variables are only updated at deploy time. After adding a canister, run `icp deploy` (without a canister name) so every canister gets the complete ID set.
- User-defined variables (`settings.environment_variables` in `icp.yaml`) are static YAML strings shared across environments: a create-class install (first install or `--mode reinstall`) re-applies them, overwriting anything set with `icp canister settings update --add-environment-variable`. Re-assert environment-specific values (e.g. production origins) after such a deploy.
- The replica caps an environment-variable *value* at 128 characters.

Full reference: [icp-cli environment variables](https://cli.internetcomputer.org/1.2/reference/environment-variables/).

### Web identity flows

Two specialized skills cover `icp identity link web`. Load the right one for the task — both document the stdin "Press Enter" block, the browser sign-in step, and their flag-specific pitfalls:

- `deploy-to-cloud-engine` — link the CLI to a cloud engine console with `--auth <console-origin>`, then deploy to the engine's subnet
- `agent-web-identity` — obtain a delegation for an app-specific principal with `--app <domain>`, then make canister calls as the user

## Additional References

For the complete CLI and configuration schema, consult the [icp-cli documentation index](https://cli.internetcomputer.org/llms.txt).

For detailed guides on specific topics, consult these reference files when needed:

- **`references/binding-generation.md`** — TypeScript binding generation with `@icp-sdk/bindgen` (Vite plugin, CLI, actor setup)
- **`references/canister-env-vars.md`** — reading `PUBLIC_CANISTER_ID:<name>` from canister code at runtime (Motoko/Rust examples, lazy-read pattern)
- **`references/dev-server.md`** — Vite dev server configuration to simulate the `ic_env` cookie locally. Important: wrap `getDevServerConfig()` in a `command === "serve"` guard so it only runs during `vite dev`, not `vite build`.
- **`references/dfx-migration.md`** — Complete dfx → icp migration guide (command mapping, config mapping, identity/canister ID migration, frontend package migration, post-migration verification checklist)
