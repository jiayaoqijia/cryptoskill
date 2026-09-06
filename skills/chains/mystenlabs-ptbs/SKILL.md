---
name: ptbs
description: >
  Sui Programmable Transaction Blocks (PTBs). Use when writing, reviewing, or
  debugging code that composes multiple Sui transaction commands into a single
  atomic transaction — including TypeScript SDK `Transaction` usage, CLI PTB
  construction, gas coin handling, sponsored transactions, shared-object inputs,
  chaining command results, or troubleshooting PTB execution errors.
---

# Sui Programmable Transaction Blocks (PTBs)

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

A PTB is one Sui transaction that batches up to **1,024 commands** — Move calls, coin splits/merges, object transfers, vector construction, package publish/upgrade — executed in order, atomically (one command fails ⇒ whole block fails), sharing inputs and chaining results. PTBs are the only way to execute transactions on Sui; there is no "single call" mode.

This skill routes to focused reference files. Load only the ones relevant to the current task.

All patterns in this skill are derived from:
- https://docs.sui.io/concepts/transactions/prog-txn-blocks
- https://docs.sui.io/develop/transactions/ptbs/building-ptb
- https://docs.sui.io/references/ptb-commands
- https://sdk.mystenlabs.com/sui/transactions/basics
- https://docs.sui.io/references/cli/client (CLI `sui client ptb`)

If unsure about any API, method signature, or error message, fetch the relevant page before answering. Do not guess or extrapolate from Ethereum, Solana, or other chains — PTBs have no direct analog.

---

## Reference files

### fundamentals — PTB data model
**Path:** `fundamentals.md`
**Load when:** explaining what a PTB is, talking about `Input`, `Argument`, `NestedResult`, `GasCoin`, owned vs shared vs immutable vs receiving object references, pure-input BCS rules, command chaining semantics, or execution ordering / atomicity.
**Covers:** PTB structure, `Input` (CallArg) and `ObjectArg` variants, pure input types, `Argument` enum, result chaining, execution semantics (borrow rules, move/copy, hot potato cliques, end-of-tx constraints), protocol limits.

### commands — Command reference
**Path:** `commands.md`
**Load when:** writing or reviewing any specific command — `MoveCall`, `SplitCoins`, `MergeCoins`, `TransferObjects`, `MakeMoveVec`, `Publish`, `Upgrade` — or debugging argument-type mismatches and return-value shape.
**Covers:** signature, argument rules, return shape, and common pitfalls for each of the seven commands.

### building — TypeScript SDK `Transaction` class
**Path:** `building.md`
**Load when:** writing TS/JS code that constructs a PTB with `@mysten/sui/transactions`, configuring gas, building for wallets, serializing across services, or sending PTBs between app ↔ wallet ↔ sponsor.
**Covers:** `Transaction` API (`tx.moveCall`, `tx.splitCoins`, `tx.mergeCoins`, `tx.transferObjects`, `tx.makeMoveVec`, `tx.publish`, `tx.upgrade`, `tx.balance`, `tx.coin`, `tx.add`, `tx.object`, `tx.pure`, `tx.gas`, `tx.setSender/setGasPrice/setGasBudget/setGasPayment/setGasOwner`), `Inputs.*Ref` helpers, result destructuring, `build({ onlyTransactionKind: true })`, `Transaction.from` / `fromKind`, sponsored transaction flow, signing & executing.

### cli — Building PTBs from the CLI
**Path:** `cli.md`
**Load when:** constructing PTBs from the command line using `sui client ptb`, scripting transactions without TypeScript, merging coins from the CLI, or teaching CLI-based workflows.
**Covers:** `sui client ptb` syntax, chaining commands, common CLI PTB patterns (transfers, coin merges, Move calls), gas budget, previewing before execution.

### troubleshooting — Common errors
**Path:** `troubleshooting.md`
**Load when:** diagnosing a failing PTB — any `ServerError`, `UnusedValueWithoutDrop`, `VMVerificationOrDeserializationError`, `No valid gas coins`, `InsufficientGas`, shared-object congestion, or cryptic "transaction failed" output.
**Covers:** each error category with the Move/PTB-level cause and concrete fix.

## Routing guide

| Task | Load |
|------|------|
| "What is a PTB?" / conceptual explanation | fundamentals |
| Writing a new PTB in TypeScript | building + commands |
| Writing a new PTB from the CLI | cli + commands |
| Reviewing a PTB for correctness | fundamentals + commands + building |
| A specific command fails type checking | commands |
| Sponsored / gasless transactions | building |
| Debugging a failing PTB | troubleshooting + (fundamentals if execution-semantics related) |
| Publishing or upgrading a package in a PTB | commands |
| Building PTB bytes across services (app/wallet/sponsor) | building |
| Merging coins or simple operations from the CLI | cli |
| Full code review | **all reference files** |

## Skill Content

### Key concepts

- **A PTB is the transaction.** Every Sui transaction is a PTB — even a single `moveCall` is a one-command PTB. There is no non-PTB execution path.
- **Inputs vs commands.** `inputs` are values fed in from outside (objects and BCS-encoded "pure" bytes). `commands` operate on those inputs and on each other's results. Commands reference values via the `Argument` enum: `Input(i)`, `GasCoin`, `Result(i)`, `NestedResult(cmd, result)`.
- **Chaining.** Each command produces an array of results. The next command can consume any result (by `NestedResult(cmd, idx)` or, when a command has exactly one return, `Result(cmd)`). The TS SDK surfaces this as destructurable values: `const [coin] = tx.splitCoins(tx.gas, [tx.pure.u64(100)]);`.
- **Atomicity.** Commands execute in order. Any failure reverts the entire block; no partial effects.
- **End-of-tx constraints.** Every non-`drop` value produced during execution must be consumed (transferred, destroyed, or fed into another command). Shared objects have exactly two legal endings: re-share or delete — they cannot be transferred or frozen. Gas coin is returned to its owner with unused gas refunded.

### Rules

1. **`tx.gas` must be used by reference, except in `transferObjects`.** To get an owned `Coin<SUI>` from the gas coin, use `SplitCoins(tx.gas, [amount])` first.
3. **Leave gas config to the wallet when possible.** Do not hardcode `setGasBudget` / `setGasPrice` / `setGasPayment` in app code that will be signed by a user wallet — the wallet dry-runs and selects coins correctly. Only set them for backend-signed flows.
4. **In app code that hands a PTB to a wallet, use `await tx.toJSON()` (not `tx.build()`).** The wallet must perform gas logic and coin selection itself; building bytes in app code preempts that.
5. **Use `Transaction.fromKind(kindBytes)` for sponsored flows.** Build in app with `tx.build({ client, onlyTransactionKind: true })`, send the kind-only bytes to the sponsor service, rehydrate there with `fromKind`, then `setSender`, `setGasOwner`, `setGasPayment`. The user (or either party) should submit the fully-signed transaction directly to a full node — not back through the sponsor service — to avoid censorship.
6. **Every non-`drop` value must be consumed.** If `moveCall` returns a value you don't need, pass it to `transferObjects` (if it has `key + store`), to `public_transfer`, or to a destructor. `UnusedValueWithoutDrop` is the PTB-level error.
7. **Shared objects cannot be transferred, frozen, or consumed by value if passed as read-only** (`mutable: false`). If you need mutable access, mark them mutable when building the input.
8. **Types coming from Move calls cannot be references.** `MoveCall` results are values; if a Move function returns `&T`, it cannot be called from a PTB.
9. **For multi-return Move calls, use destructuring or array indexing.** `const [a, b] = tx.moveCall(...)` or `const r = tx.moveCall(...); r[0]; r[1];`. Do not assume single-return shape.
10. **Cite the docs when unsure.** Canonical sources above. Legacy `/develop/transactions/ptbs/*` URLs still render but prefer `/concepts/transactions/prog-txn-blocks` and `/guides/developer/sui-101/building-ptb`.

### Common mistakes

- **Calling `tx.pure(value)` without a type.** Untyped pure values fail at input resolution. Use typed helpers: `tx.pure.u64(n)`, `tx.pure.address(addr)`, `tx.pure.string(s)`, or the generic `tx.pure('u64', n)`.
- **Passing a string object ID to `moveCall` arguments without `tx.object(...)`.** Mixed-type arguments require explicit `tx.object(id)` wrapping; otherwise the SDK can't distinguish pure from object.
- **Transferring or freezing a shared object.** Shared objects cannot be transferred or frozen — but they *can* be deleted. The two legal endings for a shared object in a PTB are re-share or delete. Do not include shared objects in `transferObjects`. Note that consuming a shared object by value permanently marks its hot-potato clique as "hot", which blocks subsequent non-public `entry` calls on any entangled value in that clique.
- **Forgetting to `setSender` on offline builds.** When calling `tx.build()` without signing through a signer that sets the sender, the sender field stays empty and the build fails.
- **Treating multi-return `moveCall` results as single values.** The return is a vector; index or destructure.
- **Using `transfer::transfer` / `transfer::share_object` on generic types from a PTB.** Those entries require a module-private type param. From a PTB, use `transfer::public_transfer` / `transfer::public_share_object`, which require the type to have `store`.
- **Setting a gas budget that's too tight.** A tx that exceeds budget aborts but still charges the gas coin. Prefer the SDK's dry-run-based auto-budget.
- **Not checking execution status.** A transaction can be accepted by validators but fail at the Move level (assertion, out of gas, etc.). Always check `result.$kind !== 'FailedTransaction'` before treating an operation as successful. The tx digest alone does not mean the effects were applied.
- **Looping in app code to submit N individual transactions.** Batch into one PTB (up to 1,024 ops). One PTB is cheaper and atomic.
