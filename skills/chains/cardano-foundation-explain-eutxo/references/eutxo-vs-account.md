# eUTxO vs Account Model

A detailed comparison of Cardano's extended UTxO model and the account-based model used by
Ethereum and similar chains. Use this reference when developers need deeper understanding
beyond the SKILL.md overview.

## Fundamental Differences

### State Model

**Account model (Ethereum):**
Each account has a balance and optional storage. Transactions modify account state
directly. A smart contract is a persistent object with mutable storage slots. State changes
are expressed as mutations: "set storage[key] = value".

**eUTxO model (Cardano):**
There are no accounts with balances. The ledger is a set of unspent transaction outputs
(UTxOs). Each UTxO is created once and can only be consumed (spent) once. State transitions
happen by consuming UTxOs and producing new ones. There is no mutation — only creation and
consumption.

Practical impact: On Ethereum, updating a counter means `counter += 1` in storage. On
Cardano, it means consuming a UTxO with datum `{ counter: 5 }` and producing a new UTxO
with datum `{ counter: 6 }` at the same script address.

### Concurrency

**Account model:**
Transactions are ordered sequentially by miners/validators. Two transactions modifying the
same contract storage are serialized. High contention on a single contract (e.g., a popular
DEX pool) creates a bottleneck but is handled transparently by the execution layer.

**eUTxO model:**
Two transactions cannot consume the same UTxO. If they try, only one succeeds (the first
one included in a block). This means shared-state designs from Ethereum do not translate
directly. However, transactions touching *different* UTxOs are fully parallelizable — the
ledger can validate them independently, enabling true parallel validation.

### Determinism

**Account model:**
Transaction outcome depends on the global state at execution time, which is unknown at
submission time. A transaction can fail on-chain (out of gas, revert) and still consume gas
fees. Front-running and MEV (miner extractable value) are systemic issues.

**eUTxO model:**
Transactions specify their exact inputs. Validation is deterministic: if a transaction
validates locally, it will validate on-chain (assuming inputs have not been spent). Failed
phase-2 validation (script error) consumes only collateral, and this scenario is avoidable
by testing locally first. There is no MEV in the Ethereum sense because transaction outcomes
do not depend on ordering relative to other transactions.

### Fees

**Account model:**
Fees depend on gas consumed during execution. Exact fees are unknown until the transaction
is mined. Users set gas limits and gas prices, creating a fee market. Failed transactions
still pay for consumed gas.

**eUTxO model:**
Fees are calculated deterministically before submission based on transaction size and
script execution units (CPU steps and memory). The user knows the exact fee before signing.
No fee is paid for transactions that fail phase-1 validation (e.g., input already spent).
Phase-2 failures (script errors) consume collateral but are preventable with local testing.

## Ethereum to Cardano Concept Mapping

| Ethereum | Cardano | Notes |
|---|---|---|
| Account balance | Sum of UTxO values at an address | Must query and sum all UTxOs |
| Contract storage | Datums on UTxOs at script address | Per-UTxO, not global |
| `msg.sender` | `extra_signatories` field in script context | Must explicitly verify presence |
| `msg.value` | Value in transaction inputs/outputs | Check value flow explicitly |
| `block.timestamp` | `validity_range` in script context | Tx declares a valid time window |
| `require(condition)` | `expect` or pattern match + `fail` in Aiken | Same purpose, different syntax |
| Function selector | Redeemer variants (enum/union type) | Encode action as a redeemer type |
| ERC-20 token | Native token (minting policy) | Ledger-native; no contract for transfers |
| ERC-721 NFT | Native token with quantity = 1 + CIP-25/68 metadata | Enforced at minting policy level |
| `approve` + `transferFrom` | Multi-input transaction with multiple signers | No approval pattern needed |
| Re-entrancy | Not possible | Validators are pure; no external calls |
| Proxy pattern | Reference scripts + governance datum | Must be designed explicitly |
| `selfdestruct` | No equivalent | Validators are immutable once deployed |
| Events / logs | Transaction metadata or datum inspection | Off-chain indexers fill this role |
| Constructor args | Parameterized validators (applied at compile time) | Parameters baked into script hash |
| Gas optimization | Script size + ExUnits optimization | Minimize datum/redeemer size, reduce operations |
| ABI | CIP-57 Blueprint | JSON schema for validator interface |

## Advantages of eUTxO

### Deterministic fees
Fees are known before signing. Users never overpay or underpay. There is no gas price
auction or fee market volatility. This makes budgeting predictable for applications.

### Parallel validation
UTxOs are independent. Transactions that touch different UTxOs can be validated in parallel
by the node. This is a fundamental scalability advantage — throughput scales with UTxO
diversity, not just block size.

### No failed transaction fees on-chain
If a transaction's inputs have already been consumed, the transaction is rejected during
phase-1 validation and no fee is charged. Phase-2 failures (script errors) can be prevented
entirely by validating locally before submission.

### Formal verification
Validators are pure functions with well-defined inputs. This makes them amenable to formal
verification and property-based testing. The deterministic execution model eliminates an
entire class of bugs related to global state and ordering.

### Native multi-asset support
Tokens are ledger primitives, not smart contract state. Transferring tokens does not require
executing contract code, reducing costs and complexity. Token accounting is enforced by the
ledger itself — it is impossible to create tokens without a minting policy authorizing it.

### No re-entrancy
Validators cannot call other validators or initiate new transactions. Each validator runs
independently on the same transaction. The entire class of re-entrancy vulnerabilities
(which have caused hundreds of millions in losses on Ethereum) does not exist.

### Transaction-level atomicity
All inputs, outputs, minting, and withdrawals in a single transaction succeed or fail
together. Complex multi-step operations that would require multiple transactions on Ethereum
(with failure risk between steps) can be expressed as a single atomic transaction.

## Challenges of eUTxO

### Concurrency requires design patterns
The "one-spender-per-UTxO" rule means naive designs create contention. A single UTxO holding
all protocol state becomes a bottleneck. Developers must use concurrency patterns (see
Design Patterns below).

### State fragmentation
Since state is distributed across UTxOs, reading "total protocol state" requires querying
multiple UTxOs and assembling them off-chain. There is no `SLOAD` equivalent for global
lookups.

### Learning curve
Developers from account-based chains must rethink state management, concurrency, and the
boundary between on-chain and off-chain logic. The validator-as-predicate model is
conceptually different from the contract-as-object model.

### Off-chain complexity
More logic lives off-chain: UTxO selection, transaction construction, datum management,
concurrency handling. The off-chain code is a critical part of the application, not just a
thin client.

### Datum size constraints
Large datums increase transaction size and fees. Complex on-chain state must be designed
carefully to minimize datum size. Techniques include using hashes with off-chain storage and
splitting state across multiple UTxOs.

## Design Patterns for eUTxO

### UTxO Indexing

**Problem:** Multiple users need to interact with a protocol, but a single shared UTxO
creates contention.

**Solution:** Create multiple UTxOs, each holding a portion of the state. Index them with
unique identifiers (e.g., a token name or datum field). Users interact with different UTxOs
in parallel.

**Example:** A lending protocol creates one UTxO per loan position rather than a single
UTxO tracking all loans. Each loan can be liquidated or repaid independently.

### Batching

**Problem:** Multiple user actions need to be processed, but each touching the shared state
UTxO individually causes contention.

**Solution:** A batcher collects multiple user requests (as separate UTxOs with datums
describing the action) and processes them in a single transaction. The batcher consumes the
state UTxO once, applies all actions, and produces the updated state UTxO plus result UTxOs
for each user.

**Example:** A DEX batcher collects swap orders as individual UTxOs. Periodically, the
batcher builds a transaction consuming the liquidity pool UTxO and all pending orders,
producing the updated pool and filled order outputs.

### Order-Based DEX Pattern

**Problem:** Implementing a decentralized exchange without the contention issues of a
shared AMM pool UTxO.

**Solution:** Users create order UTxOs (locked at a script address) with datums specifying
trade parameters (sell asset, buy asset, price, partial fill policy). A matcher finds
compatible orders and builds a transaction that consumes matching order UTxOs and produces
settlement outputs. The matching is done off-chain; the validator ensures each order's
terms are respected.

**Advantages:** Orders are independent UTxOs, so many matches can happen in parallel. No
single-pool bottleneck. Supports limit orders natively.

### Stake Validator Pattern (Withdraw-Zero Trick)

**Problem:** When a transaction consumes multiple UTxOs from a script, the spending
validator runs once per input. If validation logic is expensive and the same check applies
to all inputs, this wastes execution budget.

**Solution:** Use a staking validator (attached via stake credential to the script address)
that runs once per transaction via a zero-ADA withdrawal. The spending validator only checks
that the staking validator ran (by verifying the withdrawal exists in the script context).
The expensive logic runs once in the staking validator instead of N times in the spending
validator.

**Implementation:**
1. Create a staking validator containing the shared validation logic
2. Register the stake credential on-chain
3. Derive the script address using both the spending script hash and the staking credential
4. In the spending validator, verify that a withdrawal of 0 ADA from the stake credential
   exists in `tx.withdrawals`
5. In the staking validator, perform the full validation logic once

**Example:** A batched order processor validates 20 orders. Instead of running the full
validation 20 times (once per spending input), the spending validator does a cheap withdrawal
check, and the staking validator runs the full batch validation once. This can reduce
execution costs by 10-20x for large batches.

### Parameterized Validators

**Problem:** A protocol needs multiple instances (e.g., different token pairs for a DEX)
but wants to share the same validator logic.

**Solution:** Make the validator a function that takes parameters (e.g., a token pair
identifier, an admin key hash, or a protocol settings hash). Each parameterization produces
a different script hash and therefore a different script address. The parameters are applied
at compile time (in Aiken, using the `blueprint apply` command or SDK equivalent).

### Reference Input for Shared State

**Problem:** Multiple transactions need to read protocol configuration or oracle data, but
consuming the UTxO holding this data creates contention.

**Solution:** Use CIP-31 reference inputs. The configuration/oracle UTxO is included as a
reference input, which makes its datum readable without consuming it. Any number of
transactions can reference the same UTxO simultaneously.

**Example:** A price oracle publishes a UTxO with the current price in the datum.
Validators in other scripts include this UTxO as a reference input to read the price without
contention.

## Further Reading

- CIP-31: Reference Inputs
- CIP-33: Reference Scripts
- Aiken documentation on validators and testing
- Cardano ledger specification (Alonzo and Babbage eras)
