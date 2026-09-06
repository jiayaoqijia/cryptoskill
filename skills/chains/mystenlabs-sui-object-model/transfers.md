# Transferring and Deleting Objects

The `transfer` module provides eight core functions for moving objects between owners. Object deletion is the inverse operation — explicitly destroying an object and reclaiming its storage.

## Module-restricted (no `store` required)

These can only be called from the module that defines the object's type:

| Function | Effect |
|---|---|
| `transfer::transfer(obj, recipient)` | Transfer to an address |
| `transfer::party_transfer(obj, recipient)` | Transfer to consensus-address-owned (party) state |
| `transfer::share_object(obj)` | Make the object shared |
| `transfer::freeze_object(obj)` | Make the object immutable |

## Public (requires `store`)

These can be called from any module, but the object must have the `store` ability:

| Function | Effect |
|---|---|
| `transfer::public_transfer(obj, recipient)` | Transfer to an address or object ID |
| `transfer::public_party_transfer(obj, recipient)` | Transfer to consensus-address-owned (party) state |
| `transfer::public_share_object(obj)` | Make the object shared |
| `transfer::public_freeze_object(obj)` | Make the object immutable |

## Sharing constraints

`share_object` and `public_share_object` can only be called on objects created within the same transaction. An existing address-owned object cannot be converted to shared — there is no owned-to-shared conversion. Once shared, an object cannot be converted back to address-owned.

## Custom transfer rules

Objects without `store` can only be transferred by their defining module. This lets you enforce preconditions:

```move
public struct LockedItem has key {
    id: UID,
    unlocked: bool,
}

public fun transfer_if_unlocked(item: LockedItem, to: address) {
    assert!(item.unlocked, EItemLocked);
    transfer::transfer(item, to);
}
```

Once you add `store` to an object, you permanently give up the ability to enforce custom transfer rules. Anyone can call `public_transfer` on it.

## Transfer to object (Receiving)

Objects can be transferred to other object IDs, not just addresses. Sui treats 32-byte addresses and 32-byte object IDs identically for transfer purposes.

```move
// Transfer object `sword` to the object with ID 0x0B (e.g., a character)
transfer::public_transfer(sword, @0x0B);
```

The receiving object must explicitly accept sent objects using the `Receiving<T>` type. This differs from Ethereum, where tokens are automatically added to a recipient's balance — on Sui, the parent must opt in to receiving.

> **Note:** Transfer-to-object is not supported for party objects whose owning address corresponds to an object ID. You cannot use `Receiving<T>` to receive objects sent to a party object.

```move
public fun accept_item<T: key + store>(
    parent: &mut UID,
    sent: Receiving<T>,
): T {
    transfer::public_receive(parent, sent)
}
```

Key rules:

- `transfer::receive(parent_uid, receiving)` works for objects defined in the current module (no `store` required on child).
- `transfer::public_receive(parent_uid, receiving)` works for any object with `key + store`.
- Requires mutable access to the parent's `UID`, which enforces access control.
- `Receiving<T>` has only `drop`, so you can choose to receive some, none, or all objects sent to a parent.

## Deleting objects

Objects without `drop` must be explicitly unpacked. The UID must be deleted with `object::delete()`:

```move
public struct Character has key {
    id: UID,
    name: String,
}

public fun destroy_character(character: Character) {
    let Character { id, name: _ } = character;
    id.delete();
}
```

For objects with complex fields (like `LinkedTable`), you must handle each field: drop it if it has `drop`, destroy it if it has a `destroy_empty` method, or recursively unpack it.

A shared object can be destroyed if a function takes it by value and deletes it within the same transaction.

**Deleting objects with dynamic fields defined on them renders those fields permanently inaccessible.** Always remove all dynamic fields before deleting the parent.
