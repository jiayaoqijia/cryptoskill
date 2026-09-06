# Cross-SDK Mapping

Side-by-side mapping of common Sui operations across the two officially-supported SDKs (TypeScript and Rust) and the most-used community SDK (Python). Use this when porting code or answering "how do I do X in SDK Y".

All examples assume a signer is available.

## Install

| SDK | Install |
|---|---|
| TypeScript (official) | `npm install @mysten/sui` |
| Rust (official, new) | `cargo add sui-sdk-types sui-transaction-builder sui-crypto sui-rpc` |
| Rust (legacy) | Depend on `sui-sdk` from `MystenLabs/sui` monorepo |
| Python (community, pysui) | `pip install pysui` |

## Client initialization

| Op | TypeScript | Rust (new) |
|---|---|---|
| gRPC client | `new SuiGrpcClient({ network, baseUrl })` | `sui_rpc::client::Client::new(url)` |
| JSON-RPC client (deprecated) | `new SuiJsonRpcClient({ network, url: getJsonRpcFullnodeUrl(n) })` | use legacy `sui-sdk` crate |
| GraphQL client | `new SuiGraphQLClient({ network, url })` | `sui_graphql::client::Client::new(url)` |

## Build a PTB

### TypeScript

```ts
import { Transaction } from '@mysten/sui/transactions';
const tx = new Transaction();
```

### Rust

```rust
use sui_transaction_builder::TransactionBuilder;
let mut tx = TransactionBuilder::new();
```

### Python (pysui)

```python
from pysui.sui.sui_txn import SyncTransaction
txn = SyncTransaction(client=client)
```

## Core operations

### Split from gas

| TS | `const [coin] = tx.splitCoins(tx.gas, [1_000_000]);` |
|---|---|
| Rust | `let coin = tx.split_coins(tx.gas(), vec![tx.pure(&1_000_000u64)]);` |
| Python | `coin = txn.split_coin(coin=txn.gas, amounts=[1_000_000])` |

### Move call

| TS | `tx.moveCall({ target: 'pkg::m::f', arguments: [a, b], typeArguments: ['0x2::sui::SUI'] });` |
|---|---|
| Rust | `tx.move_call(Function::new(pkg, "m", "f", vec![type_arg]), vec![a, b]);` |
| Python | `txn.move_call(target='pkg::m::f', arguments=[a, b], type_arguments=['0x2::sui::SUI'])` |

### Transfer objects

| TS | `tx.transferObjects([obj], tx.pure.address(to));` |
|---|---|
| Rust | `tx.transfer_objects(vec![obj], tx.pure(&to));` |
| Python | `txn.transfer_objects(transfers=[obj], recipient=to)` |

### Pure inputs

| TS | `tx.pure.u64(100n)` / `tx.pure.address('0x..')` / `tx.pure.string('s')` |
|---|---|
| Rust | `tx.pure(&100u64)` / `tx.pure(&address)` / `tx.pure(&"s".to_string())` |
| Python | `SuiU64(100)` / `SuiAddress('0x..')` / `SuiString('s')` (passed as arguments) |

### Object input

| TS | `tx.object('0x...')` (SDK resolves) |
|---|---|
| Rust | `tx.input(ObjectInput::owned(id, version, digest))` (you supply ref) |
| Python | `ObjectID('0x...')` passed as an argument |

### Sign & execute

| TS | `const result = await keypair.signAndExecuteTransaction({ transaction: tx, client });` |
|---|---|
| Rust | build → sign with `sui-crypto` → `client.transaction_execution_service().execute_transaction(tx, vec![sig]).await` |
| Python | `result = txn.execute(gas_budget='10000000')` |

### Wait for indexing

| TS | `await client.waitForTransaction({ digest });` |
|---|---|
| Rust | Poll `ledger_service().get_transaction(digest)` until finalized |
| Python | `client.wait_for_transaction(digest)` |

### Dry run / simulate

| TS | `await client.simulateTransaction({ transaction: tx, sender });` |
|---|---|
| Rust | `client.transaction_execution_service().dry_run_transaction(...).await` |
| Python | `txn.inspect_for_result()` / `txn.inspect_all()` |

## Data access

### Get one object

| TS | `await client.core.getObject({ objectId, include: { content: true } });` |
|---|---|
| Rust | `client.ledger_service().get_object(ObjectId, read_mask).await` |
| Python | `client.get_object('0x...')` |

### List owned objects (paginated)

| TS | `await client.core.listOwnedObjects({ owner, filter: { StructType }, limit: 50 });` |
|---|---|
| Rust | `client.state_service().list_owned_objects(owner, object_type).await` |
| Python | `client.get_owned_objects(owner='0x...')` |

### List balances

| TS | `await client.core.listBalances({ owner });` |
|---|---|
| Rust | `client.ledger_service().list_balances(owner).await` |
| Python | `client.get_all_balances(owner='0x...')` |

### Get transaction

| TS | `await client.core.getTransaction({ digest, include: { effects: true } });` |
|---|---|
| Rust | `client.ledger_service().get_transaction(digest).await` |
| Python | `client.get_transaction(digest=...)` |

## Error / status shape

| TS | `if (result.$kind === 'FailedTransaction') { ... }` |
|---|---|
| Rust | Check `response.effects.status` — `TransactionStatus::Success` vs `::Failure(err)` |
| Python | Check `result.is_ok()` and inspect `result.result_data` |

## Feature matrix

| Feature | TS (official) | Rust (new) | Python (pysui) |
|---|---|---|---|
| PTB construction | ✅ | ✅ | ✅ |
| gRPC | ✅ (`SuiGrpcClient`) | ✅ (`sui-rpc`) | ✅ |
| JSON-RPC (deprecated) | ✅ (`SuiJsonRpcClient`) | ❌ (use legacy `sui-sdk`) | ✅ |
| GraphQL | ✅ (`SuiGraphQLClient`) | ✅ (`sui-graphql`) | ✅ |
| Coin intents | ✅ (`tx.balance()` / `tx.coin()`) | ✅ (`Coin`, `Balance` intents) | partial |
| MVR name resolution | ✅ (automatic v2) | depends on crate | ❌ |
| Sponsored transactions | ✅ | ✅ | ✅ |
| Multi-sig | ✅ | ✅ | ✅ |
| zkLogin | ✅ | ✅ | partial |
| Ecosystem extensions (suins, deepbook, etc.) | ✅ (`$extend`) | manual / none | manual |
| wasm build | ✅ | ✅ (designed for it) | N/A |

## Porting gotchas

- **Object input**: TS resolves versions automatically (`tx.object('0x..')`); Rust requires you to supply the `ObjectInput` ref. When porting TS → Rust, insert a preparatory `client.ledger_service().get_object(...)` to fetch the ref first.
- **Pure typing**: TS uses typed helpers (`tx.pure.u64`); Rust uses generic BCS serialization (`tx.pure(&value)`). The Python SDK passes typed wrapper classes (`SuiU64`).
- **Async model**: Rust is explicitly async (`.await` everywhere); TS is async but the builder is sync until `.build` or `.sign`; pysui has both sync and async clients — don't mix in the same program.
- **Gas config defaults**: TS auto-resolves gas via dry-run; Rust's offline `try_build` does not — you must set budget/price or use the `intents` feature with `build(client).await`.
- **Response shape**: TS uses `$kind` discriminant; Rust returns typed enum variants; pysui wraps in a result object. Don't assume shape parity.
