---
name: endianness-and-byte-order
domain: software-engineering/endianness-and-byte-order
trigger: "Deciding and implementing byte order in a binary format."
anti_trigger: "Not for text encoding, and not for choosing a serialization library."
scope: "Big-endian, little-endian, declared once, and swapping bytes across machines."
status: seedling
---

# Endianness and byte order

## Standard

Byte order is a property of the format, not of the machine that happens to write it. A format declares one order — network byte order is big-endian by long convention — and every field of more than one byte is written that way whatever the host CPU prefers. Readers that run on a machine of the other persuasion swap explicitly, and the swap is a documented step rather than a coincidence of the platform.

The failure mode is silent mismatch. A four-byte integer written little-endian and read big-endian does not produce an error; it produces a startlingly large number, and the bug surfaces three layers away from its cause. Defensive formats make the order verifiable: a known magic value at a fixed offset encodes a four-byte constant that differs between the two orders, so a wrong-order reader detects itself on the first read instead of misreading every field.

Primary sources: <https://www.rfc-editor.org/rfc/rfc9000.html> and <https://sqlite.org/fileformat2.html>.

## Decision rules

- Declare the format's byte order in the specification and apply it to every multi-byte field.
- Prefer big-endian for network-facing formats by convention; state the choice either way.
- Never let the host machine's native order decide implicitly — serialise explicitly.
- Include a multi-byte magic value at a fixed offset so wrong-order reads fail loudly.
- Record which fields, if any, deviate from the format's declared order, and why.
- Test reading on a machine of the opposite order, or simulate the swap.

## Procedure

1. Write the byte order decision into the format specification.
2. Implement serialisation with explicit byte-order conversion, not memcpy of host memory.
3. Place a magic constant that distinguishes the orders.
4. Add a round-trip test that reads what was written on the opposite-order host.
5. Verify the magic check rejects a wrong-order file.
6. Record the decision and the test command in the format record.

## Anti-patterns

- Writing host memory directly and calling the result a format.
- Mixing orders within one format without a per-field note.
- Assuming every reader shares your platform.
- Discovering the order by misreading a value instead of by reading a magic.
- Omitting the order from the specification because "it's obvious".

## Done checklist

- [ ] Byte order declared in the specification.
- [ ] Explicit conversion at every multi-byte field.
- [ ] Magic constant detects wrong-order reads.
- [ ] Round-trip tested across orders.
- [ ] Deviations documented.
- [ ] Decision recorded.

## Sources

- Transmission protocol field ordering: <https://www.rfc-editor.org/rfc/rfc9000.html>
- A production file format's documented layout: <https://sqlite.org/fileformat2.html>
- Schema-driven encoding with declared types: <https://protobuf.dev/programming-guides/encoding/>
