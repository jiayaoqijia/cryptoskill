# PTB Command Reference

All seven PTB commands, with argument types, return shape, and common pitfalls.

Source: https://docs.sui.io/references/ptb-commands · https://docs.sui.io/concepts/transactions/prog-txn-blocks

## `TransferObjects`

Transfers a list of objects to an address. Objects are taken **by value**.

```
TransferObjects(ObjectArgs: [Argument], AddressArg: Argument)
Signature:  (vector<forall T: key + store. T>, address): ()
Returns:    []
```

- All object arguments must have `key + store`.
- Address can be a `Pure` input or a `Result` (e.g., the return of a `MoveCall` that produces an address).
- TS SDK: `tx.transferObjects([coin1, coin2], tx.pure.address(to))`.
- The one case where `tx.gas` can be passed by value: `tx.transferObjects([tx.gas], to)` transfers the entire remaining gas balance.
- Do **not** include shared objects — sharing is permanent; such a tx will fail at commit.

## `SplitCoins`

Splits a source coin into one or more new coins.

```
SplitCoins(CoinArg: Argument, AmountArgs: [Argument])
Signature:  <T: key + store>(coin: &mut Coin<T>, amounts: vector<u64>): vector<Coin<T>>
Returns:    [Coin<T>, Coin<T>, …]  (one per amount, in order)
```

- `CoinArg` is taken by `&mut` — can be `tx.gas`, a `tx.object(coinId)`, or a prior result.
- `AmountArgs` are `u64` values (pure or result); copied, so they're reusable.
- TS SDK: `const [a, b] = tx.splitCoins(tx.gas, [tx.pure.u64(100), tx.pure.u64(200)]);`
- Amounts array must be **non-empty**; empty arrays fail pre-execution.

## `MergeCoins`

Merges coins into a destination coin. Merged coins are **consumed**.

```
MergeCoins(CoinArg: Argument, ToMergeArgs: [Argument])
Signature:  <T: key + store>(coin: &mut Coin<T>, to_merge: vector<Coin<T>>): ()
Returns:    []
```

- Destination is `&mut`; sources are moved.
- Common pattern: consolidate owned gas coins at start of tx — `tx.mergeCoins(tx.gas, [tx.object(coin1), tx.object(coin2)])`.
- `ToMergeArgs` must be non-empty.

## `MakeMoveVec`

Builds a `vector<T>` usable as a Move call argument.

```
MakeMoveVec(VecTypeOption: Option<TypeTag>, Args: [Argument])
Signature:  (T...): vector<T>
Returns:    [vector<T>]  (single result)
```

- `VecTypeOption` is **required** for non-object element types or empty vectors; optional when elements are objects whose type can be inferred.
- Elements **cannot** be accessed individually via `NestedResult`. The vector is one result; pass it as a whole to a `MoveCall` to work with elements.
- TS SDK:
  - `tx.makeMoveVec({ elements: [tx.object(id1), tx.object(id2)] })`
  - `tx.makeMoveVec({ type: '0x2::foo::Bar', elements: [] })` — empty vector needs explicit type.

## `MoveCall`

Call a Move function. The core command for business logic.

```
MoveCall(Package, Module, Function, TypeArgs, Args)
Returns:  values per the Move function signature (no references)
```

- Callable functions: **`public`** functions, **all `entry` functions** (including private `entry fun` and `public(package) entry`). Non-entry private or non-entry `public(package)` functions are **not** callable.
- **Cannot** return `&T` or `&mut T`. Returning a reference makes the function uncallable from a PTB.
- `TxContext` parameters (`&TxContext` / `&mut TxContext`) are auto-injected. Do **not** supply them; do **not** count them when indexing arguments. They can appear at any position and multiple `&TxContext` are allowed.
- **Module-private type parameters can't be supplied from PTBs.** For generics, use `transfer::public_transfer` instead of `transfer::transfer`, and `transfer::public_share_object` instead of `transfer::share_object` — the `public_*` variants require `T: store` instead of a private type witness.
- TS SDK:
  ```ts
  tx.moveCall({
    target: '0x2::devnet_nft::mint',
    arguments: [tx.pure.string(name), tx.pure.string(desc), tx.pure.string(url)],
    typeArguments: ['0x2::sui::SUI'],
  });
  ```
- Multi-return destructuring:
  ```ts
  const [nft1, nft2] = tx.moveCall({ target: '0xpkg::mint::two' });
  tx.transferObjects([nft1, nft2], tx.pure.address(to));
  ```

## `Publish`

Publish a new Move package.

```
Publish(ModuleBytes: vector<vector<u8>>, TransitiveDependencies: vector<ObjectID>)
Returns:  [UpgradeCap]   (sui::package::UpgradeCap)
```

- `ModuleBytes` must be non-empty.
- After bytecode verification, each module's `init` function (if present) is called **in the order modules appear** in the byte vector. `init` takes `&mut TxContext` and optionally a one-time witness.
- The returned `UpgradeCap` is a regular object — you must transfer or consume it (typically `tx.transferObjects([cap], tx.pure.address(deployer))`).
- TS SDK: `tx.publish({ modules, dependencies })`.

## `Upgrade`

Upgrade an existing Move package.

```
Upgrade(ModuleBytes, TransitiveDependencies, PackageID, UpgradeTicket)
Returns:  [UpgradeReceipt]   (sui::package::UpgradeReceipt)
```

- Takes exactly one PTB argument: the `UpgradeTicket` (by value). The ticket is produced by calling the `UpgradeCap`'s authorization function.
- Does **not** call `init` on new modules. New modules cannot define `init` (restriction may be lifted).
- Module digest and package ID in the ticket must match exactly.
- Upgrade policy (compatible / additive / dep-only) is enforced from the ticket.
- The `UpgradeReceipt` must be committed back to the `UpgradeCap` via `package::commit_upgrade` (typically another `MoveCall` in the same PTB).
- TS SDK: `tx.upgrade({ modules, dependencies, packageId, ticket })`.

## Quick reference

| Command | Mutates | Consumes | Returns |
|---|---|---|---|
| `TransferObjects` | — | all object args | — |
| `SplitCoins` | source coin | — | `[Coin<T>]` per amount |
| `MergeCoins` | dest coin | source coins | — |
| `MakeMoveVec` | — | element args | `[vector<T>]` |
| `MoveCall` | per signature | per signature | per signature |
| `Publish` | — | — | `[UpgradeCap]` |
| `Upgrade` | — | `UpgradeTicket` | `[UpgradeReceipt]` |
