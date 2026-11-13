---
name: alignment-and-unaligned-access
domain: software-engineering/alignment-and-unaligned-access
trigger: "Working out what alignment guarantees and when unaligned access is safe."
anti_trigger: "Not for text-encoding boundaries, and not for binary format design alone."
scope: "What alignment guarantees, and when reading unaligned is safe or traps."
status: seedling
---

# Alignment and unaligned access

## Standard

An access is aligned when its address is a multiple of its size, and hardware historically guaranteed aligned accesses while charging a penalty — or raising a fault — for unaligned ones. Modern mainstream architectures handle many unaligned accesses in hardware, which makes the penalty invisible in some workloads and severe in others, particularly when an unaligned access crosses a cache-line or page boundary and becomes two trips.

The design consequence is a rule about ownership of layout: alignment is a property of how a structure is laid out, so whoever owns the layout owns the guarantee. A binary format that starts a field at an arbitrary offset is deciding that every reader will either copy the field or pay the unaligned cost, and a hand-written parser that casts a pointer into a byte buffer is trusting the writer's layout choice without checking it.

Primary sources: <https://en.cppreference.com/w/c/language.html> and <https://en.cppreference.com/w/c/language/arith.html>.

## Decision rules

- Record the natural alignment of each field type in the structures on the hot path.
- Record whether the target hardware faults on unaligned access or merely slows.
- Never cast a pointer into a byte buffer at an unaligned offset without a copy or a check.
- Prefer explicit padding fields to compiler-specific packing pragmas for layout control.
- Record any format or protocol whose fields can land at unaligned offsets.
- Verify with a static assertion that the offsets the code assumes are the ones the compiler produced.

## Procedure

1. Write the intended field order and alignment for the structure.
2. Check the offsets with a static assertion.
3. Identify any field whose offset can be externally controlled.
4. Copy or check at those fields rather than casting.
5. Measure the hot path if unaligned access is suspected.
6. Record the layout and the alignment assumptions in the record.

## Anti-patterns

- Casting a buffer pointer to a structure pointer at an arbitrary offset.
- Assuming unaligned access is free because it worked once.
- Using packing pragmas without recording why the layout was compacted.
- Skipping the static offset assertion.
- Letting a wire format dictate alignment without documenting the consequence.

## Done checklist

- [ ] Field alignment recorded.
- [ ] Hardware behaviour on unaligned recorded.
- [ ] External-offset fields identified.
- [ ] Copy or check at those fields.
- [ ] Static offsets asserted.
- [ ] Layout and assumptions recorded.

## Sources

- C language reference on types and alignment: <https://en.cppreference.com/w/c/language.html>
- Arithmetic conversions: <https://en.cppreference.com/w/c/language/arith.html>
- Binary layout context: <https://capnproto.org/encoding.html>
