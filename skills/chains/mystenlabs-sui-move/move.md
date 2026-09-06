# Move Language Fundamentals

Move is Sui's smart contract language. It is platform-agnostic and designed around resource safety. Smart contracts on Sui are called Move packages.

For the complete language reference, see [The Move Book](https://move-book.com).

## Move abilities

Every struct in Move has a set of abilities that control what you can do with it. There are four abilities:

| Ability | What it allows | When to use |
|---|---|---|
| `key` | The struct is a Sui object with a globally unique ID. Must have an `id: UID` field. | Every onchain object needs this. |
| `store` | The struct can be stored inside other objects and transferred using `public_transfer`. | Add when other modules need to transfer or wrap this object. |
| `copy` | The struct can be duplicated. | Rarely used for objects. Useful for config values or read-only data. |
| `drop` | The struct can be silently discarded at the end of a scope. | Useful for ephemeral data like events or receipts. Objects with `key` typically should not have `drop` because you want to force explicit handling. |

Common combinations:

- `has key` alone: The object can only be transferred by functions in its own module. Use when you want strict access control.
- `has key, store`: The object can be transferred, wrapped, or stored by any module. Use for assets that should be freely composable.
- `has key, store, drop`: Rare for objects, but used for ephemeral, disposable items.
- `has copy, drop`: Not an object (no `key`). A plain data struct that can be passed around freely. Used for events, configs, or intermediate values.
- `has store`: Not an object on its own, but can be stored as a field inside an object.

Abilities are enforced at compile time. You cannot add abilities to a struct after publishing — abilities are fixed at publish time. Adding an ability to an existing struct would be a non-compatible upgrade, which Sui's upgrade policy does not allow.

## TxContext

`TxContext` is a special parameter that the Sui runtime automatically provides as the last parameter to any Move function that declares it. Callers never pass it explicitly — the runtime injects it behind the scenes. It provides access to transaction metadata:

- `ctx.sender()`: The address that submitted the transaction.
- `ctx.epoch()`: The current epoch number (useful for time-based logic). Since TxContext is automatically provided by the runtime as the last parameter, you can call `ctx.epoch()` in any function that declares `ctx: &mut TxContext` without the caller needing to pass it.
- `ctx.epoch_timestamp_ms()`: The epoch start timestamp in milliseconds. Less precise than the Clock object but does not require passing an additional object.
- `object::new(ctx)`: Generates a fresh unique ID for a new object. This is the only way to create a `UID`.

`TxContext` is always the last parameter in a function signature as `ctx: &mut TxContext`. The Sui runtime automatically injects it — callers (whether PTBs, CLI commands, or SDK calls) never pass `TxContext` explicitly. The runtime supplies it as the final argument behind the scenes. When you see `ctx: &mut TxContext` in a function signature, treat it as an implicit parameter that the runtime fills in, not something you provide as an input.

## Clock object

The Clock is a shared system object at the well-known address `0x6`. It provides the current network timestamp in milliseconds. Pass it to Move functions that need precise time:

```move
use sui::clock::Clock;

public fun check_deadline(clock: &Clock) {
    let now_ms = clock.timestamp_ms();
    // ...
}
```

The Clock is more precise than `ctx.epoch_timestamp_ms()` (which returns only the epoch start time). Use the Clock for time-sensitive logic like auctions or deadlines. Use `ctx.epoch()` for epoch-level checks like staking windows.

**Important:** Because the Clock is a shared object, any transaction that reads it must go through consensus. This makes Clock access incompatible with single-owner fastpath transactions (which skip consensus for lower latency). The Clock updates approximately every 1/4 second, at the checkpoint rate. If your transaction only touches owned objects and does not need sub-epoch time precision, prefer `ctx.epoch_timestamp_ms()` to stay on the fastpath.

## Init functions and One-Time Witness

### The init function

Each module can have an optional `init` function that runs exactly once when the package is published. It is never callable again. Use it to create singleton objects like admin capabilities, registries, or treasury caps.

```move
fun init(ctx: &mut TxContext) {
    transfer::transfer(
        AdminCap { id: object::new(ctx) },
        ctx.sender()
    );
}
```

If multiple modules in a package each have `init` functions, all of them run during the publish transaction. The object IDs created during `init` appear in the publish transaction's effects.

### One-Time Witness (OTW)

A One-Time Witness is a special struct that the runtime creates exactly once and passes to `init`. It proves that code is running during the module's publish transaction. The struct must:

- Have the same name as the module, in ALL CAPS.
- Have only the `drop` ability.
- Have no fields.

```move
module my_package::my_token {
    public struct MY_TOKEN has drop {}

    fun init(witness: MY_TOKEN, ctx: &mut TxContext) {
        // Use the witness to create a currency, for example
        let (treasury_cap, metadata) = coin::create_currency(
            witness, 9, b"MYT", b"My Token", b"", option::none(), ctx
        );
        // ...
    }
}
```

OTW is required by `coin::create_currency` and other framework functions that need proof of module authority.

### `internal::Permit<T>` — type-level authorization

`std::internal::Permit<T>` is a stdlib primitive for proving that you are the module that defines type `T`. Create one by calling `internal::permit<T>()` — this compiles only inside the module that defines `T`.

```move
use std::internal;

/// Works in any function, not just init
public fun register_my_type(registry: &mut Registry) {
    let permit = internal::permit<MyType>();
    registry.add_type(permit);
}
```

Unlike OTW (which exists only during `init`) and Publisher (which proves package-level authority), `Permit<T>` proves type-level authority and can be created in any function at any time.

| Mechanism | When to use |
|---|---|
| OTW | One-time setup in `init` (coin creation, etc.) |
| Publisher | Proving package authority to external systems |
| `internal::Permit<T>` | Proving you define type `T` — works in any function, not just `init` |

## Move packages

A Move package is a set of compiled bytecode modules published to the Sui network as an immutable object. Every published package receives a unique package ID on the network.

A package contains:

- `sources/` directory with `.move` module files
- `Move.toml` configuration file defining the package name, edition, dependencies, and named addresses

## Package upgrades

Packages can be upgraded by publishing a new version, but the original version is always preserved onchain. Upgrades are controlled through an `UpgradeCap` object that the publisher receives at publish time. The `UpgradeCap` is an address-owned object sent to the publishing address.

Upgrade policies restrict what can change:

- **Compatible:** Functions can be added but not removed. Struct layouts cannot change.
- **Additive:** New modules can be added, but existing modules cannot change.
- **Dependency-only:** Only dependency versions can be updated.

You can restrict the `UpgradeCap` in the same PTB as the publish command (for example, calling `only_additive_upgrades` on it immediately). Once restricted, you cannot widen the policy. You can also transfer the `UpgradeCap` to a multisig address or destroy it to make the package permanently immutable.

## Move modules

A module lives inside a package and defines the types (structs) and functions that interact with onchain objects. Modules are the unit of encapsulation in Move.

## `type_name` deprecations

The `std::type_name` module has renamed several functions. Use the new names — the old ones still compile but are deprecated and may be removed in a future release.

| Deprecated | Replacement |
|---|---|
| `type_name::get<T>()` | `type_name::with_defining_ids<T>()` |
| `type_name::get_with_original_ids<T>()` | `type_name::with_original_ids<T>()` |

Additionally, `type_name::original_id<T>(): address` is a native helper that returns the defining package address directly. Use it instead of manually parsing via `address_string()` and `from_ascii_bytes()`.

## Move objects (structs)

Objects in Move are structs with typed fields. A struct can contain primitives, other objects, or non-object structs. The `key` ability marks a struct as an object (it must have an `id: UID` field). The `store` ability allows a struct to be stored inside other objects. See the "Move abilities" section above for the full ability reference.

## Resource safety

Move enforces two critical constraints at compile time:

1. All resources must be either moved into global storage or destroyed by the end of a transaction. You cannot silently drop an object (unless it has `drop`).
2. Resources without `copy` cannot be duplicated. There is always exactly one owner of any given resource.

These guarantees are enforced by the compiler, not by gas metering. This differs from Ethereum where the EVM prices operations to prevent abuse. In Move, invalid resource handling is a compilation error, not a runtime cost.

To destroy an object that lacks `drop`, you must explicitly unpack (destructure) the struct and handle each field. The UID field must be deleted using `object::delete(id)`, which consumes the UID by value. All other fields must be dropped (if they have `drop`), stored, or recursively unpacked.

```move
public struct Character has key {
    id: UID,
    name: String,
}

public fun destroy_character(character: Character) {
    let Character { id, name: _ } = character; // unpack the struct
    id.delete(); // delete the UID — required for all objects
}
```

A shared object can also be destroyed this way: if a function takes the shared object by value and deletes it within the same function, the system permits it.

## Example: a Greeting module

```move
module hello_world::greeting {
    use std::string::String;

    public struct Greeting has key, store {
        id: UID,
        text: String,
    }

    public fun new(ctx: &mut TxContext) {
        let greeting = Greeting {
            id: object::new(ctx),
            text: b"Hello world!".to_string(),
        };
        transfer::share_object(greeting);
    }

    public fun update_text(greeting: &mut Greeting, new_text: String) {
        greeting.text = new_text;
    }
}
```

Key patterns in this example:

- `Greeting` has the `key` ability (making it a Sui object) and `store` (allowing nested storage and public transfers).
- `object::new(ctx)` generates a unique ID for the new object.
- `transfer::share_object()` places the object in shared global storage so any address can interact with it.
- `&mut Greeting` is a mutable reference, allowing modification without violating resource safety.

## Access control patterns

### Admin rotation (two-step transfer)

Never transfer an `AdminCap` directly to a new address in one step — if the recipient address is wrong, the cap is lost forever. Use a two-step pattern:

```move
public struct AdminTransferRequest has key {
    id: UID,
    new_admin: address,
}

/// Step 1: current admin proposes a transfer
public fun propose_admin_transfer(
    cap: &AdminCap,
    new_admin: address,
    ctx: &mut TxContext,
) {
    transfer::transfer(AdminTransferRequest {
        id: object::new(ctx),
        new_admin,
    }, new_admin);
}

/// Step 2: new admin accepts and receives the cap
public fun accept_admin_transfer(
    cap: AdminCap,
    request: AdminTransferRequest,
    ctx: &mut TxContext,
) {
    let AdminTransferRequest { id, new_admin } = request;
    assert!(ctx.sender() == new_admin);
    id.delete();
    transfer::transfer(cap, new_admin);
}
```

The new admin must actively call `accept_admin_transfer`, proving they control the target address. If the request is never accepted, the cap stays with the original admin.

### Deny lists (regulated coins)

Sui provides a system-level `DenyList` shared object (`0x403`) for regulated coins. Use `coin::create_regulated_currency_v2` instead of `coin::create_currency` to enable address-based transfer restrictions:

```move
use sui::coin;
use sui::deny_list::DenyList;

public struct MY_TOKEN has drop {}

fun init(otw: MY_TOKEN, ctx: &mut TxContext) {
    let (treasury_cap, deny_cap, metadata) = coin::create_regulated_currency_v2(
        otw, 9, b"TKN", b"Token", b"A regulated token", option::none(), ctx,
    );
    transfer::public_transfer(treasury_cap, ctx.sender());
    transfer::public_transfer(deny_cap, ctx.sender());
    transfer::public_freeze_object(metadata);
}

/// Add an address to the deny list (requires DenyCapV2)
public fun block_address(
    deny_list: &mut DenyList,
    deny_cap: &mut DenyCapV2<MY_TOKEN>,
    addr: address,
    ctx: &mut TxContext,
) {
    coin::deny_list_v2_add(deny_list, deny_cap, addr, ctx);
}

/// Remove an address from the deny list
public fun unblock_address(
    deny_list: &mut DenyList,
    deny_cap: &mut DenyCapV2<MY_TOKEN>,
    addr: address,
    ctx: &mut TxContext,
) {
    coin::deny_list_v2_remove(deny_list, deny_cap, addr, ctx);
}

/// Pause all transfers of this coin type globally
public fun global_pause(
    deny_list: &mut DenyList,
    deny_cap: &mut DenyCapV2<MY_TOKEN>,
    ctx: &mut TxContext,
) {
    coin::deny_list_v2_enable_global_pause(deny_list, deny_cap, ctx);
}

/// Unpause all transfers of this coin type globally
public fun global_unpause(
    deny_list: &mut DenyList,
    deny_cap: &mut DenyCapV2<MY_TOKEN>,
    ctx: &mut TxContext,
) {
    coin::deny_list_v2_disable_global_pause(deny_list, deny_cap, ctx);
}
```

Key points:
- `create_regulated_currency_v2` returns an additional `DenyCapV2<T>` alongside the `TreasuryCap`.
- The `DenyCapV2` authorizes adding/removing addresses from the deny list and enabling/disabling global pause. Custody of the `DenyCapV2` is as important as the `TreasuryCap`.
- Denied addresses cannot receive the coin type in any transaction. The restriction is enforced at the validator level.
- Use `coin::deny_list_v2_enable_global_pause` / `coin::deny_list_v2_disable_global_pause` to pause or resume all transfers of the coin type globally (emergency freeze).
- The `DenyList` object at `0x403` is a system shared object. Reference it from TypeScript with `tx.object.denyList()`.

For custom (non-coin) deny lists, store a `Table<address, bool>` or `VecSet<address>` in a shared object and check it in your entry functions.

### Security review checklist

When reviewing a Move package's access control:

1. **Capability custody.** Where is each cap (`AdminCap`, `TreasuryCap`, `DenyCapV2`, `UpgradeCap`) created? Where does it end up? Is it transferred to `ctx.sender()` in `init`, or is it shared/wrapped? Can it be transferred to a new owner, and if so, through what mechanism? Never freeze or share the `TreasuryCap` — doing so might allow malicious actors to call functions as the currency owner.
2. **Shared object entry points.** Every `public` or `entry` function that takes a `&mut SharedObject` is callable by any address. Verify that each one either (a) checks a capability, (b) checks `ctx.sender()` against a stored admin address, or (c) is intentionally permissionless.
3. **`entry` vs `public` visibility.** `entry` functions are callable from PTBs (at any position, not just the first command) but cannot be called from other Move packages — they restrict cross-package composability, not PTB ordering. `public` functions are callable from other Move code and PTBs. Prefer `public` for composability, but be aware that `public` functions can be called by any other package.
4. **Admin rotation.** Is there a way to transfer admin authority? If so, does it use a two-step pattern? A single-step transfer risks permanent loss if the recipient address is wrong.
5. **Deny list / blocklist.** For regulated tokens, is `create_regulated_currency_v2` used? Is the `DenyCapV2` custody secured? For custom deny lists, are blocked addresses checked in all relevant entry points?
6. **Event emission.** Are security-critical actions (admin changes, deny list modifications, object deletions, configuration updates) emitting events? Events are the only way for offchain monitoring to detect these actions.
7. **Object deletion.** Can shared objects be deleted? If so, who can delete them? Deleting a shared object with dynamic fields renders those fields permanently inaccessible.
8. **Upgrade policy.** Is the `UpgradeCap` held by a multisig or has the package been made immutable? An unrestricted `UpgradeCap` held by a single key means the entire package can be rewritten.

## Advanced design patterns

### Ability dosing — default to minimum abilities

Only add `store` if you genuinely need cross-module transferability or wrapping. Adding `store` weakens module-level invariants because it enables `public_transfer` — anyone can move the object, bypassing your module's transfer logic. Default to `key` only and add `store` consciously.

### Phantom type parameters on events

Use `phantom T` on event structs for native RPC type-filtering instead of carrying type names as string fields:

```move
public struct Attested<phantom T> has copy, drop { subject: address }
```

The event's full type `0xPKG::module::Attested<ConcreteT>` is filterable via RPC `eventType` — no string parsing needed.

### Event limit

A single transaction can emit a maximum of 1,024 events (`max_num_event_emit` protocol config). If your logic could exceed this limit (e.g., batch operations emitting per-item events), aggregate into fewer, larger events or split across multiple transactions.

### Event denormalization anti-pattern

Events should not carry information already derivable from the transaction effects (e.g., `tx.sender` for who executed, package address for type identity). This adds storage cost and creates dual sources of truth.

### Prefer `&` over `&mut` on shared objects

Sui consensus serializes transactions that take `&mut` references to shared objects. If your function only reads from a shared object, take `&` instead of `&mut` — this allows concurrent execution. This is one of the most impactful performance optimizations on Sui.

### Receiver-syntax-friendly argument ordering

Put capabilities (`Permit<T>`, `OwnerCap`, etc.) late in the argument list so the "main" object can be the receiver:

```move
// Good: enables registry.attest(...)
public fun attest<T>(&Registry, ..., _: Permit<T>)
// Bad: no receiver syntax
public fun attest<T>(_: Permit<T>, &Registry, ...)
```

### Clever error constants

Use `#[error]` attributes with human-readable messages:

```move
#[error(code = 0)]
const EBoxAlreadyExists: vector<u8> = b"A Box already exists for this subject";
```

### `transfer::receive` privacy

`transfer::receive<T>(uid, rcv)` is restricted to `T`'s defining module (same as `transfer::transfer`). Use `transfer::public_receive` (requires `T: key + store`) for cross-module access. Symmetric to `transfer`/`public_transfer`.

### Field privacy as a safety primitive

Move struct fields are private to the defining module. This is load-bearing for safe by-value APIs — even when you return an owned object, callers cannot mutate its fields. Combined with hot potatoes and no-`store`, this is why borrow-style patterns are safe.

### Move 2024 macro gotchas

- `()` is not a nameable type in macro return position. `public macro fun foo<$T, $R>(...) -> $R` fails when the caller substitutes `()`. Fix: return a value or have a separate void macro.
- Macros expand in caller-module scope for privacy. A macro touching private fields can only be invoked from inside the defining package — macros are not a privacy escape hatch.

### Common API mistakes

These are frequently hallucinated or confused APIs. **Always use the correct version.**

| Wrong | Correct | Notes |
|---|---|---|
| `event::emit_event(...)` | `event::emit(MyEvent { ... })` | There is NO `emit_event` function. The function is `sui::event::emit`. |
| `emit_event(...)` | `event::emit(...)` | Same — no `emit_event` exists anywhere in the Sui framework. |
| `transfer::transfer_coin(...)` | `transfer::public_transfer(coin, addr)` | There is NO `transfer_coin`. Use `public_transfer` for objects with `store`. |
| `ctx` used as standalone | `ctx: &mut TxContext` declared as parameter | `ctx` is a parameter name, not a global. Declare it in every function that needs it. |
| `sui::test_utils::destroy(x)` | `std::unit_test::destroy(x)` | `test_utils::destroy` is deprecated. Use `std::unit_test::destroy`. |
| `vector::empty()` | `vector[]` | Use literal syntax in Move 2024. |
| `vector::push_back(&mut v, x)` | `v.push_back(x)` | Use method syntax in Move 2024. |
| `coin::mint_for_testing(...)` | `coin::mint_for_testing<T>(amount, ctx)` | Needs explicit type parameter `<T>` and `&mut TxContext`. |
| `object::new(ctx)` inside struct literal | `let id = object::new(ctx);` then use `id` | Create the UID first, then use it in the struct. |
| `borrow_global<T>(addr)` | Not available — use object references | Sui Move does NOT have `borrow_global`. This is an Aptos/Diem function. In Sui, pass objects as function parameters (`&T` or `&mut T`). |
| `create_signer(addr)` | Not available — use `TxContext` | Sui does NOT have `create_signer`. The signer is implicit via `ctx: &mut TxContext`. Use `ctx.sender()` for the sender address. |
| `create_clock()` | Pass `&Clock` as a parameter | Sui does NOT have `create_clock`. The Clock is a shared object at `0x6`. Pass it as `clock: &Clock` in function params. In tests, use `clock::create_for_testing(ctx)`. |
| `vector::matches(...)` | Use `vector::contains(&v, &elem)` or loop | There is no `matches` function on vectors. Use `v.contains(&elem)` or iterate manually. |
| `table::keys(...)` | Iterate with known keys or use a separate vector | Sui `Table` does not have a `keys()` method. Track keys separately in a `vector` if you need enumeration. |

### Sui Move is NOT Aptos Move

Sui Move and Aptos Move diverged significantly. **Do not use Aptos/Diem patterns:**

- **No `borrow_global` / `move_from` / `move_to`** — Sui uses object-centric storage. Objects are passed as function parameters, not borrowed from global storage.
- **No `create_signer`** — Sui uses `TxContext` for sender identity. `ctx.sender()` returns the sender address.
- **No `acquires` keyword** — Sui functions don't acquire resources. Objects are passed explicitly.
- **No global storage operators** — In Sui, objects are owned, shared, or immutable. Access them via transfer, dynamic fields, or function parameters.
- **The Clock is shared, not created** — Pass `clock: &sui::clock::Clock` as a parameter. The Clock lives at address `0x6`. In tests, create with `sui::clock::create_for_testing(ctx)`.

### Correct event emission pattern

**Always write events exactly like this:**

```move
use sui::event;

public struct TransferCompleted has copy, drop {
    sender: address,
    recipient: address,
    amount: u64,
}

public fun transfer_tokens(recipient: address, amount: u64, ctx: &mut TxContext) {
    // ... transfer logic ...
    event::emit(TransferCompleted {
        sender: ctx.sender(),
        recipient,
        amount,
    });
}
```

### Correct test cleanup pattern

```move
#[test]
fun test_example() {
    use std::unit_test::destroy;  // NOT sui::test_utils::destroy

    let mut ctx = tx_context::dummy();
    let item = create_item(&mut ctx);
    // ... assertions ...
    destroy(item);
}
```
