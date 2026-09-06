# Common Aiken Validator Patterns

Reusable code structures for common Cardano validator designs in Aiken, plus the
**design decisions** behind them. The concrete patterns below show *how*; the "eUTxO
Design Decisions" section at the end is *what to reach for when*, distilled from real
validators in the bundle. For advanced/scaling techniques (UTxO indexers, merkelized
validators, linked lists) when a straightforward validator won't fit, see
`advanced-patterns.md`.

All patterns target the current Aiken stdlib (v3, `cardano/*` modules) and are
compile-checked against aiken v1.1.21 + stdlib v3.1.0. Note for readers of older
material: the `aiken/transaction/value` module generation is gone — `tx.mint` is a
plain `Value` (no `from_minted_value` conversion), credentials are
`VerificationKey`/`Script` (not `VerificationKeyCredential`/`ScriptCredential`),
and `tx.withdrawals` is `Pairs<Credential, Lovelace>`, not a `Dict`.

## Vesting Validator

Lock funds until a deadline, then allow the beneficiary to claim.

```aiken
use aiken/collection/list
use aiken/crypto.{VerificationKeyHash}
use aiken/interval
use cardano/transaction.{OutputReference, Transaction}

pub type VestingDatum {
  beneficiary: VerificationKeyHash,
  owner: VerificationKeyHash,
  deadline: Int,
}

pub type VestingRedeemer {
  Claim
  Cancel
}

validator vesting {
  spend(
    datum: Option<VestingDatum>,
    redeemer: VestingRedeemer,
    _own_ref: OutputReference,
    tx: Transaction,
  ) {
    expect Some(d) = datum
    when redeemer is {
      Claim -> {
        let signed = list.has(tx.extra_signatories, d.beneficiary)
        let after_deadline =
          interval.is_entirely_after(tx.validity_range, d.deadline)
        signed && after_deadline
      }
      Cancel -> {
        list.has(tx.extra_signatories, d.owner)
      }
    }
  }
}
```

Key points:
- Check both signer AND deadline for Claim
- Use `is_entirely_after` to prevent time range manipulation
- Separate owner for Cancel so the funder can reclaim if needed
- No continuing output needed (funds leave the script entirely)

## Marketplace (Buy/Sell)

List an asset for sale at a fixed price.

```aiken
use aiken/collection/list
use cardano/address.{Address, VerificationKey}
use cardano/assets.{AssetName, PolicyId}
use cardano/transaction.{OutputReference, Transaction}

pub type ListingDatum {
  seller: Address,
  price: Int,
  policy_id: PolicyId,
  asset_name: AssetName,
}

pub type ListingRedeemer {
  Buy
  Cancel
}

validator marketplace {
  spend(
    datum: Option<ListingDatum>,
    redeemer: ListingRedeemer,
    _own_ref: OutputReference,
    tx: Transaction,
  ) {
    expect Some(d) = datum
    when redeemer is {
      Buy -> {
        // Find seller payment output by address (not index)
        let seller_paid =
          list.any(
            tx.outputs,
            fn(output) {
              output.address == d.seller && assets.lovelace_of(output.value) >= d.price
            },
          )
        seller_paid
      }
      Cancel -> {
        // Extract payment key hash from seller address
        expect VerificationKey(seller_pkh) = d.seller.payment_credential
        list.has(tx.extra_signatories, seller_pkh)
      }
    }
  }
}
```

Key points:
- Find seller output by full address (payment + staking), not by index
- Beware double satisfaction when multiple listings exist -- each Buy must pay its own seller independently
- Consider adding NFT authentication to prevent datum hijacking
- Check full address to prevent staking credential theft

## Multisig

Require M-of-N signatures to spend.

```aiken
use aiken/collection/list
use aiken/crypto.{VerificationKeyHash}
use cardano/transaction.{OutputReference, Transaction}

pub type MultisigDatum {
  signers: List<VerificationKeyHash>,
  required: Int,
}

pub type MultisigRedeemer {
  Approve
}

validator multisig {
  spend(
    datum: Option<MultisigDatum>,
    redeemer: MultisigRedeemer,
    _own_ref: OutputReference,
    tx: Transaction,
  ) {
    expect Some(d) = datum
    when redeemer is {
      Approve -> {
        let valid_count =
          list.foldl(
            d.signers,
            0,
            fn(signer, acc) {
              if list.has(tx.extra_signatories, signer) {
                acc + 1
              } else {
                acc
              }
            },
          )
        valid_count >= d.required
      }
    }
  }
}
```

Key points:
- Keep the signers list bounded (e.g., max 10) to prevent unbounded datum
- Consider adding a deadline or expiration for time-limited authorization
- Consider adding an Update action to rotate signers (with current threshold approval)

## Token Minting Policy (One-Shot / Unique NFT)

Mint a single token whose uniqueness is guaranteed by consuming a specific *seed*
UTxO. Because any UTxO can be spent only once in the whole history of the chain, a
policy gated on that spend can fire **at most once** — this is the foundation of
NFTs, thread tokens, and singleton state. The token name is an *optional* extra
constraint, **not** the uniqueness mechanism.

```aiken
use aiken/collection/dict
use aiken/collection/list
use cardano/assets.{AssetName, PolicyId}
use cardano/transaction.{OutputReference, Transaction}

pub type MintRedeemer {
  Mint
  Burn
}

validator token_mint(utxo_ref: OutputReference, expected_name: AssetName) {
  mint(redeemer: MintRedeemer, policy_id: PolicyId, tx: Transaction) {
    // Exactly one asset name may move under this policy, in either direction.
    // Destructuring a singleton list rejects any second token name outright,
    // and binds its signed quantity (positive = mint, negative = burn).
    expect [Pair(asset_name, amount)] =
      tx.mint
        |> assets.tokens(policy_id)
        |> dict.to_pairs()
    when redeemer is {
      // Uniqueness comes entirely from spending the seed UTxO -- a UTxO can be
      // spent only once ever, so this branch succeeds at most once. The name
      // check is an extra guard, not the guarantee.
      Mint -> {
        let seed_spent =
          list.any(tx.inputs, fn(input) { input.output_reference == utxo_ref })
        seed_spent && amount == 1 && asset_name == expected_name
      }
      Burn -> amount == -1 && asset_name == expected_name
    }
  }

  // Reject every other script purpose this hash might be invoked for.
  else(_) {
    fail
  }
}
```

Key points:
- The seed `utxo_ref` spent in the minting transaction is what makes this
  one-shot — not the name. Off-chain, pick any unspent UTxO from the minter's
  wallet and bake its `OutputReference` into the policy parameters.
- Destructuring `assets.tokens(tx.mint, policy_id) |> dict.to_pairs()` against the
  singleton `[Pair(asset_name, amount)]` forces exactly one token name under the
  policy — a second name makes the `expect` fail. This also removes the classic
  footgun of `list.all(fn(p) { p.2nd < 0 })`, which returns `True` on an empty
  list (a vacuously-passing burn).
- `Mint -> amount == 1` and `Burn -> amount == -1` constrain both quantity and
  direction.
- End the validator with `else(_) { fail }` so the same script hash can't be
  abused for another purpose.
- For fungible tokens with ongoing minting, gate on an admin signature or a
  supply cap instead of UTxO consumption (which only ever permits one mint).

**Canonical reference:** `docs/sources/aiken-examples/gift_card/validators/oneshot.ak`
(Aiken's own example) is the compile-tested version of this pattern; read it verbatim.

**Minting many unique NFTs at once (derive the name).** For a *batch* of unique
tokens rather than one fixed name, derive each name from the seed instead of
parameterizing it: hash the (unique) spent `output_reference`, e.g.
`blake2b_256(builtin.serialise_data(output_reference))`, or the first input's
reference concatenated with a counter. Because the seed reference is itself unique,
the derived names are unforgeable and collision-free — no `expected_name` parameter
needed. See `docs/sources/aiken-examples/gift_card/validators/multi.ak`.

**Burn-to-unlock (multi-purpose validators).** A common idiom pairs this `mint`
handler with a `spend` handler in the *same* validator, so a UTxO locked at the
script can only be unlocked by burning its token. Since both handlers share one
script hash, the spend handler recovers its own `policy_id` from the input's script
credential (`expect Script(policy_id) = own_input.output.address.payment_credential`)
rather than taking it as a parameter. See "eUTxO design decisions" below.

## Staking Validator (Withdraw-Zero Pattern)

Use a staking validator as a shared checker for batch operations.

```aiken
use aiken/collection/pairs
use aiken/crypto.{ScriptHash}
use cardano/address.{Credential, Script}
use cardano/transaction.{OutputReference, Transaction}

pub type BatchRedeemer {
  Process
}

fn validate_batch(_redeemer: BatchRedeemer, _tx: Transaction) -> Bool {
  todo @"shared batch validation"
}

fn check_input_specific(_datum: Data, _tx: Transaction) -> Bool {
  todo @"per-input checks"
}

validator shared_logic {
  withdraw(redeemer: BatchRedeemer, _account: Credential, tx: Transaction) {
    // Shared validation runs once per transaction
    // instead of once per input -- saves execution cost
    validate_batch(redeemer, tx)
  }
}

validator my_spending(staking_script_hash: ScriptHash) {
  spend(
    datum: Option<Data>,
    _redeemer: Data,
    _own_ref: OutputReference,
    tx: Transaction,
  ) {
    expect Some(d) = datum
    // Verify the staking validator ran by checking for its withdrawal.
    // Withdrawals are Pairs<Credential, Lovelace>, keyed by the bare credential.
    let staking_ran =
      pairs.has_key(tx.withdrawals, Script(staking_script_hash))
    // Do input-specific checks here (cheap, per-input)
    staking_ran && check_input_specific(d, tx)
  }
}
```

Key points:
- The staking validator runs once per transaction, reducing total cost for batch operations
- The spending validator MUST verify the withdrawal exists in `tx.withdrawals`
- The staking validator MUST perform real validation (never just return True)
- Use this pattern for DEX order matching, batch settlements, and similar operations

## State Machine

Track state transitions with an authentication NFT.

```aiken
use aiken/collection/list
use aiken/crypto.{VerificationKeyHash}
use cardano/assets.{AssetName, PolicyId}
use cardano/transaction.{InlineDatum, OutputReference, Transaction}

pub type State {
  Initialized
  Active
  Completed
}

pub type StateDatum {
  state: State,
  owner: VerificationKeyHash,
  data: Int,
  auth_token: AssetName,
}

pub type StateRedeemer {
  Activate
  Complete
  Abort
}

fn valid_transition(from: State, action: StateRedeemer) -> Option<State> {
  when (from, action) is {
    (Initialized, Activate) -> Some(Active)
    (Active, Complete) -> Some(Completed)
    (Initialized, Abort) -> None
    (Active, Abort) -> None
    _ -> fail @"Invalid state transition"
  }
}

validator state_machine(auth_policy: PolicyId) {
  spend(
    datum: Option<StateDatum>,
    redeemer: StateRedeemer,
    own_ref: OutputReference,
    tx: Transaction,
  ) {
    expect Some(d) = datum
    // Resolve own input and address
    expect Some(own_input) = transaction.find_input(tx.inputs, own_ref)
    let own_address = own_input.output.address
    // Verify auth token is present in input
    expect
      assets.quantity_of(own_input.output.value, auth_policy, d.auth_token) == 1
    when valid_transition(d.state, redeemer) is {
      Some(new_state) -> {
        // Find continuing output by auth token (not by index)
        expect Some(cont_output) =
          list.find(
            tx.outputs,
            fn(o) {
              o.address == own_address && assets.quantity_of(
                o.value,
                auth_policy,
                d.auth_token,
              ) == 1
            },
          )
        // Extract and verify datum transition
        expect InlineDatum(raw) = cont_output.datum
        expect cont_datum: StateDatum = raw
        // Check: state transitions correctly, immutable fields unchanged
        cont_datum.state == new_state && cont_datum.owner == d.owner && cont_datum.auth_token == d.auth_token
      }
      None ->
        // Terminal action: no continuing output, owner must sign
        list.has(tx.extra_signatories, d.owner)
    }
  }
}
```

Key points:
- Define valid transitions explicitly -- reject anything not listed
- Auth token prevents datum hijacking and enables output lookup by token
- Check that immutable fields (owner, auth_token) remain unchanged
- Handle terminal states (Abort) separately -- no continuing output required
- Find continuing output by auth token presence, never by output index

---

# eUTxO Design Decisions

The patterns above show *how* to write specific validators. This section is about
*what to reach for when* — the design decisions that recur across real Aiken code.
Every claim here is distilled from validators you can read in the bundle: the
Cardano Foundation use-case templates under
`docs/sources/cardano-use-case-templates/` (cited by use-case directory; each
validator lives at `<use-case>/onchain/aiken/validators/`) and Aiken's own examples
under `docs/sources/aiken-examples/`.

The mechanical security checks (double-satisfaction, datum hijacking, value
preservation, staking-credential theft…) live in the review-contract skill's
`references/vulnerability-checklist.md` — this section is the design layer above
them: how to shape the contract in the first place so those checks are easy to get
right.

## Parameter vs datum vs redeemer — the central axis

Every piece of information a validator needs enters through one of three doors.
Choosing the right door *is* eUTxO design.

- **Parameter** — a compile-time value baked into the script, producing a **unique
  script hash (and address) per configuration**. Reach for this when a value is
  fixed for the life of an instance and you *want* each instance to have its own
  address: a seed UTxO for one-shot uniqueness, an owner key, a deadline, a
  cross-script hash. Examples: `htlc(secret, expiration, owner)`,
  `crowdfund(beneficiary, goal, deadline)`, `vault(owner, wait_time)`, the factory's
  `factory_marker(owner, utxo_ref)`.
- **Datum** — state attached to a UTxO. Reach for this when state **evolves between
  transactions**, or when you deliberately want *many* independent instances to
  **share one address**, distinguished only by their datum. Examples: `vesting`
  (many independent schedules at one address), `escrow` (a lifecycle datum),
  `auction`, `decentralized-identity`. The recurring in-code justification: "a single
  script address can host many independent schedules."
- **Redeemer** — the action to take this transaction, plus caller-supplied witnesses
  (a revealed preimage, the claimed winner, a deposit bundle). Almost always an enum
  driving `when redeemer is`. Contracts with no state machine set the redeemer to
  `Data` and ignore it (vesting, htlc's datum, simple-transfer).

Rule of thumb: *fixed for this instance and should change the address* → parameter;
*changes across transactions, or shared address* → datum; *the caller's choice this
transaction* → redeemer, verified independently.

## Authenticate a UTxO before you trust its datum

A datum is just bytes at an address; anyone can create a UTxO at your script address
carrying a *look-alike* datum. Before a validator trusts datum fields, it must prove
the UTxO is a genuine protocol UTxO. Two enforced patterns:

- **Thread / identity NFT** — mint a policy-locked token, then require it present in
  the input before reading the datum; burn it to end the lifecycle. Reach for this
  whenever an impostor UTxO at the same address could spoof state, or when many UTxOs
  share an address. Exemplars: `factory` (`has_nft_strict` + marker continuity),
  `lottery` (`inputs_with_policy`, and `only_minted_token(..., -1)` to close the game),
  `bet` (checks the token's policy equals the owning script:
  `policies(value) |> map(from_script) |> has(own_address)`).
- **Address + signature** — sufficient and cheaper when the datum names a pubkey you
  then require in `extra_signatories`, and there is no value/identity being trusted
  blindly. Exemplars: `escrow`, `vesting`, `decentralized-identity`.

If in doubt, authenticate. The cost of a thread token is small; the cost of trusting
a forged datum is total loss.

## Guaranteeing uniqueness (one-shot)

The universal eUTxO trick: **consume a specific `OutputReference`**. Because a UTxO
is spendable exactly once in the chain's history, any policy or spend gated on that
consumption can fire at most once — the foundation of NFTs, thread tokens, and
singleton state machines. Derive the token's asset name from a **hash of the seed**
(or of caller data) to make names unforgeable and self-describing:
`sha2_256(snapshot_id)` (storage), `sha3_256(tx_id ‖ output_index)` (upgradable-proxy
state token), `blake2b_256(pkh ‖ nonce)` (anonymous-data). See the "Token Minting
Policy" pattern above and `docs/sources/aiken-examples/gift_card/`.

## Locate outputs by criteria, never by index

Universally, real validators find the outputs they care about by **address and/or
value**, then assert **exactly one** — never by trusting a positional index the
caller supplied. Assert exactly-one with `expect [x] = list.filter(...)`,
`expect ([_], [_]) = ...`, or `expect list.length(xs) == 1`. Duplicating a state
cell ("two competing identities sharing the same address") is a real attack; the
exactly-one assertion is what blocks it. Exemplars: `escrow`, `decentralized-identity`,
`auction`. (If you *do* accept an index as a performance hint, you must still verify
the resolved output matches the expected address/value — see the review-contract
checklist and the "singular UTxO indexer" advanced pattern below.)

## Value conservation: `==` vs `≥`

A deliberate choice, made explicit in the templates' own comments:

- **Strict `==`** when the amount is a *provable invariant of the protocol*: bet's
  doubled pot (`lovelace_of(out) == 2 * lovelace_of(in)`), vault and identity value
  conservation, simple-wallet's exact intent payout ("any surplus would be a tip the
  owner didn't authorise"). Use `==` when *any* deviation is an error.
- **Loose `≥` / `value_geq`** when only a *floor* matters and ride-along min-ada or
  padding is harmless: escrow deposits, auction's non-decreasing pot, pricebet
  payouts ("can pile on extra ada… but cannot drain"). Use `≥` when more-than-expected
  is fine but less is theft.

Watch the semantics of your comparison: `assets.match(out, expected, cmp)` applies
`cmp` to **lovelace only** — every other asset must match *exactly*. For a genuine
multi-asset floor use `assets.lovelace_of` / `assets.quantity_of` on the specific
assets, or `assets.contains` on per-policy token maps (see the vuln checklist,
item 9).

## Time handling: mutual exclusion via strict/non-strict bounds

Deadlines are enforced against `tx.validity_range` (values are `Int` POSIX
milliseconds since the Unix epoch — the ledger translates the transaction's slot
bounds before the validator runs; there is no `POSIXTime` type in stdlib v3). The
idiom for making a claim path and a refund path **mutually exclusive at every
point in time** is to pair a non-strict and a strict inequality:
`valid_before(deadline)` for the active phase vs `valid_after(deadline)` for
settlement/refund (htlc, bet, auction, vault, crowdfund). When comparing bounds by
hand, mind strictness: pricebet uses `tx_upper <= deadline` for Join/Win vs
`tx_lower > deadline` for Timeout. Use `interval.is_entirely_after` /
`is_entirely_before` (stdlib) or the cocktail `valid_after` / `valid_before` helpers.

## Representing "not set yet": sentinel vs Option vs lifecycle enum

The templates predominantly use a **flat sentinel** — an empty `""` pubkey/name or a
zero — with an explicit rationale: "keep the datum flat and cheap to compare
on-chain" (auction's `highest_bidder == ""`, bet's `player2 == ""`, lottery's
unrevealed `n1/n2 == ""`). Use a **lifecycle enum** for genuine stages (escrow's
`Initiation | ActiveEscrow`, storage's `SnapshotType`). Use `Option` when you want the
type system to force you to handle the absent case (pricebet's
`player: Option<VerificationKeyHash>`) — cleaner, marginally costlier. There is no
single right answer; match the cost/clarity trade-off to how hot the field is.

## Escape hatches and recovery paths

Treat "what happens to a mis-sent or stranded UTxO" as a first-class design question,
not an afterthought. Common deliberate hatches: `None -> True` so datum-less dust
sent to the script is freely recoverable (crowdfund, token-transfer); an
unconditional owner path (vesting clawback, simple-wallet `Withdraw`). The *inverse*
is also a deliberate design: storage makes its spend `fail @"immutable"` so nothing
can ever be spent — the absence of an exit *is* the feature. Decide which you want on
purpose.

## Multi-validator composition

Anything stateful or composed is usually **several validators**, not one. Bind them
by passing one script's hash as another's **parameter** (factory→product,
simple-wallet's three scripts, proxy→logic). Let one script **observe** another
without consuming it via a **reference input** (pricebet reads an oracle UTxO;
simple-wallet reads the intent; proxy reads its pointer). And delegate hot-swappable
logic via **withdraw-zero**: the stable script requires a withdrawal from a pointed
logic script, whose `withdraw` handler carries the real rules — swap the pointer to
upgrade behind a fixed address (`upgradable-proxy`). See `advanced-patterns.md`.

## Reading the templates critically (what NOT to copy)

Not everything in the corpus is exemplary — a few are stubs or teaching toys. Do not
cite these as finished patterns:

- `constant-product-amm`, `editable-nft` — **README only, no Aiken code**.
- `atomic-transaction` — intentionally toy (`password == "super_secret_password"`,
  `spend = True`); fine as a tx-composition demo only.
- `upgradable-proxy` **logic bodies** (`script_logic_v_1/v_2`) — placeholder rules;
  the *proxy/delegation architecture* is exemplary, the logic is illustrative.
- `bet` — has **no reclaim path** for an un-joined bet (funds can lock); the code
  comment concedes it. A good teaching gap, not a finished contract.
- `auction`'s `WITHDRAW -> fail` is a deliberate dead branch (refunds are inlined
  into `BID`); don't present it as a usable action.
