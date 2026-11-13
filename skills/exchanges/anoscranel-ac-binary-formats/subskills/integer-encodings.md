---
name: integer-encodings
domain: software-engineering/integer-encodings
trigger: "Choosing how integers are encoded in a binary layout."
anti_trigger: "Not for choosing a wire library, and not for floating-point policy."
scope: "Fixed-width, signed, and variable-length encodings and their trade-offs."
status: seedling
---

# Integer encodings

## Standard

An integer in a binary format is a policy, and the policy has three clauses: the width, the signedness handling, and whether the width is fixed or variable. Fixed-width fields are simple to seek and patch but waste space when most values are small; variable-length encodings — varints — spend one byte on small values and more as the number grows, at the cost of not knowing a field's length without reading it.

Signedness is where formats quietly break. A naive varint on a negative number produces its maximum length, because two's-complement negatives are enormous as unsigned values. Production formats fix this with zig-zag encoding, which maps signed values onto the unsigned sequence so small-magnitude negatives stay small. A format that skipped this step pays for every negative number forever.

Primary sources: <https://protobuf.dev/programming-guides/encoding/> and <https://capnproto.org/encoding.html>.

## Decision rules

- Record each integer field's width and its maximum value as an invariant.
- Choose fixed-width for fields that are patched in place; variable-length for streamed or size-dominated formats.
- Encode signed integers with a signedness-preserving scheme, not raw two's-complement in a varint.
- Record the overflow behaviour: a value that exceeds the field width must fail explicitly, not truncate.
- Document lengths in bytes, and note which fields' lengths depend on their values.
- Keep count fields wide enough for the largest collection the format can hold.

## Procedure

1. List every integer field with its plausible range.
2. Choose width and encoding per field against that range.
3. Define signed handling and overflow failure explicitly.
4. Compute the encoded size of the smallest and largest realistic record.
5. Test boundary values: zero, one, the maximum, and one past it.
6. Record the policy per field in the format record.

## Anti-patterns

- Raw two's-complement in a variable-length encoding.
- Silent truncation on overflow.
- A count field too narrow for the collection it sizes.
- Choosing variable-length for a field that must be patched without rewriting the record.
- Assuming the reader's integer type matches the field's width.

## Done checklist

- [ ] Widths and maxima recorded per field.
- [ ] Fixed versus variable chosen with a reason.
- [ ] Signed encoding chosen and documented.
- [ ] Overflow fails loudly.
- [ ] Boundary values tested.
- [ ] Policy in the format record.

## Sources

- Varint and zig-zag encoding, specified: <https://protobuf.dev/programming-guides/encoding/>
- An alternative layout with fixed offsets: <https://capnproto.org/encoding.html>
- Canonical integer serialisation rules, including length: <https://www.rfc-editor.org/rfc/rfc8785.html>
