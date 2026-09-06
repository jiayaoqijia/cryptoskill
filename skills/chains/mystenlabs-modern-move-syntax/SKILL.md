---
name: modern-move-syntax
description: Use when writing Move code on Sui to ensure 2024 edition syntax is used. Applies to method calls, string literals, vector operations, option handling, loops, and struct unpacking. Use whenever writing Move code to avoid legacy function-call syntax patterns.
---

# modern-move-syntax

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

## Overview

The Move 2024 edition introduced method syntax and several convenience features. AI agents frequently fall back to pre-2024 function-call patterns from training data. This skill covers every modern syntax pattern.

All patterns sourced from https://move-book.com/guides/code-quality-checklist

## Method Syntax for Common Operations

Use method-call syntax (dot notation) instead of module function calls.

### Coin and Balance

```move
// WRONG — legacy function-call syntax
let value = coin::value(&payment);
let balance = coin::into_balance(payment);
balance::join(&mut pool.reserve, balance);
let coin = coin::from_balance(balance::split(&mut pool.reserve, amount), ctx);

// CORRECT — method syntax
let value = payment.value();
let balance = payment.into_balance();
pool.reserve.join(balance);
let coin = coin::from_balance(pool.reserve.split(amount), ctx);

// BEST — chained method calls
let balance = payment.split(amount, ctx).into_balance();
```

### TxContext

```move
// WRONG
tx_context::sender(ctx)

// CORRECT
ctx.sender()
```

### UID and Object

```move
// WRONG
object::delete(id);

// CORRECT
id.delete();
```

## String Literals

Use quoted string literals directly, not `std::string::utf8()` or byte-string conversion.

```move
// WRONG
use std::string;
let s = string::utf8(b"hello");

// ALSO WRONG — unnecessary conversion
let s = b"hello".to_string();

// CORRECT — direct string literals (2024 edition)
let s = "hello";                    // String (UTF-8)
let ascii = "hello";                // also works for ASCII strings
let s = b"hello".to_string();      // still valid but prefer quoted form
let ascii = b"hello".to_ascii_string(); // explicit ASCII when needed
```

## Vector Literals and Methods

Use vector literal syntax and method calls instead of module functions.

```move
// WRONG
let mut v = vector::empty();
vector::push_back(&mut v, 10);
let first = vector::borrow(&v, 0);
let len = vector::length(&v);

// CORRECT
let mut v = vector[10];
let first = &v[0];
let len = v.length();
v.push_back(20);
```

### Collection Index Syntax

```move
// WRONG
let val = vec_map::get(&map, &key);

// CORRECT
let val = &map[&key];
```

## Option Macros

Use macros instead of manual `is_some` / `destroy_some` patterns.

```move
// WRONG
if (opt.is_some()) {
    let value = opt.destroy_some();
    call_function(value);
};

// CORRECT
opt.do!(|value| call_function(value));
```

### Default values

```move
// WRONG
let value = if (opt.is_some()) { opt.destroy_some() } else { default };

// CORRECT
let value = opt.destroy_or!(default);
```

## Loop Macros

```move
// WRONG — manual counter loop
let mut i = 0;
while (i < 32) {
    do_action();
    i = i + 1;
};

// CORRECT — do! macro
32u8.do!(|_| do_action());
```

### Range-based loops

```move
// Iterate over a numeric range
let mut sum = 0;
10u64.do!(|i| { sum = sum + i });  // i goes 0..9

// With index for more complex logic
let mut results = vector[];
5u64.do!(|i| results.push_back(i * i));  // [0, 1, 4, 9, 16]
```

### Vector iteration

```move
// WRONG
let mut i = 0;
while (i < vec.length()) {
    call_function(&vec[i]);
    i = i + 1;
};

// CORRECT
vec.do_ref!(|e| call_function(e));
```

### Vector creation from range

```move
// WRONG
let mut v = vector[];
let mut i = 0;
while (i < 32) { v.push_back(i); i = i + 1; };

// CORRECT
let v = vector::tabulate!(32, |i| i);
```

### Fold and filter

```move
// fold
let sum = source.fold!(0, |acc, v| { acc + v });

// filter (requires T: drop)
let filtered = source.filter!(|e| e > 10);
```

## Struct Unpacking: `..` Syntax

Use `..` to ignore unused fields when destructuring in 2024 edition.

```move
// WRONG
let MyStruct { id, field_1: _, field_2: _, field_3: _ } = value;

// CORRECT
let MyStruct { id, .. } = value;
```

## Renamed Standard Library Functions

Some standard library functions have been renamed. Using the old name produces a deprecation warning or compile error.

```move
// WRONG — deprecated, renamed
dynamic_field::exists_(&id, key)

// CORRECT
dynamic_field::exists(&id, key)
```

## Positional Fields (Tuple Structs)

Structs can use positional fields instead of named fields:

```move
// Named fields (traditional)
public struct Wrapper has copy, drop, store { value: u64 }

// Positional fields (2024 edition)
public struct Wrapper(u64) has copy, drop, store;

// Access by position
let w = Wrapper(42);
let val = w.0;
```

Positional structs are useful for newtype wrappers and dynamic field keys (see `naming-conventions` skill).

## Public Structs

The `public` keyword on structs controls visibility of the struct's fields. Without `public`, fields are module-private — only the defining module can construct or destructure the struct.

```move
// Fields visible only within this module
struct Config has key { id: UID, admin: address }

// Fields visible to other modules
public struct Token has key, store { id: UID, value: u64 }
```

Use `public` when other modules need to read fields or construct/destructure the struct. Omit it for encapsulation.

## Enums

Move 2024 supports enum types:

```move
public enum Color {
    Red,
    Green,
    Blue,
    Custom(u8, u8, u8),
}

public fun is_red(c: &Color): bool {
    match (c) {
        Color::Red => true,
        _ => false,
    }
}
```

Enums can have variants with positional fields, named fields, or no fields. Use `match` expressions for exhaustive pattern matching. Enums cannot have the `key` ability — they cannot be objects directly, but they can be stored as fields inside objects.

## Quick Reference

| Legacy Pattern | Modern 2024 Syntax |
|---|---|
| `coin::value(&c)` | `c.value()` |
| `coin::into_balance(c)` | `c.into_balance()` |
| `balance::join(&mut b, v)` | `b.join(v)` |
| `balance::split(&mut b, n)` | `b.split(n)` |
| `tx_context::sender(ctx)` | `ctx.sender()` |
| `object::delete(id)` | `id.delete()` |
| `string::utf8(b"x")` | `"x"` (or `b"x".to_string()`) |
| `vector::empty()` | `vector[]` |
| `vector::push_back(&mut v, x)` | `v.push_back(x)` |
| `vector::length(&v)` | `v.length()` |
| `opt.is_some() + destroy_some` | `opt.do!(\|v\| ...)` |
| `while (i < n) { ... i++ }` | `n.do!(\|_\| ...)` |
| `let S { a, b: _ } = x` | `let S { a, .. } = x` |
