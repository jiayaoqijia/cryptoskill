---
name: padding-and-alignment
domain: software-engineering/padding-and-alignment
trigger: "Handling alignment and padding in a binary layout."
anti_trigger: "Not for memory-layout tuning, and not for CPU alignment in code."
scope: "Padding bytes, natural alignment, and formats that forbid them."
status: seedling
---

# Padding and alignment

## Standard

In memory, a CPU's preferred alignment inserts padding between fields, and a naive serialisation that dumps a struct's memory inherits that padding as format — making the layout depend on the compiler and the platform that happened to build the writer. A deliberate format instead specifies every byte, and the specification says either "no padding" or "padding with a defined filler value at these offsets".

The choice matters at the boundaries. A format with no padding is denser but may hand a reader unaligned values, which some architectures accept slowly and others trap on; a format with alignment padding is faster to read into matched memory but larger and more sensitive to version changes. Both are legitimate; what is not legitimate is inheriting the compiler's decisions unexamined.

Primary sources: <https://www.rfc-editor.org/rfc/rfc8785.html> and <https://sqlite.org/fileformat2.html>.

## Decision rules

- Specify padding explicitly: forbidden entirely, or present with a fixed filler byte at documented offsets.
- Never serialise a struct's raw memory and call it a format.
- If the reader maps files directly into memory, state the alignment assumption and which platforms break it.
- Record the offset of every field in the specification so padding is visible, not inferred.
- Use fixed filler bytes, and validate them on read as a cheap consistency check.
- If a pad byte must be skipped, state what values it may legally hold.

## Procedure

1. Lay out each record with explicit offsets for every field.
2. Decide padding policy per record and write the offsets into the specification.
3. If padding exists, define the filler value and check it on read.
4. If direct-mapping readers exist, verify alignment on the target platforms.
5. Test that the writer's output is byte-identical across build configurations.
6. Record offsets and the padding policy in the format record.

## Anti-patterns

- Writing memory dumps and depending on the build's padding.
- Padding present but its contents undefined, so bytes differ between writers.
- Hidden alignment requirements that trap on strict architectures.
- Offsets implied by code order rather than stated in the specification.
- Changing a layout without recomputing every stated offset.

## Done checklist

- [ ] Offsets explicit in the specification.
- [ ] Padding policy decided and documented.
- [ ] Filler value fixed and validated.
- [ ] Alignment verified for direct-mapping readers.
- [ ] Byte-identical output across builds tested.
- [ ] Offsets recorded.

## Sources

- A canonical format that forbids padding: <https://www.rfc-editor.org/rfc/rfc8785.html>
- A file format with fully specified cell layouts: <https://sqlite.org/fileformat2.html>
- Encoding without memory-layout inheritance: <https://capnproto.org/encoding.html>
