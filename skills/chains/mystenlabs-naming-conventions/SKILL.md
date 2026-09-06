---
name: naming-conventions
description: Use when writing or reviewing Move smart contracts on Sui. Applies to naming structs, error constants, regular constants, events, getter functions, capability types, hot potato types, and dynamic field keys. Use whenever creating new types, functions, or constants in Move code.
---

# naming-conventions

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

## Overview

Move on Sui has specific naming conventions that differ from what AI agents typically generate from training data. This skill covers every naming pattern from the official code quality checklist.

All patterns sourced from https://move-book.com/guides/code-quality-checklist

## Error Constants: EPascalCase with `#[error]`

Error constants MUST use PascalCase with an `E` prefix. Do NOT use SCREAMING_SNAKE_CASE.

Use the `#[error]` attribute to attach human-readable messages to error constants. When an abort occurs, the message is included in the error output, making debugging much easier for users and support.

```move
// WRONG
const NOT_AUTHORIZED: u64 = 0;
const INSUFFICIENT_BALANCE: u64 = 1;

// CORRECT — with #[error] for readable abort messages
#[error]
const ENotAuthorized: vector<u8> = b"Caller is not authorized to perform this action";
#[error]
const EInsufficientBalance: vector<u8> = b"Insufficient balance for this operation";

// Also valid — u64 without #[error] (less informative on abort)
const ENotAuthorized: u64 = 0;
const EInsufficientBalance: u64 = 1;
```

When using `#[error]`, the constant type is `vector<u8>` (a byte string message) instead of `u64`. The compiler assigns numeric codes automatically. Prefer `#[error]` for all new code — it produces clearer error output in explorers, wallets, and logs.

## Regular Constants: ALL_CAPS

Non-error constants use uppercase snake_case. This is the opposite of error constants.

```move
// WRONG
const MyConstant: vector<u8> = b"hello";
const feeNumerator: u64 = 3;

// CORRECT
const MY_CONSTANT: vector<u8> = b"hello";
const FEE_NUMERATOR: u64 = 3;
```

## Capability Structs: `Cap` Suffix

Any struct that represents a capability (authorization to perform actions) MUST be suffixed with `Cap`.

```move
// WRONG
public struct Admin has key, store { id: UID }
public struct MintAuthority has key, store { id: UID }

// CORRECT
public struct AdminCap has key, store { id: UID }
public struct MintCap has key, store { id: UID }
```

## Events: Past Tense

Event struct names MUST use past tense to indicate something that already happened.

```move
// WRONG
public struct RegisterUser has copy, drop { user: address }
public struct CreatePool has copy, drop { pool_id: ID }
public struct LevelUp has copy, drop { new_level: u64 }

// CORRECT
public struct UserRegistered has copy, drop { user: address }
public struct PoolCreated has copy, drop { pool_id: ID }
public struct LeveledUp has copy, drop { new_level: u64 }
```

## Getter Functions: Field Name, Not `get_`

Getter functions should be named after the field they return, without a `get_` prefix. Mutable getters add `_mut` suffix.

```move
// WRONG
public fun get_name(u: &User): String { u.name }
public fun get_balance(u: &User): u64 { u.balance }

// CORRECT
public fun name(u: &User): String { u.name }
public fun balance(u: &User): u64 { u.balance }
public fun details_mut(u: &mut User): &mut Details { &mut u.details }
```

## Hot Potato Structs: No `Potato` in Name

Hot potato types (structs with no abilities) should NOT include "Potato" in the name. The absence of abilities already signals the pattern.

```move
// WRONG
public struct FlashLoanPotato {}
public struct PromisePotato {}

// CORRECT
public struct FlashLoanReceipt {}
public struct Promise {}
```

## Dynamic Field Keys: Positional Struct with `Key` Suffix

Dynamic field key types should use positional struct syntax (empty parentheses) with a `Key` suffix.

```move
// WRONG
public struct DynamicField has copy, drop, store {}
public struct ItemSlot has copy, drop, store { name: String }

// CORRECT
public struct DynamicFieldKey() has copy, drop, store;
public struct ItemKey(String) has copy, drop, store;
```

## Quick Reference

| Element | Convention | Example |
|---------|-----------|---------|
| Error constants | `E` + PascalCase | `ENotAuthorized` |
| Regular constants | ALL_CAPS | `FEE_NUMERATOR` |
| Capabilities | Suffix with `Cap` | `AdminCap` |
| Events | Past tense | `PoolCreated` |
| Getters | Field name, no `get_` | `balance()` |
| Mutable getters | Field name + `_mut` | `balance_mut()` |
| Hot potatoes | Descriptive, no `Potato` | `FlashLoanReceipt` |
| Dynamic field keys | Positional + `Key` suffix | `ItemKey()` |
