---
name: explain-eutxo
description: >-
  Explain Cardano's extended UTxO model to developers. Trigger phrases:
  "explain datum", "what is a redeemer", "eUTxO vs account model",
  "how do validators work", "what is a script context", "UTxO model",
  "how does Cardano differ from Ethereum".
allowed-tools: Read Grep Glob
disallowed-tools: Bash Edit Write WebFetch WebSearch
---

<!-- Documentation lookup path: ${CLAUDE_SKILL_DIR}/../../docs/sources/ -->

# Explain eUTxO

Help developers understand Cardano's extended UTxO (eUTxO) model, especially those
transitioning from account-based chains like Ethereum or from web2 backgrounds.

## When to use

- A developer asks what datums, redeemers, or script contexts are
- Someone coming from Ethereum or Solidity wants to understand the Cardano model
- A web2 developer is encountering UTxO concepts for the first time
- Questions about how validators differ from smart contracts on other chains
- Conceptual questions about reference inputs, reference scripts, collateral, or minting policies
- The developer is confused about concurrency, state, or how to "store data on-chain"

## When NOT to use

- The developer needs to **write** a validator or build a transaction — use `write-validator` or `build-transaction` instead
- They are asking about a specific CIP standard — use `explain-cip`
- They need to deploy or test a contract — use `setup-devnet` or `build-transaction`
- They need wallet integration — use `connect-wallet`

## Key Principles

### 1. Think in UTxOs, not accounts

There is no global mutable state. The blockchain is a set of unspent transaction outputs
(UTxOs). Each UTxO is an independent, immutable unit containing:
- An address (who can spend it)
- A value (ADA and/or native tokens)
- An optional datum (application data attached to the UTxO)

A transaction **consumes** UTxOs as inputs and **produces** new UTxOs as outputs. State
changes happen by consuming old UTxOs and creating new ones with updated datums.

### 2. Validators verify, they do not compute

Cardano validators are **predicates**: they return true or false. They do not modify state
or call other contracts. A validator receives three arguments and decides whether the
transaction is allowed:
- **Datum** — data sitting on the UTxO being spent (the current state)
- **Redeemer** — data provided by the transaction builder (the action/intent)
- **Script Context** — the full transaction being validated (inputs, outputs, signatories, mint, validity range, etc.)

The off-chain code (transaction builder) does all the computation: selecting UTxOs,
constructing outputs, calculating values. The validator merely checks that the result is
valid.

### 3. The datum/redeemer/script-context triad

Every validator invocation receives exactly these three pieces of data:

| Component | Provided by | Purpose |
|---|---|---|
| **Datum** | Attached to the UTxO at the script address | Represents current state |
| **Redeemer** | Supplied by the transaction spending the UTxO | Represents the action or intent |
| **Script Context** | Constructed by the ledger from the transaction | Full transaction view for validation |

### 4. Deterministic evaluation

Transactions are validated locally before submission. If validation passes locally, it will
pass on-chain (assuming the UTxOs have not been spent by another transaction). This means:
- No failed transactions consuming fees on-chain
- Exact fee calculation before submission
- Predictable execution costs via ExUnits (CPU and memory budgets)

## Ethereum to Cardano Concept Mapping

When a developer comes from Ethereum, use these mappings to bridge understanding:

| Ethereum Concept | Cardano Equivalent | Key Difference |
|---|---|---|
| Smart contract | **Validator** (spending, minting, or withdrawing) | Validators are stateless predicates, not persistent programs |
| Contract storage | **Datum** on UTxOs at the script address | No global storage; state is per-UTxO |
| Function call | **Redeemer** | The redeemer encodes which "action" is being taken |
| `msg.sender` | **`extra_signatories`** in script context | Must explicitly check that a required key signed the tx |
| `msg.value` | **Value in the transaction inputs/outputs** | Explicitly check value flow in the script context |
| ERC-20 token | **Native token** (minting policy) | Tokens are ledger-native, no contract needed to transfer |
| `require()` | **`expect`** / **`fail`** in Aiken | Pattern matching with `expect` is idiomatic |
| Contract-to-contract call | **Multiple validators in one transaction** | No re-entrancy; all validators run independently |
| `block.timestamp` | **Validity range** (`valid_after`, `valid_before`) | Tx specifies a time window; validator checks the range |
| Mapping(address => uint) | **Multiple UTxOs** with datums, or a datum containing a data structure | No native key-value store; design around UTxOs |
| Events / logs | **Datum content** or **transaction metadata** | No native event system; off-chain indexers watch the chain |
| Constructor | **Parameterized validator** | Validators can take compile-time parameters |
| Proxy / upgradeable contract | **Reference scripts (CIP-33)** + governance pattern | Validators are immutable; upgradeability needs explicit design |

## Workflow

### Step 1: Identify the concept and the developer's background

Determine:
- What specific concept are they asking about?
- Are they coming from Ethereum/Solidity, another blockchain, or web2?
- Do they need a high-level overview or a detailed technical explanation?

### Step 2: Search Bundled Documentation

Search the bundled documentation for relevant content:
- `${CLAUDE_SKILL_DIR}/../../docs/sources/plinth/` - Plinth (PlutusTx) docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/aiken/` - Aiken language docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/developer-portal/` - Cardano Developer Portal

### Step 3: Explain using analogies from their background

For Ethereum developers, use the mapping table above. For web2 developers, use analogies:
- **UTxO** = a sealed envelope containing money and a note (datum). To use the money, you
  must open (consume) the envelope, take the contents, and create new envelopes.
- **Validator** = a lock on the envelope. It checks conditions before allowing you to open it.
- **Redeemer** = the key you present to the lock.
- **Script Context** = security camera footage of the entire operation, so the lock can
  verify what you are doing with the contents.

### Step 4: Provide a practical scenario

Show **when** a developer encounters this concept. Examples:
- "You want to lock ADA so only a specific person can claim it" -> spending validator with datum containing the beneficiary's key hash
- "You want to create a token" -> minting policy that validates the conditions under which tokens can be minted/burned
- "You want to read on-chain data without spending it" -> reference inputs (CIP-31)

### Step 5: Show a code example

Provide a minimal Aiken validator plus the off-chain interaction pattern:

```aiken
// A simple vesting validator
validator vesting {
  spend(
    datum: Option<VestingDatum>,
    _redeemer: Data,
    _self: OutputReference,
    tx: Transaction,
  ) {
    expect Some(VestingDatum { beneficiary, deadline }) = datum

    // Check that the beneficiary signed the transaction
    let signed = list.has(tx.extra_signatories, beneficiary)

    // Check that the deadline has passed
    let deadline_passed = when tx.validity_range.lower_bound.bound_type is {
      Finite(lower) -> lower >= deadline
      _ -> False
    }

    signed && deadline_passed
  }
}
```

Off-chain pattern (conceptual):
1. Query UTxOs at the script address
2. Find the UTxO with the matching datum
3. Build a transaction that consumes the UTxO, provides a redeemer, includes the
   beneficiary's signature, and sets `valid_after` past the deadline
4. Sign and submit

### Step 6: Highlight common mistakes

- **Forgetting the datum on outputs:** When sending to a script address, always attach a
  datum. UTxOs without datums at script addresses are unspendable.
- **Not checking all conditions:** Validators must check every invariant. If you check the
  signer but not the value, someone can drain the funds to a different address.
- **Double satisfaction:** When multiple script inputs exist in one transaction, each
  validator only sees that "its" UTxO is being spent. A malicious user can satisfy one
  validator's checks using another validator's UTxO. Always verify outputs specific to your
  script.
- **Ignoring the change output:** The eUTxO model requires explicit handling of change.
  The off-chain code must account for leftover ADA.
- **Using datum as global state:** Datum is per-UTxO. If you need shared state across
  multiple interactions, you need a design pattern (see reference docs).

## Concepts Covered by This Skill

| Concept | Quick Definition |
|---|---|
| **Datum** | Application data attached to a UTxO. Represents the "state" at a script address. |
| **Redeemer** | Data provided by the spender to indicate intent/action. The "key" to unlock. |
| **Script Context** | Full transaction data available to the validator during execution. |
| **Validator** | A predicate script that authorizes spending, minting, or withdrawing. |
| **Reference Input** | A UTxO included in the transaction for reading only (not consumed). CIP-31. |
| **Reference Script** | A script attached to a UTxO that other transactions can reference instead of including. CIP-33. |
| **Collateral** | A pure-ADA UTxO pledged to cover fees if script execution fails during phase-2 validation. |
| **UTxO Selection** | The off-chain process of choosing which UTxOs to use as transaction inputs. |
| **Script Address** | An address derived from a validator hash. UTxOs here are governed by the validator. |
| **Stake Credential** | A credential for staking/delegation, which can also be a script (enabling withdraw-zero). |
| **Withdraw-Zero Pattern** | A technique using a staking validator with a zero-ADA withdrawal to run validation logic once per transaction instead of once per input. Useful for batching. |
| **Minting Policy** | A validator that controls creation and destruction of native tokens. |

## References

- `references/eutxo-vs-account.md` — detailed comparison of eUTxO and account models
- Shared principles: `../shared/PRINCIPLES.md`
