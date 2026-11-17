---
name: naming-conventions
description: Naming rules for Move smart contracts on Sui - error constants, regular constants, events, capability structs, getter functions, hot potatoes, and dynamic field keys. Use when the user asks to write, scaffold, or review a Move module or Sui smart contract (AMM, liquidity pool, NFT, game profile, inventory, access control, roles, registry), or mentions Move structs, events, error codes, capabilities, getters, or dynamic object fields.
---

# Move on Sui: Naming Conventions

## Quick start

Copy this shape. It applies every convention at once.

```move
module my_pkg::game;

use std::string::String;

// Regular constants: ALL_CAPS
const MAX_LEVEL: u64 = 100;
const XP_PER_LEVEL: u64 = 1000;

// Error constants: E + PascalCase, with #[error] message
#[error]
const ENotAuthorized: vector<u8> = b"Caller is not authorized";
#[error]
const EMaxLevelReached: vector<u8> = b"Player is already at max level";

// Capability: Cap suffix
public struct AdminCap has key, store { id: UID }

public struct Player has key, store {
    id: UID,
    username: String,
    xp: u64,
    level: u64,
}

// Dynamic field key: positional struct, Key suffix
public struct InventoryKey(String) has copy, drop, store;

// Events: past tense
public struct XpEarned has copy, drop { player: ID, amount: u64 }
public struct LeveledUp has copy, drop { player: ID, new_level: u64 }

// Getters: field name, no get_ prefix
public fun username(p: &Player): String { p.username }
public fun xp(p: &Player): u64 { p.xp }
public fun level(p: &Player): u64 { p.level }
public fun xp_mut(p: &mut Player): &mut u64 { &mut p.xp }
```

## Rules

### Error constants — `E` + PascalCase
Never `SCREAMING_SNAKE_CASE`.
`NOT_AUTHORIZED` → `ENotAuthorized`; `INSUFFICIENT_LIQUIDITY` → `EInsufficientLiquidity`.
Default: `#[error] const EName: vector<u8> = b"message";`. Escape hatch: `const EName: u64 = 0;` if you don't want messages — the name is unchanged.

### Regular constants — ALL_CAPS
`feeNumerator` → `FEE_NUMERATOR`; `MyConstant` → `MY_CONSTANT`.

### Capability structs — `Cap` suffix
`Admin` → `AdminCap`; `MintAuthority` → `MintCap`; `GameAdmin` → `GameAdminCap`.
Non-capability objects stay plain PascalCase nouns: `RoleRegistry`, `Pool`, `AccessControl`.

### Events — past tense
`CreatePool` → `PoolCreated`; `AddLiquidity` → `LiquidityAdded`; `Swap` → `Swapped`; `EarnXp` → `XpEarned`; `LevelUp` → `LeveledUp`; `GrantRole` → `RoleGranted`; `RevokeRole` → `RoleRevoked`.

### Getters — field name, no `get_`
`get_balance()` → `balance()`; `get_xp()` → `xp()`; `get_role_admin()` → `role_admin()`.
Mutable getters add `_mut`: `details_mut()`.

### Hot potatoes — no `Potato` in the name
`FlashLoanPotato` → `FlashLoanReceipt`; `PromisePotato` → `Promise`. The absence of abilities already signals the pattern.

### Dynamic field keys — positional struct with `Key` suffix
```move
// WRONG
public struct ItemSlot has copy, drop, store { name: String }

// CORRECT
public struct ItemKey(String) has copy, drop, store;
public struct ConfigKey() has copy, drop, store;
```

## Common contract shapes

| Request | Correct names |
|---------|---------------|
| AMM / liquidity pool | `Pool`, `FEE_NUMERATOR`, `FEE_DENOMINATOR`, `EInsufficientLiquidity`, `PoolCreated`, `LiquidityAdded`, `LiquidityRemoved`, `Swapped` |
| Game profile NFT + inventory | `Player`, `AdminCap`, `InventoryKey(String)`, `XpEarned`, `LeveledUp`, `xp()`, `level()`, `username()` |
| Role-based access control | `AdminCap` or `RoleRegistry`, `ENotAuthorized`, `ERoleMissing`, `RoleGranted`, `RoleRevoked`, `role_admin()`, `has_role()` |

## Rename pass before returning code

Run this over every module you produce and fix any hit:

- [ ] Every `const E...` is PascalCase, not `UPPER_SNAKE`.
- [ ] Every non-error `const` is `UPPER_SNAKE`.
- [ ] Every struct holding authorization ends in `Cap`.
- [ ] Every event struct name is past tense (reads as something that happened).
- [ ] No public function name starts with `get_`.
- [ ] Every mutable accessor ends in `_mut`.
- [ ] No type name contains `Potato`.
- [ ] Every dynamic field key is a positional struct ending in `Key` with `copy, drop, store`.

## Reference

Full list of conventions: https://move-book.com/guides/code-quality-checklist
