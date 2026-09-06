---
name: func2tolk
description: "Port TON smart contracts from FunC (.fc/.func) to modern Tolk (.tolk) with Acton: use acton func2tolk when helpful, then refactor storage/messages/opcodes into typed structs and serialization, implement Acton-style entrypoints, generate wrappers, migrate JS/TS tests to native Tolk tests, and use acton build/test/script/verify/disasm to preserve TL-B compatibility and behavior. Use when asked to convert, port, or modernize FunC contracts into idiomatic Tolk."
---

# func2tolk

## Overview

Port a legacy FunC smart contract to Tolk while preserving:
- TL-B layout (storage and message bodies)
- opcode numbers and error codes
- observable behavior (including bounce handling and send modes)

Prefer Acton as the development framework (build, wrappers, native Tolk tests, scripts, deploy, verify).

Use `acton func2tolk` as a first-pass converter when it accelerates the job, then treat the output as a draft to audit and refactor into idiomatic, testable Tolk.

For common mappings and gotchas, open `references/porting-checklist.md`. For public idiomatic examples and original FunC baselines, open `references/repo-examples.md`.

## Non-negotiable rules (MUST follow)

These rules are mandatory for every FunC -> Tolk porting run.

- MUST follow the idioms in this skill and in:
  - `https://docs.ton.org/languages/tolk/idioms-conventions`
- MUST use typed message schemas + union dispatch (`type Allowed...` + `lazy ...fromSlice(...)` + `match`) for known opcode families.
- MUST use structs for storage/message decoding instead of imperative field-by-field parsing in business logic.
- MUST use typed maps (`map<K, V>`) and typed helpers in core logic; raw dict parsing is allowed only at boundaries and must be wrapped immediately.
- MUST keep TL-B compatibility constraints explicit when deviating from idiomatic code (for example: `UnsafeBodyNoRef`, `any_address?`, legacy inline-body quirks).
- MUST open and apply `references/porting-checklist.md` during the run.
- MUST NOT end a porting run before completing the mandatory completion gate in this file.

Forbidden unless explicitly justified by compatibility:

- manual opcode `if/elseif` ladders for messages that can be modeled as tagged structs + union + `match`
- ad-hoc message parsing (`load_uint/load_msg_addr/...`) in domain logic where a typed struct is feasible
- raw `udict_*` operations spread through core business branches instead of typed map helpers
- finishing the run without a checklist-based self-audit

## Portable references and example corpus

- Skill references in this skill directory:
  - `references/porting-checklist.md`
  - `references/repo-examples.md`
- Primary public style oracle:
  - `https://github.com/ton-blockchain/acton-contracts`
  - Each contract suite contains Acton/Tolk contracts, native tests, scripts, generated wrappers, benchmark snapshots where relevant, and a README linking to the original FunC implementation.
- High-value Acton/Tolk suites to study:
  - `jetton-v2` paired with `https://github.com/ton-blockchain/jetton-contract/tree/jetton-2.0`
  - `nft` paired with `https://github.com/ton-blockchain/nft-contract`
  - `w5` paired with `https://github.com/ton-blockchain/wallet-contract-v5`
  - `dns` paired with `https://github.com/ton-blockchain/dns-contract`
  - `multisig-v2` paired with `https://github.com/ton-blockchain/multisig-contract-v2`
  - `highload-v3` paired with `https://github.com/ton-blockchain/highload-wallet-contract-v3`
  - `notcoin` paired with `https://github.com/OpenBuilders/notcoin-contract`
  - `config` paired with `https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/config-with-ownable-params.fc`
  - `elector` paired with `https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/elector-code.fc`
- `counter` in `acton-contracts` has no original FunC counterpart; use it only for minimal Acton project mechanics.
- Acton docs:
  - `https://github.com/ton-blockchain/acton/tree/master/docs/content/docs`
  - otherwise use `acton --help` and the official hosted docs
- Tolk idioms and conventions (docs-first style target):
  - `https://docs.ton.org/languages/tolk/idioms-conventions`
- Before running `acton ...`, `cd` to the directory that contains `Acton.toml` (Acton resolves contracts/config relative to it).

## Porting workflow (Acton-first)

### 1) Identify the behavioral contract

- Locate FunC entrypoints (`recv_internal`, `recv_external`, `run_ticktock`, getters) and list handled opcodes.
- Extract invariants to preserve:
  - exact storage layout (bit widths, field order, presence/absence of refs)
  - message TL-B layout (including `Either` payloads and `Maybe` fields)
  - gas/reserve behavior and send modes
- Treat existing JS/TS tests as the spec; translate them into native Tolk tests as you port.

### 2) Set up Acton project structure

- Scaffold or reuse a project:
  - `acton new PROJECT --template empty|counter|jetton`
- Define contracts in `Acton.toml` under `[contracts.*]`.
- Use `[mappings]` to avoid deep relative imports (mirror the `@stdlib/...` import style).
- If the system is multi-contract (Jetton minter + wallet, collection + item, etc.), model dependencies in `Acton.toml` and use `acton build --graph` to sanity-check the dependency DAG.

### 3) Translate storage and TL-B types first

- Split types into files importable by tests/wrappers (avoid putting message/storage structs inside the contract entrypoint file):
  - `errors.tolk` — error codes
  - `messages.tolk` — message TL-B structs and union types
  - `storage.tolk` — persistent structs and helpers
- Model contract data as `struct Storage { ... }` (and related structs).
- Implement storage helpers:
  - `fun Storage.load() { return Storage.fromCell(contract.getData()) }`
  - `fun Storage.save(self) { contract.setData(self.toCell()) }`
- If FunC has “maybe initialized” storage, model it explicitly (for example a wrapper that starts parsing a `slice`, checks remaining refs, and then parses either Initialized or NotInitialized variants).

### 4) Translate message bodies using tagged structs

- Replace FunC `op::...` + manual parsing with tagged structs:
  - `struct (0x...) SomeMessage { ... }`
- Create a union type for dispatch:
  - `type AllowedMessage = A | B | C`
- Parse using lazy decoding:
  - `val msg = lazy AllowedMessage.fromSlice(in.body);`
- To match legacy encodings, prefer correct types over ad-hoc bit twiddling:
  - `RemainingBitsAndRefs` for “remainder” payloads / snaked formats
  - `Cell<T>` for ref payloads
  - `any_address?` when the legacy encoding is not `address?`-compatible

### 5) Implement entrypoints in Acton style

- Internal messages:
  - `fun onInternalMessage(in: InMessage) { ... }`
- Bounced messages:
  - `fun onBouncedMessage(in: InMessageBounced) { ... }`
  - Use it to restore balances/supply on failed sends (common in Jettons).
- External messages (wallets, signatures):
  - `fun onExternalMessage(inMsgBody: slice) { ... }`
- Prefer `match` for dispatch; decide explicitly whether to ignore unknown/empty bodies or throw `0xFFFF`.
- If you must handle bounces manually inside `onInternalMessage`, use compiler policies (for example `@on_bounced_policy("manual")`) and document why.

### 6) Replace low-level message building

- Prefer `createMessage({ ... })` + `.send(SEND_MODE_...)` over manual `builder` encoding.
- Keep send modes and bounce flags consistent with FunC behavior.
- Prefer `@stdlib/gas-payments` helpers when porting contracts that rely on `raw_reserve`, `accept_message`, storage fee reservation, etc.

### 7) Migrate tests (JS/TS → native Tolk)

- Write Acton tests in `tests/*.test.tolk`.
- Use `net.treasury("name")` to create funded emulated accounts.
- Use `expect(res)` matchers on returned transaction lists.
- Generate wrappers (recommended):
  - `acton wrapper CONTRACT_ID --test`
- Keep shared types in a separate file (for example `contracts/types.tolk`) so wrappers/tests can import them without importing contract entrypoints (avoids duplicate `onInternalMessage` definitions).

### 8) Iterate with Acton tooling

- Build: `acton build` (add `--clear-cache` when debugging).
- Test: `acton test` (use `--filter`, `--coverage`, `--debug` as needed).
- Debug compilation differences: `acton disasm` (use `--source-map` when available).
- Dry-run deployment logic locally: `acton script scripts/deploy.tolk` (no real TON spent).
- Broadcast only after local success:
  - `acton script scripts/deploy.tolk --broadcast --net testnet|mainnet`

### 9) Verify on-chain

- After deployment:
  - `acton verify CONTRACT_ID --address EQ... --net testnet|mainnet`

## High-signal FunC -> idiomatic Tolk patterns (from acton-contracts)

Use this section as the default translation strategy unless compatibility constraints force lower-level code.

### A) Opcode dispatch: replace `if (op == ...)` chains with typed unions + `match`

FunC baseline:
- `op = in_msg_body~load_uint(32); if (op == op::x) { ... } if (op == op::y) { ... }`

Idiomatic Tolk:
- declare tagged message structs in `messages.tolk`
- group them into a union (`type AllowedMessage = A | B | C`)
- parse lazily and dispatch with `match`

```tolk
type AllowedMessage = Transfer | Burn | TopUp

fun onInternalMessage(in: InMessage) {
    val msg = lazy AllowedMessage.fromSlice(in.body);
    match (msg) {
        Transfer => { ... }
        Burn => { ... }
        TopUp => { ... }
        else => throw 0xFFFF
    }
}
```

Why this is better:
- preserves opcode compatibility while eliminating manual parse drift
- keeps branch-local parsing strongly typed
- scales better for large opcode sets (wallet-v5/vesting/telemint style)

### B) Parse bodies into structs, not ad-hoc loads

Prefer:
- `struct (0x...)` for externally visible opcodes
- nested structs for grouped payloads (`TransferOwnershipData`, `MsgInner`, etc.)
- `Cell<T>` when payload is explicitly by-reference
- `RemainingBitsAndRefs` for true remainder payloads / snake / either wrappers

Avoid:
- repeated `load_uint/load_msg_addr/load_ref` in business logic when a struct can model the same layout.

### C) Use dedicated `messages.tolk` modules for inbound formats

Pattern used broadly in ports:
- keep all incoming message schemas in `messages.tolk`
- import message types into contract entrypoints
- define `Allowed...` unions near message definitions

This keeps entrypoint files focused on behavior, not byte parsing.

### D) Storage translation: tuple loaders -> typed storage structs + methods

FunC baseline:
- `(a, b, c) load_data()` and `save_data(a, b, c)`

Idiomatic Tolk:
- `struct Storage { ... }`
- `Storage.load()` / `Storage.save()`
- keep TL-B layout identical (field order + ref/inline shape)

```tolk
struct Storage { totalSupply: coins adminAddress: address? }
fun Storage.load() { return Storage.fromCell(contract.getData()) }
fun Storage.save(self) { contract.setData(self.toCell()) }
```

### E) Model multi-shape state explicitly (initialized vs not initialized)

Common in NFT/DNS/Telemint items:
- FunC checks `slice_bits() > 0` or ref presence to decide shape.

Idiomatic Tolk:
- loader wrapper + explicit parsers:
  - `startLoading...()`
  - `.isInitialized()`
  - `.parseNotInitialized()`
  - `.parseInitialized()`

This keeps state transitions explicit and avoids brittle remainder parsing.

### F) Dictionaries: replace raw `udict_*` plumbing with typed maps

FunC baseline:
- manual `udict_get?`, `udict_set_ref`, `udict_delete?`, `udict_delete_get_min`

Idiomatic Tolk:
- `map<K, V>` aliases + typed helpers (`exists`, `set`, `delete`, `findFirst`, `iterateNext`)
- convert low-level dicts only at boundaries (`createMapFromLowLevelDict(...)`)

Examples:
- DNS records: `type DnsRecords = map<uint256, cell>`
- Wallet extensions: `map<uint256, bool>`
- Query bitmaps: `map<uint13, Bitmap>`

### G) Prefer `createMessage(...)` over manual `begin_cell()` message assembly

Default:
- build outgoing messages with `createMessage({ ... })`
- send via `.send(SEND_MODE_...)`

Keep manual builders only when:
- emulating historical quirks exactly
- forcing exact inline/no-ref body layout

### H) External signature flows: parse suffixes/remainders deliberately

For wallet-style externals:
- separate signature from signed payload (`getLastBits/removeLastBits` or explicit field ordering)
- validate hash/signature first
- update replay state (`seqno` / query maps), persist, commit
- then execute actions/messages

This mirrors hardened wallet-v5/highload patterns.

### I) Bounce handling: prefer `onBouncedMessage` with typed bounced unions

FunC baseline:
- bounce branch in `recv_internal` + manual `load_uint`

Idiomatic Tolk:
- `onBouncedMessage(in: InMessageBounced)`
- optional union for bounced op subset:
  - `type BounceOpToHandle = A | B`
- restore balances/supply from typed parsed message

### J) Compatibility levers to preserve legacy TL-B/behavior

Use these intentionally when matching FunC tests:
- `UnsafeBodyNoRef { forceInline: ... }` for no-ref body compatibility
- `any_address?` when legacy layout is broader than `address?`
- explicit `(Either Cell ^Cell)` remainder validation helpers for payload correctness
- keep unknown-op behavior identical (`throw 0xFFFF` vs ignore empty/body)

### K) Domain-specific recipes extracted from real ports

Jetton family:
- `AllowedMessageToMinter` / `AllowedMessageToWallet`
- typed bounce restore (`InternalTransferStep | BurnNotification...`)
- typed forward payload (`RemainingBitsAndRefs`) + validator helper

NFT + DNS items:
- explicit uninitialized->initialized transition path
- ownership transfer payload as nested struct
- map-based content records instead of imperative dict bit twiddling

Highload wallet:
- validate minimal shape early, then typed parse
- model replay bitmaps as typed map + helper methods
- typed validation for outbound raw message shape before forwarding

Vesting / policy wallets:
- whitelist maps as typed `map<address, ()>`
- validate allowed opcodes using union parsing + `match` (instead of numeric opcode allowlists spread across branches)

## Mandatory completion gate (before ending any porting run)

Do not end the run until all items below are checked.

1. Checklist was opened and applied:
   - `references/porting-checklist.md`
2. Dispatch is idiomatic:
   - known message families use tagged structs + union + `match`
3. Parsing is typed:
   - no avoidable imperative parsing in business branches
4. Storage is typed:
   - `Storage.load()` / `Storage.save()` (or explicit initialized/uninitialized loader pattern)
5. Dict usage is typed:
   - `map<K,V>` + helpers in logic; boundary raw dict decoding is wrapped
6. Compatibility exceptions are documented:
   - any non-idiomatic construct is justified as TL-B/behavior parity
7. Build/tests status is reported:
   - run relevant `acton build`/`acton test` (or report exact blocker)
8. Final response includes a short self-audit summary against the gate above.

If any gate item cannot be completed, do not silently finish. Report the blocker and list incomplete gate items explicitly.

## Using acton-contracts as a style oracle

Use `https://github.com/ton-blockchain/acton-contracts` as the default public style oracle for production ports:

- use each suite's README to find the original FunC repo or file
- use the original FunC source as the behavioral baseline, especially for edge cases
- use the matching Acton/Tolk suite as the target style for module layout, typed storage, message unions, wrappers, scripts, tests, and benchmark snapshots

Prefer searching by:
- opcode hex (for example `0xd53276db`)
- message type name (for example `InternalTransferStep`)
- storage field name (for example `totalSupply`, `ownerAddress`)

Open `references/repo-examples.md` for suite mappings, original FunC links, and search targets.

## Docs-first lookups

- For Tolk language details and standard library, use TON Docs pages under `languages/tolk/` (overview, serialization, standard library, FunC comparison).
- For Acton specifics (commands, wrappers, testing, scripts), use Acton docs and `acton --help`.
