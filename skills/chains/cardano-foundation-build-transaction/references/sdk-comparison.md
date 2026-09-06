# Cardano Off-Chain SDK Comparison

Quick reference for choosing and using Cardano transaction-building SDKs.

## Overview

| SDK | Language | Level | Maintenance | Best For |
|-----|----------|-------|-------------|----------|
| Mesh SDK | TypeScript/JS | High | Active | Web dApps, rapid prototyping |
| Evolution SDK | TypeScript | High | Active | Type-safe composable txs |
| PyCardano | Python | Mid | Active | Python backends, scripting |
| cardano-client-lib | Java | Mid-Low | Active | JVM fine-grained control |
| Apollo | Go | Mid | Active | Go backends, Conway-era certs |
| cardano-js-sdk | TypeScript | Low-Mid | IOG-maintained | Full-stack TS, Lace wallet |
| Cardano Serialization Lib | Rust/WASM | Low | IOG-maintained | Custom tooling, performance |
| Tx3 | DSL -> TS/Rust/Go/Python | High/Declarative | Active (pre-1.0) | Multi-language teams, published protocols |
| cardano-ledger | Haskell | Low (ledger types) | Active (Intersect) | Haskell services; same types as the node |

## Mesh SDK

- **Language:** TypeScript / JavaScript
- **Repository:** github.com/MeshJS/mesh
- **Documentation:** meshjs.dev (comprehensive guides and examples)

**Strengths:**
- Highest-level API -- fewest lines of code to build transactions
- Built-in wallet connectors for browser wallets (CIP-30)
- React hooks and components for dApp frontends
- Strong community and documentation
- Supports Plutus V1, V2, and V3

**Weaknesses:**
- Abstractions can hide details needed for complex transactions
- Tied to the JavaScript ecosystem
- Some edge cases require dropping to lower-level APIs

**Installation:**
```bash
npm install @meshsdk/core
```

**Basic send-ADA pattern:**
```typescript
import { MeshTxBuilder, BlockfrostProvider } from "@meshsdk/core";

const provider = new BlockfrostProvider("YOUR_KEY");
const txBuilder = new MeshTxBuilder({ fetcher: provider, submitter: provider });

const unsignedTx = await txBuilder
  .txOut(recipient, [{ unit: "lovelace", quantity: "5000000" }])
  .changeAddress(sender)
  .selectUtxosFrom(utxos)
  .complete();
```

---

## Evolution SDK

- **Language:** TypeScript
- **Repository:** github.com/IntersectMBO/evolution-sdk
- **Documentation:** evolution-sdk.dev (detailed with examples)

**Strengths:**
- Effect-TS based, type-safe composable API
- Built-in Blockfrost, Koios, Kupmios, and Maestro providers
- Supports Plutus V1, V2, V3 and native scripts
- Works in Node.js and browser environments
- Declarative, chainable transaction builder

**Weaknesses:**
- Newer SDK, smaller community than Mesh
- Effect-TS paradigm has a learning curve
- Fewer tutorials and third-party guides

**Installation:**
```bash
npm install @evolution-sdk/evolution
```

**Basic send-ADA pattern:**
```typescript
import { Address, Assets, preprod, Client } from "@evolution-sdk/evolution"

const client = Client.make(preprod)
  .withBlockfrost({
    baseUrl: "https://cardano-preprod.blockfrost.io/api/v0",
    projectId: process.env.BLOCKFROST_API_KEY!
  })
  .withSeed({ mnemonic: process.env.WALLET_MNEMONIC!, accountIndex: 0 })

const tx = await client
  .newTx()
  .payToAddress({
    address: Address.fromBech32("addr_test1..."),
    assets: Assets.fromLovelace(5_000_000n)
  })
  .build()

const signed = await tx.sign()
const txHash = await signed.submit()
```

---

## PyCardano

- **Language:** Python
- **Repository:** github.com/Python-Cardano/pycardano
- **Documentation:** pycardano.readthedocs.io

**Strengths:**
- Pythonic API, easy to learn
- Good for scripting and automation
- Supports Plutus V1, V2, and V3
- Built-in Blockfrost and Ogmios chain context
- Solid datum/redeemer serialization

**Weaknesses:**
- Smaller ecosystem than TypeScript options
- Fewer high-level abstractions than Mesh
- No built-in browser wallet support (server-side only)

**Installation:**
```bash
pip install pycardano
```

**Basic send-ADA pattern:**
```python
from pycardano import (
    BlockFrostChainContext, TransactionBuilder,
    TransactionOutput, Address
)

context = BlockFrostChainContext("YOUR_KEY", base_url="https://cardano-preview.blockfrost.io/api")
builder = TransactionBuilder(context)
builder.add_input_address(sender_address)
builder.add_output(TransactionOutput(recipient_address, 5_000_000))

signed_tx = builder.build_and_sign(
    signing_keys=[payment_skey],
    change_address=sender_address
)
context.submit_tx(signed_tx)
```

---

## Apollo

- **Language:** Go
- **Repository:** github.com/Salvionied/apollo
- **Module path:** github.com/Salvionied/apollo/v2
- **Documentation:** pkg.go.dev/github.com/Salvionied/apollo/v2

**Strengths:**
- Only maintained fluent transaction builder for Go
- Pluggable chain backends: Blockfrost, Maestro, Ogmios, UTxORPC, fixed/cached
- Broad Conway coverage: DRep registration, votes, proposals, treasury donations
- Shares gOuroboros ledger types, so Go services can pass `common.Address` and
  ledger structs between tx building and node communication without conversion
- Plutus datum encoding via `plutusencoder`, plus script attachment helpers

**Weaknesses:**
- Small community relative to TypeScript and Python options; few tutorials
- Mixed return conventions: fallible builder steps return `(*Apollo, error)`
  while state-only steps return a bare `*Apollo`, so a chain breaks wherever a
  fallible step appears
- No browser wallet support (server-side only)

**Installation:**
```bash
go get github.com/Salvionied/apollo/v2
```

Use the `/v2` path. The unsuffixed `github.com/Salvionied/apollo` module is
feature-complete and no longer receives updates; `docs/v2_migration/MIGRATION.md`
in the mirror covers porting off it.

**Basic send-ADA pattern:**
```go
cc := blockfrost.NewBlockFrostChainContext(
    "https://cardano-preprod.blockfrost.io/api/v0", 0, projectID)

b, err := apollo.New(cc).AddInputAddressFromBech32(senderBech32)
if err != nil { return err }
b, err = b.PayToAddressBech32(recipientBech32, 5_000_000)
if err != nil { return err }
b, err = b.Complete()
if err != nil { return err }
```

---

## cardano-client-lib

- **Language:** Java / Kotlin (JVM)
- **Repository:** github.com/bloxbean/cardano-client-lib
- **Documentation:** cardano-client.dev (mirrored under `docs/sources/cardano-client-lib/`) + javadoc

**Strengths:**
- QuickTx gives a declarative builder comparable to Mesh, with the composable-functions
  API underneath when byte-level control is needed
- First-class Aiken support: CIP-57 blueprint loading, parameter application,
  and compile-time-checked datum codegen via the annotation processor
- Mature and battle-tested; the reference off-chain stack for JVM backends

**Weaknesses:**
- More verbose than the TypeScript SDKs
- Sharp edges around script-cost evaluation and protocol-parameter drift that the
  API surface does not advertise
- Worked script-spending examples live in the examples repo, not the docs site

**Installation (Maven):**
```xml
<dependency>
  <groupId>com.bloxbean.cardano</groupId>
  <artifactId>cardano-client-lib</artifactId>
  <version>0.7.2</version>
</dependency>
```

**Basic send-ADA pattern (QuickTx -- the recommended API):**
```java
BackendService backendService = new BFBackendService(
        "https://cardano-preprod.blockfrost.io/api/v0/", "<PROJECT_ID>");
QuickTxBuilder quickTxBuilder = new QuickTxBuilder(backendService);

Tx tx = new Tx()
        .payToAddress(receiver, Amount.ada(5))
        .from(sender.baseAddress());

TxResult result = quickTxBuilder.compose(tx)
        .withSigner(SignerProviders.signerFrom(sender))
        .completeAndWait();
```

For Plutus spending, minting, datum encoding and signer semantics, see
`cclib-quicktx.md` in this directory.

---

## cardano-js-sdk

- **Language:** TypeScript
- **Repository:** github.com/input-output-hk/cardano-js-sdk
- **Documentation:** Limited (inline JSDoc, some guides)

**Strengths:**
- Official IOG SDK, used in Lace wallet
- Comprehensive coverage of Cardano features
- Modular package architecture
- Good TypeScript types

**Weaknesses:**
- Complex API surface -- steep learning curve
- Documentation is sparse compared to Mesh
- Designed primarily for wallet use cases
- Frequent breaking changes between versions

**Installation:**
```bash
npm install @cardano-sdk/core @cardano-sdk/wallet
```

---

## Cardano Serialization Lib (CSL)

- **Language:** Rust (with WASM/JS and mobile bindings)
- **Repository:** github.com/input-output-hk/cardano-multiplatform-lib
- **Documentation:** Limited (Rust docs)

**Strengths:**
- Lowest-level SDK -- maximum control
- Best performance (Rust/WASM)
- Cross-platform (Rust, JS/WASM, mobile)
- Foundation for many other tools

**Weaknesses:**
- Very verbose -- simple transactions require many lines
- No built-in chain query or submission
- Steep learning curve
- Must manually handle fee calculation and coin selection

---

## Tx3

- **Language:** `.tx3` DSL, with generated clients in TypeScript, Rust, Go, and Python
- **Repository:** github.com/tx3-lang/tx3
- **Documentation:** docs.txpipe.io/tx3

Tx3 sits at a different level from the SDKs above. Instead of building a transaction
imperatively in one language, you **declare** a protocol's transactions in a `.tx3`
interface file — an ABI/OpenAPI analogue for UTxO protocols — then generate typed
clients for any supported language. A resolver reached over the Transaction Resolver
Protocol (TRP) does coin selection, fee calculation, and change.

**Strengths:**
- One interface definition, typed clients in four languages -- no per-language rewrite
- Protocol interface is a publishable, machine-readable artifact others can integrate against
- Toolchain included: `trix` (package manager, build, local devnet, test runner), LSP, VS Code extension
- Declarative `.tx3` reads as intent, not UTxO plumbing

**Weaknesses:**
- Pre-1.0 -- smaller ecosystem and less battle-tested than the imperative SDKs
- Extra moving parts: a TRP endpoint plus a codegen step
- New concepts to learn (parties, the `.tx3` language, TII/TIR/TRP)
- For a single-language app with simple needs, an imperative SDK is more direct

**Installation:**
```bash
tx3up                      # install the toolchain (trix, compiler, LSP)
npm install tx3-sdk        # runtime SDK for the generated client (TS shown)
```

**Basic send-ADA pattern (two parts):**

Declare the transaction:
```tx3
// transfer.tx3 -- the interface
party Sender;
party Receiver;

tx transfer(quantity: Int) {
    input source  { from: Sender, min_amount: Ada(quantity) }
    output        { to: Receiver, amount: Ada(quantity) }
    output        { to: Sender,   amount: source - Ada(quantity) - fees }
}
```

Consume transaction after generating:
```typescript
// after `trix codegen --plugin ts-client`
import { Client } from "./gen/transfer";
import { Party, Ed25519Signer } from "tx3-sdk";

const client = new Client({ endpoint: "http://localhost:8164" }, "local")
  .withSender(Party.signer(Ed25519Signer.fromHex("addr_test1...", "deadbeef...")))
  .withReceiver(Party.address("addr_test1..."));

const status = await client
  .transfer({ quantity: 5_000_000n })
  .resolve().then((r) => r.sign()).then((s) => s.submit())
  .then((sub) => sub.waitForConfirmed());
```

---

## cardano-ledger (Haskell)

- **Language:** Haskell
- **Repository:** github.com/IntersectMBO/cardano-ledger
- **Documentation:** bundled `docs/sources/cardano-ledger/`, CHaP README, haskell.nix tutorials
- **Build:** haskell.nix + CHaP + iohk-nix. See `references/haskell-ledger.md`.

**Strengths:**
- Same Conway `Tx` / cert / value types the node validates
- CIP-57 `plutus.json` from Aiken is the on-chain contract
- CHaP gives versioned `cardano-ledger-*` / `plutus-tx` instead of ad-hoc git pins

**Weaknesses:**
- No high-level builder; you construct ledger types
- Nix eval (haskell.nix) is the cold-start cost
- Not a browser / CIP-30 stack

**Installation:** not an npm/pip package. Wire CHaP + haskell.nix as in
`references/haskell-ledger.md`, then `cabal build` inside `nix develop`.

---

## Decision Guide

**Choose Mesh SDK when:**
- Building a web dApp with browser wallet integration
- Want the fastest path to a working transaction
- Team is TypeScript-focused
- Need React components for wallet UI

**Choose Evolution SDK when:**
- Want a type-safe, composable TypeScript transaction builder
- Prefer Effect-TS functional patterns
- Need built-in multi-provider support (Blockfrost, Koios, Kupmios, Maestro)
- Building Node.js or browser-based Cardano applications

**Choose PyCardano when:**
- Building Python backends or automation scripts
- Team is Python-focused
- Need quick scripting for testing or ops

**Choose Apollo when:**
- Building a Go backend or service and don't want to shell out to another runtime
- Already using gOuroboros and want shared ledger types across the stack
- Need Conway-era certificates, votes, or proposals from Go
- Accept a smaller community than the TypeScript and Python options in exchange

**Choose cardano-client-lib when:**
- The backend is JVM (Spring Boot services, existing Java/Kotlin infrastructure)
- Building against Aiken validators and you want blueprint-generated, compile-time-checked
  datum types rather than hand-encoded PlutusData
- Need low-level control over transaction bytes, via the composable-functions API
- Pairing with Yaci Store as the indexer, which speaks the Blockfrost API

**Choose cardano-js-sdk when:**
- Building a wallet application
- Need official IOG-maintained SDK
- Working on Lace ecosystem integrations

**Choose Cardano Serialization Lib when:**
- Building performance-critical tooling
- Need cross-platform Rust/WASM support
- Building a new SDK or framework on top

**Choose cardano-ledger when:**
- The off-chain service is Haskell and must share types with the node
- Validators are Aiken (CIP-57), not Plinth
- You already live in haskell.nix / CHaP

**Choose Tx3 when:**
- The same protocol is consumed from several languages and you want one interface, not N rewrites
- You are publishing a protocol for others to integrate against
- You prefer declaring transaction intent over imperative builder code
- You can accept a pre-1.0 toolchain and running (or pointing at) a TRP endpoint
