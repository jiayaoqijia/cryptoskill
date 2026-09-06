---
name: move-objects
description: Sui object model — struct declarations, abilities (key/store/copy/drop), object ownership, naming conventions, and dynamic fields.
---

## 1. Structs

All structs must be declared `public`. Ability declarations go **after** the fields:

```move
// ✅
public struct Pool has key {
    id: UID,
    balance_x: Balance<SUI>,
    balance_y: Balance<USDC>,
}

public struct PoolCap has key, store {
    id: UID,
    pool_id: ID,
}

// ❌ Legacy — no public keyword
struct Pool has key {
    id: UID,
}
```

**Object rule**: Any struct with the `key` ability **must** have `id: UID` as its first field. Use `object::new(ctx)` to create UIDs — never reuse or fabricate them.

### Naming conventions

**Capabilities** must be suffixed with `Cap`:

```move
// ✅
public struct AdminCap has key, store { id: UID }

// ❌ Unclear it's a capability
public struct Admin has key, store { id: UID }
```

**No `Potato` suffix** — a struct's lack of abilities already communicates it's a hot potato:

```move
// ✅
public struct Promise {}

// ❌
public struct PromisePotato {}
```

**Events named in past tense** — they describe something that already happened:

```move
// ✅
public struct LiquidityAdded has copy, drop { ... }
public struct FeesCollected has copy, drop { ... }

// ❌
public struct AddLiquidity has copy, drop { ... }
public struct CollectFees has copy, drop { ... }
```

**Dynamic field keys** — use positional structs (no named fields):

```move
// ✅
public struct BalanceKey() has copy, drop, store;

// ⚠️ Acceptable but not canonical
public struct BalanceKey has copy, drop, store {}
```

### Constants naming

Error constants use `EPascalCase`. All other constants use `ALL_CAPS`:

```move
// ✅
const ENotAuthorized: u64 = 0;
const MAX_FEE_BPS: u64 = 10_000;

// ❌
const NOT_AUTHORIZED: u64 = 0;   // error should be EPascalCase
const MaxFeeBps: u64 = 10_000;   // non-error should be ALL_CAPS
```

---

## 2. Object Abilities Cheat Sheet


| Ability | Meaning in Sui                                                                                                 |
| ------- | -------------------------------------------------------------------------------------------------------------- |
| `key`   | Struct is an on-chain object; requires `id: UID` as first field                                                |
| `store` | Can be embedded inside other objects; enables `public_transfer`, `public_share_object`, `public_freeze_object` |
| `copy`  | Value can be duplicated (not valid on objects with `key`)                                                      |
| `drop`  | Value can be silently discarded                                                                                |


**Object ownership model:**

```move
// Transfer to an address (owned object)
transfer::transfer(obj, recipient);             // key only — module-restricted
transfer::public_transfer(obj, recipient);      // key + store — usable anywhere

// Share (accessible by anyone, goes through consensus)
transfer::share_object(obj);                    // key only — module-restricted
transfer::public_share_object(obj);             // key + store

// Freeze (immutable forever)
transfer::freeze_object(obj);                   // key only — module-restricted
transfer::public_freeze_object(obj);            // key + store
```

Only call `transfer`, `share_object`, and `freeze_object` (the non-`public_` variants) inside the module that **defines** that object's type.

**Never** construct an object struct literal outside of its defining module.

---

## 3. Dynamic Fields

Use dynamic fields for extensible storage or when the key set is not known at compile time:

```move
use sui::dynamic_field as df;
use sui::dynamic_object_field as dof;

// Add a dynamic field (value stored inline with parent)
df::add(&mut parent.id, key, value);

// Add a dynamic object field (value is an independent object)
dof::add(&mut parent.id, key, child_obj);

// Access
let val: &MyType = df::borrow(&parent.id, key);
let val: &mut MyType = df::borrow_mut(&mut parent.id, key);

// Remove
let val: MyType = df::remove(&mut parent.id, key);
```
