# Cardano Developer Ecosystem Map

Comprehensive map of tools, SDKs, and infrastructure in the Cardano developer ecosystem.

## Smart Contract Languages

| Name | Base Language | Status | Adoption | Best For |
|---|---|---|---|---|
| **Aiken** | Own (Rust-like) | Production | High | Most new smart contract projects. Fast compilation, great DX. |
| **Plinth (formerly Plutus Tx)** | Haskell | Production | High | Haskell teams, complex on-chain logic, academic rigor. |
| **OpShin** | Python | Production | Medium | Python developers wanting to write validators in Python. |
| **Pebble** | TypeScript | Production | Medium | TypeScript devs wanting on-chain + off-chain in one language (`@harmoniclabs/pebble`, successor of Plu-ts). |
| **Scalus** | Scala | Production | Low | JVM/Scala teams. |
| **Helios** | Own (JS-like) | Production | Medium | Quick prototyping, simple validators. |
| **Plutarch** | Haskell (eDSL) | Production | Medium | Performance-optimized Plutus, Haskell experts. |

## Off-Chain SDKs

### TypeScript / JavaScript

| Name | Status | Adoption | Best For |
|---|---|---|---|
| **Mesh SDK** | Production | High | Full-stack dApp dev, beginners, React integration, comprehensive API. |
| **Evolution SDK** | Production | High | IntersectMBO's canonical Lucid-lineage successor. Type-safe, Effect-based composable tx building. Staged-builder API (`Client.make(...).withBlockfrost(...).newTx().payToAddress(...).build()`). Modern DX. |
| **Blaze** | Production | Medium | Modular, lightweight alternative. Multiple provider backends. |
| **cardano-js-sdk** | Production | Medium | Lace wallet ecosystem, full node interaction, enterprise use. |
| **Cardano Multiplatform Lib** | Production | Medium | Low-level serialization, cross-platform WASM. |

### Python

| Name | Status | Adoption | Best For |
|---|---|---|---|
| **PyCardano** | Production | High | Python backends, scripting, data science, prototyping. |

### Rust

| Name | Status | Adoption | Best For |
|---|---|---|---|
| **whisky** | Production | Low | dApp transaction building (Mesh-like API; SIDAN Lab, young project). |
| **Pallas** | Production | High | Low-level building blocks: network protocols, ledger primitives, indexers. Foundation of Dolos/Oura/Amaru; not an app-dev tx builder. |
| **Cardano Serialization Lib** | Production | Medium | Serialization/deserialization, WASM targets. |

### Java / Kotlin

| Name | Status | Adoption | Best For |
|---|---|---|---|
| **Cardano Java Client Lib** | Production | Medium | JVM backends, Android, enterprise Java. |
| **Yaci** | Production | Medium | Java mini-protocols, low-level node interaction. |

### Go

| Name | Status | Adoption | Best For |
|---|---|---|---|
| **gOuroboros** | Production | Low | Low-level building blocks: mini-protocol implementations, ledger types, CBOR codecs. Go counterpart to Pallas; not an app-dev tx builder. |
| **Apollo** | Production | Low | Go tx building. Fluent builder with pluggable Blockfrost/Maestro/Ogmios/UTxORPC backends. |
| **blockfrost-go** | Production | Low | Official Go client for the Blockfrost REST API; also IPFS and webhook signature verification. |
| **UTxORPC Go SDK** | Production | Low | Provider-agnostic chain sync/query/submit over gRPC. Swap backends without rewriting calls. |

### C# / .NET

| Name | Status | Adoption | Best For |
|---|---|---|---|
| **CardanoSharp** | Production | Low | .NET backends, Unity game development. |
| **Chrysalis** | Experimental | Low | .NET Cardano integration. |

### Haskell

| Name | Status | Adoption | Best For |
|---|---|---|---|
| **cardano-ledger** (`cardano-ledger-api`, era packages) | Production | High (node/wallet/Hydra) | Off-chain txs in the same types the ledger validates. Pair with Aiken blueprints. |
| **CHaP** | Production | High | Cabal index for Intersect Haskell packages that are not on Hackage. |
| **haskell.nix** | Production | High (every Intersect Haskell repo) | Nix frontend: flakes, CHaP `inputMap`, `--sha256` on `source-repository-package`. |
| **iohk-nix** | Production | High | Crypto overlays (`crypto`, `haskell-nix-crypto`) so `cardano-crypto-class` / `plutus-core` find libsodium-vrf, secp256k1, libblst. |
| **cardano-api** | Production | High | Client façade over ledger/consensus/network when you do not want raw ledger types. |
| **Atlas** | Maintenance unclear | Medium (historical) | PAB-style Haskell backend. Last commit 2026-02; not a registered source. |

### Interface-driven (language-agnostic)

| Name | Status | Adoption | Best For |
|---|---|---|---|
| **Tx3** | Beta (pre-1.0) | Low | A different model from the SDKs above: instead of building transactions imperatively in one language, you declare a protocol's transactions in a `.tx3` interface file (like an OpenAPI/ABI for UTxO protocols) and generate typed clients in TypeScript, Rust, Go, or Python. Fits teams shipping the same protocol across several languages, or publishing a protocol others integrate against. Toolchain: `trix` CLI, TII/TIR artifacts. By TxPipe. |

## Infrastructure - Data Providers

| Name | Type | Protocol | Status | Adoption | Best For |
|---|---|---|---|---|---|
| **Blockfrost** | Hosted | REST | Production | High | Quick start, frontend dApps, no infra management. |
| **Koios** | Hosted (community) | REST | Production | High | Free tier, open source, community-maintained. |
| **Ogmios** | Self-hosted | WebSocket | Production | High | Low-latency, tx submission, paired with Kupo. |
| **Kupo** | Self-hosted | REST | Production | High | UTxO indexing by pattern, datum resolution. |
| **DB-Sync** | Self-hosted | SQL | Production | High | Full chain in PostgreSQL, analytics, reporting. |
| **Oura** | Self-hosted | Pipeline | Production | Medium | Event streaming, Kafka/Elastic/webhooks. |
| **Adder** | Self-hosted | Pipeline | Production | Low | Event streaming in Go — chainsync/mempool inputs, webhook/push/notify outputs. Embeddable as a library, so a Go service can consume events in-process. |
| **Cardano GraphQL** | Self-hosted | GraphQL | Production | Medium | Complex queries, relationship traversal. |
| **Scrolls** | Self-hosted | Various | Production | Low | Lightweight chain indexer, key-value projections. |
| **Carp** | Self-hosted | REST | Production | Low | Lightweight indexer, specific query patterns. |

## Infrastructure - Node & Network

| Name | Status | Best For |
|---|---|---|
| **cardano-node** | Production | Running a full Cardano node. Required for SPOs and self-hosted infra. |
| **Dolos** | Experimental | Lightweight data-only node (no block production). Faster sync. |
| **Amaru** | Experimental | Alternative node implementation in Rust. |
| **Dingo** | Experimental | Alternative node implementation in Go, with UTxORPC, Blockfrost-compatible REST, and Mesh APIs served by the node itself. Block production is exercised on public testnets; its README rules out mainnet. |
| **Mithril** | Production | Fast bootstrapping via snapshot certificates. Sync in minutes, not days. |

## Testing

| Name | Type | Status | Best For |
|---|---|---|---|
| **Aiken built-in** | Unit + property tests | Production | Validator logic testing with `test` and `fuzz`. |
| **Yaci DevKit** | Local devnet | Production | Integration testing, full tx lifecycle. |
| **Preview testnet** | Public testnet | Production | Shared-state testing, new features. |
| **Preprod testnet** | Public testnet | Production | Pre-production, mainnet-mirroring params. |
| **SanchoNet** | Governance testnet | Production | Governance-specific testing. |
| **tx-village** | Tx testing framework | Experimental | Transaction-level testing. |
| **Plutip** | Local cluster | Production | Haskell-based local cluster testing. |

## Governance Tools

| Name | Status | Best For |
|---|---|---|
| **GovTool** | Production | Web UI for DRep registration, voting, delegation. |
| **cardano-cli (Conway)** | Production | CLI governance operations. |
| **SanchoNet** | Production | Governance testnet for practice. |
| **Intersect tools** | Production | Constitutional Committee and governance coordination. |

## Scaling Solutions

| Name | Type | Status | Best For / notes |
|---|---|---|---|
| **Hydra Head** | Isomorphic state channel (L2) | Production | A known, fixed set of parties transacting at high frequency among themselves, where all parties run a node and stay online. Same tx format and ledger rules as L1 (isomorphic). |
| **Mithril** | Snapshot certificates | Production | Fast node bootstrap and light-client sync — not tx throughput. |
| **Partner Chains** | Sidechains | Experimental | Custom app-specific chains anchored to Cardano. |
| **Input Endorsers (Leios)** | L1 scaling | Research | Future L1 throughput improvements; not a tool you integrate today. |
| **Midgard** | Optimistic rollup | Experimental | L2 without a fixed participant set. Frontier; **not a bundled source** — verify upstream, don't build production on it yet. |
| **Gummiworm** | Validium-style L2 | Experimental | Off-chain data-availability L2. Not mainnet-ready; not bundled. |

## Zero-Knowledge & BLS12-381

On-chain proof verification and the wider BLS12-381 primitive family. The BLS12-381 builtins sit on
the audited `blst` library; the higher-level libraries below are open source and, per the developer
portal, none are audited. For the concepts and working examples, use the `explain-zk` skill. Notes
below carry only facts (language, license) and a project's own stated caveats.

### Proof systems: circuit frontends, verifiers, toolkits

| Name | Language | Notes |
|---|---|---|
| **cardano-foundation/bls** | Aiken | Apache-2.0. Generic Groth16 verifier plus BLS signature / VRF / KDF examples; proving steps cross-checked against an independent SageMath implementation. Bundled as a source: `docs/sources/bls12-381-examples-and-standards/`, including the IETF drafts and RFCs under `standards/`. |
| **gnark-cardano** | Go | gnark circuit to a tested Aiken Groth16 verifier; the most automated path. |
| **snarkjs-cardano** | TS/JS | Circom (Groth16 / PLONK) adapted to BLS12-381 output for Plutus verifiers. |
| **plutus-halo2-verifier-gen** | Rust to Plinth/Aiken | Generates Halo2 / KZG verifiers; the path for verifying Midnight proofs. |
| **plutus-plonk-example** | Plutus | End-to-end PLONK verifier with published cost benchmarks. |
| **ak-381** (Modulo-P) | Aiken | Groth16 verifier with Circom conversion scripts; the repository ships no license. |
| **adaocommunity/zk** | Aiken | Apache-2.0. Groth16, PLONK, and Bulletproofs (range proof) verifiers for Plutus V3, with protocol walkthroughs and negative-path tests; the README emphasises educational/demonstrative use, states PLONK is still being optimized to fit resource limits, and marks Bulletproofs early-stage; no external audit. Bundled as a source: `docs/sources/aiken-zkp-verifiers/`. |
| **ZeroJ** (bloxbean) | Java | Full Java ZK pipeline with generated Plutus V3 verifiers; the authors state the code is AI-generated and not for production. |

### BLS-family libraries and learning

| Name | Language | Notes |
|---|---|---|
| **ilap/bls** | Aiken | Apache-2.0. IETF BLS signatures with the three modes (basic / aug / pop). Bundled as a source: `docs/sources/aiken-bls-signatures/`. |
| **lambdasistemi/cardano-bbs** | Aiken | BBS+ selective-disclosure / anonymous credentials. |
| **ZK-from-zero-on-Cardano** | eBook + Aiken | Catalyst Fund 14; the README marks its status "in progress". A Circom-to-Aiken walkthrough ending in a password-locked UTxO. |

## Wallet Connectors

| Name | Type | Status | Best For |
|---|---|---|---|
| **CIP-30** | Browser standard | Production | Connecting browser extension wallets to dApps. |
| **CIP-95** | Governance extension | Production | Governance actions in wallets (extends CIP-30). |
| **Mesh SDK wallet hooks** | React library | Production | React-based dApp wallet integration. |
| **WalletConnect** | Mobile bridge | Production | Mobile wallet connection. |
| **CIP-45** | Peer-to-peer DApp connector | Production | Decentralized wallet-dApp connection. |

## Popular Wallets (for developer testing)

| Name | Type | CIP-30 | CIP-95 |
|---|---|---|---|
| **Eternl** | Browser extension | Yes | Yes |
| **Lace** | Browser extension | Yes | Yes |
| **Nami** | Browser extension | Yes | Partial |
| **Flint** | Browser extension | Yes | Yes |
| **Vespr** | Mobile + extension | Yes | Yes |
| **Typhon** | Browser extension | Yes | Yes |
| **GeroWallet** | Browser extension | Yes | Partial |

## Metadata & Standards

| CIP | Name | Purpose |
|---|---|---|
| CIP-25 | NFT Metadata | Standard for NFT metadata on Cardano |
| CIP-30 | Wallet Bridge | dApp-wallet web bridge standard |
| CIP-57 | Blueprints | Plutus contract blueprint specification |
| CIP-68 | Rich Tokens | Datum-based token metadata (FTs, NFTs, RFTs) |
| CIP-95 | Governance Wallet | Governance extensions for CIP-30 |
| CIP-1694 | Governance | On-chain governance mechanism |
| CIP-1854 | Multi-sig | Multi-signature wallet standard |

## Developer Resources

| Resource | URL | Description |
|---|---|---|
| Cardano Developer Portal | developers.cardano.org | Official developer docs and guides |
| Aiken documentation | aiken-lang.org | Smart contract language docs |
| Cardano Docs | docs.cardano.org | Core Cardano documentation |
| CIPs repository | github.com/cardano-foundation/CIPs | All Cardano Improvement Proposals |
| Cardano Forum | forum.cardano.org | Community discussion |
| Cardano Stack Exchange | cardano.stackexchange.com | Q&A for developers |
