---
name: move-syntax
description: Move language syntax — module layout, imports, mutability, visibility, method syntax, enums, macros, and comments.
---

## 1. Module Layout

Use the new single-line module declaration without braces:

```move
// ✅
module my_package::my_module;

// ❌ Legacy — do not use
module my_package::my_module {
    ...
}
```

Standard section order within a module:

1. `use` imports
2. Constants (`const`)
3. Structs / Enums
4. `fun init` (if needed)
5. Public functions
6. `public(package)` functions
7. Private functions
8. Test module (`#[test_only]`)

Use `=== Section Title ===` comments to delimit sections for readability.

### `use` import rules

Don't use a lone `{Self}` — just import the module directly:

```move
// ✅
use my_package::my_module;

// ❌ Redundant braces
use my_package::my_module::{Self};
```

When importing both the module and members, group them with `Self`:

```move
// ✅
use sui::coin::{Self, Coin};

// ❌ Separate imports
use sui::coin;
use sui::coin::Coin;
```

---

## 2. Mutability — `mut` is Required

All variables that are reassigned or mutably borrowed must be declared `let mut`:

```move
// ✅
let mut pool = Pool { id: object::new(ctx), ... };
let mut balance = balance::zero<SUI>();

// ❌ Legacy
let pool = Pool { id: object::new(ctx), ... };
```

Function parameters that are mutably borrowed must also be `mut`:

```move
public fun deposit(mut pool: Pool, coin: Coin<SUI>): Pool { ... }
```

---

## 3. Visibility


| Keyword           | Scope                                          |
| ----------------- | ---------------------------------------------- |
| `public`          | Callable from any module                       |
| `public(package)` | Callable only within the same package          |
| *(none)*          | Private — callable only within the same module |


`public(friend)` and `friend` declarations are **deprecated**. Use `public(package)` instead.

```move
// ✅
public(package) fun internal_logic(pool: &mut Pool) { ... }

// ❌ Deprecated
friend my_package::other_module;
public(friend) fun internal_logic(pool: &mut Pool) { ... }
```

**Never use `public entry`** — use one or the other. `public` functions are composable in PTBs and return values; `entry` functions are transaction endpoints only and cannot return values:

```move
// ✅ Composable — can be chained in PTBs
public fun mint(ctx: &mut TxContext): NFT { ... }

// ✅ Transaction endpoint — no return value needed
entry fun mint_and_transfer(recipient: address, ctx: &mut TxContext) { ... }

// ❌ Redundant combination — avoid
public entry fun mint(ctx: &mut TxContext): NFT { ... }
```

### Function parameter ordering

Always order parameters: mutable objects → immutable objects → capabilities → primitive types → `&Clock` → `&mut TxContext`:

```move
// ✅
public fun call(
    app: &mut App,
    config: &Config,
    cap: &AdminCap,
    amount: u64,
    is_active: bool,
    clock: &Clock,
    ctx: &mut TxContext,
) { }

// ❌ Wrong order
public fun call(
    amount: u64,
    app: &mut App,
    cap: &AdminCap,
    config: &Config,
    ctx: &mut TxContext,
) { }
```

### Getter naming

Name getters after the field. Do not use a `get_` prefix:

```move
// ✅
public fun fee_bps(pool: &Pool): u64 { pool.fee_bps }
public fun fee_bps_mut(pool: &mut Pool): &mut u64 { &mut pool.fee_bps }

// ❌
public fun get_fee_bps(pool: &Pool): u64 { pool.fee_bps }
```

---

## 4. Method Syntax

Functions whose first argument matches a type are automatically callable as methods:

```move
// Given:
public fun value(coin: &Coin<SUI>): u64 { coin.value() }

// Both are valid, prefer the method form:
let v = coin.value();       // ✅ method syntax — prefer this
let v = coin::value(&coin); // ✅ also valid, but more verbose
```

Use method syntax wherever it improves readability. Declare `use fun` aliases for functions defined outside the owning module:

```move
use fun my_module::pool_value as Pool.value;
```

---

## 5. Enums

Use enums for types with multiple variants. Enums **cannot** have the `key` ability (they cannot be top-level objects), but they can be stored inside objects:

```move
public enum OrderStatus has copy, drop, store {
    Pending,
    Filled { amount: u64 },
    Cancelled,
}
```

Pattern match with `match`:

```move
match (order.status) {
    OrderStatus::Pending => { ... },
    OrderStatus::Filled { amount } => { /* use amount */ },
    OrderStatus::Cancelled => { ... },
}
```

---

## 6. Macros

Use macro functions for higher-order patterns instead of manual loops.

### Vector macros

```move
// Do something N times
32u8.do!(|_| do_action());

// Build a new vector from an index range
let v = vector::tabulate!(32, |i| i);

// Iterate by immutable reference
vec.do_ref!(|e| process(e));

// Iterate by mutable reference
vec.do_mut!(|e| *e = *e + 1);

// Consume vector, calling a function on each element
vec.destroy!(|e| handle(e));

// Fold into a single value
let sum = vec.fold!(0u64, |acc, x| acc + x);

// Filter (requires T: drop)
let big = vec.filter!(|x| *x > 100);
```

All of these replace verbose manual `while` loops. Use them whenever you iterate over a vector.

### Option macros

```move
// Execute a function if Some, then drop
opt.do!(|value| process(value));

// Unwrap with a default (or abort)
let value = opt.destroy_or!(default);
let value = opt.destroy_or!(abort ECannotBeEmpty);
```

These replace verbose `if (opt.is_some())` / `destroy_some()` patterns:

```move
// ❌ Verbose
if (opt.is_some()) {
    let inner = opt.destroy_some();
    process(inner);
};

// ✅
opt.do!(|inner| process(inner));
```

---

## 7. Comments

Use `///` for doc comments. JavaDoc-style `/** */` is not supported in Move:

```move
/// Returns the current fee in basis points.
public fun fee_bps(pool: &Pool): u64 { pool.fee_bps }

// ❌ Not supported
/** Returns the current fee in basis points. */
public fun fee_bps(pool: &Pool): u64 { pool.fee_bps }
```

Use regular `//` comments to explain non-obvious logic, potential edge cases, and TODOs:

```move
// Note: can underflow if reserve is smaller than minimum_liquidity.
// TODO: add assert! guard before production use.
let lp_supply = math::sqrt(reserve_x * reserve_y);
```
