# Advanced & Scaling Patterns

When a straightforward validator would blow the script-size limit, or would re-run
expensive logic once per script input (worst case O(n²) work), reach for these. They
are distilled from the Anastasia Labs **`aiken-design-patterns`** library (v1.7.0),
readable under `docs/sources/aiken-design-patterns/lib/aiken-design-patterns/`. Note:
several depend on the external `aiken_scott_utils` package (e.g. `foldl4`) — a
transitive dependency, not stdlib (`foldr2` is plain stdlib `aiken/collection/list`). Each entry gives *when to reach for it*, the
*mechanism*, and the *source file* to read. For the foundational validator patterns
these build on, see `aiken-patterns.md`.

## Run shared logic once: withdraw-zero / stake validator

- **Reach for it when** a transaction spends multiple UTxOs from the same script and
  you want one shared/global check instead of N copies of the spend logic — batch
  settlement, DEX order matching, any "validate the whole tx once."
- **Mechanism** — give each spend a *minimal* endpoint that only proves "a withdrawal
  for staking-script hash `H` exists in this tx," and put the real logic in `H`'s
  `withdraw` handler, which the ledger runs **once**. Withdrawing **0 ADA** is free
  and needs no rewards. This is the same pattern as the "Staking Validator" in
  `aiken-patterns.md`; the library's `stake-validator.ak` adds `validate_withdraw`,
  `validate_withdraw_with_amount`, and the cheapest `validate_withdraw_minimal`.
- **Source:** `stake-validator.ak`.

## Match inputs to outputs cheaply: UTxO indexers

- **Reach for it when** a spend must check its corresponding output(s) and on-chain
  *searching* is too costly or bug-prone. The off-chain builder passes the indices in
  the redeemer; the validator uses `list.at` (direct access) and then *proves* the
  index is right.
- **Singular** (`singular-utxo-indexer.ak`): `one_to_one(input_index, output_index,
  own_ref, …)` picks `inputs[input_index]`, asserts `own_ref == its output_reference`
  (proving the index really is the spending input), picks `outputs[output_index]`, and
  runs your `validation_logic(input, output)`. `one_to_many` walks output indices with
  a fold that **enforces strictly-ascending order** so no output index is reused.
- **Multi** (`multi-utxo-indexer.ak`): for **multiple** same-script inputs in one tx.
  The redeemer supplies `Pairs<Int, Int>` (input-idx → output-idx); a single fold
  walks inputs once, and for each script input pops the next index pair enforcing
  **strictly-ascending** in/out indices (`in1 > in0 && out1 > out0`). This is both the
  O(n) speed-up **and** the anti-double-satisfaction guard (injective pairing — two
  inputs can't claim one output). It ends by asserting every index was consumed and
  every script input matched.
- **Critical caveat:** the indexers do **not** solve double satisfaction for you in
  the singular case — `singular-utxo-indexer` takes a mandatory
  `double_satisfaction_prevented: Bool` argument precisely as a reminder that *you*
  must implement that protection. The multi-indexer's ascending-index discipline is
  what makes its pairing injective.
- **Sources:** `singular-utxo-indexer.ak`, `multi-utxo-indexer.ak`.

## Anchor once-per-tx logic to a mint: transaction-level minter

- **Reach for it when** you want the "run heavy logic once" benefit of withdraw-zero
  but the transaction already mints/burns a state token, so anchoring to the mint is
  more natural than a withdrawal.
- **Mechanism** — the spend endpoint only proves the mint endpoint runs; the real
  logic lives in the `mint` handler (executed once per policy per tx).
  `validate_mint(...)` asserts the redeemer at an index has purpose `Mint(policy)` and
  hands your validator the `Dict<AssetName, Int>` for that policy;
  `validate_mint_minimal` just requires a non-empty mint/burn under the policy.
- **Source:** `tx-level-minter.ak`.

## Offload heavy computation: merkelized validator

- **Reach for it when** a validator is too large to fit the script-size limit, or a
  costly computation (or a space-for-time lookup table) would blow the execution
  budget.
- **Mechanism** — move the computation into a separate **withdrawal** (staking)
  observer script that runs once; the main validator only *consumes the claimed
  result* and verifies the inputs match. `delegated_compute(function_input, …)` reads
  the withdrawal script's redeemer, asserts its input equals `function_input`, and
  returns the coerced `result`; `computation_withdrawal_wrapper` runs the actual
  function inside the observer and asserts `result == computed`. (Reference scripts are
  capped at 200 KiB and priced steeply — a real constraint here.)
- **Source:** `merkelized-validator.ak`.

## Authenticate a script instance on-chain: parameter validation

- **Reach for it when** one script must confirm that *another* address is a specific
  instance of a known **parameterized** script — e.g. a minting policy that must ensure
  its tokens can only land at instances of a spend script parameterized by a user's
  wallet — without hardcoding every instance hash.
- **Mechanism (two halves)** — either **reconstruct the applied hash** on-chain from a
  known compile-time prefix + `blake2b_224(param)` + postfix and compare (params must
  be constant-length), or **wrap the parameterized script** so that inside the
  instance it asserts `blake2b_224(serialise(param)) == hashed_parameter` before
  delegating to the real logic.
- **Source:** `parameter-validation.ak`.

## Unbounded on-chain collections: linked list

- **Reach for it when** you need an **unbounded, authenticated collection/set/map**
  (registry, membership set, per-user records) — you cannot grow it inside one datum,
  because the UTxO becomes too large/expensive and eventually unspendable.
- **Mechanism** — spread the collection across many UTxOs; each element is one UTxO
  holding ADA + **exactly one list NFT** + an inline `Element` datum + a `Link`
  (`Option<NodeKey>`) to its successor. The crucial idiom: **split enforcement across
  a spend gate and a mint policy** — the spend handler only *permits* structural
  changes (checks a list-policy mint/burn is present), and the paired **minting
  policy proves** the exact transition. "Spend permits, mint proves." Variants: base
  (strict), advanced (reference-script-aware, extra assets allowed), nested (two-level).
- **Source:** `linked-list.ak` (+ `linked-list/advanced.ak`, `linked-list/nested.ak`).

## Canonicalize before comparing: validity-range normalization

- **Reach for it when** any deadline/time-window logic needs to compare validity
  ranges and you want to eliminate a whole class of bugs from redundant encodings
  (per-bound inclusive flags, empty ranges).
- **Mechanism** — `normalize_time_range(validity_range)` folds the inclusive flags
  into the integer bounds (exclusive lower ⇒ +1, exclusive upper ⇒ −1) and collapses
  to a small sum type (`ClosedRange | FromNegInf | ToPosInf | Always | InvalidRange`),
  re-checking phase-1 assumptions so comparisons are source-agnostic and safe.
- **Source:** `validity-range-normalization.ak`.

The general lesson under several of these: **reduce a redundant domain to a canonical
form, or replace on-chain search with a caller-supplied index you then prove correct.**
Both trade a little redeemer data for large on-chain savings.
