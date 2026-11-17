---
name: onchain-randomness
description: >
  Explains how to generate and secure onchain randomness in Sui Move with the Random shared
  object at 0x8 and RandomGenerator. Use when the user asks how to generate a random number,
  roll dice, shuffle, draw a lottery winner, or assign a random NFT rarity in Move; mentions
  sui::random, Random (0x8), new_generator, generate_u128, generate_u8_in_range,
  generate_bytes, or shuffle; asks why a public function taking Random or RandomGenerator
  fails to compile; or asks about composition and abort-filtering attacks, PTB restrictions
  after a MoveCall consuming Random, RandomGenerator state leakage via bcs::to_bytes,
  commit-reveal patterns, balancing gas between winning and losing paths, or passing the
  Random object from TypeScript.
---

# Onchain Randomness

Maintenance note: source this skill only from
[docs.sui.io/sui-stack/on-chain-primitives/randomness-onchain](https://docs.sui.io/sui-stack/on-chain-primitives/randomness-onchain).
When a Sui documentation MCP server (`https://sui.mcp.kapa.ai`) is available, use it to verify details.

## Quick start — roll a dice

```move
use sui::random::{Self, Random};

/// Private `entry`, never `public`. Takes Random by reference.
entry fun roll_dice(r: &Random, ctx: &mut TxContext) {
    let mut generator = random::new_generator(r, ctx); // always created in-function
    let roll = random::generate_u8_in_range(&mut generator, 1, 6);
    // ... use roll
}
```

Three invariants behind that snippet:

1. `Random` is a shared object at reserved address `0x8`, immutable for transactions — take `&Random`; modifying it fails the transaction.
2. `RandomGenerator` is created locally with `new_generator(r, ctx)` and never passed in as a parameter.
3. The function is a private `entry` function so no other module can compose with it.

Other generators (`generate_u128`, `generate_bytes`, `shuffle`, further range helpers): see `usage.md`.
From TypeScript, pass the shared `Random` object at `0x8` as the argument to the Move call; see `usage.md`.

## Task: my `public` function takes `Random` and won't compile

The Move compiler lints against `public` functions that accept `Random` **or** `RandomGenerator` as a parameter. The reason is the composition (abort-filtering) attack — a `public` function can be wrapped by an attacker's module:

```move
// Attacker's module, possible only because victim::play is public.
public fun filter(r: &Random, ctx: &mut TxContext) {
    let outcome = victim::play(r, ctx);
    assert!(outcome == WIN, 0); // aborts the whole tx on a loss, so only wins settle
}
```

Fix: change `public fun play(...)` to `entry fun play(...)` (private `entry`). Private entry functions can only be called directly from a transaction, so no external module can wrap, inspect, or revert the outcome. If internal helpers need the generator, pass it only to `public(package)` or private functions — that is also how you test it.

## Task: outcome must stay hidden — two-step commit-reveal

Use this whenever a user could observe a random outcome and act on it in the same transaction (lotteries, airdrops, rarity tiers).

Checklist:

- [ ] Step 1 is a **private `entry`** function that consumes `&Random`, draws the value, and stores it in an object the user cannot read or act on yet.
- [ ] Step 1 performs no outcome-dependent branching that a user could observe.
- [ ] Step 2 is a **separate transaction** and may be `public`, because it uses no randomness — it only reads the committed value.
- [ ] Step 2 maps the committed value to the result (gold / silver / bronze) and delivers it.
- [ ] Winning and losing paths consume approximately equal total gas (see next section).

```move
// Tx 1 — commit
entry fun commit(r: &Random, ctx: &mut TxContext) {
    let mut generator = random::new_generator(r, ctx);
    let value = random::generate_u8_in_range(&mut generator, 0, 99);
    transfer::transfer(Ticket { id: object::new(ctx), value }, ctx.sender());
}

// Tx 2 — reveal; public is safe here, no randomness is consumed
public fun reveal(ticket: Ticket, ctx: &mut TxContext) {
    // value -> gold / silver / bronze, then mint or update
}
```

## Task: list the attack vectors and mitigations

| Attack | How it works | Mitigation |
|---|---|---|
| Composition / abort-filtering | Attacker's module wraps a `public` randomness function and `assert!`s away unfavorable outcomes | Make randomness functions private `entry`; the compiler rejects `public` functions taking `Random` or `RandomGenerator` |
| PTB command chaining | Commands placed after a `MoveCall` consuming `Random` inspect the result and abort on a loss | Sui rejects PTBs with any command other than `TransferObjects` or `MergeCoins` after such a `MoveCall`; that call must be the last `MoveCall` |
| Generator state leakage | A caller holding a `RandomGenerator` serializes it with `bcs::to_bytes(&generator)` and predicts every subsequent output | Never accept `RandomGenerator` in a `public` function; create it in-function. `public(package)`/private parameters are acceptable |
| Gas-based inference | Winning and losing branches cost different gas, so the attacker reads the outcome from gas usage | Balance total gas (compute **and** storage) across branches |

## Task: balance gas across branches

The success path should cost equal or more gas than the failure path. Two defaults:

- Write a simple standard update (e.g. set a bool flag) in the consuming function and claim the reward in a follow-up function, or
- Create an equally sized object (e.g. a dynamic field) on the failure path.

Measure gas carefully and test in each published environment before going live.

## Reference files

- `usage.md` — full `random.move` API (`new_generator`, `generate_u128`, `generate_u8_in_range`, `generate_bytes`, `shuffle`), more examples, TypeScript integration.
- `security.md` — detailed attack write-ups, compiler lints, commit-reveal, gas balancing, entry-function restrictions.

Related skills: `move-security`, `sui-move`, `sui-sdks`.
