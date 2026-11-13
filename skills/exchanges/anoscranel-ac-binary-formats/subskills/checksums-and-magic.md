---
name: checksums-and-magic
domain: software-engineering/checksums-and-magic
trigger: "Adding magic numbers, version heads, and checksums to a format."
anti_trigger: "Not for cryptographic signature and key management, and not for transport integrity."
scope: "Magic numbers, version heads, and checksums that detect the right failure."
status: seedling
---

# Checksums and magic

## Standard

A format's head is its handshake: a magic number that says "this is my format", a version field that says which dialect, and optionally a length that says how much to trust. The magic value is chosen so that a casual text editor or a wrong-order reader fails immediately instead of misinterpreting every field that follows — the same constant read as text and as the wrong endianness should never look valid.

A checksum is a claim about which corruptions it detects, and the claim must be honest. A weak sum detects incidental bit rot and truncated writes; it does not detect deliberate alteration and can be recomputed by any attacker. Record the intended adversary — the void, not a person — and pick the check that matches, then say what it does not cover rather than implying safety.

Primary sources: <https://sqlite.org/fileformat2.html> and <https://www.rfc-editor.org/rfc/rfc9000.html>.

## Decision rules

- Choose a magic constant that is invalid as text and order-sensitive, and record it.
- Put the version adjacent to the magic so a reader can route before parsing.
- Record what the checksum is for: accidental corruption, truncation, or nothing.
- Checksum the payload, not the whole file including the checksum field itself.
- Define the failure behaviour on mismatch: reject, repair, or log-and-continue — chosen in advance.
- Never present a checksum as tamper evidence; that is a different tool with keys.

## Procedure

1. Pick a magic constant and verify it fails as text and under byte-swapped reads.
2. Place magic, version, and length at fixed offsets in a header.
3. Choose a checksum appropriate to the corruption class expected.
4. Define computation scope and the mismatch failure behaviour.
5. Test: corrupt one byte, truncate the file, and swap the order — all must fail as designed.
6. Record constants, scope, and failure behaviour in the format record.

## Anti-patterns

- No magic value, so any file is tentatively valid.
- A checksum presented as a security control.
- Computing the checksum over itself, making it trivially satisfiable.
- Mismatch handling decided at two in the morning instead of in the specification.
- A version field that no reader actually routes on.

## Done checklist

- [ ] Magic constant chosen and tested.
- [ ] Version placed in the header.
- [ ] Checksum purpose stated.
- [ ] Computation scope defined.
- [ ] Mismatch behaviour chosen and tested.
- [ ] Constants recorded.

## Sources

- A file format with documented magic and page checksums: <https://sqlite.org/fileformat2.html>
- Transport integrity chosen per connection, with offsets: <https://www.rfc-editor.org/rfc/rfc9000.html>
- Length-prefixed value framing: <https://protobuf.dev/programming-guides/encoding/>
