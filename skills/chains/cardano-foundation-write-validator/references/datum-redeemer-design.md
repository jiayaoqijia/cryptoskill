# Datum and Redeemer Design Guide

How to design datums and redeemers for Cardano smart contracts. Good type design is the foundation of a secure and efficient validator.

## What Goes in the Datum vs the Redeemer

**Datum** -- state that persists between transactions:
- Owner/beneficiary key hashes
- Deadlines and time constraints
- Protocol parameters (prices, thresholds)
- Current state (for state machines)
- Authentication token identifiers

**Redeemer** -- the action to perform in this transaction:
- Which operation to execute (enum variant)
- Performance hints (output index, optional -- must be verified)
- Minimal action-specific data

**Neither** (compute from transaction context):
- Current time (use `tx.validity_range`)
- Signer identity (use `tx.extra_signatories`)
- Input/output values (read from `tx.inputs` / `tx.outputs`)
- Minted tokens (use `tx.mint`)

Rule of thumb: if the data changes per transaction, it is probably a redeemer or transaction context. If it persists across transactions, it belongs in the datum.

## Datum Design Principles

### Keep datums small

Every byte of datum increases:
- Deserialization cost (CPU + memory)
- Transaction size (affects fees)
- Min-UTxO requirement (more ADA locked)

```aiken
// BAD: Large datum with redundant data
type BadDatum {
  owner: VerificationKeyHash,
  owner_address: Address,         // Redundant -- derive from owner
  creation_time: Int,             // Only needed once, not for validation
  history: List<Transaction>,     // Unbounded, will grow forever
}

// GOOD: Minimal datum
type GoodDatum {
  owner: VerificationKeyHash,
  deadline: Int,
  state: State,
}
```

### Avoid unbounded collections

Lists and maps in datums can grow until the UTxO becomes unspendable.

```aiken
// BAD: Unbounded list
type PoolDatum {
  participants: List<VerificationKeyHash>,  // Grows with each deposit
}

// GOOD: Fixed size, overflow handled off-chain
type PoolDatum {
  participant_count: Int,
  merkle_root: ByteArray,  // Verify membership with proof in redeemer
}
```

### Use integers for enums

Integers are cheaper to serialize and compare than bytestrings.

```aiken
// GOOD: Enum type compiles to integer constructors
type State {
  Pending     // Constructor index 0
  Active      // Constructor index 1
  Completed   // Constructor index 2
}
```

Aiken enum constructors are already encoded as integers in UPLC, so this is handled automatically.

### Separate mutable from immutable fields

Document which fields change and when. This makes validation logic clearer and helps prevent unvalidated datum transitions.

```aiken
type EscrowDatum {
  // Immutable (set at creation, never changes)
  seller: VerificationKeyHash,
  buyer: VerificationKeyHash,
  price: Int,
  deadline: Int,
  // Mutable (changes with state transitions)
  state: EscrowState,
  deposited: Int,
}
```

### Versioning

If the protocol may upgrade, include a version field or use a versioned type wrapper.

```aiken
// Option A: Version field
type Datum {
  version: Int,
  owner: VerificationKeyHash,
  // ... fields
}

// Option B: Versioned wrapper (migration-friendly)
type Datum {
  V1 { owner: VerificationKeyHash, deadline: Int }
  V2 { owner: VerificationKeyHash, deadline: Int, min_amount: Int }
}
```

Version fields add overhead but make migration possible. Use when the protocol is expected to evolve.

## Redeemer Design Principles

### Use enum style

Each action is a separate constructor. This enables exhaustive pattern matching and clear validator structure.

```aiken
// GOOD: Clear action enum
type Redeemer {
  Claim
  Cancel
  Update { new_price: Int }
  AdminWithdraw { amount: Int }
}
```

### Keep redeemer data minimal

Redeemers are attacker-controlled. Any data in the redeemer must be verified independently.

```aiken
// BAD: Trusting redeemer data
type Redeemer {
  Withdraw { amount: Int, recipient: Address }
  // Attacker sets amount and recipient to anything
}

// GOOD: Derive from datum and transaction context
type Redeemer {
  Withdraw  // Amount comes from datum, recipient from datum.owner
}
```

### Use indices as hints only

If the redeemer provides an output index for performance, always verify the output matches expected criteria.

```aiken
type Redeemer {
  Swap { output_index: Int }  // Hint for which output to check
}

// In the validator:
when redeemer is {
  Swap { output_index } -> {
    // Use index as hint, but VERIFY the result
    expect Some(output) = list.at(tx.outputs, output_index)
    // Must still check: correct address, correct value, correct datum
    output.address == expected_address &&
    assets.lovelace_of(output.value) >= expected_amount
  }
}
```

### Avoid large redeemer structures

Large redeemers increase transaction size and fees. Move large data elsewhere.

```aiken
// BAD: Large proof data in redeemer
type Redeemer {
  ClaimWithProof { proof: List<ByteArray>, leaf: ByteArray }
  // Could be hundreds of bytes
}

// BETTER: Use reference inputs for proof data
type Redeemer {
  Claim  // Proof data in a reference input datum
}
```

## Nested vs Flat Datums

### Flat datum (simple protocols)

All fields at the top level. Simple to access, easy to validate.

```aiken
type FlatDatum {
  owner: VerificationKeyHash,
  beneficiary: VerificationKeyHash,
  deadline: Int,
  amount: Int,
  state: State,
}
```

Best for: simple contracts with fewer than 8 fields.

### Nested datum (complex protocols)

Group related fields into sub-types. Enables partial deserialization and logical grouping.

```aiken
type Config {
  min_amount: Int,
  fee_percent: Int,
  oracle_nft: PolicyId,
}

type Parties {
  owner: VerificationKeyHash,
  beneficiary: VerificationKeyHash,
  admin: VerificationKeyHash,
}

type NestedDatum {
  config: Config,
  parties: Parties,
  state: State,
  deadline: Int,
}
```

Best for: complex protocols with many fields, especially when different actions use different field groups.

Trade-off: nested datums require more deserialization steps but provide better code organization. For performance-critical validators, flat datums are slightly cheaper.

## Common Mistakes

1. **Storing computed values**: Do not store values that can be derived from other datum fields or transaction context.

2. **Unbounded growth**: Lists that grow with protocol usage will eventually lock the UTxO. Always set and enforce maximum sizes.

3. **Missing authentication**: Datums without an associated NFT can be spoofed via datum hijacking. Always pair protocol datums with an authentication token.

4. **Trusting redeemer data**: Never use redeemer values for authorization or amount calculations. Redeemers are fully attacker-controlled.

5. **Forgetting staking credentials in addresses**: When storing addresses in datums, store the complete address (payment + staking) to prevent staking credential theft.

6. **Over-engineering versioning**: Only add versioning if there is a concrete upgrade path. Unnecessary versioning adds complexity and cost.
