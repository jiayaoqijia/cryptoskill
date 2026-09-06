---
name: move-setup
description: Move package setup (Move.toml, edition, dependencies), building, testing, and common pitfalls from other Move dialects.
---

## 1. Package Setup

Always use the Move 2024 edition (`edition = "2024"` in Move.toml). The `name` in `[package]` defines the package's address name and **must match** what your Move code uses (e.g., `module my_package::m` requires `name = "my_package"`):

```toml
[package]
name = "my_package"
edition = "2024"
```

**Implicit framework dependencies (Sui 1.45+)** — do not list `Sui`, `MoveStdlib`, `Bridge`, or `SuiSystem` in `[dependencies]`. They are implicit:

```toml
# ✅ Sui 1.45+
[dependencies]
# no framework entries needed

# ❌ Outdated
[dependencies]
Sui = { git = "...", subdir = "crates/sui-framework/packages/sui-framework", rev = "..." }
```

**No `[addresses]` section (Sui CLI 1.63+)** — named addresses are derived from the `[package]` name and `[dependencies]` keys. Do not add an `[addresses]` or `[dev-addresses]` section.

Run `sui move build` after any significant change to verify the code compiles before proceeding.

---

## 2. Building and Testing

Always verify code compiles and tests pass using the Sui CLI:

```bash
# Build
sui move build

# Run all tests
sui move test

# Run a specific test by name
sui move test swap_exact_input
```

### Test conventions

**Naming** — do not prefix test functions with `test_`. The `#[test]` attribute already signals intent:

```move
// ✅
#[test] fun create_pool() { }
#[test] fun swap_returns_correct_amount() { }

// ❌
#[test] fun test_create_pool() { }
```

**Merge attributes** — combine `#[test]` and `#[expected_failure]` on one line:

```move
// ✅
#[test, expected_failure(abort_code = EInsufficientLiquidity)]
fun swap_with_zero_input() { ... }

// ❌
#[test]
#[expected_failure(abort_code = EInsufficientLiquidity)]
fun swap_with_zero_input() { ... }
```

**Don't clean up in `expected_failure` tests** — let them abort naturally, don't add `scenario.end()` or other teardown:

```move
// ✅
#[test, expected_failure(abort_code = EInsufficientLiquidity)]
fun swap_with_zero_input() {
    let mut ctx = tx_context::dummy();
    let pool = create_pool(&mut ctx);
    pool.swap(coin::zero(&mut ctx)); // aborts here — done
}

// ❌ — don't clean up after expected failure
#[test, expected_failure(abort_code = EInsufficientLiquidity)]
fun swap_with_zero_input() {
    let mut scenario = test_scenario::begin(@0xA);
    // ... test body ...
    scenario.end(); // unnecessary, misleading
}
```

**Use `tx_context::dummy()` for simple tests** — only reach for `test_scenario` when you genuinely need multi-transaction or multi-sender behaviour:

```move
// ✅ Simple test — no scenario needed
#[test]
fun create_pool() {
    let mut ctx = tx_context::dummy();
    let pool = new_pool(&mut ctx);
    assert_eq!(pool.fee_bps(), 30);
    sui::test_utils::destroy(pool);
}

// ✅ Multi-sender test — scenario is appropriate
#[test]
fun only_admin_can_set_fee() {
    let mut scenario = test_scenario::begin(@admin);
    // ...
    scenario.end();
}
```

**Assertions** — prefer `assert_eq!` over `assert!` for value comparisons (shows both sides on failure), and never pass abort codes to `assert!`:

```move
// ✅
assert_eq!(pool.fee_bps(), 30);
assert!(pool.is_active());

// ❌
assert!(pool.fee_bps() == 30);   // doesn't show the actual value on failure
assert!(pool.is_active(), 0);    // abort code conflicts with app error codes
```

**Destroying objects in tests** — use `sui::test_utils::destroy`, never write custom `destroy_for_testing` functions:

```move
// ✅
use sui::test_utils::destroy;
destroy(pool);

// ❌
pool.destroy_for_testing();
```

---

## 3. What Move on Sui is NOT


| Pattern                                               | Source            | Do NOT use on Sui                       |
| ----------------------------------------------------- | ----------------- | --------------------------------------- |
| `acquires`, `move_to`, `move_from`, `borrow_global`   | Aptos / Core Move | Sui has no global storage               |
| `signer` type                                         | Aptos / Core Move | Use `&mut TxContext` and `ctx.sender()` |
| `Script` functions                                    | Aptos             | Use `entry` functions instead           |
| `public(friend)`                                      | Legacy Move       | Use `public(package)`                   |
| Struct without `public` keyword                       | Legacy Move       | All structs must be `public`            |
| `let x = ...` for mutable vars                        | Legacy Move       | Use `let mut x = ...`                   |
| `use` inside function bodies for module-level imports | Style issue       | Put `use` at the top of the module      |
| `&signer`                                             | Rust / Aptos      | Does not exist on Sui                   |
