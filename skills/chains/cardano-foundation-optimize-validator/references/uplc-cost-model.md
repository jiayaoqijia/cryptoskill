# UPLC Cost Model Reference

How Plutus Core (UPLC) execution costs work on Cardano, and how to use this knowledge to optimize Aiken validators.

## How Costs Work

Every Cardano smart contract compiles to Untyped Plutus Core (UPLC). When a transaction includes a script, the Cardano node evaluates the UPLC and tracks two resources:

- **CPU (ExCPU)**: Measured in abstract picoseconds. Represents computational steps.
- **Memory (ExMem)**: Measured in abstract bytes. Represents peak working memory during evaluation.

Each transaction has a budget for both:

| Resource | Per-Transaction Limit |
|----------|----------------------|
| CPU      | 10,000,000,000 units |
| Memory   | 14,000,000 units     |

When multiple scripts execute in one transaction, they share the budget. If either limit is exceeded, the transaction fails Phase-2 validation and the submitter loses collateral.

## Cost Per Operation

### Cheap Operations (use freely)

| Operation | CPU (approx) | Memory |
|-----------|-------------|--------|
| Integer add/subtract | ~100,000 | ~32 |
| Integer comparison | ~50,000 | ~1 |
| Boolean logic | ~50,000 | ~1 |
| Pattern match (when) | ~50,000 | ~1 |
| List head/tail | ~50,000 | ~32 |
| If/then/else | ~50,000 | ~1 |

### Moderate Operations (use carefully)

| Operation | CPU (approx) | Memory |
|-----------|-------------|--------|
| Integer multiply | ~100,000 | ~32 |
| Integer divide/mod | ~200,000 | ~32 |
| ByteString compare | ~50,000 + O(len) | ~1 |
| ByteString append | ~50,000 + O(len) | O(len1+len2) |
| Data constructor/destructor | ~50,000 | O(fields) |
| List cons | ~50,000 | ~32 |

### Expensive Operations (minimize usage)

| Operation | CPU (approx) | Memory |
|-----------|-------------|--------|
| Blake2b_256 hash | ~400,000 + O(len) | ~32 |
| SHA-256 hash | ~500,000 + O(len) | ~32 |
| SHA3-256 hash | ~500,000 + O(len) | ~32 |
| Ed25519 signature verify | ~53,400,000 + ~14,000/byte | ~10 |
| ECDSA Secp256k1 verify | ~35,000,000+ | ~10 |
| Schnorr Secp256k1 verify | ~35,000,000+ | ~10 |

An Ed25519 verification costs roughly 0.5% of the 10B per-transaction CPU budget per call (exact figures come from the live Plutus cost model -- `verifyEd25519Signature` intercept ~53.4M). Still expensive: use `tx.extra_signatories` instead -- the ledger verifies signatures at no script cost.

## Why Certain Patterns Are Expensive

### Nested List Traversals

```aiken
// O(n * m) -- with 10 inputs and 10 outputs, that is 100 comparisons
list.all(tx.inputs, fn(input) {
  list.any(tx.outputs, fn(output) {
    matches(input, output)
  })
})
```

Each comparison involves bytestring comparison of addresses and value inspection. Restructure to single-pass algorithms or pre-filter lists.

### Value Comparisons

`Value` is a nested map: `Map<PolicyId, Map<AssetName, Int>>`. Comparing two Values traverses both maps. Cost is O(n * m) where n and m are distinct asset counts.

For multi-asset values with 5+ distinct assets, each whole-`Value` comparison (traversing both nested maps, e.g. `output.value == expected_value`) becomes significant. Minimize the number of value comparisons.

### Large Datum Deserialization

When a validator receives a datum, the entire Data structure is traversed and type-checked. A datum with 20 fields costs significantly more to deserialize than one with 3 fields.

Nested structures multiply: a list of 10 records with 5 fields each requires deserializing 50 values plus list structure overhead.

### Trace Messages

Trace strings are embedded as bytestring literals in the compiled script. Each trace:
- Increases script size (string literal stored in UPLC)
- Costs CPU even when the trace path is not executed (the literal exists in the script structure)

Building with `--trace-level silent` removes traces and typically reduces script size by 10-30%.

## Script Size Impact on Fees

### Inline Scripts

Scripts included directly in a transaction contribute to transaction size. The fee formula:

```
fee = base_fee + (tx_size_bytes * fee_per_byte) + exec_fee(cpu, mem)
```

Current `fee_per_byte` is approximately 44 lovelace. A 10 KB script adds ~440,000 lovelace (~0.44 ADA) to every transaction that uses it.

### Transaction Size Limit

Transactions are limited to approximately 16,384 bytes. A 14 KB inline script leaves almost no room for inputs, outputs, and other data.

### Reference Scripts (CIP-33)

Reference scripts are stored in a UTxO and referenced by hash. The script is not included in the transaction body.

Trade-offs:
- **Storage cost**: The UTxO holding the reference script must meet min-UTxO requirements proportional to script size
- **Reference fee**: A per-use fee based on script size (prevents free-riding on large scripts)
- **Benefit**: Paid once at creation, amortized over many transactions

Rule of thumb: use reference scripts for any script over ~4 KB used in multiple transactions.

## Practical Budget Guidelines

| Usage Level | Target CPU | Target Memory | Context |
|------------|-----------|--------------|---------|
| Simple | < 500M | < 1M | Leaves room for complex transactions |
| Moderate | < 2B | < 5M | Typical DeFi operations |
| Complex | < 5B | < 10M | Near limits, test carefully |
| Dangerous | > 5B | > 10M | High risk of transaction failure |

All scripts in a transaction share the budget. A single validator using 80% of the budget makes the transaction fragile.

## Optimization Decision Tree

**Is the validator correct and tested?**
- No: Fix correctness first, do not optimize yet.
- Yes: Continue.

**What is the bottleneck?**

Script size too large (over ~12 KB inline):
1. Remove traces (`--trace-level silent`)
2. Extract common code into shared functions
3. Simplify types (fewer constructor fields)
4. Use reference scripts

CPU too high:
1. Eliminate nested list traversals
2. Order `when` branches by frequency
3. Fail fast (cheap checks before expensive ones)
4. Reduce datum deserialization scope
5. Avoid on-chain cryptographic operations

Memory too high:
1. Reduce datum and redeemer sizes
2. Avoid building large intermediate structures
3. Use folding instead of map+filter chains
4. Check for unnecessary data copies

## Reading aiken bench Output

`aiken bench` plots **memory units** and **cpu units** per benchmark across
growing input sizes -- it does not report script size. Get script size from the
build output instead:

```bash
aiken build
cat plutus.json | jq '.validators[] | {title, size: (.compiledCode | length / 2)}'
```

- **cpu units**: ExCPU consumed as the sampled input grows
- **memory units**: ExMem consumed as the sampled input grows
- **script size**: from `plutus.json` (bytes = compiledCode hex length / 2)

## Protocol Parameter Dependencies

Cost model parameters can change via governance. Query current values:

```bash
cardano-cli query protocol-parameters --mainnet | jq '{
  cpuPrice: .executionUnitPrices.priceSteps,
  memPrice: .executionUnitPrices.priceMemory,
  maxCpu: .maxTxExecutionUnits.steps,
  maxMem: .maxTxExecutionUnits.memory,
  feePerByte: .txFeePerByte
}'
```

Key parameters:
- `executionUnitPrices.priceSteps`: Lovelace cost per CPU step
- `executionUnitPrices.priceMemory`: Lovelace cost per memory unit
- `maxTxExecutionUnits.steps`: Max CPU per transaction
- `maxTxExecutionUnits.memory`: Max memory per transaction
- `txFeePerByte`: Fee per byte of transaction size
