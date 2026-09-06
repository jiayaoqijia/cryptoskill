# Sui Rust SDK

Source: https://github.com/MystenLabs/sui-rust-sdk · https://docs.rs/sui-transaction-builder · https://mystenlabs.github.io/sui-rust-sdk/sui_transaction_builder/

## Which Rust SDK

There are two. They serve different projects:

- **Recommended: `sui-rust-sdk` family of crates** (this page). Modular, published on `crates.io` as independent crates. Pay only for what you use, wasm-compatible where possible.
- **Legacy: the `sui-sdk` crate in the `MystenLabs/sui` monorepo.** Monolithic, JSON-RPC-based (deprecated). Still used by some existing projects but not the recommended target for new code. Docs: https://docs.sui.io/references/rust-sdk.

New code → use the modular crates. Existing code on the legacy `sui-sdk` crate → can stay there for now; migrate if you need gRPC or want to move off JSON-RPC before the mainnet shutdown (week of July 27, 2026).

## Crates

From https://github.com/MystenLabs/sui-rust-sdk:

| Crate | Purpose |
|---|---|
| `sui-sdk-types` | Core types: `Address`, `Transaction`, `ObjectId`, `Digest`, `Identifier`, etc. Required by all other crates. |
| `sui-crypto` | Keypair types, signing, signature verification. Ed25519, Secp256k1, Secp256r1. |
| `sui-transaction-builder` | `TransactionBuilder` — the PTB builder. Mirrors the TS SDK's `Transaction` class. |
| `sui-rpc` | gRPC client for interacting with a fullnode. |
| `sui-graphql` | GraphQL client. |
| `sui-graphql-macros` | Macros supporting `sui-graphql`. |
| `proto-build` | Internal build helpers for protobuf compilation. |

Design goals (from the repo README):
- **Modular** — only pay for what you use.
- **Light** — minimal dependency footprint.
- **wasm-friendly** where possible.

## Minimum viable `Cargo.toml`

For a CLI that builds, signs, and submits a PTB via gRPC:

```toml
[dependencies]
sui-sdk-types = "..."
sui-transaction-builder = "..."
sui-crypto = "..."
sui-rpc = "..."
```

Pin versions from `crates.io` — the crates version independently. Check [docs.rs](https://docs.rs/sui-transaction-builder) for the latest.

## `TransactionBuilder` — core PTB API

The canonical minimal example, from the `sui-transaction-builder` crate docs:

```rust
use sui_sdk_types::Address;
use sui_sdk_types::Digest;
use sui_transaction_builder::ObjectInput;
use sui_transaction_builder::TransactionBuilder;

let mut tx = TransactionBuilder::new();

// Split 1 SUI from the gas coin
let amount = tx.pure(&1_000_000_000u64);
let gas = tx.gas();
let coins = tx.split_coins(gas, vec![amount]);

// Transfer to recipient
let recipient = tx.pure(&Address::ZERO);
tx.transfer_objects(coins, recipient);

// Metadata
tx.set_sender(Address::ZERO);
tx.set_gas_budget(500_000_000);
tx.set_gas_price(1000);
tx.add_gas_objects([ObjectInput::owned(Address::ZERO, 1, Digest::ZERO)]);

let transaction = tx.try_build().expect("build should succeed");
```

### Method mapping (TypeScript ↔ Rust)

| TypeScript | Rust |
|---|---|
| `new Transaction()` | `TransactionBuilder::new()` |
| `tx.pure.u64(n)` / `tx.pure('u64', n)` | `tx.pure(&n)` (generic over `BCS`-serializable) |
| `tx.object('0x...')` | `tx.input(ObjectInput::owned(...))` / `ObjectInput::shared(...)` / `ObjectInput::receiving(...)` |
| `tx.gas` | `tx.gas()` |
| `tx.splitCoins(coin, amounts)` | `tx.split_coins(coin, vec![amounts])` |
| `tx.mergeCoins(dest, srcs)` | `tx.merge_coins(dest, srcs)` |
| `tx.transferObjects(objs, addr)` | `tx.transfer_objects(objs, addr)` |
| `tx.moveCall({ target, arguments, typeArguments })` | `tx.move_call(Function::new(pkg, module, name, type_args), args)` |
| `tx.makeMoveVec({ type, elements })` | `tx.make_move_vec(Some(type), elements)` |
| `tx.publish({ modules, dependencies })` | `tx.publish(modules, dependencies)` |
| `tx.upgrade({ modules, dependencies, packageId, ticket })` | `tx.upgrade(modules, deps, pkg_id, ticket)` |
| `tx.setSender(addr)` | `tx.set_sender(addr)` |
| `tx.setGasBudget(n)` | `tx.set_gas_budget(n)` |
| `tx.setGasPrice(n)` | `tx.set_gas_price(n)` |
| `tx.setGasPayment([refs])` | `tx.add_gas_objects(refs)` |

### Build methods

- `tx.try_build()` — offline build; fails if intents or missing metadata remain.
- `tx.build(client).await` — async build that resolves intents and auto-fills gas via an RPC client. Requires the `intents` feature flag (**enabled by default**).

## Intents (`intents` feature)

Analogous to the TS SDK's `coinWithBalance`:

```rust
use sui_transaction_builder::intent::{Coin, Balance};
```

Two high-level intents:
- `Coin` — produces a coin with a specified balance, handling selection/merge/split automatically.
- `Balance` — abstract balance manipulation.

Resolved by `tx.build(client).await`.

Disable via `default-features = false` if you don't want the runtime / client dependency:

```toml
sui-transaction-builder = { version = "...", default-features = false }
```

## Signing (`sui-crypto`)

```rust
use sui_crypto::ed25519::Ed25519PrivateKey;
use sui_crypto::SuiKeyPair;

let kp = SuiKeyPair::Ed25519(Ed25519PrivateKey::generate(&mut rng));
let address = kp.public().derive_address();
let signature = kp.sign_transaction(&transaction)?;
```

(Exact API evolves — consult `docs.rs/sui-crypto` for the current surface.)

## Execution (`sui-rpc`)

The `sui-rpc` crate is the gRPC client. Pattern:

```rust
use sui_rpc::client::Client;

let client = Client::new("https://fullnode.mainnet.sui.io:443")?;
let response = client
    .transaction_execution_service()
    .execute_transaction(transaction, vec![signature])
    .await?;
```

Services mirror the TS SDK's service clients:
- `transaction_execution_service`
- `ledger_service` — object reads, transaction reads
- `move_package_service` — package / function introspection
- `name_service` — SuiNS

## Querying with GraphQL

Use `sui-graphql` when gRPC doesn't cover a relational query (e.g., "all NFTs of type X owned by address Y with field Z > N"):

```rust
use sui_graphql::client::Client;

let gql = Client::new("https://graphql.mainnet.sui.io/graphql")?;
```

Typed queries are built with `sui-graphql-macros`.

## Legacy `sui-sdk` crate (older monolithic)

Lives in `MystenLabs/sui/crates/sui-sdk`. Monolithic, JSON-RPC-based (deprecated).

```rust
use sui_sdk::SuiClientBuilder;

let client = SuiClientBuilder::default().build("https://fullnode.mainnet.sui.io:443").await?;
let owned = client.read_api().get_owned_objects(address, None, None, None).await?;
```

When to use:
- Existing codebase already uses it.
- You need JSON-RPC compatibility with older infrastructure (deprecated — Sui Foundation mainnet shutdown week of July 27, 2026).

Otherwise: migrate to the new modular crates.

Legacy docs: https://docs.sui.io/references/rust-sdk

## Common mistakes

- **Using both `sui-sdk` (legacy) and `sui-rust-sdk` crates in the same project.** Type conflicts. Pick one.
- **Skipping `set_sender` / `set_gas_budget` / `set_gas_price` on offline builds.** `try_build` will fail. For online builds with the `intents` feature, `build(client).await` auto-fills gas.
- **Using `tx.pure(&value)` for an object argument.** Object inputs go through `tx.input(ObjectInput::...)`. Pure is only for BCS-encodable value types.
- **Assuming the Rust SDK tracks the TS SDK's API shape exactly.** Method names are similar (`split_coins` vs `splitCoins`) but the argument types and async-ness differ. Check `docs.rs` for the exact signature.
- **Forgetting `.await` on `tx.build(client)`.** Offline `try_build()` is sync and returns `Result<Transaction>`; `build(client)` is async.
