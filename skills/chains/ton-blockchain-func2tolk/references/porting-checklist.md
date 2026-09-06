# FunC → Tolk (Acton) porting checklist

Use this as a “don’t break TL-B” checklist when rewriting a legacy FunC contract into modern Tolk.

## Mandatory usage rule (hard stop)

This checklist is mandatory. Do not end a porting run without applying it and reporting the result.

- MUST read this checklist during every porting run.
- MUST execute a self-audit against all relevant items before finalizing.
- MUST report blockers and any incomplete items explicitly.
- MUST NOT silently skip items because of time; if blocked, call it out.

## 0) Preserve invariants

- Keep opcode numbers identical.
- Keep error codes identical.
- Keep storage cell layout identical:
  - field order and bit widths
  - presence/absence of refs
  - whether a value is stored inline vs as a ref
- Keep getter method signatures and return shapes identical unless intentionally migrating the public API.

## 1) Prefer the common Tolk module split

- `errors.tolk`: `const ERROR_... = ...`
- `messages.tolk`: `struct (0x...) ...` + `type AllowedMessage = ...`
- `storage.tolk`: persistent `struct ...` + `load/save` helpers
- `*-contract.tolk`: entrypoints + logic (`onInternalMessage`, `onBouncedMessage`, `onExternalMessage`, getters)

This split also makes `acton wrapper` generation work smoothly (types stay importable).

## 2) FunC → Tolk mapping table (high-signal)

- FunC `#include "x.fc"` → Tolk `import "x"` or `import "@stdlib/..."`.
- FunC `throw_unless(ERR, cond)` / `throw_if(ERR, cond)` → Tolk `assert(cond) throw ERR` / `assert(!cond) throw ERR`.
- FunC `load_data()/save_data()` → Tolk `struct Storage` + `Storage.load()`/`Storage.save()`.
- FunC manual message parsing (`load_uint/load_coins/load_msg_addr/...`) → Tolk tagged `struct (0x...)` + `type AllowedMessage = ...` + `lazy AllowedMessage.fromSlice(...)` + `match`.
- FunC `recv_internal(...)` bounce branch (`is_bounced(flags)`) → Tolk `onBouncedMessage(in: InMessageBounced)` when possible.
- FunC “either forward payload” checks → Tolk `RemainingBitsAndRefs` + a helper that ensures `(Either Cell ^Cell)` is well-formed (if it’s a ref, no extra bits remain).
- FunC “snake string” cell format → Tolk `type SnakeString = slice` with custom `packToBuilder/unpackFromSlice`.
- FunC raw dict operations (`udict_get?/set/delete/delete_get_min`) → Tolk typed `map<K,V>` APIs (`exists`, `set`, `delete`, `findFirst`, `iterateNext`) and typed aliases.
- FunC manual outgoing message cell building (`begin_cell().store_uint(...).send_raw_message`) → Tolk `createMessage({...})` + `.send(SEND_MODE_...)`.
- FunC storage-shape branching (`slice_bits() > 0`, ref-count checks) → Tolk loader structs with explicit `isInitialized/parseInitialized/parseNotInitialized`.

## 3) Serialization gotchas (common reasons ports diverge)

- Optional addresses:
  - `address?` expects `addr_none` or internal address encoding.
  - Legacy messages may encode “maybe address” differently; use `any_address?` if you must match that layout.
- “Do not create a ref” compatibility:
  - Legacy FunC tests may assume a message body stays inline.
  - In Tolk, use wrappers like `UnsafeBodyNoRef { forceInline: ... }` (when available) to keep compatibility.
- “Remainder” fields:
  - Prefer `RemainingBitsAndRefs` when the FunC code effectively treats “the rest of slice” as an opaque payload.
- Inline-vs-ref message body compatibility:
  - Some legacy FunC tests assume body stays inline in the root message cell.
  - Use `UnsafeBodyNoRef { forceInline: ... }` when exact compatibility is required.
- Prefer modeling message schemas in `messages.tolk`:
  - Keep entrypoint files behavior-only; keep byte layout definitions centralized.
  - This reduces opcode/field drift in multi-contract systems.

## 3.1) Idiomatic dispatch policy (recommended default)

- Parse once:
  - `val msg = lazy AllowedMessage.fromSlice(in.body);`
- Dispatch with `match`, not opcode `if` ladders.
- Decide explicitly and document one policy for unknown messages:
  - ignore empty only, throw on non-empty unknown
  - or strict throw on all unknown
- Keep this policy identical to the FunC original unless intentionally changing behavior.

## 3.2) Maps and config dictionaries

- At boundaries with raw blockchain config or low-level dict cells:
  - decode once into typed maps (`createMapFromLowLevelDict(...)`)
  - then use typed map operations in core logic.
- This mirrors robust ports in DNS/highload/vesting families and reduces low-level parsing bugs.

## 4) Acton test migration notes (JS/TS → Tolk)

- Treat JS/TS tests as the behavioral specification.
- Prefer native Tolk integration tests:
  - Use `net.treasury("name")` for funded accounts.
  - Use contract wrappers for deployment, sends, and getters.
- Generate wrappers and test stubs:
  - `acton wrapper CONTRACT_ID --test`
- In tests, prefer `net.send(...)` / wrapper `.deploy(...)` over calling `.send(...)` on a message (out actions are not automatically processed in tests unless you go through `net`).

## 5) Debugging checklist

- If behavior differs:
  - compare opcode dispatch paths first
  - confirm storage bit layout by serializing and inspecting cell trees
  - disassemble compiled code (`acton disasm`) and use source maps if available
- If bounces differ:
  - ensure bounce policy is consistent
  - ensure you restore balances/supply on bounced sends

## 6) Run-end self-audit (required before final answer)

Before ending the run, confirm all applicable items:

- message dispatch uses tagged structs + `type Allowed...` + `lazy ...fromSlice(...)` + `match` (no avoidable opcode `if` ladders)
- core logic uses typed structs/maps; raw parsing/dict code is only at boundaries and wrapped
- storage uses typed load/save helpers (or explicit initialized/uninitialized loader model)
- compatibility exceptions are documented (for example `UnsafeBodyNoRef`, `any_address?`, legacy inline/no-ref constraints)
- unknown-op policy is explicit and matches intended behavior
- build/test status is reported (`acton build` / `acton test`, or explicit blocker)

If any item is not satisfied, do not finalize as “done”; report the missing items and blocker details.
