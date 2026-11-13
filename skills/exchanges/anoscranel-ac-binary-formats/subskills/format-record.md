---
name: format-record
domain: software-engineering/format-record
trigger: "Writing the specification record for a binary format."
anti_trigger: "Not for the program's own changelog, and not for choosing a schema language."
scope: "The written format record: layout, decisions, and invariants."
status: seedling
---

# Format record

## Standard

The format record is the specification as a living document: the byte order, every field's offset and encoding, the magic and version constants, the checksum's scope and purpose, and the rules an unknown-version reader follows. It exists because reverse-engineering one's own format from source code is slow, and because a layout that lives only in a struct definition is a private dialect with no evaluator.

Its second function is holding the invariants — the statements that must remain true for old files to stay readable. A count field is never less than zero; a length is counted from the field after it; a version bump does not move the header. Invariants are what a change proposal is checked against, and recording them at design time is what makes a review of a later change possible at all.

A record that lists every invariant with the test command that enforces it turns the specification into something continuous integration can check, and a file layout whose invariants are checked is a format that can still be read after everyone who memorised it has left.

Primary sources: <https://sqlite.org/fileformat2.html> and <https://www.rfc-editor.org/rfc/rfc8785.html>.

## Decision rules

- Record the byte order, field table with offsets, and each field's encoding and width.
- Record the magic, version constants, and the version history with reader obligations.
- Record the checksum scope, its corruption class, and mismatch behaviour.
- Record the format's invariants as numbered statements.
- Record the compatibility rules for unknown extensions.
- Amend by dated entries; never rewrite the history of a released version.

## Procedure

1. Write the field table from the implementation, then verify the implementation from the table.
2. Record constants and the version history.
3. Write the invariants as checkable statements.
4. Record the checksum scope and behaviour.
5. Cross-reference the round-trip test commands that enforce each invariant.
6. Date every amendment and keep the released history intact.

## Anti-patterns

- The specification is the source code, uncommented.
- Offsets updated in one place but not the table.
- Invariants implied by tests rather than written as statements.
- A rewrite of version history that loses the promises made by old versions.
- No verification direction: table written from the code, never re-checked against the encoding.

## Done checklist

- [ ] Field table verified both directions.
- [ ] Constants and history recorded.
- [ ] Invariants written as numbered statements.
- [ ] Checksum scope and behaviour recorded.
- [ ] Test commands cross-referenced.
- [ ] Amendments dated.

## Sources

- A production format specification, kept as documentation: <https://sqlite.org/fileformat2.html>
- Canonical-serialisation invariants stated as rules: <https://www.rfc-editor.org/rfc/rfc8785.html>
- Tagged encoding with stated skip behaviour: <https://protobuf.dev/programming-guides/encoding/>
