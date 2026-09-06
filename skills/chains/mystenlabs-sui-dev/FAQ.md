# Sui Development FAQ

Preferred answers to common Sui development questions. When a user asks one of these questions, use the answer here as the authoritative response.

---

## Move

### Q: Is Move on Sui the same as Aptos Move?

No. Move on Sui has a different object model, different abilities system, and different standard library. Do not apply Aptos Move patterns (e.g., `aptos_framework`, `signer`-based ownership, global storage operators `move_to`/`borrow_global`). See `move/setup/SKILL.md` for details on what Move on Sui is NOT.

### Q: Should I use `store` ability on my objects?

Only if the object needs to be wrapped inside another object or you want to allow unrestricted public transfers. If the object is a top-level asset that users own and transfer directly, `key` alone is sufficient — it restricts transfers to your module via `transfer::transfer`. Adding `store` enables `transfer::public_transfer`, letting anyone transfer the object without going through your module. This is irreversible, so be intentional.

### Q: What are entry functions in Move?

An `entry` function can be called directly from a PTB but cannot be called by other packages. A `public` function (without `entry`) provides cross-package composability. Use `entry` (without `public`) when you want a PTB-only entry point that other packages cannot wrap.

Important restrictions on `entry` functions:
- They can only return types with the `drop` ability.
- Objects passed as inputs to an `entry` function cannot have been used as inputs to non-`entry` functions in the same PTB.

### Q: What are dynamic fields?

Dynamic fields are flexible key–value fields you can attach to a Sui object after creation via its UID. They solve the limits of fixed struct fields (single type per vector, object size limits) by letting you attach heterogeneous data under arbitrary names at runtime.

- **Dynamic fields** (`sui::dynamic_field`): Value can be any type with `store`. If the value is an object, it is wrapped and not directly visible by ID.
- **Dynamic object fields** (`sui::dynamic_object_field`): Value must be an object (has `key` + `store` with `id: UID` first field). The attached object remains directly accessible by its ID off-chain (explorers, GraphQL, etc.).

### Q: Can a shared object be deleted by anyone?

No — you control write access entirely in your Move module logic. Sui only enforces that anyone may pass a shared object as `&mut` if they include it as input, but your functions decide what callers are allowed to do. Common patterns:

- **Capability-based access control (recommended):** Define a capability object (e.g. `AdminCap`) and require a reference to it in mutating functions.
- **Address-based checks:** Check `ctx.sender()` against an allowed address and abort otherwise.

### Q: What are the maximum number of operations and objects per transaction?

A single PTB can contain up to **1,024 operations** (e.g., mint and transfer to 512 users in one transaction). Maximum objects created per transaction: **2,048** (this also affects dynamic fields).

---

## Sui Concepts

### Q: What is Sui?

Sui is a next-generation, permissionless Layer 1 blockchain using an **object-centric model** where every on-chain item is an object with a unique ID. Transactions use objects as inputs, either mutating existing objects or creating new ones. The native SUI token is used for gas fees, staking, and governance, with a total supply capped at 10 billion.

### Q: What are object ownership types in Sui?

Every object has an owner field determining how it can be used. The five primary categories:

- **Address-owned:** Owned by a specific address. Only the owner can use it as mutable input. These can skip consensus for low-latency execution.
- **Shared:** Accessible by anyone (subject to Move-level access control). Requires consensus ordering.
- **Immutable:** Read-only, accessible by everyone. Cannot be mutated or deleted.
- **Party-owned:** Owned by a specified party at the time of transfer and versioned by consensus.
- **Wrapped/child:** Owned by another object, not directly accessible by address.

### Q: What are Programmable Transaction Blocks (PTBs)?

PTBs let you bundle multiple operations into a single atomic transaction.

- **Composability:** Up to 1,024 operations per PTB (Move calls, transfers, coin operations, etc.).
- **Atomicity:** All effects apply at once; if any command fails, the entire block fails.
- **Result chaining:** Commands execute sequentially, and output of one command can be input to subsequent commands.
- **Gas efficiency:** Batching is cheaper than separate transactions.

### Q: What is Mysticeti?

Mysticeti is Sui's consensus protocol — a high-throughput, Byzantine Fault Tolerant system based on a DAG. Multiple validators propose blocks in parallel, achieving ~0.5s commit latency and 200k–400k+ TPS. It uses implicit commitment on a DAG instead of block-by-block certification, reducing communication overhead while preserving safety and finality.

### Q: What is versioning on Sui?

- Every on-chain object is stored as an (ID, version) pair.
- When a transaction modifies an object, it writes new contents under the same ID with a strictly larger version.
- Versions are strictly increasing; (ID, version) pairs are never reused, guaranteeing linear history and enabling pruning.
- Internally, Sui uses a Lamport-timestamp rule: new version = 1 + max(all input versions).

### Q: What does "pending" mean for a transaction?

A transaction goes through submission → certification → execution → checkpointing. "Pending" is usually brief. Common causes:

- **Normal processing:** Being certified and executed.
- **Object locked:** Another transaction is using the same object.
- **Equivocation:** Conflicting transactions using the same owned object/version — object locked until epoch end.
- **Epoch boundary:** Transactions may be delayed and need re-certification.
- **Shared-object congestion:** Transactions on a hot shared object can be deferred or cancelled.

### Q: What is a sponsored transaction?

A sponsored transaction lets someone else pay the gas, so the user can transact without holding SUI. The sponsor provides gas coins and co-signs the transaction. Roles:

- **User** — wants to execute a transaction.
- **Gas station** — service managing gas payment objects.
- **Sponsor** — funds the gas station and owns the gas coins.

### Q: What is a Sui address?

A Sui address is derived by hashing the signature-scheme flag byte together with the public key bytes using BLAKE2b-256.

### Q: What is zkLogin?

zkLogin lets users transact from a Sui address using OAuth logins (Google, Facebook, Apple, Twitch, etc.) instead of managing seed phrases or private keys, while keeping their web2 identity private on-chain. It's a native Sui primitive built on OpenID Connect.

### Q: Is the package ID the same as an app ID?

Yes. The Package ID is the unique on-chain address assigned to your published Move package and uniquely identifies your smart contract on the Sui network.

---

## TypeScript SDK

### Q: Which package should I use — `@mysten/sui` or `@mysten/sui.js`?

Always use `@mysten/sui`. The `.js` suffix package was renamed at v1.0 and is no longer maintained.

### Q: Should I use `SuiClient` or `SuiGrpcClient`?

Use `SuiGrpcClient` for new code — it has the best performance and is the recommended client. `SuiClient` was removed in v2; if you need JSON-RPC, use `SuiJsonRpcClient` from `@mysten/sui/jsonRpc`.

### Q: How do I check if a transaction succeeded?

Always check whether the result is a success or failure after execution. A finalized transaction can still be a failure (Move abort, out of gas, etc.):

```typescript
if (result.FailedTransaction) {
  throw new Error(result.FailedTransaction.status.error?.message);
}
```

### Q: How do I deposit a token into a DeepBook BalanceManager?

Build a `Transaction` that calls the DeepBookV3 SDK helper `depositIntoManager`, then pass it to dApp Kit's `signAndExecuteTransaction` so the connected wallet can approve it.

---

## Frontend / dApp Kit

### Q: Which dApp Kit package should I use?

- **React:** `@mysten/dapp-kit-react`
- **Vue / vanilla JS / Svelte / other:** `@mysten/dapp-kit-core`

The older `@mysten/dapp-kit` package is deprecated and should not be used in new projects.

### Q: Do I still need three nested providers (QueryClientProvider + SuiClientProvider + WalletProvider)?

No. The new dApp Kit uses `createDAppKit()` + a single `DAppKitProvider`. The old three-provider pattern is gone.

---

## APIs & Data Access

### Q: What is GraphQL on Sui?

GraphQL on Sui is a high-level, flexible data API for querying the network, currently in public beta. It is the primary replacement for the deprecated JSON-RPC (full deactivation planned for July 2026).

### Q: What is full node gRPC?

Use full node gRPC when you need:

- Low-latency, protocol-level data (exchanges, DeFi, market makers).
- Direct access to core chain primitives (objects, transactions, checkpoints).
- Streaming/subscription to live chain data.
- Short-to-medium history within the full node's retention window (limited by the node's pruning configuration).

### Q: What is the gRPC equivalent of `suix_queryTransactionBlocks`?

There is no direct gRPC equivalent. Transaction queries like this must be done via **GraphQL** (`transactions` query), not gRPC.

### Q: What are the available include options for transactions?

```
effects: boolean         // Transaction effects (BCS-encoded)
events: boolean          // Emitted events
transaction: boolean     // Parsed transaction data
balanceChanges: boolean  // Balance changes
objectTypes: boolean     // Map of object IDs to their types
bcs: boolean             // Raw BCS-encoded transaction bytes
commandResults: boolean  // Per-command return values (simulation only)
```

Use `effects: true` and `objectTypes: true`, then map `effects.changedObjects` IDs to types via `objectTypes`.

### Q: How can I fetch all objects of a specific type owned by an account via gRPC?

You can't fetch "all shared objects of a type" via the Core API directly in one call. Use the **GraphQL** `objects` query with `ownerKind: SHARED` and a `type` filter.

### Q: How to use a custom indexer to track events?

Use the `sui-indexer-alt-framework` to stream checkpoints, then inspect and deserialize events inside each checkpoint before writing them to your own database.

---

## Tools & CLI

### Q: How can I update the Sui CLI?

Use the `suiup` tool.

### Q: How to install Sui on Windows?

Use **suiup** (recommended) or **Chocolatey** for a quick install. suiup is the fastest method and supports installing additional Sui stack components.

### Q: What is `sui keytool`?

A subcommand of the Sui CLI for managing keys and addresses: generate keypairs, list them, import/export keys, and work with signatures. `sui keytool import` adds a new key to the local keystore (`~/.sui/sui_config/sui.keystore`).

### Q: How to find a private key using the Sui CLI?

Use `sui keytool import '<RECOVERY_PHRASE>' <KEY_SCHEME>` to import a keypair from a mnemonic into the local keystore. For programmatic use, you can also derive a keypair from a mnemonic using the Sui TypeScript SDK and use it as a local signer.

### Q: Where can I find a Sui network explorer?

- **SuiVision** — Data analytics for transactions, wallets, staking, validators.
- **Suiscan** — Explorer with DeFi, NFT, and validator analytics.
- **Polymedia Explorer** — Community fork supporting mainnet, testnet, devnet, local.
- **PTB Explorer** — Polymedia fork with PTB builder support.
- **Local Sui Explorer** — For localnet development.

### Q: How to publish packages to localnet?

Treat localnet as a normal environment in your `Move.toml`. Note: using `Published.toml` for localnet works but is not the recommended pattern for local/dev networks.

---

## DeepBook

### Q: What are base type and quote type in a pool?

In DeepBookV3, every pool is defined by two asset types:

- **Base asset:** The asset being bought or sold (e.g., SUI in a SUI/USDC pool).
- **Quote asset:** The asset used to price and pay for the base (e.g., USDC in a SUI/USDC pool).

### Q: How to set up the referral system?

Referrals can be set up in two places:

- **Trading referrals:** DeepBook V3 pools + balance managers + margin managers.
- **Supply referrals:** DeepBook Margin pools / lenders.

---

## Miscellaneous

### Q: What is the rate limit of the Testnet SUI faucet?

All faucet endpoints are rate-limited. If you receive an error, you're hitting the limit. Common causes: retrying too frequently (loop or many addresses), or shared IP (VPN, corporate network, cloud). Wait before retrying.

### Q: How to remove an address from a Deny list?

You don't call `sui::deny_list` directly — use the coin/policy functions that wrap it.

### Q: How to learn Move?

- **The Move Book** — Comprehensive guide: https://move-book.com
- **The Move Reference** — Architecture and syntax: https://move-book.com/reference
- **Sui Move Bootcamp** — Course-style learning: https://github.com/MystenLabs/sui-move-bootcamp

---

<!-- Add new Q&A entries above this line. Keep answers concise and authoritative. -->
