# Dynamic Fields and Collections

Dynamic fields attach key-value data to an object at runtime, beyond the fields declared in the struct. Collections are higher-level types built on dynamic fields for common storage patterns.

## Dynamic field types

| Type | Module | Value requirement | External visibility |
|---|---|---|---|
| Dynamic field | `sui::dynamic_field` | Any type with `store` | Wrapped: not visible to explorers or wallets by ID |
| Dynamic object field | `sui::dynamic_object_field` | Must be an object (`key + store`) | Child retains its own ID, visible to explorers and wallets |

**When to use dynamic object field:** When the stored value is an object that should remain independently queryable (for example, an NFT inside an inventory that you want to look up by its ID). Use this when you need "my player NFT needs an inventory that supports any arbitrary Sui object."

**When to use dynamic field:** When the stored value is a plain type (like `u64`, `String`, or a non-object struct), or when you do not need the child to be independently addressable.

**Constraint:** Shared objects cannot be stored as dynamic fields — attempting to do so aborts with `ESharedObjectOperationNotSupported`.

## Field naming

Dynamic field names accept any value with `copy`, `drop`, and `store` abilities. This includes primitives (`u64`, `address`, `String`) and custom structs with those abilities. This is more flexible than regular struct fields, which require Move identifiers.

## Core API

Both modules share the same API shape:

```move
// Add a field
dynamic_field::add(&mut parent.id, name, value);

// Read a field (immutable)
let val: &V = dynamic_field::borrow(&parent.id, name);

// Read a field (mutable)
let val: &mut V = dynamic_field::borrow_mut(&mut parent.id, name);

// Remove a field (returns the value)
let val: V = dynamic_field::remove(&mut parent.id, name);

// Check existence
let exists: bool = dynamic_field::exists_(&parent.id, name);
```

Use plain function calls (`dynamic_field::add`, `table::add`, etc.) instead of receiver syntax for dynamic field and collection operations.

Replace `dynamic_field` with `dynamic_object_field` for object fields. The API is identical.

### Complete example: heterogeneous inventory with dynamic object fields

```move
module test_project::inventory;

use std::string::String;
use sui::dynamic_object_field;

/// An inventory that can hold any object type as a named slot.
public struct Inventory has key, store {
    id: UID,
}

/// Create an empty inventory.
public fun new(ctx: &mut TxContext): Inventory {
    Inventory { id: object::new(ctx) }
}

/// Add an item to a named slot. T must be an object (key + store).
public fun add_item<T: key + store>(
    inventory: &mut Inventory,
    name: String,
    item: T,
) {
    dynamic_object_field::add(&mut inventory.id, name, item);
}

/// Remove an item from a named slot, returning it to the caller.
public fun remove_item<T: key + store>(
    inventory: &mut Inventory,
    name: String,
): T {
    dynamic_object_field::remove(&mut inventory.id, name)
}

/// Check whether a slot is occupied.
public fun has_item<T: key + store>(inventory: &Inventory, name: String): bool {
    dynamic_object_field::exists_with_type<String, T>(&inventory.id, name)
}
```

Accessing a nonexistent field aborts the transaction — use `exists_` to check first when the field's presence is uncertain. Adding a field with a name that already exists (same name and type) also aborts.

> **Important:** Accessing a nonexistent dynamic field (via `borrow`, `borrow_mut`, or `remove`) aborts the transaction. Always use `exists_` to check before accessing a dynamic field whose presence is uncertain.

**Warning:** Deleting an object that still has dynamic fields attached renders those fields permanently inaccessible (orphaned storage). Always remove all dynamic fields before destroying the parent object.

## Collections

### Table and ObjectTable

`Table<K, V>` is a homogeneous key-value map backed by dynamic fields. O(1) lookup. The default choice for large or unbounded collections.

`ObjectTable<K, V>` is the same but values must be objects (`key + store`). Child objects keep their own IDs and are visible to explorers.

**Each Table entry is a separate dynamic field and therefore a separate storage operation — gas cost scales linearly with the number of entries accessed per transaction.**

```move
let mut inventory = table::new<String, Sword>(ctx);
table::add(&mut inventory, b"excalibur".to_string(), sword);
let sword_ref: &Sword = table::borrow(&inventory, b"excalibur".to_string());
```

### Bag and ObjectBag

`Bag` is a heterogeneous map: keys and values can be different types across entries. Use when you need to store mixed types under one parent (for example, an inventory that holds Swords, Shields, and Potions all in one collection).

`ObjectBag` is the same but values must be objects.

```move
let mut bag = bag::new(ctx);
bag::add(&mut bag, b"weapon".to_string(), sword);   // Sword type
bag::add(&mut bag, b"shield".to_string(), shield);   // Shield type
```

### VecMap and VecSet

`VecMap<K, V>` is a vector-backed map with O(n) lookup. Stored inline on the object (no dynamic fields). Cheaper per entry but does not scale past ~100 entries. Use for small, bounded collections where you know the maximum size.

`VecSet<K>` is a vector-backed set. Same tradeoffs.

### LinkedTable

`LinkedTable<K, V>` is a doubly-linked map that preserves insertion order and supports ordered iteration. Use when you need to traverse entries in order or pop from front/back.

### Collection cleanup

Collections lack the `drop` ability. You must explicitly clean them up:

- `destroy_empty()`: Succeeds only if the collection is empty. Works on all collection types.
- `drop()`: Drops a Table where all values have `drop`. Does not work on Bags, ObjectTables, or ObjectBags.

### Choosing a collection

| Need | Use |
|---|---|
| Large or unbounded homogeneous map | `Table<K, V>` |
| Large map where values are objects that should stay queryable | `ObjectTable<K, V>` |
| Heterogeneous storage (mixed types) | `Bag` or `ObjectBag` |
| Small bounded map (under ~100 entries) | `VecMap<K, V>` |
| Small unique-value set | `VecSet<K>` |
| Ordered iteration or pop from front/back | `LinkedTable<K, V>` |
| Inventory holding arbitrary Sui objects | `ObjectBag` (heterogeneous objects) or `ObjectTable` (homogeneous objects) |

## Reading collection entries from a frontend

`Table<K, V>`, `ObjectTable`, `Bag`, and `ObjectBag` each have their own `UID`. Entries are stored as dynamic fields under the **collection's own UID**, not the parent struct's UID. When querying entries from a frontend, you must resolve the collection's ID first:

```typescript
// Step 1: Read the parent object to get the Table's ID
const registry = await client.core.getObject({
  objectId: registryId,
  include: { json: true },
});
const tableId = registry.json.attestations; // Table's UID, NOT registryId

// Step 2: Use the Table's ID for dynamic field lookup
const entry = await client.core.getDynamicField({
  parentId: tableId, // collection ID, not parent object ID
  name: { type: "address", value: userAddr },
});
```

A common mistake is passing the parent struct's ID directly to `getDynamicField`. This returns nothing because the entries live under the collection's own object, not the struct that contains it.

## System limits

- Maximum single object size: 256 KB
- Maximum objects per transaction: 2,048
- Maximum transaction size: 128 KB
- Maximum dynamic fields per object: No hard limit, but each field is a separate storage operation

These limits are defined in the `ProtocolConfig` and can vary per network configuration.
