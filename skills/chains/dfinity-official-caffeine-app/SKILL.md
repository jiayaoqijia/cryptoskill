---
name: caffeine-app
description: "Scaffold and build a complete Caffeine app (caffeine.ai) from scratch — the project layout, the caffeine.toml workspace + canister manifests, the mops.toml for the single Motoko `backend` canister, the React/Vite frontend, and the caffeine CLI build loop (auth login, doctor, install, check --fix, preview --build). Use whenever the user wants to create, scaffold, set up, or build a Caffeine app or a caffeine.ai project, asks about caffeine.toml or mops.toml structure, or needs the caffeine CLI workflow — even if they do not say the words 'from scratch'. Always pair it with the `writing-motoko` skill for the backend code. Do NOT use it for Motoko language syntax or compiler errors (use the `writing-motoko` skill), and do NOT use it for generic Internet Computer / dfx / icp deployment (use the `icp-cli` skill)."
license: Apache-2.0
compatibility: "@caffeineai/cli (the `caffeine` command), Node.js >= 18.17, pnpm, network access + a caffeine.ai account"
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
  only downloads an *existing* cloud project — it is not a greenfield scaffold.)
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

# Authenticate against caffeine.ai (opens a browser; use --device on headless hosts).
caffeine auth login
caffeine auth status

# Check the environment: Node, pnpm, mops, caffeine-bindgen, that you are logged in,
# and that the Caffeine API is reachable (installs/repairs what it can).
caffeine doctor --fix
```

If a global install is undesirable or fails, run every `caffeine` command through an
`npx -y @caffeineai/cli@latest` prefix instead — e.g. `npx -y @caffeineai/cli@latest auth status`.

`caffeine doctor --fix` checks Node.js, pnpm, mops, and caffeine-bindgen, confirms you
are logged in, and verifies the Caffeine API is reachable — installing or repairing what
it can. It does **not** install the Motoko compiler (`moc`) or linter (`lintoko`): mops
fetches those automatically from the `[toolchain]` pins in `mops.toml` on the first
`mops install` / build. `dfx` is not part of the Caffeine build.

## Project shape

A Caffeine app is a pnpm workspace with a root manifest and two canisters. Create this
exact tree (file contents below):

```text
my-app/
├── caffeine.toml              # root workspace manifest — MUST contain [workspace]
├── mops.toml                  # Motoko build config — ONE per project, at the root
├── package.json               # pnpm workspace root + the `bindgen` script
├── pnpm-workspace.yaml         # declares src/**/* as workspace packages
├── tsconfig.json               # root TS config
└── src/
    ├── backend/                # the single Motoko canister, named "backend"
    │   ├── caffeine.toml        #   canister manifest: type = "motoko"
    │   ├── main.mo              #   actor entry point (write with the `writing-motoko` skill)
    │   └── system-idl/          #   Candid for IC system canisters (see note below)
    │       └── aaaaa-aa.did     #   IC management canister interface
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
# id is assigned by the cloud after your first `caffeine preview`/create — omit it for
# a brand-new local project; the CLI fills it in.

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

There is exactly **one** `[canisters.backend]`. The structural pieces are invariant —
the single `[canisters.backend]`, `[canisters.backend.check-stable]`, and the `[moc]`
flags `--default-persistent-actors`, `--actor-idl=src/backend/system-idl`, and
`--implicit-package=core`. The **toolchain versions, the `-E`/`-W`/`-A` diagnostic codes,
and the dependency list are a current snapshot** that the Caffeine template bumps over
time — see "Versions and dependencies drift" below.

```toml
[package]
name = "backend"
version = "0.1.0"

[build]
outputDir = "src/backend/dist"
args = ["--release"]

[canisters.backend]
main = "src/backend/main.mo"

[canisters.backend.check-stable]
path = ".old/src/backend/dist/backend.most"
skipIfMissing = true

[toolchain]
moc = "1.8.1"
lintoko = "0.10.0"

[lint]
extends = true

[moc]
args = [
  "--default-persistent-actors",
  "--actor-idl=src/backend/system-idl",
  "--implicit-package=core",
  "-no-check-ir",
  "-E=M0236,M0223,M0237,M0254",
  "-W=M0235",
  "-A=M0241",
  "--generate-view-queries",
]

[dependencies]
core = "2.5.0"
caffeineai-data-viewer = "0.1.0"
```

Notes:

- **`check-stable`** points at `.old/src/backend/dist/backend.most`. The CLI saves the
  previous build's `.most` (stable-signature snapshot) under `.old/` so the next build
  can verify your stable state did not change incompatibly. Do not delete `.old/` between
  builds; do not commit it as source — it is build state. **`skipIfMissing = true` is
  required for a from-scratch project:** on the first run that snapshot does not exist
  yet, and without it `caffeine check` fails with
  `Deployed file not found: .old/src/backend/dist/backend.most`.
- **`--actor-idl=src/backend/system-idl`** tells `moc` where to find the Candid interfaces
  of IC system canisters. `src/backend/system-idl/` must exist; the canonical template
  ships `aaaaa-aa.did` (the IC management-canister interface). A minimal backend needs only
  the directory.
- **`core = "2.5.0"`** is the `mo:core` standard library. Use `mo:core`, never the
  deprecated `mo:base` — see the `writing-motoko` skill. **`caffeineai-data-viewer`** backs the
  built-in data-viewer mixin used by the default `main.mo` (below) and pairs with the
  `--generate-view-queries` flag.

> **Versions and dependencies drift.** The `[toolchain]` versions, the `[moc]`
> `-E`/`-W`/`-A` codes, and the frontend dependency set are template-managed and change
> over time (e.g. the `@dfinity/*` → `@icp-sdk/*` migration, moc/core bumps). Treat the
> exact values here as a snapshot — for current ones, `caffeine projects clone` a recent
> project and copy its `mops.toml` + `src/frontend/package.json`. Stable across versions:
> the file layout, the single `backend` canister, the structural `[moc]` flags,
> `check-stable` with `skipIfMissing`, `mo:core`, and `useActor(createActor)`.

### `package.json` (root) — pnpm workspace + the `bindgen` script

The `bindgen` script is the bridge from backend Candid to the frontend TS client. It is
invoked by the backend canister's `[build]` step (`pnpm bindgen`).

```json
{
  "name": "@caffeine/template-app",
  "type": "module",
  "engines": {
    "node": ">=18.17.0",
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
    "sharp": "^0.34.4"
  }
}
```

### `pnpm-workspace.yaml`

```yaml
packages:
  - src/**/*
onlyBuiltDependencies:
  - esbuild
```

### `tsconfig.json` (root)

```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2020",
    "experimentalDecorators": true,
    "strictPropertyInitialization": false,
    "moduleResolution": "node",
    "allowJs": true,
    "outDir": "HACK_BECAUSE_OF_ALLOW_JS"
  }
}
```

### `src/backend/main.mo` — the starting backend

The canonical template's starting `main.mo` includes the built-in **data-viewer mixin**
(`include MixinViews()`), which pairs with the `caffeineai-data-viewer` dependency and the
`--generate-view-queries` flag in `mops.toml`. With `--default-persistent-actors` the
actor is already persistent. Add your own functions inside the actor, following the
**`writing-motoko` skill**.

```motoko
import MixinViews "mo:caffeineai-data-viewer/MixinViews";

actor {
  include MixinViews();
};
```

(A bare `actor {}` also compiles if you drop the `caffeineai-data-viewer` dependency and
the `--generate-view-queries` flag.) Do not write more Motoko than this without loading
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
- `env.json` holds runtime config placeholders (`backend_host`, `backend_canister_id`,
  `project_id`, `ii_derivation_origin`, `storage_gateway_url`), all `"undefined"` locally;
  the frontend `build` script copies it into `dist/` (`cp env.json dist/`). Caffeine
  injects real values when it serves the app. Keep `env.json` and the `copy:env` step.

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

**Generation ordering.** `src/frontend/src/backend.ts` does not exist until a build runs
`pnpm bindgen`. So if your frontend imports from `./backend`, you must run `caffeine build`
at least once before `caffeine check` can typecheck the frontend. A brand-new app whose
`App.tsx` does not yet import `./backend` typechecks fine before the first build.

**Going live.** `caffeine preview --build` (with a `project.id`) produces a *draft* and
returns its URL. Promote a draft to a live URL in the caffeine.ai web app (open it with
`caffeine chat open` or visit caffeine.ai). There is no CLI deploy command. Use
`caffeine projects show <id>` to see draft and live URLs.

### Alternative: let Caffeine's own AI build it

If you cannot run the CLI locally (no shell, no toolchain), drive Caffeine's hosted AI
instead: describe the app in natural language with `caffeine chat send "<prompt>"` (or
the caffeine.ai web chat). Caffeine's hosted AI then scaffolds, builds, and deploys it
server-side — `chat send` only submits the prompt, so this does not contradict the CLI
having no deploy command. This skill is for the **local, hand-authored** path.

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
   "do NOT make any changes in this file"; it is also excluded from Biome.
4. **Importing `./backend` before the first build.** The binding module is created by
   the build's `pnpm bindgen` step. Run `caffeine preview --build` (or `caffeine build`)
   once before relying on `import { createActor } from "./backend"`.
5. **Trying to `dfx deploy` or expecting `caffeine deploy`.** Caffeine apps build via
   the `caffeine` CLI and go live via the web app. There is no `dfx` in the workflow and
   no CLI deploy/publish command.
6. **Dropping required `mops.toml` settings.** Keep the single `[canisters.backend]`,
   the `[toolchain]` pins, `[canisters.backend.check-stable]`, and the `[moc] args`
   (especially `--default-persistent-actors` and `--actor-idl=src/backend/system-idl`).
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
    stable-signature check needs a previous build's snapshot, which a never-built project
    lacks. Set `skipIfMissing = true` under `[canisters.backend.check-stable]` (shown in
    the `mops.toml` above), or run `caffeine build` first so a baseline exists.
12. **`caffeine preview --build` fails with `No project.id in caffeine.toml`.** Uploading
    a draft needs a cloud project. Run `caffeine projects create` to get an id, set it in
    `[project] id` (or pass `--project-id <id>`), then preview. `caffeine build` alone
    needs no id and is enough to verify the app compiles.

## Related skills

- **`writing-motoko`** — REQUIRED companion. Authoritative for all backend Motoko code:
  <https://skills.internetcomputer.org/skills/writing-motoko/SKILL.md>. Always load it before
  editing `src/backend/main.mo`.
- **`icp-cli`** — for raw Internet Computer / `dfx` / `icp` projects. Not used by
  Caffeine; reach for it only when the user is *not* building a Caffeine app.

## Additional references

- [`references/frontend-template.md`](references/frontend-template.md) — the full,
  verbatim frontend boilerplate (`package.json`, `vite.config.js`, Tailwind/PostCSS/Biome
  configs, `tsconfig.json`, `index.html`, `env.json`, `main.tsx`, a starter `App.tsx`,
  and the backend-actor wiring pattern). Read it when you create `src/frontend/`.
