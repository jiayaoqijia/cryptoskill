# Testing Cardano Validators

Writing a validator is only half the job — you must *prove* it enforces what you
intended. Aiken validators are plain functions, so you test a handler by calling it
directly with a constructed `Transaction` and asserting it returns `True` (or `fail`s).
Two things make this rigorous: a disciplined methodology, and good tooling for building
the transaction.

## The boolean-toggle methodology

The most reliable way to prove every guard actually guards: write **one success test**
with all conditions valid, then **one failing test per validation condition**, each
flipping exactly one condition. If a test that flips a guard still passes, that guard
isn't doing its job. This turns "I think it checks the deadline" into a proof.

```aiken
test claim_succeeds() {
  vesting.spend(Some(datum), Claim, oref,
    tx_with([beneficiary], interval.entirely_after(deadline)))
}

test claim_before_deadline_fails() fail {
  vesting.spend(Some(datum), Claim, oref,
    tx_with([beneficiary], interval.entirely_before(deadline)))
}

test claim_wrong_signer_fails() fail {
  vesting.spend(Some(datum), Claim, oref,
    tx_with([attacker], interval.entirely_after(deadline)))
}
```

Two ways to assert failure: the **`test name() fail { … }`** annotation (the body is
expected to `fail` or return `False`), or **boolean negation** `!validator.spend(…)`.
The `fail` annotation is preferred when the invalid input should make the validator
`fail` (via an `expect`); negation when it simply returns `False`. Both appear across
the Cardano Foundation templates (payment-splitter, crowdfund, token-transfer use
`fail`; vesting uses negation).

## Building the test transaction — two styles

You need a `Transaction` to pass in. There are two approaches; they interoperate, so
you can adopt the mock primitives without committing to the full builder.

**1. Manual — stdlib `transaction.placeholder` + record update.** Start from the
placeholder and override only the fields the test cares about. Zero external
dependencies; the transaction shape is visible as a literal, which is good for
teaching and for a handful of tests.

```aiken
fn tx_with(signers, range) -> Transaction {
  Transaction {
    ..transaction.placeholder,
    extra_signatories: signers,
    validity_range: range,
  }
}
```

The cost shows at scale: building inputs/outputs with specific values and datums this
way is ~30 lines of nested `Input { output: Output { … } }` records, and it gets
copy-pasted across every test (see the manual style in
`docs/sources/cardano-use-case-templates/vault/onchain/aiken/validators/vault-test.ak`).

**2. Mocktail — a fluent builder + deterministic mock primitives.** `mocktail` is a
module of the sidan-lab **vodka** library (an external Aiken dependency,
`github.com/sidan-lab/vodka`; add it to `aiken.toml`). It is the de-facto testing
library across the Foundation's reference templates and is documented in the bundle at
`docs/sources/mesh-sdk/resources/cardano-course/04-contract-testing.mdx`. It replaces
the verbose record construction with a pipeline that fills sensible defaults:

```aiken
use mocktail.{mocktail_tx, tx_in, tx_out, mint, required_signer_hash, complete}
use mocktail/virgin_key_hash.{mock_pub_key_hash, mock_policy_id}
use mocktail/virgin_output_reference.{mock_utxo_ref}

test mint_valid() {
  let tx =
    mocktail_tx()
      |> mint(True, 1, policy_id, asset_name)
      |> tx_out(True, script_addr, from_asset(policy_id, asset_name, 1))
      |> complete()
  my_policy.mint(redeemer, policy_id, tx)
}
```

Mock primitives give deterministic values without hardcoding hex:
`mock_pub_key_hash(n)`, `mock_script_hash(n)`, `mock_policy_id(n)`,
`mock_pub_key_address(n, stake)`, `mock_script_address(n, stake)`,
`mock_utxo_ref(tx_idx, out_idx)`, `mock_tx_hash(n)`, `mock_interval(lower, upper)`.

**The killer feature — the `include: Bool` first argument.** Every builder step
(`tx_in`, `tx_out`, `mint`, `required_signer_hash`, `invalid_before`,
`invalid_hereafter`, `ref_tx_in`, …) takes an `include` flag first. That lets a
*single* parameterized `get_test_tx(...)` function generate both valid and invalid
transactions by toggling one flag — the boolean-toggle methodology, expressed once:

```aiken
fn get_tx(is_signed: Bool, is_before_expiry: Bool) -> Transaction {
  mocktail_tx()
    |> tx_in(True, mock_tx_hash(1), 0, in_value, script_addr)
    |> required_signer_hash(is_signed, owner)
    |> invalid_hereafter(is_before_expiry, 999)
    |> complete()
}
```

Real, readable examples in the bundle:
`docs/sources/cardano-use-case-templates/anonymous-data/onchain/aiken/validators/tests/anonymous-data-test.ak`,
`.../simple-wallet/onchain/aiken/validators/tests/funds-test.ak`,
`.../escrow/onchain/aiken/tests/escrow.ak`.

## When to use which

- **Few tests, teaching clarity, or a deliberate zero-dependency validator** → manual
  `placeholder`. This is what the patterns in `aiken-patterns.md` assume.
- **Many failure permutations of the same transaction shape** → mocktail's
  parameterized builder with `include` flags; far less duplication.
- Either way, you can pull in mocktail's `mock_*` constructors just to avoid
  hardcoding addresses/hashes/orefs, even in an otherwise-manual test.

## cocktail / vodka on the validator side

The same vodka library exposes **cocktail** — predicate helpers used *inside*
validators (not just tests): `key_signed` / `all_key_signed` / `one_of_keys_signed`,
`valid_after` / `valid_before`, `outputs_at` / `outputs_with` / `inputs_with` /
`inputs_with_policy`, `value_geq` / `get_all_value_to`, `only_minted_token`. Most of
the Foundation template validators import it, so you will see it constantly when
reading real Aiken — recognizing it is essential even if your own examples stay on the
stdlib. The teaching validators in this skill use the stdlib directly (self-contained,
no external dep); cocktail is a convenience layer over the same primitives, not a
different model.
