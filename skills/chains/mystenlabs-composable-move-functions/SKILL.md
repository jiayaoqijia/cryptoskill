---
name: composable-move-functions
description: Use when writing Move functions on Sui, especially public APIs. Applies to function visibility (public vs entry), parameter ordering, and return patterns. Use whenever designing function signatures or deciding whether functions should transfer objects or return them.
---

# composable-move-functions

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

## Overview

Sui transactions can chain multiple function calls in a single Programmable Transaction Block (PTB). Functions that transfer objects internally instead of returning them break this composability. This skill covers how to design functions that work well in PTBs.

All patterns sourced from https://move-book.com/guides/code-quality-checklist

## No `public entry`

Functions should be either `public` (composable, can be called from other modules and PTBs) or `entry` (transaction endpoint only). Never use `public entry` together.

```move
// WRONG — public entry is redundant and limits composability
public entry fun do_something() { }

// CORRECT — public for composable functions that return values
public fun mint(ctx: &mut TxContext): NFT { }

// CORRECT — entry for intentionally non-composable endpoints
entry fun mint_and_keep(ctx: &mut TxContext) { }
```

**When to use `entry`:** Only for convenience endpoints that are intentionally non-composable — functions that wrap a composable `public` function and handle transfers to sender.

## Return Objects, Don't Transfer Internally

Public functions should return values to the caller rather than transferring them to `ctx.sender()`. This makes them composable in PTBs — the caller decides what to do with the result.

```move
// WRONG — couples minting with transfer, can't compose
public fun mint_and_transfer(ctx: &mut TxContext) {
    let nft = NFT { id: object::new(ctx) };
    transfer::transfer(nft, ctx.sender());
}

// CORRECT — returns the object, caller decides
public fun mint(ctx: &mut TxContext): NFT {
    NFT { id: object::new(ctx) }
}

// If you need a convenience entry point, add a separate entry wrapper:
entry fun mint_and_keep(ctx: &mut TxContext) {
    let nft = mint(ctx);
    transfer::transfer(nft, ctx.sender());
}
```

### CLI implication for returned values

Functions that return non-`drop` values cannot be invoked via `sui client call` — the CLI has no way to consume the returned value, causing an `UnusedValueWithoutDrop` error. Use `sui client ptb` instead, where you can chain `--assign` and `--transfer-objects` to handle the return value:

```bash
sui client ptb \
  --move-call @pkg::module::create_thing --assign thing \
  --transfer-objects "[thing]" @sender
```

If the function is called frequently from the CLI, consider providing a companion `entry` wrapper that transfers internally (as shown above).

This applies broadly:
- `add_liquidity` should return LP coins and remainder coins, not transfer them
- `remove_liquidity` should return both coins, not transfer them
- `swap` should return the output coin, not transfer it
- `borrow` should return the borrowed asset, not transfer it

## Parameter Ordering

Function parameters follow a strict order:

1. **Objects first** — the primary object being acted on
2. **Capabilities second** — authorization tokens like `AdminCap`
3. **Primitive values** — amounts, flags, addresses
4. **Clock** — always at the end (before ctx), exception to objects-first rule
5. **`ctx: &mut TxContext` last** — ALWAYS the final parameter, after all primitives and all other arguments

```move
// WRONG — cap before object, primitives mixed in
public fun authorize_action(
    cap: &AdminCap,
    value: u8,
    app: &mut App,
    ctx: &mut TxContext,
) { }

// CORRECT — object first, cap second, primitives third, ctx last
public fun authorize_action(
    app: &mut App,
    cap: &AdminCap,
    value: u8,
    ctx: &mut TxContext,
) { }
```

### Clock Exception

`Clock` goes near the end, just before `ctx`, even though it's an object:

```move
public fun timed_action(
    app: &mut App,
    cap: &AppCap,
    value: u8,
    clock: &Clock,
    ctx: &mut TxContext,
) { }
```

## Quick Reference

| Pattern | Rule |
|---------|------|
| Visibility | `public` for composable, `entry` for endpoints. Never `public entry`. |
| Returns | Public functions return objects. Don't transfer to sender internally. |
| Entry wrappers | Separate `entry` function that calls `public` function + transfers. |
| Param order | Object → Capability → Primitives → Clock → TxContext |
