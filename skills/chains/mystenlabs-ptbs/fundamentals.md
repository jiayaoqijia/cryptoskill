# PTB Fundamentals

The data model, execution semantics, and protocol constraints for Sui Programmable Transaction Blocks.

Source: https://docs.sui.io/concepts/transactions/prog-txn-blocks · https://docs.sui.io/develop/transactions/ptbs/inputs-and-results

## Structure

```
{
  inputs:   [Input],     // external values (CallArg in Rust)
  commands: [Command],   // operations executed in order
}
```

- Commands execute **in declaration order**.
- Effects are applied **atomically at the end**. Any failing command reverts the entire block.
- A PTB can contain up to **1,024 commands**. More intricate flows (loops, conditionals) require publishing a Move package.

Transaction metadata surrounding the PTB:
- `sender` — address that signed.
- `gas_data` — `{ payment: [ObjectRef], owner, price, budget }`. Max budget is withdrawn from the gas coin at tx start; unused is refunded.
- `expiration` — optional epoch; validators reject after.
- `tx_signatures` — user signature and, for sponsored txs, sponsor signature too.

## Inputs

An `Input` is either an object or a pure (BCS-encoded) value.

### Object inputs — `ObjectArg` variants

- **`ImmOrOwnedObject(ObjectID, SequenceNumber, ObjectDigest)`** — owned by an address, or immutable. Specify a concrete version.
- **`SharedObject { id, initial_shared_version, mutable }`** — shared object. `initial_shared_version` is the version at which it was first shared (used by consensus routing). `mutable: false` makes it read-only and enables parallel execution across transactions that all read it.
- **`Receiving(ObjectID, SequenceNumber, ObjectDigest)`** — object owned by *another* object (sent via `TransferObjects` or `sui::transfer::transfer` to an object ID). Has type `sui::transfer::Receiving<T>`; unwrap inside Move with `sui::transfer::receive(&mut parent, receiving)`.

### Pure inputs — allowed BCS types

Pure values are raw BCS bytes. The pure type is **deferred**: bytes are validated against the expected Move type on first use. Allowed:

- Primitives: `u8, u16, u32, u64, u128, u256, bool, address`
- `std::ascii::String`, `std::string::String` (bytes verified for encoding)
- `sui::object::ID`
- `vector<T>` where `T` is itself a valid pure type
- `std::option::Option<T>` where `T` is itself a valid pure type

The same pure bytes can be used at multiple compatible types if they deserialize cleanly for each.

## The `Argument` enum

Commands reference values via four `Argument` kinds:

- **`Input(u16)`** — input at index `u16` in the `inputs` vector.
- **`GasCoin`** — the SUI coin paying for gas. **Always present in every transaction**, even when using address-balance payment. When paying with address balances, an ephemeral gas coin is created for the transaction and deleted at the end if not transferred. Special rules:
  - Can be used by `&` or `&mut` anywhere.
  - Can be passed by value **only** to `TransferObjects` or `sui::coin::send_funds`.
  - To get an owned `Coin<SUI>` from the gas coin, split it first: `SplitCoins(GasCoin, [amount])`.
  - In sponsored transactions, the **sender** can still use the GasCoin (which belongs to the sponsor). Sponsors should validate submitted PTBs to ensure the gas coin is not misused.
- **`Result(u16)`** — shorthand for `NestedResult(i, 0)`. Valid only when command `i` has exactly one return value.
- **`NestedResult(u16, u16)`** — `(command_index, result_index_within_that_command)`.

## Results

Each command produces a (possibly empty) vector of typed results:

| Command | Results |
|---------|---------|
| `MoveCall` | Whatever the Move function returns (zero or more; no references) |
| `SplitCoins` | `[Coin<T>, Coin<T>, …]` (one per amount) |
| `MergeCoins` | empty |
| `TransferObjects` | empty |
| `MakeMoveVec` | one `vector<T>` (elements not individually addressable) |
| `Publish` | `UpgradeCap` |
| `Upgrade` | `UpgradeReceipt` |

Chaining example (verbatim from the docs):
```ts
const tx = new Transaction();
const hero = tx.moveCall({ target: `0x123::hero::mint_hero`, arguments: [], typeArguments: [] });
const sword = tx.moveCall({
  target: `0x123::hero::new_sword`,
  arguments: [tx.pure.u64(10)],
  typeArguments: [],
});
tx.moveCall({ target: `0x123::hero::equip_sword`, arguments: [hero, sword] });
```

## Execution semantics

### Start-of-transaction

1. Input objects loaded (ownership + existence validated upstream).
2. Pure bytes loaded but not yet typed.
3. **Max gas budget (in MIST) is withdrawn from the gas coin.** Unused gas is refunded at end of execution, even if the gas coin changed owners.

### Argument usage rules

These rules are **inferred by the runtime** from the Move function signatures being called. The PTB itself does not specify whether an argument is passed by reference, mutable reference, or value — the system determines this from the target function's parameter types.

For each argument position:
- **`&mut T` expected** — mutable borrow. Fails if any other borrow is outstanding.
- **`&T` expected** — immutable borrow. Fails if a mutable borrow is outstanding; multiple immutable borrows are fine.
- **`T` expected** — copy if `T: copy`, else move. Objects are always moved because `sui::object::UID` has no `copy`.
- Using an argument **after it's been moved** fails the transaction.
- For `copy` + no-`drop` types, the **last use must be by value**.

### Object consumption

- Every value created or returned by a Move command must be **consumed** by end of tx: transferred, destroyed, or passed into another command. Exception: values whose type has `drop` can be left to drop.
- Shared objects **cannot** be transferred or frozen at tx end (the ops "succeed" during execution but the tx fails at commit).
- Shared objects **cannot** be wrapped or converted to dynamic fields mid-execution — doing so causes the transaction to fail. Shared objects must be re-shared or deleted before commit.
- Gas coin returns to its owner; remaining budget refunded.

### Hot-potato cliques (non-public `entry` calls)

Values without `drop` or `store` (hot potatoes) must be consumed before tx end. Cliques track entangled values:
- Each input starts in its own clique with hot count 0.
- Using values together as args merges their cliques.
- Non-public `entry` calls require their argument clique to have hot count **0**.
- Consuming a hot potato decrements the count.
- **Consuming a shared object by value permanently marks its clique hot.**

If you're calling non-public entries, resolve hot potatoes (e.g., repay a flash loan) before the entry call.

### End-of-transaction

- Immutable / read-only inputs: skipped.
- Mutable input objects: returned to original owner.
- Pure inputs: dropped.
- Shared objects: must be re-shared or deleted; else tx fails.
- Results with `drop`: dropped automatically.
- Results with `copy` but no `drop`: last use must have been by value.
- Other unused non-`drop` values: transaction error.
- Gas coin: returned to owner with unused gas refunded.

## Protocol limits

- **Max unique operations per PTB: 1,024.**
- **Max Move object size: 250 KB.** Exceeding aborts the tx.
- `vector`-backed collections (`vector`, `VecSet`, `VecMap`, `PriorityQueue`): recommend ≤ 1,000 items. Use `Table`, `Bag`, `ObjectBag`, `ObjectTable`, `LinkedTable` for unbounded or third-party-written collections.
- `MoveCall` return values **cannot be references** (`&T`, `&mut T`) — restriction may be lifted later.
- Only `public` functions and `entry` functions (including private `entry` and `public(package) entry`) are callable from a PTB.
- Shared objects passed as `mutable: false` cannot be used by value.
- Module-private type parameters cannot be supplied from a PTB — use the `public_*` variants of `transfer::transfer` / `transfer::share_object`.

## Worked execution example

Verbatim from the PTB concept page:

```
{
  inputs: [
    Pure(<@0x808 BCS bytes>),
    Object(SharedObject { id: market_id, ... }),
    Pure(<100u64 BCS bytes>),
  ]
  commands: [
    SplitCoins(GasCoin, [Input(2)]),                                // -> [Coin<SUI>]
    MoveCall("some_package", "some_marketplace", "buy_two", [],
             [Input(1), NestedResult(0, 0)]),                       // -> [Nft, Nft]
    TransferObjects([GasCoin, NestedResult(1, 0)], Input(0)),       // gas + first NFT -> 0x808
    MoveCall("sui", "tx_context", "sender", [], []),                // -> [address]
    TransferObjects([NestedResult(1, 1)], NestedResult(3, 0)),      // second NFT -> sender
  ]
}
```

State transitions (gas balance shifts, moved-value tracking) are walked through in the source page — consult it if you need the complete trace.
