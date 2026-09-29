# Annotated Config Templates

Reference snippets for the config files the scaffold prints. Each template is annotated inline so the developer understands what every field does and which fields they need to adjust.

Versions are intentionally left as placeholder markers. At scaffold time, check the project's GitHub releases page or the bundled docs at `../../docs/sources/<source>/` and replace the marker with the latest stable release.

## `aiken.toml` (all stacks)

Lives at the root of the on-chain project (or at `onchain/aiken.toml` in a monorepo).

```toml
# aiken.toml -- on-chain project manifest
name = "acme/onchain"                     # owner/project. Used as the module prefix.
version = "0.0.0"                         # bump on each release; semver
license = "Apache-2.0"                    # or whichever license you ship under
description = "On-chain validators for the Acme dApp."

# Compiler used for this project. Aiken pins itself; do not change unless you
# also change CI and every developer's local toolchain.
compiler = "v1.1.21"                      # PIN: the compiler the templates are tested with.
                                          # Bump together with the stdlib pin below.
plutus = "v3"                             # Plutus V3 is the current target; required for
                                          # Conway-era features.

[repository]
user = "acme-org"                         # GitHub org / user
project = "acme-dapp"                     # repo name
platform = "github"

# Dependencies. Pin to a tag, never to a branch. Always commit aiken.lock.
[[dependencies]]
name = "aiken-lang/stdlib"
version = "v3.1.0"                        # PIN: stdlib v3 provides the aiken/collection,
                                          # aiken/crypto and cardano/* modules the
                                          # validators import.
source = "github"

# Optional but recommended: design-patterns library. Drop if not used.
# [[dependencies]]
# name = "Anastasia-Labs/aiken-design-patterns"
# version = "v1.6.3"
# source = "github"

[config]
# Defaults to empty; uncomment to define environment-specific config that the
# build step compiles into the validator (e.g., admin pubkey hash per network).
# default = { admin = "abc...def" }
```

Run `aiken build` to emit `plutus.json` (CIP-57 blueprint) into the project root. That file is what every off-chain SDK loads.

## `.gitignore` (shared, all stacks)

```gitignore
# --- Aiken ---
build/                        # aiken build output (compiled UPLC, plutus.json copies)
artifacts/                    # any per-validator artifacts
.aiken/                       # local Aiken cache

# --- Secrets ---
.env                          # never committed; .env.example is the committed template
.env.*.local                  # framework-specific local overrides
.keys/                        # dev signing keys from Yaci DevKit
*.skey                        # signing keys
*.vkey                        # verification keys (usually safe but kept private by convention)

# --- OS / editor ---
.DS_Store
.vscode/
.idea/
*.swp
*~

# Add stack-specific entries below.
```

Stack-specific additions:

**Mesh SDK / Evolution SDK (Node.js):**
```gitignore
node_modules/
dist/
.next/
*.tsbuildinfo
coverage/
```

**PyCardano (Python):**
```gitignore
__pycache__/
*.py[cod]
.venv/
.pytest_cache/
.mypy_cache/
.ruff_cache/
dist/
build/
*.egg-info/
```

**cardano-client-lib (JVM):**
```gitignore
target/
*.class
.gradle/
build/
.mvn/
hs_err_pid*.log
```

## `.env.example` (all stacks)

Committed. Real `.env` is gitignored. Copied via `cp .env.example .env` on first checkout.

The template below covers all supported networks. Leave the variables for the networks you are not using empty; the off-chain code only requires the active one.

```bash
# .env.example -- copy to .env and fill in real values.

# --- Active network ---
# Which network to talk to. Default to a testnet always; do NOT default to
# mainnet — bugs in untested validators can lock real funds permanently on
# mainnet.
#   devnet  : Yaci DevKit, local instant-finality. Fastest iteration.
#   preview : public Preview testnet, ~20s blocks, mainnet-like behaviour.
#   preprod : public Preprod testnet, mirrors mainnet protocol params most closely.
#   mainnet : production. Only switch after thorough testing and (for non-trivial
#             code) an audit.
CARDANO_NETWORK=devnet               # devnet | preview | preprod | mainnet

# --- Yaci DevKit (local devnet) ---
# Yaci Store serves a Blockfrost-compatible API under /api/v1 on this URL.
# Use `yaci-cli` (or the dev-up.sh script in the scaffold) to launch it; see
# the `setup-devnet` skill for full instructions.
# Fund an address: `topup <address> <ada>` at the yaci-cli devnet prompt.
YACI_STORE_URL=http://localhost:8080
# DevKit admin API (CLI, wallet page, MCP). Not a chain-query endpoint.
YACI_ADMIN_URL=http://localhost:10000
# Yaci DevKit auto-seeds wallets with test ADA at startup. Replace with an
# address printed by `yaci-cli` when you start the devnet.
DEV_WALLET_ADDRESS=

# --- Blockfrost (any non-devnet network) ---
# Sign up free at https://blockfrost.io for a development project ID.
# Each network has its OWN project ID — you cannot reuse a preview key for
# preprod or mainnet. Copy the matching key into BLOCKFROST_PROJECT_ID below
# at runtime (or set per-env in your shell / CI).
# NEVER COMMIT REAL PROJECT IDs.
#   preview  : starts with "preview..."  faucet at https://docs.cardano.org/cardano-testnets/tools/faucet (Preview selector)
#   preprod  : starts with "preprod..."  faucet at https://docs.cardano.org/cardano-testnets/tools/faucet (Preprod selector)
#   mainnet  : starts with "mainnet..."  no faucet — real ADA, real consequences
BLOCKFROST_PROJECT_ID=

# Network IDs used by the wallet/SDK layer. 0 = testnet (any of preview /
# preprod / devnet); 1 = mainnet. The off-chain code derives this from
# CARDANO_NETWORK automatically, but the literal is here for reference.
# CARDANO_NETWORK_ID=0

# Optional Koios endpoint override; default is the public mainnet/testnet URL.
# KOIOS_URL=

# --- Wallet ---
# Mnemonic for the dev wallet used by off-chain scripts. Generated by Yaci
# DevKit on launch (devnet) or by your wallet at account creation (preview /
# preprod). Treat as a secret even though it is dev-only; never reuse on
# mainnet, never commit, and rotate if accidentally leaked.
DEV_WALLET_MNEMONIC=
```

### Per-network checklist

When you flip `CARDANO_NETWORK` between scaffolded environments, update only the relevant block above. Cross-reference:

| Network | Blockfrost key prefix | Faucet | Notes |
|---|---|---|---|
| devnet | not used | `topup <address> <ada>` at the yaci-cli prompt | YACI_STORE_URL must be reachable |
| preview | `preview...` | https://docs.cardano.org/cardano-testnets/tools/faucet (select Preview) | network ID = 0, ~20s blocks |
| preprod | `preprod...` | https://docs.cardano.org/cardano-testnets/tools/faucet (select Preprod) | network ID = 0, mainnet-like params |
| mainnet | `mainnet...` | none — real ADA | network ID = 1, audit before deploying |

## `package.json` (Stack 1: Mesh SDK)

```jsonc
{
  "name": "acme-offchain",
  "version": "0.0.0",
  "private": true,
  "type": "module",                            // ESM; required by modern @meshsdk/core
  "engines": {
    "node": ">=20"                             // PIN: match your CI Node version
  },
  "scripts": {
    "build": "tsc -p tsconfig.json",
    "typecheck": "tsc --noEmit",
    "test": "node --test dist/",               // or vitest / jest; see references/layout-aiken-mesh.md
    "tx:lock": "tsx src/hello/lock.ts",        // first-tx helper from the scaffold
    "tx:redeem": "tsx src/hello/redeem.ts"
  },
  "dependencies": {
    "@meshsdk/core": "1.9.1",                  // PIN: exact; check `npm view @meshsdk/core version`.
    "dotenv": "^16.4.5"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "tsx": "^4.0.0",
    "typescript": "^5.4.0"
  }
}
```

## `package.json` (Stack 2: Evolution SDK)

```jsonc
{
  "name": "acme-offchain",
  "version": "0.0.0",
  "private": true,
  "type": "module",
  "engines": {
    "node": ">=20"
  },
  "scripts": {
    "build": "tsc -p tsconfig.json",
    "typecheck": "tsc --noEmit",
    "test": "node --test dist/",
    "tx:lock": "tsx src/hello/lock.ts",
    "tx:redeem": "tsx src/hello/redeem.ts"
  },
  "dependencies": {
    "@evolution-sdk/evolution": "0.5.14",      // PIN: exact; check `npm view @evolution-sdk/evolution version`.
    "dotenv": "^16.4.5"                        // Evolution brings its own Effect dependency
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "tsx": "^4.0.0",
    "typescript": "^5.4.0"
  }
}
```

## `tsconfig.json` (Stacks 1 and 2)

```jsonc
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "rootDir": "./src",
    "outDir": "./dist",
    "strict": true,                            // never disable; catches half the bugs
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,                 // required to import plutus.json directly
    "forceConsistentCasingInFileNames": true,
    "declaration": true                        // emit .d.ts for downstream consumers
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules", "dist"]
}
```

## `pyproject.toml` (Stack 3: PyCardano)

```toml
# pyproject.toml -- Python project manifest using Poetry.
[tool.poetry]
name = "acme-offchain"
version = "0.0.0"
description = "Off-chain code for the Acme dApp, built on PyCardano."
authors = ["Acme Org <devs@example.invalid>"]
readme = "README.md"
packages = [{ include = "acme_offchain", from = "src" }]

[tool.poetry.dependencies]
python = "^3.11"                          # PIN: match your CI Python version
pycardano = "0.19.2"                      # PIN: exact; bump deliberately.
cbor2 = ">=5.6.5,<6"                      # cbor2 6 breaks `import pycardano` 0.19.2;
                                          # drop once PyCardano supports it.
python-dotenv = "^1.0.1"                  # reads .env at startup
requests = "^2.32.0"                      # provider HTTP

[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
ruff = "^0.5.0"
mypy = "^1.10.0"
types-requests = "^2.32.0"

[tool.poetry.scripts]
tx-lock = "acme_offchain.hello.lock:main"      # `poetry run tx-lock`
tx-redeem = "acme_offchain.hello.redeem:main"

[build-system]
requires = ["poetry-core>=1.8.0"]
build-backend = "poetry.core.masonry.api"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.mypy]
python_version = "3.11"
strict = true

# PyCardano and blockfrost-python ship no type information.
[[tool.mypy.overrides]]
module = ["pycardano.*", "blockfrost.*"]
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = ["acme_offchain.yaci"]
disallow_subclassing_any = false
```

## `pom.xml` (Stack 4: cardano-client-lib)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>

  <groupId>org.acme</groupId>
  <artifactId>acme-offchain</artifactId>
  <version>0.0.0</version>
  <packaging>jar</packaging>

  <properties>
    <maven.compiler.source>21</maven.compiler.source>     <!-- PIN: match your CI JDK -->
    <maven.compiler.target>21</maven.compiler.target>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <!-- PIN: one version for every com.bloxbean.cardano artifact; bump deliberately. -->
    <cclib.version>0.7.2</cclib.version>
  </properties>

  <dependencies>
    <!-- Core transaction builder; brings the plutus and blueprint modules with it. -->
    <dependency>
      <groupId>com.bloxbean.cardano</groupId>
      <artifactId>cardano-client-lib</artifactId>
      <version>${cclib.version}</version>
    </dependency>

    <!-- Backend client; pick one. Blockfrost is the default for hosted networks. -->
    <dependency>
      <groupId>com.bloxbean.cardano</groupId>
      <artifactId>cardano-client-backend-blockfrost</artifactId>
      <version>${cclib.version}</version>
    </dependency>

    <!-- Testing. -->
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <version>5.10.2</version>
      <scope>test</scope>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.13.0</version>
      </plugin>
      <plugin>
        <artifactId>maven-surefire-plugin</artifactId>
        <version>3.2.5</version>
      </plugin>
    </plugins>
  </build>
</project>
```

## Notes on pinning

- Aiken: pin both `compiler` and the stdlib dependency. Mismatched versions cause confusing build errors.
- TypeScript: exact versions for `@meshsdk/*`, `@evolution-sdk/*`, pre-1.0 packages and `next`; `^` ranges for the rest. Commit `package-lock.json` or `pnpm-lock.yaml`.
- PyCardano: pin it exactly and commit `poetry.lock`. Poetry's `^0.x` already holds the minor version, so pre-1.0 tools such as `ruff` can keep it.
- cardano-client-lib: pin a single `cclib.version` property and reuse it across all `com.bloxbean.cardano:*` dependencies. Mixing versions across the cclib family causes runtime classpath errors.

## Notes on secrets

Never commit `.env`. Never paste real Blockfrost project IDs or real mnemonics into source files, READMEs, or test fixtures. If a developer accidentally commits one, treat the credential as compromised and rotate it.
