---
name: setup-devnet
description: >-
  Guides setting up a local Cardano development environment. Triggers: "setup devnet", "local testnet", "Yaci DevKit", "development environment", "local Cardano node", "devnet", "preview testnet", "preprod testnet".
allowed-tools: Read Grep Glob
disallowed-tools: WebFetch WebSearch
---

<!-- Documentation lookup path: ${CLAUDE_SKILL_DIR}/../../docs/sources/ -->

# Set Up a Cardano Development Environment

Help the developer set up a local Cardano development network for building, testing, and deploying smart contracts.

## When to use

- Developer wants to run a local Cardano network for development
- Setting up Yaci DevKit or similar local devnet tooling
- Configuring local chain indexers (Kupo, Ogmios) for development
- Establishing a smart contract development workflow (build, deploy, test)
- Connecting to Preview or Preprod public testnets
- Setting up CI/CD pipelines for Cardano projects

## When NOT to use

- Querying mainnet or production chain data (use `query-chain` skill)
- Choosing between SDKs or tools broadly (use `suggest-tooling` skill)
- Writing smart contract logic in Aiken or Plutus
- Wallet integration in a web frontend (use `connect-wallet` skill)

## Key principles

1. **Start local, then move to testnets.** Local devnets give instant feedback. Use Preview/Preprod for integration testing.
2. **Two fast local-devnet options.** Yaci DevKit (standalone CLI tool with a visual explorer) and Evolution SDK devnet (`@evolution-sdk/devnet`, a TypeScript library) are both Docker-based — pick by workflow, not speed.
3. **Automate from day one.** Scripts for devnet startup, contract deployment, and testing save hours.
4. **Match your devnet to your target network.** Ensure protocol parameters and era match what you will deploy to.
5. **Keep test wallets organized.** Use named wallets with known keys for reproducible testing.

## Workflow

### Step 1: Choose the environment

Ask the developer (if not already clear):

- **Are you developing smart contracts or off-chain code (or both)?**
- **Do you need a fully isolated local network or a shared testnet?**
- **What OS are you on?** (Docker availability matters)
- **Do you need governance features (Conway era)?**

| Environment | Best for | Setup time |
|---|---|---|
| **Yaci DevKit** | Smart contract dev, fast iteration, visual block explorer | 5 minutes |
| **Evolution SDK devnet** | TypeScript projects; code-first devnet inside the test suite | 5 minutes |
| **Dingo devnet** | Node-side behaviour: consensus, diffusion, mempool, fast epoch boundaries | 10 minutes |
| **Preview testnet** | Integration testing, shared state, longer-lived deployments | 10 minutes |
| **Preprod testnet** | Pre-production testing, mirrors mainnet parameters | 10 minutes |
| **Custom local cluster** | Advanced scenarios, custom protocol params | 30+ minutes |

### Step 2: Search Bundled Documentation

Search the bundled documentation for relevant content:
- `${CLAUDE_SKILL_DIR}/../../docs/sources/yaci-devkit/` - Yaci DevKit docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/yaci-store/` - Yaci Store docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/evolution-sdk/devnet/` - Evolution SDK devnet docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/cardano-node-wiki/` - Cardano node wiki
- `${CLAUDE_SKILL_DIR}/../../docs/sources/dingo/` - Dingo devnet (see the README's DevNet section)

### Step 3: Set up Yaci DevKit (CLI tool, visual explorer)

Reference the quickstart guide for detailed commands:

```
File: skills/setup-devnet/references/yaci-devkit-quickstart.md
```

#### Quick setup

1. **Prerequisites**: Docker and Docker Compose installed
2. **Install + start the devnet** (the DevKit ships as a `devkit` script that
   manages the containers and opens the Yaci CLI):
   ```bash
   devkit start                        # opens yaci-cli
   yaci-cli:> create-node -o --start   # create + start a default devnet
   ```
3. **Fund wallets**: `topup <address> <ada>` inside the CLI (the `devnet:default>` prompt), or pre-fund via `config/env`
4. **Access points**:
   - Yaci Store API (Blockfrost-compatible): `http://localhost:8080/api/v1/`
   - Yaci Viewer (block explorer): `http://localhost:5173`
   - CLI/Admin, wallet, MCP: `http://localhost:10000`
   - cardano-cli against the node: `devkit cli`

#### Configure for your needs

- Set era (Babbage, Conway) for governance testing
- Adjust protocol parameters (min fee, collateral percentage)
- Configure slot length for faster/slower block production
- Enable/disable Plutus cost model overrides for testing

### Step 3b: Set up Evolution SDK devnet (code-first alternative)

If the project is TypeScript-based, `@evolution-sdk/devnet` runs the same local Cardano network as a library — the devnet's genesis, lifecycle, and UTxO queries live in your code and test suite instead of a separate CLI tool. Reference the quickstart:

```
File: skills/setup-devnet/references/evolution-sdk-devnet.md
```

#### Quick setup

1. **Prerequisites**: Docker running, Node.js 18+
2. **Install**: `pnpm add @evolution-sdk/devnet @evolution-sdk/evolution`
3. **Create and start a cluster** in code:
   ```typescript
   import { Cluster } from "@evolution-sdk/devnet";

   const cluster = await Cluster.make({
     clusterName: "dev",
     ports: { node: 3001, submit: 3002 },
     kupo: { enabled: true, port: 1442 },
     ogmios: { enabled: true, port: 1337 },
   });
   await Cluster.start(cluster);
   ```
4. **Fund addresses at genesis** via `shelleyGenesis.initialFunds` — deterministic, no faucet. Genesis UTxOs are not indexed by Kupo; derive them with `Genesis.calculateUtxosFromConfig(...)` and pass via the builder's `availableUtxos`.
5. **Connect a client**: `Client.make(Cluster.getChain(cluster)).withKupmios({ kupoUrl, ogmiosUrl })`.

Choose this over Yaci DevKit when you want the devnet managed from inside integration tests; choose Yaci DevKit for its visual block explorer and Blockfrost-compatible REST API. Both run a standard `cardano-node`, so chain behaviour is identical.

### Step 3c: Set up a Dingo devnet (all-Go network, fast epochs)

Reach for this when what you are testing is node-side rather than dApp-side:
consensus, block diffusion, mempool behaviour, or how your service reacts to
epoch boundaries. Yaci DevKit remains the better default for ordinary dApp
integration work, because it ships a Blockfrost-compatible API and a block
explorer aimed at that job.

**What the default profile runs** — a private all-Dingo network: three Dingo
block producers, one Dingo relay, and `txpump` feeding transactions into the
mempool. Passing `--conformance` instead runs Dingo beside `cardano-node`, which
is the configuration to use when you care whether both implementations agree.

**Prerequisites**: Docker with the Compose plugin, and Go 1.26+.

**Why the fast parameters matter.** The devnet uses 1-second slots and 500-slot
epochs — roughly eight minutes per epoch — with `activeSlotsCoeff=0.4` and
`k=40`. Epoch transitions, leader election, and stake-snapshot rotation all
become observable in minutes, which is the thing a public testnet cannot give
you. If your code has epoch-boundary logic, this is where to exercise it.

For quick iteration without Docker, `devmode.sh` runs a single Dingo node
against a local devnet genesis, resetting state and refreshing genesis
timestamps on each run.

**Scope caveat.** Dingo's own README places it on testnets and devnets only, not
mainnet with real funds. For devnet work that is the intended envelope rather
than a limitation, but do not let a Dingo-only devnet be your last check before
mainnet — validate against `cardano-node` too, which is what `--conformance`
exists for.

### Step 4: Set up local chain indexers

If your application needs Ogmios/Kupo (e.g. for Evolution SDK's `.withKupmios`),
use the DevKit's built-in services instead of hand-run containers:

```bash
# Inside Yaci CLI
yaci-cli:> enable-kupomios

# Or in the DevKit's config/env
ogmios_enabled=true
kupo_enabled=true
```

Ogmios serves `ws://localhost:1337`, Kupo `http://localhost:1442`. Since DevKit
v0.12.0-beta5, Yaci Store evaluates scripts with `scalus` when Ogmios is not
running — Ogmios is optional for transaction evaluation. For standalone (non-DevKit)
setups, see `docs/sources/ogmios/` and `docs/sources/kupo/`.

### Step 5: Smart contract workflow

#### Aiken build-and-exercise cycle

1. **Build**: `aiken build` compiles validators to UPLC
2. **Generate blueprint**: Produces `plutus.json` with compiled scripts and parameter schemas
3. **Lock**: Use an off-chain SDK (Mesh, Evolution SDK, PyCardano, cardano-client-lib) to
   read the blueprint, derive the script address, and pay to it with a datum
4. **Spend**: Build a spending transaction that attaches the validator and a redeemer,
   submit to the local devnet, query results, iterate

There is **no deployment step** on Cardano. A validator is not installed on-chain
ahead of time — it travels in the witness set of the transaction that spends from it.
Publishing a script into a UTxO's `script_ref` (CIP-33) is an optional optimization for
large, frequently-spent validators, not a prerequisite; see `optimize-validator`.

```bash
# Typical Aiken workflow
aiken build
aiken check        # Run unit tests
# Then use an SDK to lock to, and spend from, the script on the local devnet
```

#### Test structure

- **Unit tests**: Aiken's built-in `test` keyword for validator logic
- **Integration tests**: Off-chain SDK scripts against local devnet
- **Property tests**: Aiken's `fuzz` support for property-based testing
- **End-to-end**: Full workflow tests against Preview testnet

### Step 6: Connect to public testnets

#### Preview testnet

- **Purpose**: Testing new features, faster epoch transitions
- **Faucet**: https://docs.cardano.org/cardano-testnets/tools/faucet/
- **Network magic**: 2
- **Configuration files**: Download from https://book.play.dev.cardano.org/environments.html

#### Preprod testnet

- **Purpose**: Pre-production testing, mirrors mainnet parameters
- **Faucet**: Same faucet site, select Preprod
- **Network magic**: 1
- **Configuration files**: Same source as Preview

#### Getting test ADA

```bash
# Request test ADA from the faucet (web interface or API)
# Provide your testnet address
# Dispenses ~10,000 test ADA per request (same on Preview and Preprod)
# Faucet is rate-limited per address/API key
```

### Step 7: CI integration

#### GitHub Actions example

```yaml
# .github/workflows/cardano-ci.yml
name: Cardano CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Aiken
        uses: aiken-lang/setup-aiken@v1
      - name: Build contracts
        run: aiken build
      - name: Run unit tests
        run: aiken check
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
      - name: Install Yaci DevKit
        run: npm install -g @bloxbean/yaci-devkit
      - name: Start a devnet
        run: |
          nohup yaci-devkit up --enable-yaci-store &
          # poll http://localhost:8080 until the Yaci Store API answers
      - name: Run integration tests
        run: |
          # Run off-chain integration tests against localhost:8080
```

#### Key CI considerations

- Install the Yaci DevKit npm package and start the devnet in a background step (`yaci-devkit up`)
- Cache Aiken build artifacts
- Run unit tests first (fast), then integration tests (slower)
- Use deterministic wallet keys for reproducible tests
- Clean devnet state between test suites if needed

### Step 8: Troubleshooting common issues

- **Docker not starting**: Check Docker daemon is running, ports not in use
- **Node not syncing**: For local devnet, check logs inside container
- **Transactions failing**: Verify era matches (Babbage vs Conway), check collateral
- **Slow block production**: Adjust slot length in devnet config
- **Out of test ADA**: Re-create devnet (local) or use faucet (testnet)
- **cardano-cli version mismatch**: Match CLI version to node version in the devnet

## References

- `skills/setup-devnet/references/yaci-devkit-quickstart.md` -- Yaci DevKit quickstart guide
- `skills/setup-devnet/references/evolution-sdk-devnet.md` -- Evolution SDK devnet quickstart guide
- Yaci DevKit: https://github.com/bloxbean/yaci-devkit
- Evolution SDK devnet: https://github.com/IntersectMBO/evolution-sdk
- Cardano testnets: https://docs.cardano.org/cardano-testnets/
- Aiken: https://aiken-lang.org
- Ogmios: https://ogmios.dev
- Kupo: https://cardanosolutions.github.io/kupo
