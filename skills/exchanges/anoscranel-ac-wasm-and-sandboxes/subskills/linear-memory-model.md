---
name: linear-memory-model
domain: software-engineering/linear-memory-model
trigger: "Understanding linear memory and what the sandbox boundary guarantees."
anti_trigger: "Not for cache memory layout, and not for language memory models."
scope: "One memory, no pointers out, and what the boundary guarantees."
status: seedling
---

# Linear memory model

## Standard

A sandboxed guest operates on a linear memory: a contiguous, bounds-checked region it addresses with offsets from zero. The guest cannot form a pointer outside that region, because addresses in the instruction set are memory operands against the linear memory, statically bound-checked by the runtime. The host can read and write the guest's memory; the guest cannot reciprocate — every reach outward must go through a host function.

The guarantees and the obligations follow from the same fact. Data crosses the boundary by shared layout: the host writes into linear memory before a call and reads results after, so both sides agree on representation, and a disagreement is silent corruption rather than a crash. The memory is also growable but bounded — a guest that grows memory unboundedly consumes host resources, and the limit policy is the host's decision to set and enforce.

Primary sources: <https://webassembly.github.io/spec/> and <https://llvm.org/docs/>.

## Decision rules

- Record the memory limits granted per guest, initial and maximum.
- Record the byte layout of every structure shared across the boundary, with an asserted size.
- Treat shared-structure changes as interface changes, versioned like any contract.
- Copy in and copy out at the boundary unless the cost justifies shared-memory protocols.
- Record alignment assumptions for shared structures and assert them.
- Track memory growth events as resource consumption, not as an internal detail.

## Procedure

1. Define the shared structures and their byte layouts.
2. Assert sizes and alignments on both sides of the boundary.
3. Set per-guest memory limits from the task's real working set.
4. Implement copy-in and copy-out at the boundary.
5. Version the shared layout like an interface.
6. Record limits, layouts, and the growth policy.

## Anti-patterns

- Sharing structures without an asserted layout.
- Changing a shared field without a version note.
- No memory limit, treating the guest's growth as free.
- Letting the guest dictate layout the host merely accepts.
- Assuming a mismatch will crash rather than corrupt.

## Done checklist

- [ ] Limits recorded per guest.
- [ ] Shared layouts asserted both sides.
- [ ] Copy discipline at the boundary documented.
- [ ] Layout changes versioned.
- [ ] Alignment asserted.
- [ ] Growth policy recorded.

A shared-layout convention earns a second rule from practice: keep the layouts declarative and generated rather than hand-maintained, so both sides consume one definition and a drift error becomes a compile failure on one side instead of a silent reading on the other.

## Sources

- Specification of linear memory: <https://webassembly.github.io/spec/>
- Toolchain targets: <https://llvm.org/docs/>
- Encoding and layout context: <https://capnproto.org/encoding.html>
