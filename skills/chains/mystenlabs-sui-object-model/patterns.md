# Common Patterns and Derived Objects

Design patterns for modeling data and enforcing invariants with the Sui object model.

## Hot potato pattern

A hot potato is a struct with no abilities at all. It cannot be stored, copied, or dropped. It must be consumed by a function in the same transaction (PTB). This enforces multi-step workflows:

```move
public struct Receipt {}  // no abilities

public fun borrow_item(safe: &mut Safe): (Item, Receipt) {
    let item = /* remove item from safe */;
    (item, Receipt {})
}

public fun return_item(safe: &mut Safe, item: Item, receipt: Receipt) {
    let Receipt {} = receipt;  // consume the hot potato
    /* put item back in safe */
}
```

The borrower must call `return_item` in the same PTB, because `Receipt` cannot be stored or dropped. If they do not, the transaction aborts.

## Capability pattern

A capability (cap) is an object that grants permission to perform an action. Common examples: `AdminCap`, `TreasuryCap`, `UpgradeCap`. Typically created in the module's `init` function and transferred to the publisher.

```move
public struct AdminCap has key, store { id: UID }

fun init(ctx: &mut TxContext) {
    transfer::transfer(AdminCap { id: object::new(ctx) }, ctx.sender());
}

public fun admin_action(_: &AdminCap, registry: &mut Registry) {
    // Only callable by whoever holds the AdminCap
}
```

### Borrow pattern

Caps can be stored inside other objects and temporarily borrowed using the `sui::borrow` module. This module provides a `Referent<T>` wrapper and a hot potato receipt to ensure the cap is returned in the same PTB.

The type wrapped in `Referent<T>` must have `key + store` abilities. This means only objects with both `key` and `store` can be placed inside a `Referent`.

The flow:

1. Store the cap inside a `Referent<T>` wrapper.
2. When a caller needs temporary access, call `borrow::borrow(&mut referent)` which returns the cap and a hot potato `Borrow` receipt.
3. The caller uses the cap (for example, mints tokens with a `TreasuryCap`).
4. The caller must call `borrow::put_back(&mut referent, cap, receipt)` in the same PTB to return the cap and consume the receipt.

Because the `Borrow` receipt has no `drop`, the caller cannot keep the cap — the transaction aborts if the receipt is not consumed. This is safer than transferring the cap, which would give permanent access.

## Soulbound objects

An object without `store` can only be transferred by its defining module. To make it fully non-transferable, simply do not expose any transfer function. To allow temporary borrowing with forced return, use the hot potato pattern with a `ReturnReceipt`: the module lends the soulbound object out and issues a `ReturnReceipt` hot potato (a struct with no abilities) that forces the borrower to return the object in the same PTB. If the borrower does not call the return function, the transaction aborts because the receipt cannot be stored or dropped.

## Inventory pattern

For an object that holds an arbitrary collection of other objects (like a player character with an equipment inventory), use `ObjectBag` or `ObjectTable`:

```move
public struct Player has key {
    id: UID,
    inventory: ObjectBag,  // holds any object type
}

public fun add_to_inventory<T: key + store>(player: &mut Player, item: T) {
    let item_id = object::id(&item);
    object_bag::add(&mut player.inventory, item_id, item);
}

public fun remove_from_inventory<T: key + store>(
    player: &mut Player, item_id: ID
): T {
    object_bag::remove(&mut player.inventory, item_id)
}
```

Use `ObjectBag` when items can be different types (Sword, Shield, Potion). Use `ObjectTable<ID, T>` when all items are the same type.

## Derived objects

Derived objects use deterministic IDs computed from a parent object's ID and a key, rather than random assignment. Compute the address before creating the object:

```move
let derived_addr = derived_object::derive_address(parent_id, key);
```

Key properties:

- **Deterministic:** The same (parent, key) always produces the same address.
- **Not hierarchical:** Despite using a parent for uniqueness, derived objects are independent. The parent only ensures uniqueness.
- **Parallel-friendly:** Unrelated keys can be updated simultaneously because derived objects are independently owned, unlike dynamic fields which sequence through the parent.
- **Receive before creation:** Assets can be sent to a derived address before the derived object exists.

### Derived objects vs dynamic fields

| Aspect | Derived objects | Dynamic fields |
|---|---|---|
| Address predictable before creation | Yes | Yes |
| Parent required for access | Only at creation | Always |
| Independent ownership | Yes (owned, shared, party, immutable, or wrapped) | No (always owned by parent) |
| Can receive objects | Yes | No |
| Parallel access | Yes | Limited (sequenced through parent) |
| Supports reclaiming | Not currently supported | Yes (remove from parent) |
| Supports deletion | Yes | Yes |

Use derived objects for registries, per-user configurations, soulbound tokens, and cases where you need parallel access without bottlenecking through a parent.

## Object ownership as an index (TTO pattern)

Transfer to Object (TTO) can replace shared-object collections as an index. Instead of storing entries in a `Table` on a shared object, create "box" objects at derived addresses and transfer items to the box. Queries use `listOwnedObjects` on the box address, and authorized access uses `Receiving<T>`.

The pattern:

1. **Derive a deterministic address** for each logical key (e.g., per-user or per-category).
2. **Transfer items** to that derived address using `transfer::public_transfer(item, derived_addr)`.
3. **Query** from the frontend with `listOwnedObjects(owner=derived_addr)` — paginated and type-filtered, no BCS decoding needed.
4. **Access on-chain** by passing `Receiving<T>` into a function that holds `&mut UID` of the box object, calling `transfer::public_receive` for authorized pickup.

Unlike Ethereum where tokens are automatically added to a recipient's balance, objects sent to another object on Sui are not usable until explicitly received via `transfer::receive` (or `transfer::public_receive` for objects with `key + store`).

### When to use TTO vs Table

| Concern | Table + shared object | TTO + derived addresses |
|---|---|---|
| Write contention | All writes serialize on shared object | Writes to different keys are independent |
| Index maintenance | Manual Table updates | Runtime maintains ownership graph |
| Frontend queries | BCS dynamic field lookups + Table UID resolution | `listOwnedObjects` — paginated, type-filtered |
| On-chain readability | Callable from Move via Table lookup | Off-chain only via RPC |

Use TTO when write contention is the bottleneck and you do not need to read the index from Move. Use Table when on-chain readability matters (other modules need to look up entries in your collection).
