---
name: optimize-validator
description: >-
  Optimize Aiken validators for lower execution costs and smaller script size.
  Covers CPU/memory reduction, script size, data structures, and benchmarking.
  Trigger: "optimize validator", "reduce script size", "lower execution cost",
  "reduce CPU", "reduce memory", "script too large", "transaction too expensive".
allowed-tools: Read Grep Glob
disallowed-tools: WebFetch WebSearch
---

<!-- Documentation lookup path: ${CLAUDE_SKILL_DIR}/../../docs/sources/ -->

# Optimize Cardano Validator

Guide optimization of Aiken validators for lower execution costs (CPU/memory) and smaller compiled script size. Optimization should only be applied to validators that are already correct and tested.

## When to use

- User has a working validator and wants to reduce transaction fees
- Script size exceeds limits or is unnecessarily large
- Execution units (CPU/memory) are higher than expected
- User wants to compare optimization strategies
- Before deploying a reference script (size directly affects storage deposit)
- Transaction is failing due to exceeding execution unit limits

## When NOT to use

- User needs to write a new validator (use write-validator)
- User needs a security review (use review-contract)
- The validator has not been tested yet (correctness comes before performance)
- The optimization would remove a security check

## Key principles

1. **Measure before optimizing**: Use `aiken build` to check script size and `aiken bench` to measure execution units. Without baseline numbers, you cannot know if changes helped.
2. **Script size and execution units are independent costs**: A larger script is not necessarily more expensive to execute. Inlining functions increases size but can reduce CPU by avoiding closure allocation.
3. **CPU and memory budgets are separate**: A transaction can fail by exceeding either limit independently. Identify which resource is the bottleneck before optimizing.
4. **The stdlib is well-optimized**: Do not rewrite stdlib functions unless profiling shows they are a bottleneck. Custom implementations often end up larger and slower.
5. **Correctness over performance**: Never sacrifice security checks for performance. Optimize how a check is performed, not whether it runs.

## Workflow

### Step 1: Establish baseline

Read the validator code and gather current metrics.

Suggest the user run:

```bash
# Build and check script sizes
aiken build

# Run benchmarks if available
aiken bench

# Check compiled script sizes
cat plutus.json | jq '.validators[] | {title, size: (.compiledCode | length / 2)}'
```

Note the following:
- Current script size in bytes (from `plutus.json` or build output)
- Execution unit estimates per action (from `aiken bench`)
- Which operations the validator performs (list traversals, value comparisons, datum deserialization)

### Step 2: Search Bundled Documentation

Search the bundled documentation for relevant content:
- `${CLAUDE_SKILL_DIR}/../../docs/sources/aiken/` - Aiken language docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/aiken-stdlib/` - Aiken standard library docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/plinth/` - Plinth (PlutusTx) docs

### Step 3: Identify expensive operations

Search the validator code for known cost centers:

**High CPU cost:**
- Nested list traversals (O(n*m) comparisons)
- Value comparisons (comparing two `Value`s traverses both nested maps) -- expensive for multi-asset values
- Large datum deserialization
- Cryptographic hashing (blake2b, sha256)
- On-chain signature verification (extremely expensive -- use `extra_signatories` instead)

**High memory cost:**
- Building large intermediate data structures
- Repeated datum deserialization
- String concatenation for trace messages
- Map/filter chains that create intermediate lists

**Script size bloat:**
- Trace messages (string literals embedded in compiled output)
- Dead code (unreachable branches, unused functions)
- Redundant type conversions
- Inlined functions that could be shared

### Step 4: Apply optimizations

#### Execution unit optimizations

**Order pattern matching by frequency:**
```aiken
// Most common action first -- UPLC checks branches sequentially
when redeemer is {
  Swap -> check_swap(...)           // 90% of transactions
  AddLiquidity -> check_add(...)    // 8%
  RemoveLiquidity -> check_remove(...)  // 1.5%
  UpdateParams -> check_update(...)     // 0.5%
}
```

**Fail fast -- check cheap conditions before expensive ones:**
```aiken
// GOOD: Cheap signer check (O(small n)) before expensive output scan (O(large n))
list.has(tx.extra_signatories, datum.owner) &&
check_outputs(tx.outputs, expected_value)
```

**Extract common sub-expressions:**
```aiken
// BAD: Resolves own input twice
list.any(tx.outputs, fn(o) { o.address == resolve_own_address(tx, own_ref) }) &&
list.all(tx.outputs, fn(o) {
  o.address != resolve_own_address(tx, own_ref) || check_value(o)
})

// GOOD: Compute once, reuse
expect Some(own_input) = transaction.find_input(tx.inputs, own_ref)
let own_addr = own_input.output.address
list.any(tx.outputs, fn(o) { o.address == own_addr }) &&
list.all(tx.outputs, fn(o) { o.address != own_addr || check_value(o) })
```

**Reduce list traversals:**
```aiken
// BAD: Two separate passes over outputs
let has_script_output = list.any(tx.outputs, fn(o) { o.address == script_addr })
let has_payment = list.any(tx.outputs, fn(o) { o.address == seller })

// GOOD: Single pass with combined check
let (has_script, has_pay) =
  list.foldl(tx.outputs, (False, False), fn(o, acc) {
    let (s, p) = acc
    (s || o.address == script_addr, p || o.address == seller)
  })
```

**Use `expect` instead of `when` for single-variant destructuring:**
```aiken
// LARGER (compiled): when with explicit fail
when datum is {
  MyDatum { owner, amount } -> use(owner, amount)
  _ -> fail
}

// SMALLER: expect compiles to direct destructure
expect MyDatum { owner, amount } = datum
use(owner, amount)
```

#### Script size optimizations

**Remove traces for production builds:**
```bash
# Development (with traces for debugging)
aiken build

# Production (traces removed, 10-30% smaller)
aiken build --trace-level silent
```

**Extract shared helper functions:**
```aiken
// BAD: Duplicated logic in each branch
when redeemer is {
  Claim -> {
    expect Some(out) = list.find(tx.outputs, fn(o) { o.address == addr })
    assets.lovelace_of(out.value) >= amount && list.has(tx.extra_signatories, owner)
  }
  Update -> {
    expect Some(out) = list.find(tx.outputs, fn(o) { o.address == addr })
    assets.lovelace_of(out.value) >= amount && list.has(tx.extra_signatories, owner)
  }
}

// GOOD: Shared function
fn check_output_and_signer(tx, addr, amount, signer) {
  expect Some(out) = list.find(tx.outputs, fn(o) { o.address == addr })
  assets.lovelace_of(out.value) >= amount && list.has(tx.extra_signatories, signer)
}
```

**Remove dead code and unused imports:**
Search for functions, types, and imports that are not referenced. Unused code still contributes to script size.

#### Data structure optimizations

- Use `Pair<a, b>` instead of 2-element tuples when possible (smaller UPLC representation)
- For small fixed collections, explicit fields are cheaper than lists
- For lookups, sorted lists with early-exit beat unsorted lists
- Smaller datums mean less deserialization cost -- remove fields that can be computed from other fields

### Step 5: Consider reference scripts

For scripts over approximately 4 KB that will be used in multiple transactions:

- Store the script as a reference script in a UTxO
- Reference it by hash in subsequent transactions
- The script is paid for once at creation and amortized over many uses
- Reduces per-transaction size significantly

### Step 6: Verify and benchmark

After applying optimizations, the user should verify:

1. **All existing tests still pass**: `aiken check`
2. **Script size delta**: Compare compiled sizes before and after
3. **CPU units delta**: Run `aiken bench` and compare
4. **Memory units delta**: Run `aiken bench` and compare
5. **No security checks were removed**: Review changes for correctness

Provide before/after comparison format:
```
                Before        After        Delta
cpu:        2,345,678    1,890,123     -19.4%
mem:          234,567      198,432     -15.4%
size:           4,567        3,890     -14.8%
```

### Step 7: Document trade-offs

If any optimization involves a trade-off (e.g., increased size for lower CPU), document:
- What was changed and why
- The measured impact on each metric
- Any correctness considerations

## References

- `references/uplc-cost-model.md` -- UPLC cost model basics, operation costs, and budget limits
- Search `${CLAUDE_SKILL_DIR}/../../docs/sources/` for benchmark results and performance requirements
- Aiken documentation on optimization: https://aiken-lang.org
- Use `aiken build --trace-level silent` for production builds
- Use `aiken bench` for execution unit measurements
