---
name: move-unit-testing
description: Use when writing unit tests for Move smart contracts on Sui. Applies to test function naming, assertions, test attributes, context usage, and cleanup patterns. Use whenever user asks to write tests, add tests, or test a Move module.
---

# move-unit-testing

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

## Overview

AI agents consistently use outdated or suboptimal patterns when writing Move unit tests. This skill covers the correct testing conventions from the official Sui Move code quality checklist and testing documentation.

All patterns sourced from https://move-book.com/guides/code-quality-checklist and https://move-book.com/testing/

## No `test_` Prefix in Test Modules

Test functions inside `_tests` modules should NOT be prefixed with `test_`. The module name already indicates these are tests. Use descriptive names that read as statements.

```move
// WRONG — redundant prefix
module my_package::my_module_tests;

#[test]
fun test_create_pool() { /* ... */ }

#[test]
fun test_swap_fails_on_zero() { /* ... */ }

// CORRECT — descriptive statement names
module my_package::my_module_tests;

#[test]
fun create_pool_with_initial_liquidity() { /* ... */ }

#[test]
fun swap_aborts_on_zero_input() { /* ... */ }
```

## Use `assert_eq!` Instead of `assert!` for Comparisons

`assert_eq!` displays both values on failure, making debugging much easier. Never use `assert!(x == y)` or `assert!(x == y, 0)` for equality checks.

```move
// WRONG — no diagnostic info on failure
assert!(result == 100);
assert!(result == expected_value, 0);

// CORRECT — shows both values on failure
use std::unit_test::assert_eq;

assert_eq!(result, 100);
assert_eq!(result, expected_value);
```

Use plain `assert!` only for boolean conditions where there's nothing to compare:

```move
// assert! is fine for boolean checks
assert!(is_valid);
assert!(vec.length() > 0);
```

## No Abort Codes in Test `assert!`

Do not pass numeric abort codes to `assert!` in tests. They can accidentally match application error codes and confuse debugging.

```move
// WRONG — numeric code may collide with app errors
assert!(is_success, 0);
assert!(balance > 0, 1);

// CORRECT — no abort code
assert!(is_success);
assert!(balance > 0);
```

## Merge `#[test]` and `#[expected_failure]` on One Line

```move
// WRONG — separate attributes
#[test]
#[expected_failure(abort_code = EInvalidInput, location = my_app)]
fun invalid_input_aborts() { /* ... */ }

// CORRECT — merged on one line
#[test, expected_failure(abort_code = EInvalidInput, location = my_app)]
fun invalid_input_aborts() { /* ... */ }
```

## `expected_failure` with `location` for cross-module aborts

When the abort happens in a different module than the test, you **must** specify `location`. Without it, the test framework expects the abort to originate in the test module and the test fails.

```move
// Test module: my_package::app_tests
// Abort happens in: my_package::app

const ENotAuthorized: u64 = 0;  // mirror the constant value from app module

// WRONG — no location; test fails because abort comes from `app`, not `app_tests`
#[test, expected_failure(abort_code = ENotAuthorized)]
fun unauthorized_call_aborts() { /* ... */ }

// CORRECT — location points to the module where the abort originates
#[test, expected_failure(abort_code = ENotAuthorized, location = app)]
fun unauthorized_call_aborts() { /* ... */ }
```

The `location` value is just the module name (e.g., `app`), not the fully qualified path (`my_package::app`). Using the fully qualified form causes a compile error: "Unexpected module member identifier."

## Skip Cleanup in `expected_failure` Tests

Tests annotated with `expected_failure` will abort — any cleanup code after the abort point is dead code. Don't call `.end()` or destroy objects after the expected abort.

```move
// WRONG — cleanup after abort is dead code
#[test, expected_failure(abort_code = my_app::EInsufficientBalance)]
fun withdraw_more_than_balance_aborts() {
    let mut scenario = test_scenario::begin(@0xA);
    my_app::withdraw(1000, scenario.ctx());
    scenario.end(); // never reached
}

// CORRECT — let it abort naturally
#[test, expected_failure(abort_code = my_app::EInsufficientBalance)]
fun withdraw_more_than_balance_aborts() {
    let mut scenario = test_scenario::begin(@0xA);
    my_app::withdraw(1000, scenario.ctx());
    // no cleanup needed — test aborts above
}
```

## Use `tx_context::dummy()` for Simple Tests

If a test only needs a `TxContext` and doesn't need multi-transaction simulation, use `tx_context::dummy()` instead of a full `test_scenario`. Reserve `test_scenario` for tests that actually need to simulate multiple transactions, shared objects, or transfers between addresses.

```move
// WRONG — unnecessary overhead for a simple test
#[test]
fun mint_returns_correct_value() {
    let mut scenario = test_scenario::begin(@0xA);
    let item = app::create_item(100, scenario.ctx());
    assert_eq!(item.value(), 100);
    std::unit_test::destroy(item);
    scenario.end();
}

// CORRECT — dummy context is sufficient
#[test]
fun mint_returns_correct_value() {
    let ctx = &mut tx_context::dummy();
    let item = app::create_item(100, ctx);
    assert_eq!(item.value(), 100);
    std::unit_test::destroy(item);
}
```

**When to use `test_scenario`:** shared objects, multi-transaction flows, testing transfers between addresses, testing `init` functions, epoch/time manipulation.

**When to use `tx_context::dummy()`:** pure function tests, single-operation tests, anything that just needs a ctx to create objects.

## `test_scenario` for Multi-Transaction and Authorization Tests

Use `test_scenario` when you need to simulate multiple transactions, different senders, shared objects, or test `init` functions. The core API:

| Function | Purpose |
|---|---|
| `test_scenario::begin(@addr)` | Start a scenario with `@addr` as the first sender |
| `scenario.next_tx(@addr)` | Advance to a new transaction with `@addr` as sender |
| `scenario.take_from_sender<T>()` | Take an owned object sent to the current sender |
| `scenario.return_to_sender(obj)` | Return an owned object to the current sender |
| `scenario.take_shared<T>()` | Take a shared object by type |
| `test_scenario::return_shared(obj)` | Return a shared object |
| `scenario.has_most_recent_for_sender<T>()` | Check if sender has an object of type `T` |
| `scenario.end()` | Finalize the scenario (must be called in non-aborting tests) |

### Success test — create and verify

```move
#[test]
fun owner_can_update_item() {
    let owner = @0xA;
    let mut scenario = test_scenario::begin(owner);

    // Tx 1: create an item (transferred to owner inside create_item)
    app::create_item(b"sword".to_string(), scenario.ctx());

    // Tx 2: owner takes the item and updates it
    scenario.next_tx(owner);
    let mut item = scenario.take_from_sender<Item>();
    app::set_name(&mut item, b"great sword".to_string());
    assert_eq!(app::name(&item), b"great sword".to_string());
    scenario.return_to_sender(item);

    scenario.end();
}
```

### Unauthorized caller test

```move
#[test, expected_failure(abort_code = app::ENotOwner, location = app)]
fun non_owner_cannot_update_item() {
    let owner = @0xA;
    let attacker = @0xB;
    let mut scenario = test_scenario::begin(owner);

    // Tx 1: owner creates a shared item
    app::create_shared_item(b"shield".to_string(), scenario.ctx());

    // Tx 2: attacker tries to update it — should abort
    scenario.next_tx(attacker);
    let mut item = scenario.take_shared<Item>();
    app::admin_update(&mut item, b"hacked".to_string(), scenario.ctx());
    // no cleanup — test aborts above
}
```

### Shared object test

```move
#[test]
fun shared_counter_increments() {
    let mut scenario = test_scenario::begin(@0xA);

    // Tx 1: create and share
    app::create_counter(scenario.ctx());

    // Tx 2: anyone can increment
    scenario.next_tx(@0xB);
    let mut counter = scenario.take_shared<Counter>();
    app::increment(&mut counter);
    assert_eq!(app::value(&counter), 1);
    test_scenario::return_shared(counter);

    scenario.end();
}
```

### Testing `init` functions

```move
#[test]
fun init_creates_admin_cap() {
    let mut scenario = test_scenario::begin(@0xA);

    // init is called automatically for the first tx in begin()
    // if the module has an init function — but in tests you call it explicitly:
    app::init_for_testing(scenario.ctx());

    scenario.next_tx(@0xA);
    assert!(scenario.has_most_recent_for_sender<AdminCap>());

    scenario.end();
}
```

Note: modules typically expose a `init_for_testing` or `test_init` helper since `init` itself is not directly callable in tests. Use `#[test_only]` to gate these helpers.

## Use `std::unit_test::destroy` for Cleanup

Use `std::unit_test::destroy` to clean up test objects. The old `sui::test_utils::destroy` is **deprecated**.

```move
// WRONG — deprecated
use sui::test_utils::destroy;

// WRONG — custom cleanup functions
nft.destroy_for_testing();

// CORRECT — use std::unit_test::destroy
use std::unit_test::destroy;

destroy(nft);
destroy(app);
```

## Quick Reference

| Pattern | Correct | Common Mistake |
|---------|---------|----------------|
| Test function naming | `create_pool_succeeds()` | `test_create_pool()` |
| Equality assertions | `assert_eq!(x, 100)` | `assert!(x == 100, 0)` |
| Boolean assertions | `assert!(is_valid)` | `assert!(is_valid, 0)` |
| Test attributes | `#[test, expected_failure(...)]` | Separate `#[test]` and `#[expected_failure]` |
| Expected failure cleanup | Let it abort, no cleanup | Calling `.end()` after abort |
| Simple test context | `tx_context::dummy()` | Full `test_scenario` for simple tests |
| Object cleanup | `test_utils::destroy(obj)` | `obj.destroy_for_testing()` |
