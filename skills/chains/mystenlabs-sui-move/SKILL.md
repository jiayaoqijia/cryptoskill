---
name: sui-move
description: >
  Sui Move smart contract development. Use when writing, reviewing, or debugging
  Move code on Sui. Covers Move abilities (key, store, copy, drop), TxContext,
  init functions, One-Time Witness, package publishing and upgrades, resource safety,
  events, and coins. Also use when the user asks about struct abilities, UID,
  how to destroy objects, or how to create a fungible token.

  For object model and ownership, see the `object-model` skill.
  For programmable transaction blocks, see the `ptbs` skill.
  For frontend dApp development, see the `frontend-apps` skill.
  For project setup and Move.toml, see the `sui-move-project` skill.
---

# Sui Move

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information in this skill is sourced exclusively from [docs.sui.io](https://docs.sui.io) and [move-book.com](https://move-book.com). When extending or updating this skill, only pull from these sources. Do not use third-party blogs, tutorials, or unofficial documentation.

Move is Sui's smart contract language, designed around resource safety and an object-centric data model. This skill covers the core Move language: the type system, abilities, resource safety, events, and coins.

This skill routes to focused reference files. Load only the ones relevant to the current task.

---

## Reference files (this skill)

### move — Move Language Fundamentals
**Path:** `move.md`
**Load when:** writing Move code, working with abilities, TxContext, time/Clock, init functions, One-Time Witness, `internal::Permit<T>`, `type_name` deprecations, packages, modules, structs, resource safety, access control patterns, admin rotation, deny lists, security review, or advanced design patterns (ability dosing, phantom events, shared-object concurrency, receiver syntax, error attributes, `transfer::receive`, field privacy, macros).
**Covers:** the four abilities and common combinations, TxContext methods, Clock object, init functions, OTW pattern, `internal::Permit<T>` type-level authorization, `type_name` deprecations, packages and upgrades, modules, structs, resource safety and object destruction, a worked Greeting example, admin rotation (two-step transfer), regulated coins and deny lists, security review checklist, advanced design patterns (ability dosing, phantom-type events, event denormalization, shared-object `&` vs `&mut`, receiver-syntax ordering, `#[error]` constants, `transfer::receive` privacy, field privacy, macro gotchas).

### events-coins — Events and Coins
**Path:** `events-coins.md`
**Load when:** emitting events, subscribing to events offchain, creating fungible tokens, or working with coin operations (mint, burn, split, join).
**Covers:** event emission, event struct requirements, coin::create_currency, TreasuryCap, CoinMetadata, standard coin operations.

---

## Related skills (load from separate skill directories)

| Topic | Skill | Load when |
|-------|-------|-----------|
| Object model, ownership, dynamic fields, collections, Display, transfer patterns | `object-model/` | Designing data models, choosing ownership types, using dynamic fields or collections, setting up Object Display |
| Programmable transaction blocks, commands, equivocation | `ptbs/` | Building PTBs, composing transactions, sponsored transactions, troubleshooting transaction errors |
| Frontend dApp development, dApp Kit, wallet connection | `frontend-apps/` | Building React/Vue frontends, wallet integration, querying onchain state from the browser |
| Project setup, Move.toml, dependencies, publishing | `sui-move-project/` | Creating a Move project, configuring Move.toml, resolving build errors, publishing packages |
| Move 2024 syntax, method syntax, macros | `modern-move-syntax/` | Using Move 2024 edition features like method syntax, vector literals, option/loop macros |
| Composable function design | `composable-move-functions/` | Designing functions for PTB composability, parameter ordering, return patterns |
| Unit testing conventions | `move-unit-testing/` | Writing Move unit tests, test patterns, expected_failure, cleanup |
| Naming conventions | `naming-conventions/` | Naming errors, constants, capabilities, events, getters, dynamic field keys |

---

## Routing guide

| Task | Load |
|------|------|
| Writing a Move struct with abilities | move |
| Using TxContext or the Clock object | move |
| Writing an init function or OTW | move |
| Using `type_name` functions | move |
| Proving module authority with `internal::Permit<T>` | move |
| Publishing or upgrading a package | move |
| Destroying an object without drop | move |
| Emitting or subscribing to events | events-coins |
| Creating a fungible token | move + events-coins |
| Designing an object data model | `object-model/` skill |
| Choosing shared vs owned objects | `object-model/` skill |
| Using dynamic fields or collections | `object-model/` skill |
| Setting up Object Display | `object-model/` skill |
| Building a PTB | `ptbs/` skill |
| Implementing sponsored transactions | `ptbs/` skill |
| Building a frontend | `frontend-apps/` skill |
| Setting up Move.toml | `sui-move-project/` skill |
| Writing a complete smart contract | move + events-coins + `object-model/` + `naming-conventions/` + `modern-move-syntax/` |
| Code review | move + events-coins + `composable-move-functions/` + `naming-conventions/` + `modern-move-syntax/` |
| Security review / access control audit | move + `object-model/` (patterns) + events-coins |
| Advanced design patterns / performance tuning | move |

---

## Rules

- Always use `object::new(ctx)` to create UIDs. There is no other way.
- Use `public_transfer` (not `transfer`) when the object has `store` and the call originates outside the defining module.
- Event structs must have `copy` and `drop` abilities.
- No `as` casts on numeric types. Use `from`/`into` or `try_from`/`try_into`.
- To destroy an object without `drop`, unpack the struct and call `object::delete(id)` on the UID.

## Common mistakes

- **Confusing `transfer` with `public_transfer`.** The non-public variant only works within the defining module. Calling it from another module is a compile error.
- **Forgetting to delete the UID.** When destroying an object, you must call `object::delete(id)` on the UID field.
- **Assuming `ctx.epoch_timestamp_ms()` is precise.** It returns the epoch start time. Use the Clock object (`0x6`) for real-time timestamps.
