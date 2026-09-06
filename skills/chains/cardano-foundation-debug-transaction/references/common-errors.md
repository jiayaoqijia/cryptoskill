# Common Cardano Transaction Errors

Reference for Cardano ledger errors: what they mean, what causes them,
and how to fix them.

---

## ValueNotConservedUTxO

**What it means:** The total value of inputs does not equal the total value
of outputs plus the fee (adjusted for minting/burning).

**The ledger rule:**
```
sum(inputs) + mint = sum(outputs) + fee + burn
```

**Common causes:**
- Forgot to include all input UTxOs in the transaction
- Manually set output values incorrectly
- Minted tokens but did not include them in an output
- Burned tokens but did not remove them from outputs
- Fee was not accounted for correctly

**Fix:** Let the SDK handle coin selection and change output calculation.
If building manually, verify the value equation above balances exactly.

---

## InsufficientCollateral

**What it means:** The transaction executes a Plutus script but does not
provide enough collateral, or provides no collateral at all.

**Common causes:**
- No collateral input specified in a Plutus transaction
- Collateral UTxO value is less than 150% of the transaction fee
- Collateral UTxO was consumed by another transaction

**Fix:**
- Add a collateral input: a UTxO containing at least 5 ADA with no native tokens
- Keep a dedicated collateral UTxO that you never spend in normal transactions
- If using a wallet, enable collateral setting (most wallets have this option)

---

## NonOutputSupplimentaryDatums

**What it means:** The transaction includes a datum in its witness set that
is not referenced by any output or script.

**Common causes:**
- Provided a datum hash in the witness set but no output uses that datum hash
- Removed an output that referenced the datum but forgot to remove the datum
- Mismatch between inline datum and datum hash usage

**Fix:** Either remove the unused datum from the witness set, or ensure an
output references it via datum hash. If using inline datums, the datum should
be attached directly to the output, not in the witness set.

---

## ExUnitsTooBigUTxO

**What it means:** The Plutus script execution units (CPU and/or memory)
exceed the per-transaction protocol limits.

**Protocol limits (mainnet, current — verify against live protocol params):**
- CPU: 10,000,000,000 steps per transaction (`max_tx_ex_steps`)
- Memory: 16,500,000 units per transaction (`max_tx_ex_mem`)

**Common causes:**
- Script performs too much computation (large loops, complex math)
- Too many script inputs in a single transaction
- Inefficient use of on-chain data structures (large lists, maps)
- Script traces left in production code

**Fix:**
- Optimize the validator: remove traces, simplify logic, use efficient patterns
- Reduce the number of script inputs per transaction (batch smaller)
- Move computation off-chain and verify results on-chain
- Use the `optimize-validator` skill for specific optimization guidance

---

## ScriptFailure

**What it means:** A Plutus script evaluated to `False` or threw an error
during execution.

**Common causes:**
- Wrong redeemer value for the action being performed
- Datum does not match expected structure (wrong Constr index, missing fields)
- Authorization check failed (wrong signer)
- Time check failed (transaction validity interval outside script's range)
- Business logic condition not met

**Fix:**
1. Check the script's trace output for the specific assertion that failed
2. Verify the redeemer matches the expected variant and data
3. Verify the datum structure matches the script's type definition
4. Check `extra_signatories` includes required key hashes
5. Verify `validity_range` satisfies the script's time checks
6. Test with an emulator to get detailed failure information

---

## MissingRequiredSigners

**What it means:** The transaction specifies `required_signers` (used by
Plutus scripts to check `extra_signatories`) but the corresponding
signatures are not present.

**Common causes:**
- Forgot to sign the transaction with all required keys
- Added a required signer for the wrong key hash
- Multi-sig transaction missing one or more signatories

**Fix:** Ensure every key hash listed in `required_signers` has a
corresponding signature in the transaction. In most SDKs, add all
required signing keys to the sign step.

---

## OutputTooSmallUTxO

**What it means:** One or more transaction outputs contain less ADA than
the minimum UTxO value required by protocol parameters.

**How min-UTxO is calculated:**
The minimum ADA depends on the output's size:
- ADA-only output: ~1 ADA
- Output with one token: ~1.2-1.5 ADA
- Output with many tokens or large datum: can be 2-5+ ADA

**Common causes:**
- Sending only tokens without enough ADA to cover min-UTxO
- Creating a script output with a datum but insufficient ADA
- Splitting UTxOs too finely

**Fix:** Increase the ADA amount in the offending output. Most SDKs have
a `min_utxo` helper that calculates the exact minimum for a given output.

---

## FeeTooSmallUTxO

**What it means:** The fee specified in the transaction is less than the
minimum fee calculated from the transaction size and protocol parameters.

**Common causes:**
- Manually set the fee too low
- Transaction grew larger after fee calculation (e.g., additional signatures)
- Using outdated protocol parameters for fee estimation

**Fix:** Let the SDK calculate the fee automatically. If calculating
manually, use the formula: `fee = a * tx_size_bytes + b` where `a` and `b`
are protocol parameters (`minFeeA` and `minFeeB`). For Plutus transactions,
execution unit costs are added on top.

---

## BadInputsUTxO

**What it means:** One or more transaction inputs reference UTxOs that do
not exist in the current ledger state.

**Common causes:**
- The UTxO was already consumed by a previous transaction
- Using a UTxO from a different network (preview vs. preprod)
- Stale UTxO cache -- the UTxO was consumed between query and submit
- Typo in the transaction hash or output index

**Fix:**
- Re-query the UTxO set for the address and use fresh UTxOs
- Implement retry logic: if submission fails, re-query and rebuild
- Verify you are targeting the correct network
- Check the UTxO exists on a block explorer before building

---

## CollateralContainsNonADA

(Ledger constructor name; Ogmios reports it as `NonAdaCollateral`, code 3133.)

**What it means:** The collateral input contains native tokens in addition
to ADA. Collateral must be pure ADA.

**Common causes:**
- Selected a UTxO with native tokens as collateral
- Wallet automatically selected an inappropriate UTxO

**Fix:** Use a UTxO that contains only ADA as collateral. Create a
dedicated collateral UTxO by sending 5 ADA to yourself in a simple
transaction, then use that UTxO exclusively for collateral.

---

## OutsideValidityIntervalUTxO

**What it means:** The current slot (time) is outside the transaction's
declared validity interval.

**Common causes:**
- `invalid_before` is set to a future slot (transaction not yet valid)
- `invalid_hereafter` is set to a past slot (transaction expired)
- Transaction was built long ago and the validity window has passed
- Clock skew between the machine and the Cardano node
- Slot-to-POSIX-time conversion error

**Fix:**
- Set a reasonable validity window: current slot to current slot + 900
  (roughly 15 minutes on mainnet)
- For time-sensitive Plutus scripts: ensure the validity interval is tight
  enough to satisfy the script's time assertions but wide enough to allow
  for submission delays
- Rebuild the transaction if it has expired
- Verify your slot calculations match the network's epoch settings

---

## Debugging Checklist

When encountering any error:

1. Read the full error message -- the error type name identifies the issue
2. Check the simplest causes first (wrong network, stale UTxOs, insufficient ADA)
3. Verify the value equation balances: inputs = outputs + fee +/- mint/burn
4. For Plutus errors: check redeemer, datum, signers, and validity range
5. Use transaction evaluation (dry run) to test fixes before submitting
6. Test on Preview testnet before Preprod or Mainnet
