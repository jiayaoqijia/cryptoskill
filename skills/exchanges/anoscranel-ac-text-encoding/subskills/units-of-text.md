---
name: units-of-text
domain: software-engineering/units-of-text
trigger: "Knowing which unit an operation needs: byte, code point, or grapheme."
anti_trigger: "Not for normalization rules (that is normalization-forms)."
scope: "Bytes, code points, and grapheme clusters, and which operation needs which."
status: seedling
---

# Units of text

## Standard

Text has three units that code confuses constantly. The byte is the storage unit; the code point is the character unit; the grapheme cluster is the human unit — what a reader perceives as one character, which can be several code points. "é" as e-plus-accent is two code points but one grapheme; a flag emoji is several code points but one grapheme; a truncation limit measured in code points can split a grapheme and show half a character.

Each operation has a correct unit and bugs live in the mismatches. Length limits for human display should count graphemes; wire and storage sizes count bytes; character-level logic rarely wants code points directly but gets them from a naive "length". Counting the wrong unit is invisible until an accented name, an emoji, or a non-Latin script arrives.

## Decision rules

- State the unit for every text measurement: bytes for size, graphemes for display limits.
- Truncation for display must cut on grapheme boundaries.
- Storage and wire lengths count bytes; say so where the number is used.
- Do not use string "length" for display limits without knowing what it counts.
- Test the unit-aware paths with multi-code-point examples: emoji, combining accents.
- Where a protocol fixes its own unit, match it exactly rather than approximating.

## Procedure

1. Inventory text measurements in the code: limits, lengths, validations.
2. Classify each by needed unit: byte, code point, or grapheme.
3. Fix mismatches, starting with display truncation.
4. Add multi-code-point test cases to each path.
5. Document the unit beside each limit, not in tribal memory.
6. Record the inventory and decisions in the text policy.

## Anti-patterns

- A 140-code-point limit enforced on a 140-grapheme requirement.
- Byte truncation for display.
- Testing lengths only with ASCII.
- Assuming "characters" in documentation means graphemes.
- Mixing units in one validation chain.

## Done checklist

- [ ] Text measurements inventoried.
- [ ] Needed unit classified per measurement.
- [ ] Mismatches fixed.
- [ ] Multi-code-point tests added.
- [ ] Units documented at each limit.
- [ ] Policy updated.

A corollary worth writing beside every limit: the safe default is graphemes for anything a human sees, bytes for anything a machine pays for, and code points only where a protocol's standard names them — and any limit whose unit is undocumented should be treated as a defect, not an assumption.

## Sources

- Unicode text segmentation, grapheme clusters: <https://www.unicode.org/reports/tr29/>
- UAX #29 documentation: <https://www.unicode.org/versions/latest/>
- UTF-8 byte structure: <https://www.rfc-editor.org/rfc/rfc3629>
