---
name: abi-as-contract
domain: software-engineering/abi-as-contract
trigger: "Treating layout, calling convention, and symbol naming as a binding agreement."
anti_trigger: "Not for API design at source level, and not for format versioning."
scope: "Layout, calling convention, and symbol naming as a binding agreement."
status: seedling
---

# ABI as a contract

## Standard

An application binary interface is an agreement at a level below source: how large a type is, where its members sit, how arguments arrive in registers or on the stack, which registers a callee preserves, and how names become symbols. Code compiled today links with code compiled months ago because both sides hold that agreement, and the agreement holds only if the toolchain, the flags, and the declared types are compatible.

The contract's fragility is invisible at source level. Adding a member to a struct changes its size and the offset of everything after it; changing an inline function can change inlined layout in downstream builds; a new calling convention flag makes old objects incompatible. The source-compatible change is not necessarily the ABI-compatible change, and interfaces that cross a shared-object boundary must be managed as binary contracts explicitly, since nothing in the language enforces it.

Primary sources: <https://en.cppreference.com/w/c/language.html> and <https://sourceware.org/binutils/docs/ld/>.

## Decision rules

- Identify which types and functions cross a binary boundary; only those need ABI discipline.
- Record the layout assumptions of boundary types with static assertions on offsets and size.
- Treat member addition, reorder, and basis-type change as ABI breaks needing a compatibility plan.
- Keep the calling-convention and key compilation flags constant across a linked set.
- Version or rename boundary symbols when the contract changes, rather than reusing names.
- Verify binary compatibility by linking against a prebuilt object of the old contract.

## Procedure

1. List the types and functions that cross binary boundaries.
2. Assert sizes and offsets for those types.
3. Review pending changes against the boundary list.
4. Classify each change compatible or breaking.
5. Plan symbol versioning for breaking changes.
6. Verify by linking old and new objects together.

## Anti-patterns

- Assuming source compatibility implies binary compatibility.
- Adding a member to a boundary struct with no compatibility plan.
- Changing optimization or convention flags mid-library.
- Testing compatibility only by recompiling everything.
- Reusing a symbol name for changed semantics.

## Done checklist

- [ ] Boundary types and functions listed.
- [ ] Layout asserted statically.
- [ ] Changes classified as compatible or breaking.
- [ ] Flags kept constant across the linked set.
- [ ] Breaking changes versioned.
- [ ] Mixed-version linking verified.

A further discipline is to freeze the boundary description itself: a generated header or a checked-in layout assertion documents the contract where both sides can see it, so a change that breaks the contract fails a build rather than failing a customer's load, and the contract's history becomes reviewable alongside the code it governs.

## Sources

- Type layout semantics: <https://en.cppreference.com/w/c/language.html>
- Linker documentation: <https://sourceware.org/binutils/docs/ld/>
- Symbol visibility context: <https://llvm.org/docs/>
