---
name: caffeine-app
description: "Scaffold and build a complete Caffeine app (caffeine.ai) from scratch — the project layout, the caffeine.toml workspace + canister manifests, the mops.toml for the single Motoko `backend` canister, the React/Vite frontend, and the caffeine CLI build loop (auth login, doctor, install, check --fix, preview --build). Use whenever the user wants to create, scaffold, set up, or build a Caffeine app or a caffeine.ai project, asks about caffeine.toml or mops.toml structure, or needs the caffeine CLI workflow — even if they do not say the words 'from scratch'. Always pair it with the `writing-motoko` skill for the backend code. Do NOT use it for Motoko language syntax or compiler errors (use the `writing-motoko` skill), and do NOT use it for generic Internet Computer / dfx / icp deployment (use the `icp-cli` skill)."
license: Apache-2.0
compatibility: "@caffeineai/cli (the `caffeine` command), Node.js >= 20.19, pnpm, mops >= 3.0.0, network access + a caffeine.ai account"
metadata:
  title: "Caffeine App (build from scratch)"
  category: Integration
---

# Caffeine App (build from scratch)

Caffeine (caffeine.ai) builds and hosts full-stack apps on the Internet Computer: a
single **Motoko backend canister** plus a **React/Vite frontend** served as an assets
canister. This skill teaches the exact **project shape** and the **CLI build loop** so
you can produce a buildable Caffeine app from nothing.

**This skill owns the project shape and the build workflow. It does NOT own the Motoko
language.** Before you write or edit any backend code, fetch and follow the `writing-motoko`
skill: <https://skills.internetcomputer.org/skills/writing-motoko/SKILL.md>. That skill is
authoritative for actor syntax, stable state, `mo:core`, and compiler errors. This
skill only shows the minimal empty actor and where it lives.

## When to use this skill

- Creating/scaffolding a new Caffeine app or caffeine.ai project from scratch.
- Writing or fixing `caffeine.toml` (workspace or canister manifest) or `mops.toml`.
- Running the caffeine CLI loop: `auth login`, `doctor`, `install`, `check`, `preview`.

Do **not** use it for Motoko language details (use `writing-motoko`) or for raw IC/`dfx`/`icp`
deployment (use `icp-cli`). Caffeine apps are built and deployed through the `caffeine`
CLI and the caffeine.ai web app, **not** through `dfx`.

## Critical facts

- **There is no `caffeine init` / `caffeine new`.** "From scratch" means you create the
  files in this skill by hand, then run the build loop. (`caffeine projects clone <id>`
  only downloads an *existing* cloud project, and `caffeine projects import <zip>` only
  unpacks a project archive such as one made by `caffeine export`; neither is a
  greenfield scaffold.)
- **Exactly one backend canister, and it must be named `backend`.** `mops.toml` declares
  a single `[canisters.backend]`.
- **The frontend↔backend binding files are generated, never hand-written.**
  `src/frontend/src/backend.ts` and `src/frontend/src/declarations/` are produced by
  `caffeine-bindgen` during the build. Editing them is pointless — they are overwritten.
- **Deploying to a live URL is done in the caffeine.ai web app, not the CLI.** The CLI
  takes you as far as a built **draft** (`caffeine preview --build`, which needs a cloud
  `project.id` — see the build loop). There is no `caffeine deploy`/`publish` command.

## Prerequisites (run once)

```bash
# Install the CLI (public npm package). The binary is `caffeine`.
npm install -g @caffeineai/cli

# Authenticate against caffeine.ai. Opens a browser; without one (or with --device) it
# uses the device flow. On a host with no OS keychain (headless Linux, containers), add
# --insecure-storage to keep the token in ~/.caffeine/tokens.json (mode 0600) instead.
caffeine auth login
caffeine auth status

# Check the environment: Node, pnpm, mops, caffeine-bindgen, that you are logged in,
# and that the Caffeine API is reachable (installs what it can).
caffeine doctor --fix
```

If a global install is undesirable or fails, run every `caffeine` command through an
`npx -y @caffeineai/cli@latest` prefix instead — e.g. `npx -y @caffeineai/cli@latest auth status`.

`caffeine doctor` requires Node.js 20 or later (the template's `engines` field asks for
`>=20.19.0`) and checks pnpm, mops (2.13.0 or later), `caffeine-bindgen`, your login,
and whether the Caffeine API is reachable. With `--fix` it installs a missing pnpm, a
missing or outdated mops (`ic-mops`), and a missing `caffeine-bindgen`
(`@caffeineai/bindgen`) with `npm install -g`; it does not install Node.js. It does
**not** install the Motoko compiler (`moc`) or linter (`lintoko`): mops fetches those
automatically from the `[toolchain]` pins in `mops.toml`. On Windows, compiling Motoko
requires WSL. `dfx` is not part of the Caffeine build.

## Project shape

A Caffeine app is a pnpm workspace with a root manifest and two canisters. Create this
exact tree (file contents below):

```text
my-app/
├── .old/src/backend/dist/
│   └── backend.most           # stable-signature baseline — seed with an empty actor (see below)
├── caffeine.toml              # root workspace manifest — MUST contain [workspace]
├── mops.toml                  # Motoko build config — ONE per project, at the root
├── package.json               # pnpm workspace root + the `bindgen` script
├── pnpm-workspace.yaml         # declares src/**/* as workspace packages
├── tsconfig.json               # root TS config
└── src/
    ├── backend/                # the single Motoko canister, named "backend"
    │   ├── caffeine.toml        #   canister manifest: type = "motoko"
    │   ├── main.mo              #   actor entry point (write with the `writing-motoko` skill)
    │   └── migrations/          #   enhanced-migration chain (see the `mops.toml` notes)
    │       └── 00000000_000000.mo #   first migration: initializes the actor's stable state
    └── frontend/               # the assets canister (React + Vite)
        ├── caffeine.toml        #   canister manifest: type = "assets"
        ├── package.json         #   frontend deps + scripts (see references/frontend-template.md)
        ├── vite.config.js       #   (see references/frontend-template.md)
        ├── tsconfig.json        #   (see references/frontend-template.md)
        ├── biome.json           #   (see references/frontend-template.md)
        ├── tailwind.config.js   #   (see references/frontend-template.md)
        ├── postcss.config.js    #   (see references/frontend-template.md)
        ├── index.html
        ├── env.json             #   runtime config — copied into dist/ on build
        ├── public/              #   static files served as-is (for example favicon.ico)
        └── src/
            ├── main.tsx          #   React entry (providers)
            ├── App.tsx
            ├── index.css
            ├── backend.ts        #   GENERATED by caffeine-bindgen — do NOT edit
            └── declarations/     #   GENERATED by caffeine-bindgen — do NOT edit
```

Only the **root** manifest, the two **canister** manifests, `mops.toml`, `main.mo`, and
the small root config files are shown inline below. The full frontend boilerplate
(`package.json`, `vite.config.js`, the Tailwind/PostCSS/Biome configs, `index.html`,
`env.json`, `main.tsx`, a starter `App.tsx`) is in
[`references/frontend-template.md`](references/frontend-template.md) — read it when you
create the frontend.

## Manifests

### Root `caffeine.toml` — the workspace

The root manifest **must** contain a `[workspace]` section. That section is what marks
it as the workspace root; without it, the CLI treats this file as an ordinary canister
manifest and discovery fails.

```toml
manifest_version = "0.1.0"

[project]
name = "My App"
# id is the cloud project id, a UUID. Omit it for a brand-new local project; once
# `caffeine projects create` reports one, set it here (or pass --project-id to preview).
# A placeholder such as "my-app" makes `caffeine preview` refuse to upload.

[workspace]
include = [ "src/**" ]

# Build the backend before the frontend, because the frontend imports generated
# bindings produced from the backend's Candid interface.
[canisters.frontend]
depends_on = [ "backend" ]
```

`[workspace].include` is a list of globs the CLI scans for nested canister manifests.
`src/**` finds `src/backend/caffeine.toml` and `src/frontend/caffeine.toml`.

### `src/backend/caffeine.toml` — the Motoko canister

```toml
manifest_version = "0.1.0"

[project]
name = "backend"
type = "motoko"
main = "main.mo"

[build]
commands = ["mops build", "pnpm bindgen"]
out = "dist"

[check]
commands = ["mops check"]

[check.fix]
commands = ["mops check --fix"]
```

`[build].commands` run in order: `mops build` compiles `main.mo` to Wasm + Candid, then
`pnpm bindgen` (defined in the root `package.json`) turns that Candid into the frontend's
TypeScript client. `caffeine check --fix` runs `[check.fix].commands`.

### `src/frontend/caffeine.toml` — the assets canister

```toml
manifest_version = "0.1.0"

[project]
name = "frontend"
type = "assets"

[build]
commands = ["pnpm build"]
out = "dist"

[check]
commands = ["pnpm typecheck", "pnpm check"]

[check.fix]
commands = ["pnpm typecheck", "pnpm fix"]
```

### `mops.toml` — the Motoko build (one per project, at the root)

There is exactly **one** `[canisters.backend]`. `caffeine preview` checks only the
structural pieces, which are invariant: the single `[canisters.backend]`,
`[canisters.backend.check-stable]` with the path shown and no `skipIfMissing`, and
`[build] outputDir = "src/backend/dist"`. Everything else — the **toolchain versions, the
`[moc]` flags and `-E`/`-W`/`-A` diagnostic codes, and the dependency list — is a current
snapshot** that the Caffeine template bumps over time; see "Versions and dependencies
drift" below.

```toml
[package]
name = "backend"
version = "0.1.0"

[build]
outputDir = "src/backend/dist"
args = ["--release"]
check-wasm = true

[canisters.backend]
main = "src/backend/main.mo"

[canisters.backend.check-stable]
path = ".old/src/backend/dist/backend.most"

[toolchain]
moc = "2.1.0"
lintoko = "0.12.0"

[lint]
extends = true

[moc]
args = [
  "--implicit-package=core",
  "-no-check-ir",
  "-E=M0254",
  "-W=M0235,M0223,M0236,M0237",
  "-A=M0241"
]

[dependencies]
core = "2.6.1"
ic = "5.0.0"
caffeineai-authorization = "1.0.0"
caffeineai-lints = "0.1.0"
caffeineai-oql = "0.8.0"

[canisters.backend.migrations]
chain = "src/backend/migrations"
check-limit = 1
```

Notes:

- **New projects use moc 2.** Under moc 2 a bare `actor` is persistent, and the
  `persistent` keyword only triggers warning M0217. Older guides add
  `--default-persistent-actors` or `--generate-view-queries` to `[moc] args`: those are
  moc 1.x flags that moc 2.0 removed, and passing them fails every compile with
  `unknown option`. Projects cloned from before the switch may still pin moc 1.x
  (the template's moc 1 variant is `moc = "1.16.0"` with `--default-persistent-actors`
  first in `[moc] args`); leave such a project on its pinned version, or move it with the
  `migrating-to-moc-2` skill:
  <https://github.com/caffeinelabs/skills/tree/main/skills/migrating-to-moc-2>.
- **`check-stable`** points at `.old/src/backend/dist/backend.most`, the stable-signature
  snapshot of the last deployed backend. `caffeine check` compares your stable state
  against it, and `caffeine projects clone` restores it from the cloud. Do not delete
  `.old/`. **A from-scratch project must seed it** with an empty actor, as the Caffeine
  template does, or `caffeine check` fails with
  `Deployed file not found: .old/src/backend/dist/backend.most`:

  ```motoko
  // Version: 1.0.0
  actor {};
  ```

  Do not set `skipIfMissing = true` instead: mops deprecated it, and `caffeine preview`
  rejects it because a skipped check only fails later, at deploy.
- **`[canisters.backend.migrations]`** turns on enhanced migration (mops adds
  `--enhanced-migration` itself; do not put it in `[moc] args`). Every `.mo` file in
  `src/backend/migrations/`, in name order, is one step that maps the previous stable
  state to the next. Stable fields in the actor have **no initializers**; their initial
  values come from the chain. A new project starts with `00000000_000000.mo`, which
  creates the state the starting `main.mo` declares (below) and sorts before the
  `YYYYMMDD_HHMMSS.mo` files later migrations use:

  ```motoko
  import AccessControl "mo:caffeineai-authorization/access-control";

  module {
    public type OldActor = {};
    public type NewActor = { accessControlState : AccessControl.AccessControlState };

    public func migration(_ : OldActor) : NewActor {
      { accessControlState = AccessControl.initState() };
    };
  };
  ```

  `check-limit = 1` allows **one pending (not yet deployed) migration**. Against the seeded
  empty baseline, `00000000_000000.mo` is itself pending, so until the first deploy you add
  new stable fields by editing that file, not by adding a second one; a second file fails
  `caffeine check` with `too many pending migrations for check-limit=1`. Never edit,
  rename, or delete a migration after it is deployed. The rules for writing migrations
  are in the `migrating-motoko-actors` skill:
  <https://github.com/caffeinelabs/skills/tree/main/skills/migrating-motoko-actors>.
- **`core`** is the `mo:core` standard library. Use `mo:core`, never the deprecated
  `mo:base` — see the `writing-motoko` skill. **`caffeineai-oql`** provides the `Expose` mixin the
  starting `main.mo` includes (below).
- **`caffeineai-authorization`** provides Internet Identity sign-in and roles
  (`MixinAuthorization`, `AccessControl`). It also ships a lint rule that fails
  `caffeine check` unless `main.mo` includes `MixinAuthorization`. To use custom
  authentication instead before the first deploy, remove the package
  (`mops remove caffeineai-authorization`) together with its imports, include, state
  field, and migration line — see the `extension-authorization` skill:
  <https://github.com/caffeinelabs/skills/tree/main/skills/extension-authorization>.
  After a deploy, the applied first migration imports the package, so removing it
  breaks the build: keep the package and `MixinAuthorization`, and add custom checks
  alongside them.
- **`[lint] extends = true`** runs the lint rules that dependencies ship (such as the one
  above) with the `lintoko` pinned in `[toolchain]`, as part of `mops check`.
- **`ic`** provides the IC management canister's types and calls (`mo:ic/Types`,
  `mo:ic/Call`). Use it instead of `import ... "ic:aaaaa-aa"`, which only resolves with an
  `--actor-idl` flag that the template no longer passes.
- **Add a package** with `mops add <name>` (one package per command) rather than by
  editing `[dependencies]`, so `mops.lock` stays in sync. The `mops-cli` skill covers the
  mops commands: <https://github.com/caffeinelabs/skills/tree/main/skills/mops-cli>.

> **Versions and dependencies drift.** The `[toolchain]` versions, the `[moc]`
> `-E`/`-W`/`-A` codes, and the frontend dependency set are template-managed and change
> over time (e.g. the `@dfinity/*` → `@icp-sdk/*` migration, moc/core bumps). Treat the
> exact values here as a snapshot — for current ones, `caffeine projects clone` a recent
> project and copy its `mops.toml` + `src/frontend/package.json`. Stable across versions:
> the file layout, the single `backend` canister, `check-stable` with the seeded
> baseline, `[build] outputDir`, `mo:core`, and `useActor(createActor)`.

### `package.json` (root) — pnpm workspace + the `bindgen` script

The `bindgen` script is the bridge from backend Candid to the frontend TS client. It is
invoked by the backend canister's `[build]` step (`pnpm bindgen`).

```json
{
  "name": "@caffeine/template-app",
  "type": "module",
  "engines": {
    "node": ">=20.19.0",
    "pnpm": ">=7.0.0",
    "npm": "please use pnpm"
  },
  "scripts": {
    "build": "pnpm -r --if-present run build",
    "typecheck": "pnpm -r --if-present run typecheck",
    "check": "pnpm -r --if-present run check",
    "fix": "pnpm -r --if-present run fix",
    "bindgen": "caffeine-bindgen --did-file ./src/backend/dist/backend.did --out-dir ./src/frontend/src --actor-interface-file --force"
  },
  "devDependencies": {
    "@icp-sdk/core": "^5.3.0",
    "sharp": "^0.34.4"
  }
}
```

The Caffeine template also pins pnpm with a `packageManager` field and adds
`@dfinity/pic` for its hosted backend tests; a local project needs neither.

### `pnpm-workspace.yaml`

pnpm 10 reads `onlyBuiltDependencies`; pnpm 11 and later read only `allowBuilds`. Keep
both so either version runs the packages' install scripts.

```yaml
packages:
  - src/**/*
allowBuilds:
  '@biomejs/biome': true
  esbuild: true
  sharp: true
onlyBuiltDependencies:
  - '@biomejs/biome'
  - esbuild
  - sharp
```

### `tsconfig.json` (root)

```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2020",
    "experimentalDecorators": true,
    "strictPropertyInitialization": false,
    "module": "esnext",
    "moduleResolution": "bundler",
    "allowJs": true,
    "outDir": "HACK_BECAUSE_OF_ALLOW_JS"
  }
}
```

### `src/backend/main.mo` — the starting backend

The canonical template's starting `main.mo` includes two mixins: **`MixinAuthorization`**
from `caffeineai-authorization`, which provides Internet Identity sign-in and roles (the
first user to sign in becomes admin), and **`Expose`** from `caffeineai-oql`, which
publishes the backend's query interface. `accessControlState` is a stable field with no
initializer; `00000000_000000.mo` gives it its value. Add your own functions inside the
actor, following the **`writing-motoko` skill**.

```motoko
import AccessControl "mo:caffeineai-authorization/access-control";
import MixinAuthorization "mo:caffeineai-authorization/MixinAuthorization";
import Expose "mo:caffeineai-oql/Expose";

actor {
  let accessControlState : AccessControl.AccessControlState;
  include MixinAuthorization(accessControlState, null);
  include Expose({ entities = [] });
};
```

To guard methods by role, store user profiles, or capture verified names and emails at
sign-in, follow the `extension-authorization` skill.

Do not write more Motoko than this without loading
the `writing-motoko` skill — it covers persistent actors, stable types, `mo:core`, and the
compiler-error pitfalls that an agent will otherwise hallucinate.

## The frontend

**Fetch this skill's companion reference file** —
[`references/frontend-template.md`](references/frontend-template.md), which sits next to
this `SKILL.md` (i.e. `…/skills/caffeine-app/references/frontend-template.md`) — and create
the frontend files from it; it holds the verified `package.json`, the Vite/Tailwind/Biome
configs, `main.tsx`, and the worked `useActor(createActor)` backend call. The essentials:

- The entry point `src/frontend/src/main.tsx` wraps the app in
  `InternetIdentityProvider` (from `@caffeineai/core-infrastructure`) and a TanStack
  `QueryClientProvider`.
- The frontend talks to the backend through the **generated** module
  `src/frontend/src/backend.ts` (and `src/frontend/src/declarations/`), which exports a
  `createActor(...)` factory typed from your backend's Candid. You do not write these —
  they appear after the first build. Call the backend by passing that `createActor` to
  `useActor(createActor)` from `@caffeineai/core-infrastructure` (the same package provides
  the auth provider used in `main.tsx`); you do **not** hand-write the actor/config/storage
  glue. See the worked example in
  [`references/frontend-template.md`](references/frontend-template.md).
- Sign-in uses `useInternetIdentity()` from the same package (`login()` from a button's
  `onClick`, `clear()`, `isAuthenticated`, and Google, Microsoft, or company SSO
  variants). `useActor` re-creates the actor with the signed-in identity. The hook's full
  API and the sign-in UI rules are in the `extension-core-infrastructure` skill:
  <https://github.com/caffeinelabs/skills/tree/main/skills/extension-core-infrastructure>.
- `env.json` holds runtime config placeholders (`backend_host`, `backend_canister_id`,
  `project_id`, `ii_derivation_origin`, `storage_gateway_url`), all `"undefined"` locally;
  the frontend `build` script copies it into `dist/` (`cp env.json dist/`), and
  `@caffeineai/core-infrastructure` fetches it at runtime. Caffeine injects real values
  when it serves the app. Keep `env.json` and the `copy:env` step.

## The build loop

Run from the project root. Order matters.

```bash
# 1. Install dependencies. On a brand-new project, generate the pnpm lockfile FIRST
#    (first run only — see Common Pitfalls), then install the rest (pnpm + mops).
pnpm install
caffeine install

# 2. Write your backend in src/backend/main.mo using the `writing-motoko` skill, and your
#    frontend in src/frontend/src/.

# 3. Build: compiles the backend, then `pnpm bindgen` regenerates the frontend client
#    (src/frontend/src/backend.ts + declarations/), then the frontend `pnpm build` runs.
#    Run this BEFORE check, so the frontend has the generated ./backend to typecheck
#    against. Artifacts land in src/backend/dist + src/frontend/dist (no cloud / no id).
caffeine build

# 4. Lint + typecheck + auto-fix (runs each canister's [check.fix] commands:
#    backend `mops check --fix`, frontend `pnpm typecheck` + `pnpm fix`).
caffeine check --fix

# 5. Upload a built draft (needs a cloud project id). For a brand-new app, create the
#    cloud project once to obtain an id, then preview:
caffeine projects create                 # reports a new project id
#    put that id in caffeine.toml [project] id = "...", OR pass --project-id:
caffeine preview --build --project-id <id>
```

`caffeine preview` refuses to upload when sources changed since the last `caffeine build`;
`--build` rebuilds first. It also checks the `mops.toml` structure described above and
needs `src/backend/dist/backend.wasm` and `src/frontend/dist/index.html`. Do not
`caffeine projects clone` a project you just created: it has no code yet, so the clone
fails with `No committed draft found`.

Set `CAFFEINE_VERBOSE=1` to stream complete subprocess output from `caffeine install`,
`caffeine build`, and `caffeine check`. This is equivalent to passing `--verbose` to
each command. `--json` continues to suppress streamed output.

Without a TTY (an agent's shell, CI, piped output) progress and results print as plain
lines. Add `--json` to any command for a machine-readable `{ "ok": true, "data": ... }` or
`{ "ok": false, "error": ... }` envelope.

**Generation ordering.** `src/frontend/src/backend.ts` does not exist until a build runs
`pnpm bindgen`. So if your frontend imports from `./backend`, you must run `caffeine build`
at least once before `caffeine check` can typecheck the frontend. A brand-new app whose
`App.tsx` does not yet import `./backend` typechecks fine before the first build.

**Going live.** `caffeine preview --build` (with a `project.id`) produces a *draft* and
returns its URL. Promote a draft to a live URL in the caffeine.ai web app (open it with
`caffeine chat open` or visit caffeine.ai), or with the `caffeine_go_live` tool of the
Caffeine MCP connector. There is no CLI deploy command. Use
`caffeine projects show <id>` to see draft and live URLs, and any custom domains.

### Alternative: let Caffeine's own AI build it

If you cannot run the CLI locally (no shell, no toolchain), drive Caffeine's hosted AI
instead: create a cloud project with `caffeine projects create`, then describe the app in
natural language with `caffeine chat send --project-id <id> "<prompt>"` (or use the
caffeine.ai web chat). Caffeine's hosted AI then scaffolds, builds, and deploys it
server-side. `chat send` only sends the prompt and follows the AI's progress (or returns
at once with `--detach`), so this does not contradict the CLI having no deploy command.
This skill is for the **local, hand-authored** path.

## Component skills

Caffeine ships ready-made components for sign-in and roles, file storage, payments,
email, invite links, and third-party connectors (Google, Slack, Twilio, and more). Each is
a mops package (`caffeineai-*`), often an npm package (`@caffeineai/*`), and a skill that
shows how to wire them. Before building one of those features, read its skill and use the
component instead of writing it yourself.

- **A cloned project** lists its component skills in `skills-lock.json`. Restore them into
  `.agents/skills/` from the project root:

  ```bash
  npx skills experimental_install -y
  ```

- **A project you scaffold by hand** has no lock file. Fetch the skill you need from
  <https://github.com/caffeinelabs/skills>: one `skills/<name>/SKILL.md` per component, listed
  in its README.

## Using the app from Claude or another AI assistant

A deployed Caffeine app already works with DFINITY's ICP MCP connector,
`https://mcp.internetcomputer.org/mcp`. The user adds it to their assistant as a custom
connector, signs in with Internet Identity, and asks it to open the app by its web address;
the assistant then calls the app's backend methods as that user. Do **not** build an MCP
server, an HTTP endpoint, or a secret link into the app for this. Clear backend method names
and Candid types are what the assistant reads, so a capability it should have is an
ordinary backend method.

## Common Pitfalls

1. **Missing `[workspace]` in the root `caffeine.toml`.** Without it the root file is
   parsed as a canister manifest and the CLI cannot find your canisters. The root
   manifest is defined by the presence of `[workspace]`, not by being at the top.
2. **Renaming the backend canister.** It must be `backend` — `mops.toml` declares
   `[canisters.backend]` and the root `bindgen` script reads `./src/backend/dist/backend.did`.
   Renaming breaks the build and the generated client.
3. **Hand-writing or editing `src/frontend/src/backend.ts` or `declarations/`.** These
   are generated by `caffeine-bindgen` and overwritten on every build. Add backend
   methods in `main.mo`, rebuild, and the client regenerates. The generated header says
   "You should NOT make any changes in this file"; it is also excluded from Biome.
4. **Importing `./backend` before the first build.** The binding module is created by
   the build's `pnpm bindgen` step. Run `caffeine preview --build` (or `caffeine build`)
   once before relying on `import { createActor } from "./backend"`.
5. **Trying to `dfx deploy` or expecting `caffeine deploy`.** Caffeine apps build via
   the `caffeine` CLI and go live via the web app. There is no `dfx` in the workflow and
   no CLI deploy/publish command.
6. **Dropping required `mops.toml` settings.** Keep the single `[canisters.backend]`,
   `[canisters.backend.check-stable]`, `[build] outputDir`, and a `[toolchain] moc` pin
   (mops cannot compile without one).
7. **Deleting `.old/` or `env.json`, or skipping `copy:env`.** `.old/` holds the
   stable-signature snapshot `check-stable` compares against; `env.json` must be copied
   into `dist/` so the served frontend can read its runtime config.
8. **Writing Motoko without the `writing-motoko` skill.** Modern Caffeine Motoko uses
   `mo:core`, persistent actors, and specific patterns. Guessing produces compiler
   errors. Load <https://skills.internetcomputer.org/skills/writing-motoko/SKILL.md> first.
9. **Using `npm`/`yarn` instead of `pnpm`.** The workspace is pnpm-based
   (`pnpm-workspace.yaml`, `pnpm -r` scripts). `caffeine install` uses pnpm + mops.
10. **`caffeine install`/`build` fails with `ERR_PNPM_NO_LOCKFILE` on a fresh project.**
    In a non-interactive shell (an agent, CI, or any run without a TTY) these commands
    run `pnpm install --frozen-lockfile`, which requires a `pnpm-lock.yaml` that a
    brand-new project does not have. Run `pnpm install` once first to generate the
    lockfile, then the loop works. (An interactive terminal creates it for you.)
11. **First `caffeine check` fails with `Deployed file not found: …/backend.most`.** The
    stable-signature check needs the last deployed snapshot, which a never-deployed project
    lacks. Seed `.old/src/backend/dist/backend.most` with an empty actor (shown under the
    `mops.toml` above). `caffeine build` does not create it.
12. **`caffeine preview --build` fails with `No project.id in caffeine.toml`.** Uploading
    a draft needs a cloud project. Run `caffeine projects create` to get an id, set it in
    `[project] id` (or pass `--project-id <id>`), then preview. `caffeine build` alone
    needs no id and is enough to verify the app compiles.
13. **`too many pending migrations for check-limit=1`.** Only one migration can be pending
    at a time, and on a never-deployed project `00000000_000000.mo` already is. Fold the
    new state into that pending file instead of adding another.
14. **`include-authorization` lint error, or `M0169` "stable variable `accessControlState`
    … cannot be implicitly discarded".** `main.mo` dropped `MixinAuthorization` or its
    `accessControlState` field while the package and the first migration still provide
    them. Keep the starting `main.mo` lines, or remove authorization completely as the
    `extension-authorization` skill describes.

## Related skills

- **`writing-motoko`** — REQUIRED companion. Authoritative for all backend Motoko code:
  <https://skills.internetcomputer.org/skills/writing-motoko/SKILL.md>. Always load it before
  editing `src/backend/main.mo`.
- **`migrating-motoko-actors`** — load before changing the actor's stable state: how to
  write and fold migrations in `src/backend/migrations/`.
  <https://github.com/caffeinelabs/skills/tree/main/skills/migrating-motoko-actors>
- **`extension-core-infrastructure`** — `InternetIdentityProvider`, `useInternetIdentity`,
  and `useActor` on the frontend.
  <https://github.com/caffeinelabs/skills/tree/main/skills/extension-core-infrastructure>
- **`extension-authorization`** — roles, guards, user profiles, and the sign-in screen
  built on `caffeineai-authorization`.
  <https://github.com/caffeinelabs/skills/tree/main/skills/extension-authorization>
- **`mops-cli`** — mops commands: `mops add`, `mops check`, toolchain pins.
  <https://github.com/caffeinelabs/skills/tree/main/skills/mops-cli>
- **`migrating-to-moc-2`** — moving a cloned moc 1 project to moc 2.
  <https://github.com/caffeinelabs/skills/tree/main/skills/migrating-to-moc-2>
- **`icp-cli`** — for raw Internet Computer / `dfx` / `icp` projects. Not used by
  Caffeine; reach for it only when the user is *not* building a Caffeine app.

## Additional references

- [`references/frontend-template.md`](references/frontend-template.md) — the full,
  verbatim frontend boilerplate (`package.json`, `vite.config.js`, Tailwind/PostCSS/Biome
  configs, `tsconfig.json`, `index.html`, `env.json`, `main.tsx`, a starter `App.tsx`,
  and the backend-actor wiring pattern). Read it when you create `src/frontend/`.
