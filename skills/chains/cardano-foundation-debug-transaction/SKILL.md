---
name: debug-transaction
description: >-
  Debug failing Cardano transaction, fix transaction error, diagnose
  ValueNotConservedUTxO, InsufficientCollateral, script failure, budget
  exceeded, datum mismatch, missing signer, min-UTxO error.
allowed-tools: Read Grep Glob
disallowed-tools: WebFetch WebSearch
---

<!-- Documentation lookup path: ${CLAUDE_SKILL_DIR}/../../docs/sources/ -->

# Debug Cardano Transaction

Guide the user through diagnosing and fixing failing Cardano transactions.
Works with any SDK (Mesh, Evolution SDK, PyCardano, cardano-client-lib)
and covers both native script and Plutus script errors.

## When to Use

- User has a transaction that fails to build, sign, or submit
- User gets a Cardano ledger error message they do not understand
- User has a Plutus script that fails during execution
- User has a transaction rejected by the node
- User wants to understand why a transaction was rolled back

## When NOT to Use

- User wants to build a new transaction from scratch -- use `build-transaction`
- User wants to review a smart contract for vulnerabilities -- use `review-contract`
- User wants to optimize a validator's execution budget -- use `optimize-validator`
- User is designing a token standard -- use `design-token`

## Key Principles

1. **Read the error message carefully.** Cardano error messages are verbose
   but precise. They usually tell you exactly what is wrong. The error type
   name alone often identifies the problem.

2. **Reproduce before fixing.** Ensure you can consistently reproduce the error
   before attempting a fix; transaction failures are deterministic, so the same inputs
   produce the same error. A root cause you have reproduced beats one reasoned from logs
   alone.

3. **Isolate the failure layer.** Determine if the error occurs during
   transaction building (SDK), during submission (node), or during script
   evaluation (Plutus VM).

4. **Check the simple things first.** Most transaction failures are caused
   by insufficient ADA, missing UTxOs, or wrong network. Check these
   before investigating complex script logic.

5. **Use the transaction evaluator.** Most SDKs support dry-run evaluation
   that simulates the transaction without submitting. Use this to test
   fixes before spending real resources.

## Workflow

### Step 1: Capture the Full Error

Ask the user for:

1. The complete error message (not just the first line)
2. The SDK and version they are using
3. The network (preview, preprod, mainnet)
4. The transaction type (send, mint, script interaction, etc.)
5. The code that builds the transaction (if available)

### Step 2: Search Bundled Documentation

Search the bundled documentation for relevant content:
- `${CLAUDE_SKILL_DIR}/../../docs/sources/evolution-sdk/` - Evolution SDK docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/mesh-sdk/` - Mesh SDK docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/pycardano/` - PyCardano docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/cardano-client-lib/` - cardano-client-lib docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/cardano-node-wiki/` - Cardano node wiki

### Step 3: Identify the Error Category

Classify the error into one of these categories:

| Category | Common Errors | Likely Cause |
|----------|---------------|--------------|
| Value errors | `ValueNotConservedUTxO`, `OutputTooSmallUTxO` | Math error in inputs/outputs, min-UTxO not met |
| Input errors | `BadInputsUTxO` | UTxO already spent or does not exist |
| Fee errors | `FeeTooSmallUTxO` | Fee calculation incorrect or overridden |
| Collateral errors | `InsufficientCollateral`, `CollateralContainsNonADA` | Missing or wrong collateral for Plutus tx |
| Script errors | `ScriptFailure`, `ExUnitsTooBigUTxO` | Plutus script fails or exceeds budget |
| Datum errors | `NonOutputSupplimentaryDatums` | Datum provided but not referenced |
| Signer errors | `MissingRequiredSigners` | Required signature not included |
| Validity errors | `OutsideValidityIntervalUTxO` | Transaction time range does not match current slot |

Search `${CLAUDE_SKILL_DIR}/../../docs/sources/` or see `references/common-errors.md` for
detailed error explanations.

### Step 4: Diagnose the Root Cause

For each error category, follow these diagnostic steps:

#### Value Errors

1. List all transaction inputs and their values (ADA + tokens)
2. List all transaction outputs and their values
3. Verify: sum(input values) = sum(output values) + fee - mint + burn
4. Check each output meets the minimum UTxO value (~1-2 ADA depending on
   datum and token bundle size)
5. For token transactions: ensure all input tokens appear in outputs
   (tokens cannot disappear)

#### Input Errors

1. Check if the UTxO reference (tx_hash#index) exists on-chain
2. Verify it has not been consumed by another transaction
3. Confirm you are querying the correct network
4. Check for race conditions: another transaction may have consumed
   the UTxO between query and submit

#### Fee Errors

1. Check if you are manually setting fees instead of letting the SDK
   calculate them
2. Verify protocol parameters are up to date
3. For Plutus transactions: ensure execution units are included in
   fee calculation

#### Collateral Errors

1. Verify a collateral input is included in the transaction
2. Ensure the collateral UTxO contains only ADA (no native tokens)
3. Check collateral amount is at least 150% of the transaction fee
4. Verify the collateral UTxO has not been consumed

#### Script Errors

1. Check the redeemer matches what the script expects
2. Verify the datum (if spending) matches the expected structure
3. Look at script logs/traces for the specific assertion that failed
4. Check execution budget -- scripts have CPU and memory limits
5. Test the script in an emulator or with `evaluate_tx` before submitting

#### Datum Errors

1. If using inline datums: ensure the output has the datum attached
2. If using datum hashes: ensure the full datum is included in the
   transaction witness set
3. Verify datum CBOR encoding matches what the script expects
4. Check for Plutus data type mismatches (Constr index, field count)

#### Signer Errors

1. Check which verification key hashes the script requires
   in `extra_signatories`
2. Ensure all required keys are signing the transaction
3. For multi-sig native scripts: verify the correct combination of signers

#### Validity Errors

1. Check the transaction's validity interval (valid_from, valid_to)
2. Verify current slot is within that interval
3. For Plutus scripts that check time: ensure `validity_range` is tight
   enough for the script's `must_be_before` / `must_be_after` checks
4. Account for slot-to-POSIX-time conversion

### Step 5: Apply the Fix

Once the root cause is identified:

1. Explain what went wrong and why
2. Provide corrected code for the specific SDK the user is using
3. Highlight the exact change (e.g., "add this collateral input" or
   "change the output value from X to Y")
4. Explain how the fix addresses the root cause

### Step 6: Verify the Fix

1. Use transaction evaluation (dry run) to test before submitting
2. Submit to testnet first
3. Verify on a block explorer that the transaction succeeded
4. Check all outputs match expectations

### Step 7: Prevention

Suggest practices to avoid the error in the future:

- **For value errors:** Always let the SDK calculate change outputs.
  Never manually compute output values.
- **For input errors:** Query UTxOs immediately before building.
  Implement retry logic for concurrent environments.
- **For collateral errors:** Maintain a dedicated collateral UTxO
  (5 ADA, no tokens) and never spend it in regular transactions.
- **For script errors:** Write comprehensive test cases. Use
  property-based testing for validators.
- **For datum errors:** Define datum types in a shared module used
  by both on-chain and off-chain code.
- **For validity errors:** Set reasonable time windows (e.g., current
  time +/- 15 minutes) rather than exact times.

## Debugging Tools

### Transaction Evaluation (Dry Run)

Most SDKs support evaluating a transaction without submitting:

- **Mesh SDK:** Use Ogmios `evaluateTx` endpoint
- **Evolution SDK:** Use `client.newTx()...buildEither()` for non-throwing inspection (`result._tag === "Left"` carries a tagged error). On Plutus failure, `EvaluationError` exposes `failures[]` with per-script `purpose`, `label`, `validationError`, and `traces` for trace-message-level debugging
- **PyCardano:** `context.evaluate_tx(tx)`
- **cardano-cli:** `cardano-cli latest transaction calculate-plutus-script-cost` (there is no `transaction evaluate` subcommand; `transaction build` also evaluates implicitly)

### Block Explorers

- Preview: https://preview.cardanoscan.io
- Preprod: https://preprod.cardanoscan.io
- Mainnet: https://cardanoscan.io

Look up transaction hashes, UTxOs, and script addresses.

### CBOR Decoders

For inspecting raw transaction bytes:
- https://cbor.me
- `cardano-cli transaction view --tx-file tx.signed`

### Script Budget Analysis

When `ExUnitsTooBigUTxO` occurs:

1. Evaluate the transaction to get actual CPU and memory usage
2. Compare against protocol limits (mainnet currently: 10,000,000,000 CPU
   steps and 16,500,000 memory units per transaction — query
   `max_tx_ex_steps`/`max_tx_ex_mem` from current protocol parameters rather
   than trusting static numbers)
3. If close to limits: optimize the validator (use `optimize-validator`)
4. If far over limits: redesign the approach (fewer script inputs,
   simpler logic, batching)

## References

- `references/common-errors.md` -- complete error reference with causes and fixes
- Search `${CLAUDE_SKILL_DIR}/../../docs/sources/` for SDK-specific error handling guides
- Cardano ledger errors: https://github.com/IntersectMBO/cardano-ledger
