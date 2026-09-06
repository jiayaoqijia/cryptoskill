---
name: move-stdlib
description: Common Sui Move standard library patterns — strings, Coin/Balance, Option, addresses, UID, TxContext, vectors, and struct unpacking.
---

## 1. Common Standard Library Patterns

```move
// Strings — use method syntax, don't import utf8
let s: String = b"hello".to_string();
let ascii: ascii::String = b"hello".to_ascii_string();

// Coin and Balance
use sui::coin::{Self, Coin};
use sui::balance::{Self, Balance};

let balance: Balance<SUI> = coin.into_balance();
let coin: Coin<SUI> = balance.into_coin(ctx);  // ✅ method syntax
let amount: u64 = coin.value();

// Split a payment
let exact = payment.split(amount, ctx);        // ✅
let exact = payment.balance_mut().split(amount); // ✅ avoids ctx

// Consuming values without `drop` — the @0x0 burn pattern
//
// Move's linear type system requires every non-`drop` value to be
// explicitly consumed. The `_` prefix only suppresses warnings for values
// that *do* have `drop` — it won't help for Balance<T>, Coin<T>, or your
// own structs that lack `drop`.
//
// To permanently destroy any `key + store` object, transfer it to @0x0
// (an address no one controls, equivalent to Solidity's address(0)):
transfer::public_transfer(my_obj, @0x0);       // ✅ permanent burn
//
// Balance<T> has neither `drop` nor `key`, so it cannot be transferred
// directly, and `balance::destroy_zero` only works on empty balances.
// Wrap it in a Coin first:
//
//   let _locked = supply.increase_supply(MINIMUM_LIQUIDITY); // ❌ compile error
//
let locked = supply.increase_supply(MINIMUM_LIQUIDITY).into_coin(ctx);
transfer::public_transfer(locked, @0x0);       // ✅ burns the minimum liquidity
//
// Hot potatoes (structs with no abilities at all) cannot use this pattern —
// they must be destructured and each field consumed individually.

// Option
let opt: Option<u64> = option::some(42);
let val = opt.destroy_or!(default_value);      // ✅ macro form
let val = opt.borrow();

// Address and IDs
let id: ID = object::id(&my_obj);
let addr: address = id.to_address();

// UID deletion
id.delete();                                   // ✅
// object::delete(id);                         // ❌ verbose

// TxContext sender
ctx.sender()                                   // ✅
// tx_context::sender(ctx)                     // ❌ verbose

// Vector literals and index syntax
let mut v = vector[1, 2, 3];                   // ✅ literal
let first = v[0];                              // ✅ index syntax
assert!(v.length() == 3);                      // ✅ method syntax
// let mut v = vector::empty();               // ❌ verbose
// vector::push_back(&mut v, 1);              // ❌ verbose

// Struct unpack — use .. to ignore fields you don't need
let MyStruct { id, .. } = value;               // ✅
// let MyStruct { id, field_a: _, field_b: _ } = value; // ❌ verbose
```
