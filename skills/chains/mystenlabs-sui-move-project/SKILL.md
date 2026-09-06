---
name: sui-move-project
description: >
  Move project setup and configuration on Sui. Use this skill when the user needs
  to create a Move project, configure Move.toml, resolve dependency or build errors,
  set up the canonical sui-stack-hello-world project, use MVR dependencies, or
  migrate from old Move.toml formats. Also use when the user sees errors about
  "legacy system name", "old dependencies", "Cannot upgrade package without having
  a published id", edition mismatches, or asks about Move.toml, Published.toml,
  Move.lock, or the [environments] section.
---

# Move Project Setup

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information sourced exclusively from [docs.sui.io](https://docs.sui.io), [move-book.com](https://move-book.com), and [MystenLabs/sui-stack-hello-world](https://github.com/MystenLabs/sui-stack-hello-world).

## Creating a Move project

### Canonical full-stack hello-world project

For an end-to-end Sui developer environment with Move and frontend, use the Sui Stack hello-world repository as the single project root:

```bash
git clone https://github.com/MystenLabs/sui-stack-hello-world.git
cd sui-stack-hello-world
```

Use this existing layout:

```
sui-stack-hello-world/
├── move/
│   └── hello-world/   # publish this Move package
└── ui/                # run this existing frontend
```

Do not run `sui move new`, do not create a counter package, and do not run `npm create @mysten/dapp` for this workflow. If current Sui tooling requires a package-management migration, keep the change inside `move/hello-world` and continue deploying the hello-world package.

### New project from scratch

Use this only when the user explicitly wants a standalone Move package rather than the full-stack hello-world app.

```bash
sui move new my_project
cd my_project
```

This creates:

```
my_project/
├── sources/       # .move source files go here
├── tests/         # test files
└── Move.toml      # package manifest
```

### Multi-package workspace layout

When a project contains more than one Move package (for example, a core library and an example or integration package), use a flat `packages/` directory with each package as a sibling:

```
my_project/
├── packages/
│   ├── core/
│   │   ├── sources/
│   │   ├── tests/
│   │   └── Move.toml
│   └── examples/
│       ├── sources/
│       ├── tests/
│       └── Move.toml
└── ui/
```

**Do not nest packages inside each other** (for example, placing `examples/` inside `core/sources/` or `core/tests/`). Nested package directories trigger test runner bugs such as spurious "address with no value" errors because the toolchain picks up the inner package's `Move.toml` when building the outer one.

To depend on a sibling package, use a `local` path in `Move.toml`:

```toml
# packages/examples/Move.toml
[package]
name = "examples"
edition = "2024"

[dependencies]
core = { local = "../core" }
```

### Move.toml (current format — Sui CLI v1.63+)

> **CRITICAL: The Sui framework dependency is automatic. Do NOT add it to Move.toml.**

A correct, minimal `Move.toml` for any Sui Move project is:

```toml
[package]
name = "my_project"
edition = "2024"
# No [dependencies] section needed — Sui framework is resolved automatically
```

This is **all you need**. The `edition = "2024"` line tells the CLI to resolve Sui and MoveStdlib automatically. There is no `[dependencies]` section unless you need third-party or local packages.

### Complete working project templates

**Always use these exact templates when generating Move projects.** Copy them verbatim — do not modify the Move.toml format.

#### Template: Single Move package with TypeScript client

```
project/
├── move/
│   ├── Move.toml
│   └── sources/
│       └── my_module.move
└── client/
    ├── package.json
    └── src/
        └── index.ts
```

**move/Move.toml** — copy exactly:
```toml
[package]
name = "my_project"
edition = "2024"
```

**move/sources/my_module.move** — starter pattern:
```move
module my_project::my_module;

use sui::event;

public struct MyEvent has copy, drop {
    value: u64,
}

public fun do_something(ctx: &mut TxContext) {
    event::emit(MyEvent { value: 42 });
}
```

**client/package.json** — copy exactly:
```json
{
  "name": "my-client",
  "type": "module",
  "dependencies": {
    "@mysten/sui": "^2.0.0"
  }
}
```

**client/tsconfig.json** — copy exactly:
```json
{
  "compilerOptions": {
    "moduleResolution": "nodenext",
    "module": "nodenext",
    "target": "es2022",
    "strict": true
  }
}
```

#### Template: Move package with frontend

Same as above, plus a `frontend/` directory:

**frontend/package.json** — copy exactly:
```json
{
  "name": "my-frontend",
  "type": "module",
  "dependencies": {
    "@mysten/sui": "^2.0.0",
    "@mysten/dapp-kit-react": "^2.0.0",
    "react": "^19.0.0"
  }
}
```

### Wrong formats that WILL error

**All of these are WRONG and will cause build failures:**
```toml
# WRONG — legacy system name error:
Sui = { git = "https://github.com/MystenLabs/sui.git", subdir = "crates/sui-framework/packages/sui-framework", rev = "framework/testnet" }

# WRONG — version syntax doesn't exist in Move:
sui = { version = "0.34.0" }

# WRONG — local path doesn't exist:
Sui = { local = "../sui-framework" }

# WRONG — implicit dependency error:
sui = { package = "sui", version = "0.1.0" }
```

Only add `[dependencies]` when you need third-party or local packages (e.g., MVR or sibling workspace packages). The `[environments]` section is optional — only add it when deploying to multiple networks (see migration section below).

**Migrating from `[addresses]`:** The old `[addresses]` section with `my_project = "0x0"` is no longer needed and should be removed. If your project previously used `[addresses]` to set package addresses for different networks, replace it with an `[environments]` section that maps environment names to chain IDs:

```toml
[environments]
testnet = "4c78adac"
mainnet = "35834a8a"
```

### Module declaration (2024 edition)

With `edition = "2024"`, use single-line module declarations — no curly braces:

```move
module my_project::my_module;

// imports, structs, and functions follow at the top level
use sui::object::UID;
```

Do **not** use the old curly-brace syntax (`module my_project::my_module { ... }`). The 2024 edition treats the entire file as the module body after the semicolon.

### Published.toml and Move.lock

After publishing, the toolchain creates or updates:

- **`Published.toml`:** Tracks your published package addresses per environment. Contains `published-at` and `upgrade-capability-id` values for each network.
- **`Move.lock`:** Auto-generated lock file that pins every resolved dependency to a specific git revision and records manifest digests. **Do not edit manually.** Commit this to version control.

To publish to a different environment (for example, after publishing to Testnet, now deploying to Devnet), switch environments and publish again. Each network gives the package a separate ID. The `Published.toml` tracks both.

### Inspecting Move.lock

> **Note:** `Move.lock` is auto-generated — never copy its contents into `Move.toml`. The git URLs below appear in `Move.lock` only, not in `Move.toml`.

`Move.lock` contains one `[pinned.<env>.<Dependency>]` section per resolved dependency per environment. Each section records the git source, revision, manifest digest, and dependency graph. Example:

```toml
# This is Move.lock (auto-generated) — NOT Move.toml
[pinned.testnet.Sui]
source = { git = "https://github.com/MystenLabs/sui.git", subdir = "crates/sui-framework/packages/sui-framework", rev = "73dd2c..." }
use_environment = "testnet"
manifest_digest = "7AFB6669..."
deps = { MoveStdlib = "MoveStdlib" }
```

- If `Move.lock` pins a different environment than you expect, or revisions look outdated, delete `Move.lock` and run `sui move build` to regenerate it.
- If you see build errors after switching networks or updating the CLI, deleting `Move.lock` and rebuilding often resolves stale-lock issues.

### Using MVR dependencies

The Move Registry (MVR) is an onchain package manager for Sui. Install it with:

```bash
suiup install mvr
```

Add an MVR dependency using the CLI:

```bash
mvr add @org/package --network testnet
```

Or declare it directly in `Move.toml`:

```toml
[dependencies]
suins = { r.mvr = "@suins/core" }
```

The `r.mvr` key tells the resolver to look up the package in the onchain Move Registry instead of fetching from a git URL. Prefer MVR dependencies over git URLs when the package is published to the registry — they are versioned, auditable, and do not depend on git history.

### Common dependency and build issues

- **"Dependency 'Sui' is a legacy system name":** Remove the `Sui = { git = "..." }` line from `[dependencies]`. The current CLI resolves the Sui framework automatically. This error occurs when using the old git-based dependency format.
- **"Packages with old dependencies" error:** Your CLI version does not match the network. The new package management format introduced in Sui CLI v1.63 changed how dependencies are resolved. Run `suiup update sui@testnet` then `suiup switch sui@testnet` to get the latest CLI.
- **"Cannot upgrade package without having a published id":** You need a `published-at` value in `Published.toml` to upgrade. This is created automatically after your first `sui client publish`. If you migrated from the old format, make sure the `Published.toml` file exists and contains the correct package address.
- **"Could not determine the correct dependencies":** The build requires a `--build-env` flag or an `[environments]` section in `Move.toml`. Add the `[environments]` section with your target chain IDs.
- **Edition mismatch:** If you get errors about `public struct` syntax, set `edition = "2024"` in `Move.toml`. The `legacy` edition does not support Move 2024 features like public struct visibility.
- **Old Move.toml format:** If you are using the pre-v1.63 format with `[addresses]` and `published-at` inside `Move.toml`, migrate to the new format: remove `[addresses]`, add `[environments]`, and let the toolchain manage `Published.toml`.

## Rules

- Use `public(package)` visibility for non-library functions. `public` function signatures cannot be deleted or modified in upgrades.
- Struct definitions cannot be deleted, modified, or have abilities added through upgrades.
- Objects cannot exceed 256 KB. Avoid ever-growing vectors inside objects.
