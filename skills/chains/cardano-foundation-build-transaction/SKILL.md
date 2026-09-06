---
name: build-transaction
description: >-
  Build Cardano transaction, send ADA, mint NFT, mint token, interact with
  smart contract, delegate stake, register DRep, vote on-chain using Mesh SDK,
  Evolution SDK, PyCardano, cardano-client-lib, or Haskell cardano-ledger
  (Aiken CIP-57 + haskell.nix + CHaP).
allowed-tools: Read Grep Glob
disallowed-tools: WebFetch WebSearch
---

<!-- Documentation lookup path: ${CLAUDE_SKILL_DIR}/../../docs/sources/ -->

# Build Cardano Transaction

Guide the user through building Cardano transactions step by step using their
chosen off-chain SDK. Covers the full lifecycle: prerequisites, transaction
construction, signing, submission, and verification on a testnet.

## When to Use

- User wants to send ADA or native tokens to an address
- User wants to mint an NFT or fungible token
- User wants to interact with a deployed smart contract (lock, redeem, etc.)
- User wants to delegate stake to a pool or DRep
- User wants to register as a DRep or cast a governance vote
- User asks how to build, sign, or submit a Cardano transaction
- User asks which SDK to use for off-chain transaction building
- User is in Haskell and wants to build a Conway tx from an Aiken blueprint
  with cardano-ledger / haskell.nix / CHaP

## When NOT to Use

- User wants to write or review on-chain validator logic -- use `write-validator`
  or `review-contract`
- User is designing token metadata standards -- use `design-token`
- User has a failing transaction and needs help debugging -- use `debug-transaction`
- User wants to set up a local devnet or node infrastructure -- use `setup-devnet`

## Key Principles

1. **Choose the right SDK for the job.** Mesh SDK (TypeScript) and Evolution SDK
   (TypeScript) have the best documentation and highest-level APIs. PyCardano is best
   for Python shops. cardano-client-lib suits JVM projects needing fine control.
   Haskell services that share types with the node use **cardano-ledger** (not
   Mesh, not Atlas) and are built with **haskell.nix** + **CHaP**.
   Search `${CLAUDE_SKILL_DIR}/../../docs/sources/` for the latest SDK comparison details.

2. **Always prototype on Preview testnet.** Never build against mainnet first.
   Use the Cardano faucet to obtain test ADA. Set the network parameter
   explicitly in every code example.

3. **UTxO selection matters.** Cardano uses the EUTxO model. The SDK must
   select unspent outputs that cover the transaction value plus fees. Understand
   coin selection to avoid `ValueNotConservedUTxO` errors.

4. **Fees and change are computed, not guessed.** All SDKs have fee estimation.
   Let the SDK calculate fees and construct change outputs automatically.

5. **Transactions are deterministic.** The same inputs and parameters always
   produce the same transaction. This enables dry-run testing before submission.

6. **Collateral is required for Plutus interactions.** Any transaction that
   executes a Plutus script must include collateral UTxOs containing only ADA.

## Workflow

### Step 1: Gather Parameters

Ask the user to specify or confirm:

| Parameter | Options | Default |
|-----------|---------|---------|
| SDK | `mesh`, `evolution-sdk`, `pycardano`, `cardano-client-lib`, `tx3`, `cardano-ledger`, `apollo` | `mesh` |
| Transaction type | `send-ada`, `mint-nft`, `mint-token`, `interact-with-contract`, `delegate-stake`, `register-drep`, `vote` | required |
| Network | `preview`, `preprod`, `mainnet` | `preview` |
| Wallet | mnemonic, private key, browser wallet | mnemonic |

If the user does not specify an SDK, recommend **Mesh SDK** for TypeScript
projects, **cardano-client-lib** for Java/JVM, **Apollo** for Go, or
**cardano-ledger** for Haskell (see `references/haskell-ledger.md`).

**Alternative paradigm with Tx3:** Most SDKs above build transactions imperatively in
code. Tx3 takes a declarative route: you describe a protocol's transactions
in a `.tx3` interface file and generate typed clients in TypeScript, Rust, Go, or
Python (an ABI/OpenAPI analogue for UTxO protocols). Reach for it when the same
protocol is consumed from several languages, or when you are publishing a protocol
for others to integrate. It is pre-1.0; for a single-language app the imperative SDKs
are the more battle-tested default. 

### Step 2: Search Bundled Documentation

Search the bundled documentation for relevant content:
- `${CLAUDE_SKILL_DIR}/../../docs/sources/evolution-sdk/` - Evolution SDK docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/mesh-sdk/` - Mesh SDK docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/mesh-sdk-packages/` - Mesh SDK package docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/pycardano/` - PyCardano docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/cardano-client-lib/` - Cardano Client Lib docs
  (QuickTx API, blueprint codegen, backend providers). For a worked lock-and-spend
  cycle, read the Java programs under
  `${CLAUDE_SKILL_DIR}/../../docs/sources/cardano-use-case-templates/<use-case>/offchain/ccl-java/`
  -- they are `.java`, so a markdown-only search will miss them.
- `${CLAUDE_SKILL_DIR}/../../docs/sources/tx3/` - Tx3 docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/chap/` - CHaP cabal.project + haskell.nix inputMap
- `${CLAUDE_SKILL_DIR}/../../docs/sources/haskell-nix/` - flakes, `--sha256` on git deps
- `${CLAUDE_SKILL_DIR}/../../docs/sources/iohk-nix/` - crypto overlays
- `${CLAUDE_SKILL_DIR}/../../docs/sources/cardano-ledger/` - Conway tx types / phase-1
- `${CLAUDE_SKILL_DIR}/../../docs/sources/aiken/` - CIP-57 `plutus.json` from `aiken build`

- `${CLAUDE_SKILL_DIR}/../../docs/sources/apollo/` - Apollo (Go) builder: `docs/**` prose plus `.go` API source
- `${CLAUDE_SKILL_DIR}/../../docs/sources/gouroboros/` - gOuroboros (Go) ledger types Apollo builds on

### Step 3: Set Up Prerequisites

For each SDK, ensure the user has the required environment:

**Mesh SDK (TypeScript/JavaScript)**

```bash
npm install @meshsdk/core
```

- Requires Node.js 18+
- Needs a blockchain provider (Blockfrost, Koios, or Ogmios)
- Blockfrost API key from https://blockfrost.io

**Evolution SDK (TypeScript)**

```bash
npm install @evolution-sdk/evolution
```

- Requires Node.js 18+ and TypeScript 5.0+
- Effect-TS based, type-safe composable API
- Built-in Blockfrost, Koios, Kupmios, and Maestro providers
- Works in Node.js and browser environments

**PyCardano (Python)**

```bash
pip install pycardano
```

- Requires Python 3.8+
- Needs a chain context (Blockfrost, Ogmios, or CardanoCliContext)

**cardano-client-lib (Java)**

```xml
<dependency>
  <groupId>com.bloxbean.cardano</groupId>
  <artifactId>cardano-client-lib</artifactId>
  <version>0.7.2</version>
</dependency>
```

- Java/JVM library by BloxBean
- Good for fine-grained transaction control

**Tx3 (declarative, multi-language)**

Tx3 is not a library you install into one project — it is a toolchain plus a
per-language runtime SDK. Setup has three parts:

```bash
# 1. Install the toolchain (provides trix, the compiler, and the LSP)
tx3up                       # see docs/sources/tx3/installation.mdx for the installer
tx3up show                  # verify installed components

# 2. Install the runtime SDK for your target language, e.g. TypeScript
npm install tx3-sdk         # Rust: tx3-sdk crate · Go: go-sdk · Python: tx3-sdk
```

- Needs a **TRP endpoint** to resolve, sign, and submit — `trix devnet` exposes a
  local one at `http://localhost:8164`; for preview/preprod/mainnet point at a hosted
  TRP endpoint.
- Needs the toolchain for whichever client language you generate (Node.js 18+,
  Rust 1.78+, Go 1.22+, or Python 3.10+).
- Search `${CLAUDE_SKILL_DIR}/../../docs/sources/tx3/` for the language reference,
  `trix` commands, and Cardano examples.

**cardano-ledger (Haskell)**

This path is a haskell.nix flake, not cabal on a system GHC. Full wiring
(CHaP stanza, `inputMap`, iohk-nix overlays, Aiken blueprint):
`references/haskell-ledger.md`. Short form:

```bash
# inside the haskell.nix dev shell
cabal update
cabal build all -O0
```

- `cabal.project` must contain the CHaP `repository` stanza and a **dual**
  `index-state` (Hackage + `cardano-haskell-packages`). See
  `docs/sources/chap/README.md`.
- Flake input `CHaP` on `?ref=index-only`, then
  `inputMap = { "https://chap.intersectmbo.org/" = CHaP; }`.
- iohk-nix overlays `crypto` and `haskell-nix-crypto` (CHaP README: needed
  for `libblst` / `plutus-core`).
- `source-repository-package` stanzas need a `--sha256` comment
  (`docs/sources/haskell-nix/tutorials/source-repository-hashes.md`).
- Load scripts from Aiken `plutus.json` (CIP-57). Datums/redeemers are
  `plutus-tx` `ToData`, not JSON.

**Apollo (Go)**

```bash
go get github.com/Salvionied/apollo/v2
```

- Needs a `backend.ChainContext` (Blockfrost, Maestro, Ogmios, UTxORPC, or a fixed/cached backend)
- Builds on gOuroboros ledger types, so `common.Address` and friends are shared across the Go stack
- **Always use the `/v2` module path.** It is the maintained line and what the
  mirror documents. The unsuffixed `github.com/Salvionied/apollo` path is
  feature-complete and no longer receives updates — when porting code off it,
  see `docs/v2_migration/MIGRATION.md` in the mirror.
- The `/v2` path is on a stable release line, so `go get` resolves to a released
  tag rather than a pre-release or a commit off the default branch

### Step 4: Build the Transaction

Provide step-by-step code for the chosen SDK and transaction type.
Follow these patterns:

#### Send ADA Pattern

1. Initialize the provider and wallet
2. Create a transaction builder
3. Add the payment output (recipient address + lovelace amount)
4. Let the SDK handle coin selection, fee calculation, and change
5. Sign with the wallet
6. Submit to the network
7. Log the transaction hash

#### Mint NFT / Token Pattern

1. Initialize the provider and wallet
2. Define the minting policy (time-locked or Plutus script)
3. Prepare token metadata conforming to CIP-25 or CIP-68
4. Create a transaction builder
5. Add the minting action (policy, asset name, quantity)
6. Add metadata to the transaction
7. Sign with policy key + wallet key
8. Submit and log the transaction hash

#### Interact with Contract Pattern

1. Initialize the provider and wallet
2. Load the Plutus script (from file or CIP-57 blueprint)
3. For locking: build a tx that sends value to the script address with a datum
4. For redeeming: query UTxOs at the script address, select the target,
   build a tx that spends it with the correct redeemer, include collateral
5. Sign, submit, and verify

#### Delegate Stake Pattern

1. Initialize the provider and wallet
2. Create or retrieve the stake address
3. Register the stake address (if not already registered -- costs 2 ADA deposit)
4. Build a delegation certificate targeting the chosen pool ID
5. Sign and submit

#### Register DRep / Vote Pattern

1. Initialize the provider and wallet
2. For DRep registration: build a DRep registration certificate with metadata anchor
3. For voting: build a voting procedure targeting a governance action ID
4. Sign and submit

### Step 5: Explain the Transaction

After providing code, explain:

- What each part of the transaction does
- How coin selection works in this context
- What fees are expected
- What happens on-chain when this transaction is processed

### Step 6: Common Pitfalls

Warn about these frequent issues:

- **Insufficient ADA for min-UTxO:** Every UTxO must hold a minimum amount of
  ADA (roughly 1-2 ADA depending on datum/token bundle size). The SDK usually
  handles this, but manual outputs can fail.
- **Forgetting collateral:** Plutus transactions require a collateral input.
  Use a UTxO with only ADA (no tokens).
- **Wrong network:** Addresses are network-specific. A Preview address will
  not work on Preprod or Mainnet.
- **Stale UTxO set:** If another transaction consumed your inputs between
  query and submit, you get `BadInputsUTxO`. Re-query and rebuild.
- **Token name encoding:** Asset names are hex-encoded bytes. Ensure proper
  encoding (e.g., `Buffer.from("MyToken").toString("hex")`).
- **Transaction size limit:** Max 16 KB. Large token bundles or many inputs
  can exceed this. Split into multiple transactions if needed.

### Step 7: Test on a testnet before mainnet

A transaction that type-checks can still fail at submission (min-UTxO, fees, collateral,
script evaluation). Always run it on a testnet first — and for Plutus-script flows, a local
Yaci DevKit devnet (`setup-devnet`) gives the fastest build→submit→confirm loop.

1. Get test ADA from the Cardano faucet: https://docs.cardano.org/cardano-testnets/tools/faucet/
2. Run the transaction code against Preview or Preprod
3. Verify on a block explorer (Preview: https://preview.cardanoscan.io ·
   Preprod: https://preprod.cardanoscan.io)
4. Check the transaction hash matches expected outputs
5. For minting: verify the token appears in the wallet

## SDK Quick Reference

### Mesh SDK -- Transaction Builder

```typescript
import { MeshTxBuilder, BlockfrostProvider } from "@meshsdk/core";

const provider = new BlockfrostProvider("<BLOCKFROST_KEY>");
const txBuilder = new MeshTxBuilder({ fetcher: provider, submitter: provider });

// Build, sign, submit pattern
const unsignedTx = await txBuilder
  .txOut(recipientAddress, [{ unit: "lovelace", quantity: "5000000" }])
  .changeAddress(senderAddress)
  .selectUtxosFrom(utxos)
  .complete();

const signedTx = await wallet.signTx(unsignedTx);
const txHash = await wallet.submitTx(signedTx);
```

### Evolution SDK -- Composable Builder

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

### PyCardano -- TransactionBuilder

```python
from pycardano import TransactionBuilder, TransactionOutput, Address

builder = TransactionBuilder(context)
builder.add_input_address(sender_address)
builder.add_output(TransactionOutput(recipient, 5_000_000))
signed_tx = builder.build_and_sign([signing_key], change_address=sender_address)
context.submit_tx(signed_tx)
```

### cardano-client-lib -- QuickTx

```java
BackendService backendService = new BFBackendService(
        "https://cardano-preprod.blockfrost.io/api/v0/", "<PROJECT_ID>");
QuickTxBuilder quickTxBuilder = new QuickTxBuilder(backendService);

Tx tx = new Tx()
        .payToAddress(receiver, Amount.ada(1.5))
        .from(sender.baseAddress());

TxResult result = quickTxBuilder.compose(tx)
        .withSigner(SignerProviders.signerFrom(sender))
        .completeAndWait();
```

Spending from a Plutus script uses `ScriptTx` and attaches the validator inline --
no reference script needs to be published first:

```java
ScriptTx scriptTx = new ScriptTx()
        .collectFrom(List.of(utxo), redeemer)
        .payToAddress(receiver, utxo.getAmount())
        .attachSpendingValidator(plutusScript);

TxResult result = quickTxBuilder.compose(scriptTx)
        .feePayer(sender.baseAddress())
        .withSigner(SignerProviders.signerFrom(sender))       // signs the tx
        .withRequiredSigners(sender.getBaseAddress())         // satisfies must_be_signed_by
        .completeAndWait();
```

Full guide -- datum encoding, minting, collateral: `${CLAUDE_SKILL_DIR}/references/cclib-quicktx.md`.

### Tx3 -- Declarative Interface + Typed Client

Tx3 splits the work in two. First, **describe** the transaction once in a `.tx3`
file (this is the protocol interface, language-agnostic):

```tx3
party Sender;
party Receiver;

tx transfer(quantity: Int) {
    input source {
        from: Sender,
        min_amount: Ada(quantity),
    }
    output {
        to: Receiver,
        amount: Ada(quantity),
    }
    output {
        to: Sender,
        amount: source - Ada(quantity) - fees,
    }
}
```

Then **generate** a typed client and drive the lifecycle from your app (TypeScript
shown; Rust/Go/Python clients are generated the same way):

```bash
trix codegen --plugin ts-client   # emits a typed client from the .tx3 interface
```

```typescript
import { Client } from "./gen/transfer";
import { Party, Ed25519Signer } from "tx3-sdk";

const client = new Client({ endpoint: "http://localhost:8164" }, "local")
  .withSender(Party.signer(Ed25519Signer.fromHex("addr_test1...", "deadbeef...")))
  .withReceiver(Party.address("addr_test1..."));

// Each `tx` becomes a typed method; the lifecycle is resolve → sign → submit
const status = await client
  .transfer({ quantity: 10_000_000n })
  .resolve()
  .then((r) => r.sign())
  .then((s) => s.submit())
  .then((sub) => sub.waitForConfirmed());
```

The resolver (reached over TRP) does coin selection, fee calculation, and change —
the `.tx3` file declares intent, not the concrete UTxOs.

### Apollo -- Fluent Builder (Go)

Verified to compile against `apollo/v2` at `v2.0.1` (2026-08-19). The builder is
fluent, but the steps that can fail return `(*Apollo, error)` rather than a bare
`*Apollo` — `AddInputAddressFromBech32` and `PayToAddressBech32` among them — so
handle the error and re-assign at each of those:

```go
import (
    apollo "github.com/Salvionied/apollo/v2"
    "github.com/Salvionied/apollo/v2/backend/blockfrost"
)

cc := blockfrost.NewBlockFrostChainContext(
    "https://cardano-preprod.blockfrost.io/api/v0", 0, projectID)

b, err := apollo.New(cc).AddInputAddressFromBech32(senderBech32)
if err != nil { return err }
b, err = b.PayToAddressBech32(recipientBech32, 10_000_000)
if err != nil { return err }
b, err = b.Complete()          // coin selection, fee calculation, balancing
if err != nil { return err }
```

Methods that only mutate builder state — `AddLoadedUTxOs`, `RegisterDRep`,
`AddRequiredSigner` — return a bare `*Apollo` and do chain, recording any error
internally for `Complete` to report. Start from `doc.go` in a mirrored package
for the overview, then `Grep` a method name in
`${CLAUDE_SKILL_DIR}/../../docs/sources/apollo/` for its signature and doc
comment.

Then `SetWalletFromMnemonic` + `Sign` + `Submit` for a signed submission, or
`GetTxCbor` to hand the CBOR to an external signer. The mirror's `docs/`
directory carries worked examples for staking, governance, and Plutus V3.

## References

- `references/sdk-comparison.md` -- detailed SDK comparison table
- `references/haskell-ledger.md` -- Aiken + cardano-ledger + CHaP + haskell.nix
- Search `${CLAUDE_SKILL_DIR}/../../docs/sources/` for CIP-25, CIP-68 metadata standards
- Cardano Developer Portal: https://developers.cardano.org
- Mesh SDK docs: https://meshjs.dev
- Evolution SDK docs: https://evolution-sdk.dev
- PyCardano docs: https://pycardano.readthedocs.io
- Tx3 docs: https://docs.txpipe.io/tx3

- Apollo docs: https://pkg.go.dev/github.com/Salvionied/apollo/v2
