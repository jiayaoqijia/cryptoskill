---
name: suggest-tooling
description: >-
  Recommends Cardano developer tools and SDKs for a specific project. Triggers: "which SDK", "recommend tools", "best library for", "Cardano SDK", "Mesh vs Evolution SDK", "Aiken vs Plutus", "what tools should I use", "Cardano ecosystem", "haskell.nix", "CHaP", "cardano-ledger off-chain", "Haskell Cardano stack", "Cardano in Go".
allowed-tools: Read Grep Glob
disallowed-tools: Bash Edit Write WebFetch WebSearch
---

<!-- Documentation lookup path: ${CLAUDE_SKILL_DIR}/../../docs/sources/ -->

# Suggest Cardano Tooling

Help the developer choose the right tools, SDKs, and libraries for their Cardano project based on their requirements and preferred programming language.

## When to use

- Developer is starting a new Cardano project and needs tool recommendations
- Comparing SDKs (Mesh vs Evolution SDK vs PyCardano vs others)
- Choosing a smart contract language (Aiken vs Plutus vs others)
- Picking a Haskell off-chain stack (cardano-ledger + CHaP + haskell.nix)
- Selecting infrastructure components (indexers, APIs, testing tools)
- Evaluating wallet integration options
- Understanding which CIPs are relevant to their project
- Deciding whether a project needs Layer 2 / scaling (Hydra) or can stay on L1

## When NOT to use

- Already chosen tools and needs help using them (use specific tool skills)
- Building a transaction once the stack is chosen (use `build-transaction`)
- Setting up a devnet (use `setup-devnet` skill)
- Querying chain data with a specific provider (use `query-chain` skill)
- Detailed wallet integration steps (use `connect-wallet` skill)

## Key principles

1. **Start from the project requirements, not the tools.** Understand what they are building before recommending.
2. **Language preference matters.** A Python developer should know about PyCardano; a TypeScript developer about Mesh and Evolution SDK; a Haskell developer about cardano-ledger, CHaP, and haskell.nix.
3. **Recommend production-ready tools first.** Flag experimental tools clearly.
4. **Fewer tools is better.** Do not recommend 10 options when 2 will do.
5. **Consider the full stack.** Smart contracts, off-chain code, infrastructure, testing, and deployment are all part of the picture.

## Workflow

### Step 1: Understand the project

Ask the developer (if not already clear):

- **What are you building?** (dApp, DeFi protocol, NFT platform, governance tool, data analytics, wallet, library)
- **What programming language(s) do you prefer?**
- **Do you need smart contracts?** If yes, how complex?
- **What is your deployment target?** (mainnet, testnet, local devnet)
- **What is your experience level with Cardano?** (new, intermediate, advanced)
- **Any existing infrastructure?** (running a node, using hosted APIs)
- **Do you require high throughput, sub-second-finality, or any other requirement that L1 is not fit to handle?** (micro-payments, sub-second-finality, etc.)

### Step 2: Search Bundled Documentation

Search the bundled documentation for relevant content:
- `${CLAUDE_SKILL_DIR}/../../docs/sources/mesh-sdk/` - Mesh SDK docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/evolution-sdk/` - Evolution SDK docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/aiken/` - Aiken language docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/ogmios/` - Ogmios WebSocket bridge docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/blockfrost-openapi/` - Blockfrost API docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/hydra/` - Hydra (Layer 2 state channels) docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/tx3/` - Tx3 interface DSL and toolchain docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/chap/` - CHaP (Cabal index + haskell.nix inputMap)
- `${CLAUDE_SKILL_DIR}/../../docs/sources/haskell-nix/` - haskell.nix flakes and source-repository-package hashes
- `${CLAUDE_SKILL_DIR}/../../docs/sources/iohk-nix/` - crypto overlays (libsodium-vrf, libblst)
- `${CLAUDE_SKILL_DIR}/../../docs/sources/cardano-ledger/` - ledger types and Conway tx validation
- `${CLAUDE_SKILL_DIR}/../../docs/sources/apollo/` - Apollo (Go) tx builder docs and API source
- `${CLAUDE_SKILL_DIR}/../../docs/sources/gouroboros/` - gOuroboros (Go) protocol and ledger API source

Go sources mirror `.go` files, so their API reference is the doc comment above each exported identifier. Start with a package's `doc.go` for the overview, then `Grep` a type or function name rather than looking for a prose manual.

### Step 3: Search the ecosystem map

Reference the ecosystem map for the full landscape:

```
File: skills/suggest-tooling/references/ecosystem-map.md
```

### Step 4: Recommend by category

#### Smart Contract Languages

| Language | Best for | Language base | Status |
|---|---|---|---|
| **Aiken** | Most new projects, performance-critical validators | Own syntax (Rust-like) | Production |
| **Plinth (formerly Plutus Tx)** | Haskell teams, complex on-chain logic | Haskell | Production |
| **OpShin** | Python developers writing validators | Python | Production |
| **Pebble** | TypeScript developers wanting on-chain code in TS (`@harmoniclabs/pebble`, successor of Plu-ts) | TypeScript | Production |
| **Scalus** | Scala/JVM teams | Scala | Production |
| **Helios** | Simple validators, quick prototyping | Own syntax (JS-like) | Production |

**Default recommendation**: Aiken. Best tooling, fastest compilation, growing community, excellent documentation. Unless the team has a strong reason to use another language.

#### Off-Chain SDKs

| SDK | Language | Best for | Status |
|---|---|---|---|
| **Mesh SDK** | TypeScript/JS | Full-stack dApp development, beginners | Production |
| **Evolution SDK** | TypeScript/JS | IntersectMBO's canonical Lucid-lineage successor. Type-safe, Effect-based composable tx building (`Client.make(...).withBlockfrost(...).newTx().payToAddress(...).build()`) | Production |
| **PyCardano** | Python | Python backends, scripting, data science | Production |
| **Cardano CLI** | Shell | DevOps, scripting, node operators | Production |
| **cardano-js-sdk** | TypeScript | Lace wallet ecosystem, full node interaction | Production |
| **Blaze** | TypeScript | Lightweight, modular tx building | Production |
| **Cardano Java Client Lib** | Java/Kotlin | JVM backends, Android | Production |
| **whisky** | Rust | Transaction building for dApps (Mesh-like API; young project by SIDAN Lab) | Production |
| **Pallas** | Rust | Low-level building blocks: network protocols, ledger primitives, indexers (foundation of Dolos, Oura, Amaru) | Production |
| **Tx3** | DSL → TS/Rust/Go/Python | Interface-driven alternative: declare a protocol's transactions in a `.tx3` file, generate typed clients across languages (like an ABI/OpenAPI for UTxO protocols). Good for multi-language teams or publishing a protocol others integrate. TxPipe. | Beta (pre-1.0) |
| **cardano-ledger** | Haskell | Era types and Conway tx construction (`cardano-ledger-api`, `cardano-ledger-conway`, `plutus-tx` for `ToData`/`FromData`). Same types the node validates. Built with **haskell.nix** + **CHaP**, not cabal-on-system-GHC. | Production |
| **cardano-api** | Haskell | Client façade over ledger/consensus/network. Use when you want that wrapper; not required if you already speak ledger types. | Production |
| **Atlas** | Haskell | Higher-level PAB-style backend. Last library commit 2026-02; fails this repo's 6-month source bar. Mention only; do not start a new project on it. | Maintenance unclear |
| **Apollo** | Go | Go backends and services: fluent tx building, pluggable chain backends (Blockfrost/Maestro/Ogmios/UTxORPC) | Production |
| **gOuroboros** | Go | Low-level building blocks: mini-protocol implementations, ledger types, CBOR codecs (Go counterpart to Pallas) | Production |

**Default recommendation by language**:
- TypeScript/JavaScript: **Mesh SDK** (comprehensive, well-documented, great for beginners) or **Evolution SDK** (type-safe, Effect-based composable builder)
- Python: **PyCardano**
- Rust: **Pallas**
- Java/Kotlin: **Cardano Java Client Lib**
- Haskell: **cardano-ledger** via **haskell.nix** + **CHaP**. On-chain default stays **Aiken** (CIP-57 `plutus.json`); do not switch to Plinth unless the team is writing validators in Haskell. Search `docs/sources/chap/README.md` for the repository stanza and `inputMap`.
- Go: **Apollo** for transaction building, **gOuroboros** for protocol and ledger primitives

Go adoption is lower than TypeScript or Python, so expect fewer tutorials and smaller communities. Weigh that against an existing Go backend: rewriting a service in TypeScript to gain SDK maturity is rarely the cheaper trade.

#### Infrastructure

| Tool | Purpose | Type |
|---|---|---|
| **Blockfrost** | Chain data API | Hosted |
| **Koios** | Chain data API | Hosted (community) |
| **Ogmios** | Node WebSocket bridge | Self-hosted |
| **Kupo** | UTxO indexer | Self-hosted |
| **DB-Sync** | Full chain PostgreSQL | Self-hosted |
| **Oura** | Event pipeline | Self-hosted |
| **Adder** | Event pipeline (Go, embeddable) | Self-hosted |
| **Dingo** | Go node + UTxORPC/Blockfrost/Mesh APIs (pre-production) | Self-hosted |
| **Yaci DevKit** | Local devnet | Self-hosted |

**Default recommendation**: Blockfrost for getting started (easy, hosted). Ogmios + Kupo for production self-hosted.

#### Scaling / Layer 2

**Most projects do not need Layer 2.** Cardano L1 handles the large majority of dApp workloads. Reach for L2 only against a *specific, confirmed* throughput or latency requirement L1 cannot meet and validate that the requirement is real before recommending it. **If there's a posibility of needing an L2, hand off the decision to the `suggest-scalability` skill.**

#### Testing

| Tool | Purpose |
|---|---|
| **Aiken built-in tests** | Unit and property tests for Aiken validators |
| **Yaci DevKit** | Local devnet for integration tests |
| **Preview testnet** | Public testnet with frequent hard forks |
| **Preprod testnet** | Public testnet mirroring mainnet |
| **tx-village** | Transaction-level testing framework |

#### Wallet Integration

| Tool | Purpose |
|---|---|
| **Mesh SDK** | React hooks and components for wallet connection |
| **CIP-30 direct** | Vanilla JS wallet connection |
| **CIP-95** | Governance extensions for wallets |
| **WalletConnect** | Mobile wallet connection |

### Step 5: Recommend a stack

Based on the project requirements, recommend a concrete stack. Example stacks:

#### Beginner dApp (TypeScript)
- Smart contracts: **Aiken**
- Off-chain: **Mesh SDK**
- Infrastructure: **Blockfrost**
- Testing: Aiken tests + Yaci DevKit
- Wallet: Mesh wallet hooks

#### DeFi Protocol (TypeScript, advanced)
- Smart contracts: **Aiken**
- Off-chain: **Evolution SDK** or **Blaze**
- Infrastructure: **Ogmios + Kupo** (self-hosted)
- Testing: Aiken property tests + Preview testnet
- Wallet: CIP-30 direct integration

#### Python Backend
- Smart contracts: **Aiken** (or OpShin if team prefers Python on-chain too)
- Off-chain: **PyCardano**
- Infrastructure: **Blockfrost** or **Koios**
- Testing: Aiken tests + pytest with PyCardano

#### Go Backend
- Smart contracts: **Aiken**
- Off-chain: **Apollo** for tx building, **gOuroboros** for ledger types and direct node protocols
- Infrastructure: **blockfrost-go** (hosted) or **UTxORPC Go SDK** (provider-agnostic gRPC)
- Testing: Aiken tests + Go `testing` against Yaci DevKit

#### Data Analytics Platform
- Infrastructure: **DB-Sync** (SQL) + **Oura** (streaming)
- Language: Python or SQL
- No smart contracts needed

#### Governance Tool
- Off-chain: **Mesh SDK** (CIP-95 support)
- Infrastructure: **Blockfrost** or **Koios** (governance endpoints)
- Wallet: CIP-30 + CIP-95
- Reference: CIP-1694 for governance actions

#### Haskell service (Aiken on-chain, ledger off-chain)
- Smart contracts: **Aiken** → CIP-57 `plutus.json`
- Off-chain: **cardano-ledger-*** + `plutus-tx` / `plutus-ledger-api`
- Build: **haskell.nix** flake, **CHaP** `inputMap`, **iohk-nix** `crypto` + `haskell-nix-crypto` overlays (CHaP README: those overlays supply `libblst` and friends)
- Pin: dual `index-state` (Hackage + `cardano-haskell-packages`); align the CHaP flake input to a `cardano-node` release
- Then hand off to `build-transaction` (SDK `cardano-ledger`)

### Step 6: Mention relevant CIPs

Based on the project type, flag relevant CIPs:

| Project type | Relevant CIPs |
|---|---|
| Any dApp | CIP-30 (wallet bridge), CIP-57 (blueprints) |
| Token/NFT | CIP-25 (NFT metadata), CIP-68 (rich FTs/NFTs) |
| Governance | CIP-1694 (governance), CIP-95 (wallet governance) |
| Multi-sig | CIP-1854 (multi-sig wallets) |
| Metadata | CIP-20 (tx metadata), CIP-25 (NFT metadata) |
| DEX | CIP-35 (on-chain message signing) |

### Step 7: Flag trade-offs

For each recommendation, briefly note:

- **Maturity**: How battle-tested is this tool?
- **Community**: Size and responsiveness of the community
- **Documentation**: Quality and completeness
- **Maintenance**: Is it actively maintained? Who maintains it?
- **Lock-in**: How easy is it to switch later?

## References

- `skills/suggest-tooling/references/ecosystem-map.md` -- Full ecosystem map with all tools
- Cardano developer portal: https://developers.cardano.org
- Aiken: https://aiken-lang.org
- Mesh SDK: https://meshjs.dev
- Evolution SDK: https://github.com/IntersectMBO/evolution-sdk (docs: https://evolution-sdk.dev)
- PyCardano: https://pycardano.readthedocs.io
- Blockfrost: https://blockfrost.io
- Apollo (Go): https://pkg.go.dev/github.com/Salvionied/apollo/v2
- gOuroboros (Go): https://pkg.go.dev/github.com/blinklabs-io/gouroboros
