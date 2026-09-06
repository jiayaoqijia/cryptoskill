# Tolk Development Checklist

Use this before finalizing a Tolk contract implementation, review, or debugging pass.

## Table of Contents

- Docs lookup
- Design checklist
- Implementation checklist
- Tooling
- Testing checklist
- Debugging checklist
- Run-end audit

## Docs Lookup

Use official docs first:

```bash
curl -fsSL https://docs.ton.org/llms.txt
```

Search the index for the topic, then fetch only needed pages. Useful pages:

- Tolk overview: `https://docs.ton.org/tolk/overview`
- Idioms: `https://docs.ton.org/tolk/idioms-conventions`
- Message handling: `https://docs.ton.org/tolk/features/message-handling`
- Sending messages: `https://docs.ton.org/tolk/features/message-sending`
- Contract storage: `https://docs.ton.org/tolk/features/contract-storage`
- Auto-serialization: `https://docs.ton.org/tolk/features/auto-serialization`
- Getters: `https://docs.ton.org/tolk/features/contract-getters`
- Maps: `https://docs.ton.org/tolk/types/maps`
- Cells: `https://docs.ton.org/tolk/types/cells`
- Contract examples: `https://docs.ton.org/tolk/examples`
- Internal messages: `https://docs.ton.org/foundations/messages/internal`
- Sending modes: `https://docs.ton.org/foundations/messages/modes`
- Testing: `https://docs.ton.org/contract-dev/testing/overview`

For standard contracts, also open the relevant standard page before writing opcodes, getters, or client-facing return structs.

## Design Checklist

- Contract roles and authority checks are named.
- Inbound messages have opcode-prefixed structs and fixed-width fields.
- Outgoing messages have typed bodies and documented send modes.
- Getter names and return shapes match applicable standards.
- Storage field order, integer widths, refs, defaults, and optional fields are explicit.
- Multi-contract deployment helpers return `AutoDeployAddress` or a documented `StateInit`.
- Bounce policy is chosen for every outgoing message that can affect state.
- Fee and reserve assumptions are expressed as constants or helper methods.
- Time, seqno, signature, allowlist, and replay invariants are listed before implementation.

## Implementation Checklist

- Use `errors.tolk`, `messages.tolk`, `storage.tolk`, and entrypoint files unless the project has a stronger existing convention.
- Use `Storage.load()` / `Storage.save()` helpers.
- Use `lazy` for storage and message parsing when not all fields are needed.
- Use `type Allowed... = ...` and `match` for known inbound message families.
- Keep assertions close to the parsed fields they validate.
- Use methods to group behavior with data shapes and avoid global symbol collisions.
- Use typed `map<K, V>` in core logic.
- Wrap low-level cells, slices, builders, dictionaries, or assembler in small named helpers.
- Avoid changing public binary layouts by accident when refactoring code.

## Tooling

Prefer the repository's existing commands.

For Acton projects, detect `Acton.toml` and run from the directory that contains it:

```bash
acton build
acton test
acton test --coverage
acton wrapper CONTRACT_ID --test
acton disasm CONTRACT_ID
acton script scripts/deploy.tolk
```

For Blueprint projects, detect `blueprint.config.*`, `wrappers/`, and the project's package manager:

```bash
npx blueprint build
npx blueprint test
npx blueprint test --coverage
npx blueprint test --gas-report
```

Use existing package scripts when present:

```bash
npm test
yarn test
pnpm test
bun test
```

Do not broadcast deployment transactions unless the user explicitly asks for a real network action and the local dry run succeeds.

## Testing Checklist

Cover at least the behavior touched by the change:

- deployment and initial storage;
- empty top-up messages;
- each accepted inbound message;
- unknown non-empty inbound messages;
- unauthorized senders;
- invalid values and expected exit codes;
- getter return values and field order;
- outgoing message destination, body opcode, value, bounce mode, and send mode;
- bounced-message state repair;
- fee-sensitive branches and remaining-balance handling;
- replay protection, seqno, signatures, expiration, or query maps;
- large payloads, remainder payloads, and typed refs;
- map insertion, deletion, lookup, and iteration boundaries;
- multi-contract address calculation and deployment state.

For local blockchain emulators, keep each test isolated with fresh chain state unless the framework intentionally models a scenario across steps.

## Debugging Checklist

When behavior diverges:

- Compare message body structure and opcode first.
- Inspect storage serialization by dumping cell trees or comparing field order.
- Confirm `createMessage` body inline/ref behavior; use `UnsafeBodyNoRef` only when required.
- Confirm bounce mode and bounced body parser are aligned.
- Confirm getter return stack order and names.
- Confirm map key/value types are fixed-width and serializable.
- Confirm `fromSlice` end assertion behavior when payloads carry remainders.
- Disassemble compiled output when source-level reasoning is insufficient.

## Run-End Audit

Before final response, report:

- docs and standards consulted;
- files changed;
- build/test commands run and results;
- any low-level serialization or raw data exceptions;
- any unverified behavior or blocker.
