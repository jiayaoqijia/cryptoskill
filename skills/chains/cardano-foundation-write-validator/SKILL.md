---
name: write-validator
description: >-
  Guide writing a Cardano validator from a specification. Covers datum/redeemer design,
  validator logic, security checks, and test planning. Default language is Aiken.
  Trigger: "write validator", "create contract", "build smart contract", "new validator",
  "implement spending validator", "write minting policy".
allowed-tools: Read Grep Glob
disallowed-tools: WebFetch WebSearch
---

<!-- Documentation lookup path: ${CLAUDE_SKILL_DIR}/../../docs/sources/ -->

# Write Cardano Validator

Guide the development of a Cardano smart contract from specification to implementation, with security built in from the start.

## When to use

- User wants to write a new Cardano validator, minting policy, or staking script
- User has a specification or requirements for on-chain logic
- User asks "how do I build a contract that does X?"
- User wants to implement a specific DeFi pattern (escrow, DEX, lending, etc.)

## When NOT to use

- User wants to review an existing contract (use review-contract)
- User wants to optimize an existing contract (use optimize-validator)
- User wants to build off-chain/transaction building code only
- User wants infrastructure or node setup help

## Key principles

1. **Security first**: Design for security from the start. Every design decision should consider the vulnerability checklist.
2. **Minimal on-chain logic**: Keep validators simple. Complex logic increases attack surface and execution costs. Move complexity off-chain where possible.
3. **Explicit over implicit**: Every validator check should be explicit and readable. Avoid clever tricks that obscure intent.
4. **Test-driven design**: Define expected behavior before writing code. Think about which transactions should succeed and which should fail.
5. **eUTxO-native design**: Design for the eUTxO model, not account-based patterns. Think in terms of UTxOs, datums, and transaction shapes.

## Workflow

### Step 1: Define the datum type

The datum represents the state stored at the script address.

- List every piece of information the validator needs for decisions
- Separate mutable fields (change between transactions) from immutable fields (set once)
- Keep datum small; avoid unbounded collections (vulnerability #3 in checklist)
- Include authentication data: owner key hash, protocol NFT policy ID
- Consider versioning if the protocol may need upgrades

Questions to answer:
- What state needs to persist between transactions?
- Who is authorized to perform each action?
- Are there time-based conditions? Store deadlines in the datum.
- Does the protocol need a state machine? Define the state enum.

See `references/datum-redeemer-design.md` for detailed guidance, and the **eUTxO
Design Decisions** section of `references/aiken-patterns.md` for how to choose between
parameter, datum, and redeemer — the central design axis.

### Step 2: Search Bundled Documentation

Search the bundled documentation for relevant content:
- `${CLAUDE_SKILL_DIR}/../../docs/sources/aiken/` - Aiken language docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/aiken-stdlib/` - Aiken standard library docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/aiken-examples/` - Aiken example projects
- `${CLAUDE_SKILL_DIR}/../../docs/sources/aiken-design-patterns/` - Aiken design patterns
- `${CLAUDE_SKILL_DIR}/../../docs/sources/plinth/` - Plinth (PlutusTx) docs

### Step 3: Define the redeemer type

The redeemer represents the action the user wants to perform.

- Use an enum: `type Redeemer { Action1 | Action2 { field: Type } }`
- Keep redeemer data minimal -- use it as a hint, verify independently
- Common patterns: Create, Update, Delete, Claim, Cancel, Admin

For each redeemer variant, define:
- Who can submit it (signer requirements)
- What time constraints apply
- What value changes are allowed
- What datum transitions are valid
- What outputs must be produced

### Step 4: Write the validator logic

Structure the validator clearly:

```aiken
validator my_validator(params: Params) {
  spend(
    datum: Option<Datum>,
    redeemer: Redeemer,
    own_ref: OutputReference,
    tx: Transaction,
  ) {
    expect Some(datum) = datum
    when redeemer is {
      Action1 -> handle_action1(datum, tx)
      Action2 { field } -> handle_action2(datum, field, tx)
    }
  }
}
```

For each action handler:
1. Check authorization (signer, NFT, etc.)
2. Check time constraints
3. Find and validate outputs (by criteria, never by index)
4. Check value preservation
5. Check datum transitions (immutable fields unchanged, valid state change)
6. Return True only if all checks pass

See `references/aiken-patterns.md` for worked patterns (vesting, marketplace,
multisig, one-shot minting, withdraw-zero, state machine) and
`references/advanced-patterns.md` for when a straightforward validator won't fit
(UTxO indexers, merkelized validators, linked lists).

### Step 5: Security checklist

Before considering the validator complete, verify each item:

- [ ] Double satisfaction: Inputs are uniquely identified (NFT or unique datum field)
- [ ] Datum hijacking: Only authenticated datums are trusted
- [ ] Value preservation: Output values match expected amounts
- [ ] Signer checks: Every restricted action checks `extra_signatories`
- [ ] Staking credentials: Output addresses include correct staking part
- [ ] Output lookup: Outputs found by criteria, not by index
- [ ] Time handling: Validity range bounds checked correctly
- [ ] Datum transitions: Only allowed fields change per action
- [ ] Minting controls: If minting, quantity and conditions are constrained
- [ ] State token: Protocol NFT preserved in exactly one output

### Step 6: Plan off-chain interaction

For each redeemer action, document the transaction shape:

- Required inputs (script inputs, fee inputs, reference inputs)
- Required outputs (script output with datum, change, recipient)
- Required signers
- Validity range constraints
- Minting/burning (if any)
- Metadata (if any)

This becomes the specification for the off-chain transaction building code.

### Step 7: Write test cases

Define tests for each redeemer action:

**Positive tests** (should succeed):
- Normal execution of each action with valid parameters
- Edge cases with minimum/maximum valid values

**Negative tests** (should fail):
- Wrong signer attempts each restricted action
- Wrong time (before/after deadline)
- Insufficient value in output
- Invalid datum transition (wrong fields changed)
- Missing authentication token
- Double satisfaction attempt (two script inputs, one output)

Use Aiken's built-in test framework. Call the validator handler directly with a
constructed transaction (`transaction.placeholder` + record-update overrides), and
use the **boolean-toggle methodology**: one success test with all conditions valid,
then one `test ... fail` per validation condition, each flipping exactly one
condition — so every guard is individually proven to guard. See
`references/testing-validators.md` for the full manual-vs-mocktail guidance, the
mocktail builder API, and the `include: Bool` pass/fail-matrix idiom.
```aiken
fn tx_with(signers, range) -> Transaction {
  Transaction { ..transaction.placeholder, extra_signatories: signers, validity_range: range }
}

test claim_succeeds() {
  vesting.spend(Some(datum), Claim, oref, tx_with([beneficiary], interval.entirely_after(deadline)))
}

test claim_before_deadline_fails() fail {
  vesting.spend(Some(datum), Claim, oref, tx_with([beneficiary], interval.entirely_before(deadline)))
}
```

**Plutus/Haskell notes:**
- New Haskell *off-chain* work uses Aiken on-chain + cardano-ledger
  off-chain (see `build-transaction`). Do not start new validators in
  Plinth unless the team already writes Plinth.
- Existing Plinth code: search `docs/sources/plinth/`. Testing:
  `plutus-simple-model` or `cardano-testnet`.

**OpShin notes:**
- Use Python dataclasses for datum/redeemer types
- Use `build()` function from `opshin.builder` (e.g., `from opshin.builder import build; contract = build("path/to/contract.py")`)
- Use `opshin eval` for local testing

## References

- `references/aiken-patterns.md` -- Validator patterns with code structure, plus eUTxO design decisions
- `references/advanced-patterns.md` -- Advanced/scaling patterns (UTxO indexers, merkelized validators, linked lists)
- `references/datum-redeemer-design.md` -- Designing datums and redeemers
- `references/testing-validators.md` -- How to test validators (manual placeholder vs mocktail)
- Search `${CLAUDE_SKILL_DIR}/../../docs/sources/` for existing protocol specifications and design documents
- Aiken language docs: https://aiken-lang.org
- Plutus docs: https://plutus.cardano.intersectmbo.org
- OpShin docs: https://opshin.dev
