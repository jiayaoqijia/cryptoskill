# cardano-client-lib: QuickTx

Building transactions in Java with BloxBean's cardano-client-lib (CCL). QuickTx is
the declarative builder and the right default; the older composable-functions API
is for cases QuickTx cannot express.

Two classes do the work:

- **`Tx`** — native transactions: payments, native-script mint/burn, staking, metadata.
- **`ScriptTx`** — Plutus-aware: spending script UTxOs, Plutus minting, attaching validators.

Both are composed and executed by a `QuickTxBuilder`. Where the two differ matters:
`Tx` carries `.from(sender)`, `ScriptTx` gets its funding through the builder's
`.feePayer(...)`.

## Wiring a backend

```java
BackendService backendService = new BFBackendService(
        "https://cardano-preprod.blockfrost.io/api/v0/", "<PROJECT_ID>");
QuickTxBuilder quickTxBuilder = new QuickTxBuilder(backendService);
UtxoSupplier utxoSupplier = new DefaultUtxoSupplier(backendService.getUtxoService());
```

Against a local devnet, point the same `BFBackendService` at Yaci Store — it speaks
the Blockfrost API, so no code changes are needed:

```java
new BFBackendService("http://localhost:8080/api/v1/", "Dummy Key");
```

Check the port against `setup-devnet` — Yaci DevKit has exposed Yaci Store on both
8080 and 10000 across versions.

Only reach for the three-argument constructor
(`new QuickTxBuilder(utxoSupplier, paramsSupplier, txProcessor)`) when you must
supply suppliers yourself. It has a sharp edge: passing `null` for the processor
also nulls the script-cost evaluator, and because evaluation errors are ignored by
default the build *succeeds* with placeholder execution units. See "Known traps".

## Loading a validator from an Aiken blueprint

```java
PlutusContractBlueprint blueprint = PlutusBlueprintLoader.loadBlueprint(plutusJson.toFile());
String compiledCode = blueprint.getValidators().getFirst().getCompiledCode();
PlutusScript plutusScript =
        PlutusBlueprintUtil.getPlutusScriptFromCompiledCode(compiledCode, PlutusVersion.v3);
Address scriptAddress = AddressProvider.getEntAddress(plutusScript, network);
```

`getFirst()` takes validator zero. A blueprint with several validators needs
selection by name — read `validators[].title` rather than trusting position.

For parameterized validators, apply parameters before deriving the address:
`AikenScriptUtil.applyParamToScript(params, compiledCode)`, then load the result.
See `${CLAUDE_SKILL_DIR}/../../docs/sources/cardano-client-lib/integrations/aiken-integration-api.mdx`.

## Simple payment

```java
Tx tx = new Tx()
        .payToAddress(receiver, Amount.ada(1.5))
        .from(sender.baseAddress());

TxResult result = quickTxBuilder.compose(tx)
        .withSigner(SignerProviders.signerFrom(sender))
        .completeAndWait();
```

`complete()` submits and returns; `completeAndWait()` blocks until the transaction
is confirmed. On a devnet with sub-second blocks prefer `completeAndWait()` — it
removes the "submitted but not yet indexed" race that makes the next query fail.

## Locking funds at a script

```java
PlutusData datum = ConstrPlutusData.of(0,
        BigIntPlutusData.of(lockUntilMs),
        BytesPlutusData.of(ownerVkh),
        BytesPlutusData.of(beneficiaryVkh));

Tx tx = new Tx()
        .payToContract(scriptAddress.getAddress(), Amount.ada(20), datum)
        .from(ownerAddress.getAddress());
```

Locking is an ordinary payment — no script witness is involved, because nothing is
being validated yet. `ConstrPlutusData.of(constructorIndex, fields...)` maps onto an
Aiken constructor; field order is the declaration order in the Aiken type, and
getting it wrong produces a datum the validator rejects with no useful diagnostic.

Get the key hash from an address with `address.getPaymentCredentialHash().get()`.

## Spending from a script — attach the validator inline

**This is the default, and it is a single transaction.** Cardano has no script
deployment step: the validator travels in the transaction's witness set.

```java
ScriptTx scriptTx = new ScriptTx()
        .collectFrom(List.of(utxo), redeemer)
        .payToAddress(beneficiary, utxo.getAmount())
        .attachSpendingValidator(plutusScript);

TxResult result = quickTxBuilder.compose(scriptTx)
        .validFrom(slot - 5)
        .validTo(slot + 5)
        .feePayer(ownerAddress.getAddress())
        .withSigner(SignerProviders.signerFrom(owner))
        .withRequiredSigners(beneficiaryAddress)
        .completeAndWait();
```

Four things here are easy to get wrong:

- **`payToAddress` is not optional.** `collectFrom` drops the script input when no
  output anchors its value. Forward the collected `utxo.getAmount()` explicitly
  rather than assuming change handling will carry it.
- **`withSigner` and `withRequiredSigners` are different.** `withSigner` attaches a
  signing key so the transaction is signed. `withRequiredSigners` adds the key hash
  to the body's `required_signers` field, which is what a validator's
  `must_be_signed_by` actually checks. A validator asserting a signature needs both.
- **Validity bounds need slack.** A validator comparing against `now` reads the
  transaction's validity interval, not wall-clock. `validFrom(slot - 5)` gives the
  chain-side check room against clock and indexer drift.
- **Collateral is automatic.** QuickTx selects and returns collateral for you.
  Override with `withCollateralInputs(...)` only when you need a specific UTxO —
  and note one UTxO can serve as both the spend input and collateral, so no
  pre-split transaction is required.

## Minting with a Plutus policy

```java
ScriptTx tx = new ScriptTx()
        .mintAsset(mintingScript, asset, redeemer, receiverAddress, outputDatum)
        .attachMintValidator(mintingScript);
```

The policy ID is the script hash; derive it rather than hardcoding. Burning is the
same call with a negative quantity, and the validator must permit it — a policy
enforcing `token_minted(+1)` will reject a burn bundled into the same transaction.

Note `mintAsset(...)` always attaches a witness copy of the policy script. That
matters only if you also reference the same script from a reference input, which
the ledger rejects as `ExtraneousScriptWitnessesUTXOW`.

## Reference scripts: an optimization, not a prerequisite

Do not publish a reference script to spend from your own validator. It costs an
extra transaction, an extra min-UTxO deposit, and an extra failure mode, and buys
nothing at hello-world scale.

Reference scripts earn their keep when a large validator (roughly >4 KB) is spent
by **many** transactions — the script bytes stop riding in every witness set. Reach
for them then, and read the trade-offs in `optimize-validator` first.

When you do consume one, CCL needs the script *bytes*, not just the hash, to charge
the Conway reference-script fee correctly — `withReferenceScripts(...)`, plus
`removeDuplicateScriptWitnesses(true)` to strip copies. A Blockfrost `Utxo` carries
only `referenceScriptHash`, never the bytes.

## Datum encoding: by hand or generated

The `ConstrPlutusData`/`BigIntPlutusData`/`BytesPlutusData` builders above are the
hand-rolled route — fine for small datums, error-prone for nested types.

For anything larger, generate Java types from the CIP-57 blueprint with the
annotation processor (`cardano-client-annotation-processor`), which gives you
POJO ↔ PlutusData conversion checked at compile time. See
`${CLAUDE_SKILL_DIR}/../../docs/sources/cardano-client-lib/annotations/plutus-blueprint-code-generation.mdx`
and `.../annotations/plutus-data-annotations.mdx`.

Whichever route, **ground the encoding against a real on-chain datum** before
trusting it. One wrong byte locks funds until a cancel path runs.

## Known traps

CCL has sharp edges that cost real money and are not visible in the API surface —
under-declared execution units that pass the mempool and fail in phase 2 (collateral
forfeit), protocol-parameter drift between the library's built-in cost model and the
chain, datum re-encoding that is not byte-stable, and output-index prediction that
breaks when withdrawals inject a dummy output.

If you are building anything beyond a tutorial, read those before shipping. They are
maintained separately from this repo, keyed by symptom.

## Where to look next

Vendored upstream docs — `${CLAUDE_SKILL_DIR}/../../docs/sources/cardano-client-lib/`:

- `apis/transaction/quicktx-api.mdx` — the QuickTx reference
- `apis/providers/backend-services-api.mdx` — Blockfrost, Koios, Ogmios, Kupmios, Yaci
- `annotations/` — blueprint codegen and datum annotations
- `integrations/aiken-integration-api.mdx` — parameter application, off-chain evaluation
- `apis/core/plutus-api.mdx` — PlutusData primitives

**Working end-to-end programs** — `${CLAUDE_SKILL_DIR}/../../docs/sources/cardano-use-case-templates/<use-case>/offchain/ccl-java/`.
Roughly twenty complete, runnable use cases (vesting, escrow, auction, HTLC,
crowdfund, payment-splitter, and more), each pairing an Aiken validator with a CCL
off-chain program. These are the best available reference for a full lock-and-spend
cycle; read one alongside its `onchain/aiken/` validator. Note they are `.java`, so
a markdown-only search will not surface them.
