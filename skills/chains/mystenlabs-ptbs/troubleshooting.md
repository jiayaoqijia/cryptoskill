# PTB Troubleshooting

Common errors from failing PTBs, with causes and fixes.

Source: https://docs.sui.io/develop/testing-debugging/common-errors · https://docs.sui.io/concepts/transactions/prog-txn-blocks

## `UnusedValueWithoutDrop { result_idx, secondary_idx }`

**Cause:** a Move call produced a value that has no `drop` ability and the PTB didn't consume it. `result_idx` is the command index; `secondary_idx` is the index within that command's return vector.

**Fix:** consume the value. Common options:
- `tx.transferObjects([value], tx.pure.address(to))` if `value` has `key + store`.
- Pass it into a later `moveCall` that takes it by value.
- Call a destructor that the module exposes (e.g., `module::destroy(value)`).

## `VMVerificationOrDeserializationError in command N`

**Cause:** the Move bytecode failed verification. Subcodes include `ZERO_SIZED_STRUCT`, `FIELD_MISSING_TYPE_ABILITY`, `UNKNOWN_VERSION`, `CONSTRAINT_NOT_SATISFIED`, `WRITEREF_WITHOUT_DROP_ABILITY`.

**Fix:** the Move source or toolchain is wrong. Not a PTB-layer issue. Rebuild the package with a matching `sui` CLI version and fix the flagged module.

## `"Failed to sign transaction by a quorum of validators because one or more of its objects is reserved for another transaction."`

**Cause:** another inflight transaction is already using an object version your transaction also needs. If enough validators have already reserved that object version for a different transaction, your transaction cannot also reserve it.

**Fix:** wait for the first transaction to finish, then rebuild or re-sign your transaction so it uses the latest object references. For related operations, combine them into one PTB. For parallel execution, use SDK helpers (`SerialTransactionExecutor`, `ParallelTransactionExecutor`) that manage gas coins and object dependencies.

## `"Failed to sign transaction … objects is equivocated until the next epoch."`

**Cause:** competing transactions used the same mutable owned object version and validator reservations were split so that no transaction could obtain quorum. The affected object version is unavailable until the next epoch.

**Fix:** wait for the next epoch (~24h on mainnet), then rebuild the transaction using current object references. Avoid submitting multiple concurrent transactions that use the same mutable owned object version. Use independent owned objects for parallel work, combine related operations into one PTB, or use SDK helpers that manage gas coins and object dependencies.

## `"No valid gas coins found for the transaction."`

**Cause:** the sender has no `Coin<SUI>` sufficient to cover `gas_budget × gas_price`, or all their SUI coins are already used as non-gas inputs.

**Fix:**
- Fund the address.
- Don't pass your only SUI coin as a `tx.object(...)` input — use `tx.gas` for gas and split from it.
- Lower `setGasBudget` if artificially high.

## `ServerError(-32002)`

**Cause:** bucket error for "invalid input at submit time." Includes:
- Missing object (wrong ID).
- Stale object version (your full node was behind, or you cached a version across a change).
- Same object referenced twice in inputs.
- Input exceeds protocol byte limits.
- Invalid signature.

**Fix:** re-fetch objects against a fresh full node before building, dedupe input references, verify signature generation.

## Insufficient gas budget

**Symptom:** tx executes but status is failure; effects show the gas coin charged.

**Cause:** `setGasBudget` too low for actual execution cost. The max budget is withdrawn at tx start and the tx aborts without effects except charging the gas input.

**Fix:** let the SDK auto-dry-run and pick the budget (don't call `setGasBudget`), or call `client.simulateTransaction` first and use the reported `gasUsed`.

## Shared object: cannot be transferred or frozen

**Symptom:** tx passes individual command validation but fails at commit.

**Cause:** passed a shared object to `transferObjects`, or called `transfer::freeze_object` on it mid-PTB.

**Fix:** shared objects have exactly two legal endings in a PTB: re-share or delete. Transferring or freezing always fails at commit. Do not include shared objects in `transferObjects`. For "unshare" patterns, the module must take the shared object by value and either re-share it or delete it before the transaction completes. Note: consuming a shared object by value permanently marks its hot-potato clique as "hot", blocking subsequent non-public `entry` calls on entangled values in that clique.

## Read-only shared object used by value

**Symptom:** validation error referring to shared-object immutability.

**Cause:** passed a shared object as `mutable: false` and then consumed it by value in a command.

**Fix:** either (a) mark the input `mutable: true` when you need value/mutable access, or (b) only use `&T` borrows of the read-only input.

## Module-private type / non-public function

**Symptom:** `"function not callable"` or similar from verifier.

**Causes:**
- Calling a `public(package)` non-entry function from a PTB.
- Supplying a type parameter whose constructor is module-private.
- Calling `transfer::transfer` / `transfer::share_object` on a generic `T` from a PTB (those require a module-private type witness).

**Fix:**
- Only call `public` or `entry` functions from a PTB.
- Use `transfer::public_transfer` / `transfer::public_share_object` for generic types with `T: store`.
- Expose a wrapper `public` / `entry` function in your module if you need to call a restricted internal function from a PTB.

## `tx.gas` misuse

**Symptoms:**
- `"argument used by value where reference expected"` on `tx.gas`.
- Gas coin disappears mid-PTB.

**Causes:**
- Passing `tx.gas` by value to anything except `transferObjects`.
- Using `tx.gas` after it was passed by value to `transferObjects` — it's gone.

**Fix:**
- For an owned `Coin<SUI>` derived from gas: `const [coin] = tx.splitCoins(tx.gas, [tx.pure.u64(n)]);`
- Transfer entire remaining gas balance at end: `tx.transferObjects([tx.gas], to);`
- Don't reference `tx.gas` after transferring it.

## Multi-return result treated as single value

**Symptom:** type error from the Move layer; argument shape doesn't match.

**Cause:** a `moveCall` that returns multiple values was passed as one argument.

**Fix:** destructure or index.
```ts
const [a, b] = tx.moveCall({ target: '0xpkg::m::pair' });
// or
const r = tx.moveCall({ target: '0xpkg::m::pair' });
nextCall(r[0], r[1]);
```

## Pure input type mismatch

**Symptom:** `"cannot deserialize pure value as type T"` or similar.

**Cause:** used untyped `tx.pure(value)` or mismatched BCS encoding.

**Fix:** use typed helpers (`tx.pure.u64(n)`, `tx.pure.address(addr)`, `tx.pure.string(s)`). For complex types, explicit `tx.pure('vector<u64>', [...])` or `tx.pure(bcs.XYZ.serialize(value))`.

## Shared-object congestion

**Symptom:** shared-object txs take seconds and fail during high contention.

**Cause:** many writers serialized through consensus on the same hot object.

**Fix:**
- Shard the shared object (many smaller shared objects keyed by hash).
- Move writes to owned objects and periodically consolidate.
- For reads, mark the input `mutable: false` so validators can schedule it in parallel.

## Empty input arrays

**Symptom:** pre-execution validation error on `SplitCoins`, `MergeCoins`, `MakeMoveVec`, or `Publish`.

**Cause:** empty amount list, empty source list, empty-but-untyped vector, empty module bytes.

**Fix:**
- `SplitCoins`: at least one amount.
- `MergeCoins`: at least one source coin.
- `MakeMoveVec`: specify `type` when `elements` is empty or non-object.
- `Publish`: at least one module.

## Sender unset on offline build

**Symptom:** `tx.build()` throws about missing sender.

**Cause:** offline build (no client) without `tx.setSender(...)`.

**Fix:** call `tx.setSender(addr)` before `tx.build()` when not going through a signer that sets it.
