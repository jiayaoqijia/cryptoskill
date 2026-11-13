---
name: normalization-forms
domain: software-engineering/normalization-forms
trigger: "Making visually identical strings compare equal."
anti_trigger: "Not for validating input bytes (that is utf8-and-malformed-input)."
scope: "NFC and NFD, composed versus decomposed, and choosing one."
status: seedling
---

# Normalization forms

## Standard

Two strings can render identically and differ byte-for-byte. "é" exists as one precomposed character and as "e" followed by a combining accent; both display as the same glyph, and both are valid, but they hash differently, match differently, and sort differently. Normalization applies a canonical rule: one form composes everything (NFC), one decomposes everything (NFD), and either choice makes comparisons honest.

The name is misleading: normalisation is not something that happens naturally in text handling. Most software passes bytes through unchanged, so a file saved by one application and the same file re-saved by another can silently differ, and the bug reports — "the dedupe missed a duplicate", "login fails for the same user" — never mention encoding. The fix is a decision: pick one form per system, apply it at a defined point, and hold every path to it.

## Decision rules

- Choose one normalisation form — typically NFC — for the whole system and write it into the policy.
- Apply normalisation at a defined point, not opportunistically in scattered code.
- Normalise before hashing, deduplicating, or comparing for identity.
- Never normalise away valid distinctions: case and locale folding are separate concerns.
- Note where the store normalises by itself — some databases do — and match the application to it.
- Test round-trip fidelity: normalised text re-normalised must be unchanged.

## Procedure

1. Choose the form from the system's needs and record it.
2. Identify the points where text enters, and apply the form there.
3. Convert existing stores once, in a tested migration, with backup.
4. Verify that hashing and dedup paths operate on normalised text.
5. Confirm the application form matches any store-level normalisation.
6. Add the round-trip test.

## Anti-patterns

- Normalizing in some code paths but not others.
- Converting existing data ad hoc, with no one migration.
- Assuming the database normalises when its configuration says otherwise.
- Treating case-insensitivity as a normalisation concern.
- Hashing raw bytes and wondering why equal-text entries differ.

## Done checklist

- [ ] Form chosen and recorded.
- [ ] Application point defined and applied.
- [ ] Existing data migrated once.
- [ ] Identity paths operate on normalised text.
- [ ] Store normalisation verified and matched.
- [ ] Round-trip test in place.

One caution earns emphasis because it reverses a correct instinct: normalisation is unsuitable for text a user will re-edit in-place, because converting their stored input changes it under them — the right split is to normalise for comparison keys while preserving the original for display and editing, so the two copies serve their two purposes.

## Sources

- Unicode normalization forms: <https://www.unicode.org/reports/tr15/>
- UAX #15 documentation: <https://www.unicode.org/versions/latest/>
- RFC on UTF-8 handling: <https://www.rfc-editor.org/rfc/rfc3629>
