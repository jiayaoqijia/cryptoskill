---
name: move-patterns
description: Move design patterns — events, error handling, one-time witness (OTW), capability pattern, and pure functions/composability.
---

## 1. Events

Emit events for all state-changing operations that clients need to observe:

```move
use sui::event;

public struct LiquidityAdded has copy, drop {
    pool_id: ID,
    amount_x: u64,
    amount_y: u64,
    lp_minted: u64,
}

// Inside function:
event::emit(LiquidityAdded {
    pool_id: object::id(pool),
    amount_x,
    amount_y,
    lp_minted,
});
```

---

## 2. Error Handling

Error constants use `EPascalCase` and `u64` values:

```move
const EInsufficientLiquidity: u64 = 0;
const EZeroAmount: u64 = 1;

assert!(amount > 0, EZeroAmount);
```

### Clever errors

Annotating a constant with `#[error]` allows it to carry a human-readable message. The value can be any valid constant type — `vector<u8>` is most common for string messages:

```move
#[error]
const EInsufficientLiquidity: vector<u8> = b"Insufficient liquidity in pool";

assert!(reserves > 0, EInsufficientLiquidity);
abort EInsufficientLiquidity
```

At runtime, the Sui CLI and GraphQL server automatically decode these into a readable message:

```
Error from '0x2::amm::swap' (line 42), abort 'EInsufficientLiquidity': "Insufficient liquidity in pool"
```

**Gotcha**: clever error abort codes encode the source line number, so their `u64` value can change if the file is reformatted or lines shift. Don't hardcode clever error abort codes in tests or off-chain tooling — match by constant name instead.

`**assert!` without an abort code** is also valid and auto-derives a clever abort code from the source line:

```move
// ✅ Valid — line number is embedded automatically
assert!(amount > 0);
```

This is fine for internal invariants where the line number alone is enough context.

---

## 3. One-Time Witness (OTW) Pattern

Use the OTW pattern for modules that need a unique, uncopyable proof-of-publication (e.g., coin types, publisher objects):

```move
public struct MY_MODULE has drop {}

fun init(otw: MY_MODULE, ctx: &mut TxContext) {
    // The OTW name must exactly match the module name in ALL_CAPS
    let publisher = package::claim(otw, ctx);
    transfer::public_transfer(publisher, ctx.sender());
}
```

---

## 4. Capability Pattern

Use capability objects to gate privileged functions instead of checking `ctx.sender()`. This is more composable and testable — the capability can be held by a contract, not just a wallet:

```move
// ✅ Capability-gated
public struct AdminCap has key, store { id: UID }

public fun set_fee(_: &AdminCap, pool: &mut Pool, new_fee: u64) {
    pool.fee_bps = new_fee;
}

// ❌ Sender check — not composable with other contracts
public fun set_fee(pool: &mut Pool, ctx: &TxContext) {
    assert!(ctx.sender() == pool.admin, ENotAdmin);
}
```

Note the parameter order: the object (`pool`) comes before the primitive (`new_fee`), and `_: &AdminCap` follows the objects-then-capabilities ordering from the syntax skill's §3 Visibility.

---

## 5. Pure Functions and Composability

Keep core logic functions **pure** — they take objects by reference/value and return values. Do not call `transfer::transfer` to deliver results to the caller:

```move
// ✅ Pure — composable with other protocols
public fun swap<X, Y>(
    pool: &mut Pool<X, Y>,
    coin_in: Coin<X>,
    ctx: &mut TxContext,
): Coin<Y> {
    // ... swap logic
}

// ❌ Transfer inside core logic breaks composability
public fun swap<X, Y>(pool: &mut Pool<X, Y>, coin_in: Coin<X>, ctx: &mut TxContext) {
    let coin_out = /* ... */;
    transfer::public_transfer(coin_out, ctx.sender()); // ❌
}
```

Internal transfers are acceptable when they serve the function's own mechanics (e.g., burning tokens to `@0x0`, sharing a newly created object). The key rule is: **don't transfer the caller's results** — return them instead so the caller can compose.

Return excess coins even if their value is zero — let the caller decide what to do with them.
