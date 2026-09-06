---
name: tolk
description: "Write, review, debug, and test idiomatic Tolk smart contracts for The Open Network (TON). Use when building or modifying .tolk contracts, designing TON storage/message/getter schemas, implementing internal/external/bounced message flows, using cells, TL-B-compatible serialization, typed maps, Jettons, NFTs, wallets, vesting, multisig, DNS, or choosing Tolk tooling and tests."
---

# Tolk

Use this skill to build production-grade Tolk contracts that are typed, auditable, and compatible with TON message and storage conventions.

## Operating Rules

- Prefer the current repository's framework and commands. Detect the project layout before introducing new tooling.
- Keep binary layouts explicit: field order, fixed integer widths, refs, optional fields, message opcodes, getter return shapes, send modes, and bounce behavior.
- Prefer Tolk's type system over manual slice/builder work: structs, typed cells, custom serializers, union dispatch, lazy loading, typed maps, and `createMessage`.
- Keep low-level cell/dict code at clear boundaries. Wrap it immediately in typed aliases, structs, maps, or helper methods.
- Treat official TON Docs as the source of truth. Start from `https://docs.ton.org/llms.txt`, then load only relevant pages under `https://docs.ton.org/tolk/`, TON foundations, contract development, and standards.
- Before finishing, report what was built, which docs or standards guided the work, and the exact build/test result or blocker.

## Workflow

1. Identify the contract surface.
   - List standards, inbound messages, outgoing messages, getters, storage fields, admin roles, fee assumptions, and deployment behavior.
   - If implementing a TON standard, open the relevant standard docs before choosing opcodes or getter names.

2. Design schemas before behavior.
   - Put persistent data in `storage.tolk`.
   - Put message bodies, opcode-prefixed structs, union types, and shared payload types in `messages.tolk`.
   - Put error constants or enums in `errors.tolk`.
   - Keep entrypoint files focused on validation, state transitions, sends, and getters.

3. Implement typed entrypoints.
   - Use `fun onInternalMessage(in: InMessage)` for internal non-bounced messages.
   - Parse known messages as `lazy AllowedMessage.fromSlice(in.body)` and dispatch with `match`.
   - Choose an explicit unknown-message policy, commonly "ignore empty top-ups, throw `0xFFFF` otherwise".
   - Use `fun onBouncedMessage(in: InMessageBounced)` when outbound messages can bounce and state must be restored.
   - Use `fun onExternalMessage(inMsg: slice)` only for external flows, and accept gas only after validation.

4. Implement storage and outgoing actions.
   - Use `Storage.load()` and `Storage.save()` helpers around `contract.getData()` and `contract.setData(...)`.
   - Use `lazy Storage.load()` in getters and read paths.
   - Compose outgoing messages with `createMessage({ ... })` and send via `.send(SEND_MODE_...)`.
   - Extract `StateInit` or `AutoDeployAddress` construction into helper methods when a contract deploys another contract.

5. Verify with focused tests.
   - Cover deployment, accepted messages, rejected messages, getter values, emitted outbound messages, bounces, fee-sensitive paths, replay protection, map iteration, and large payloads.
   - Use the repository's existing test framework. If multiple frameworks are present, prefer the one already used by adjacent contracts.

## Required Patterns

- Use `struct (0x...) MessageName { ... }` for opcode-bearing message bodies.
- Use `type AllowedMessage = A | B | C` and `match` for known inbound families.
- Use `Cell<T>` for typed refs and `cell` only when the cell contents are intentionally opaque.
- Use `RemainingBitsAndRefs` for true remainder payloads.
- Use fixed-width serializable numeric types (`uint32`, `uint64`, `int32`, `coins`, etc.) inside serialized structs.
- Use `map<K, V>` and `MapLookupResult.isFound`; do not treat map lookup as nullable value lookup.
- Use getter reply structs for multi-value responses; preserve standard getter names when a standard defines them.
- Use methods (`fun Type.method(self)`) to avoid global-name collisions and to keep behavior near the data shape.
- Avoid assembler functions and micro-optimizations unless a measured constraint requires them.

## References

- Open `references/idiomatic-patterns.md` when implementing or reviewing contract code.
- Open `references/development-checklist.md` before finalizing a contract change or choosing build/test commands.

Primary docs to consult:

- `https://docs.ton.org/tolk/overview`
- `https://docs.ton.org/tolk/idioms-conventions`
- `https://docs.ton.org/tolk/features/message-handling`
- `https://docs.ton.org/tolk/features/auto-serialization`
- `https://docs.ton.org/tolk/features/message-sending`
- `https://docs.ton.org/tolk/features/contract-storage`
- `https://docs.ton.org/tolk/features/contract-getters`
- `https://docs.ton.org/tolk/types/maps`
- `https://docs.ton.org/tolk/examples`

## Completion Gate

Do not call the task complete until these are true or explicitly blocked:

- Storage, messages, getters, and outgoing actions are modeled with typed Tolk constructs where feasible.
- Any low-level serialization, raw cells, manual refs, or manual dictionaries are localized and justified.
- Unknown-message, bounce, fee, and deployment behavior are explicit.
- Standard opcodes/getters/return shapes are checked against relevant TON standard docs when applicable.
- Build/tests were run with the project's tooling, or the exact blocker is reported.
