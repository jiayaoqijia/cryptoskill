---
name: mojibake-diagnosis
domain: software-engineering/mojibake-diagnosis
trigger: "Reading corrupted text to identify the encoding mismatch that made it."
anti_trigger: "Not for preventing the mismatch (that is encoding-boundaries)."
scope: "Reading the garbage to identify the mismatch that made it."
status: seedling
---

# Mojibake diagnosis

## Standard

Mojibake — "Ã©" for "é", "ä»Š" replacing readable text with CJK noise — is not damage; it is text read through the wrong interpretation, and the specific garbage names the mismatch. Accented characters becoming two-character sequences starting with "Ã" is UTF-8 bytes read as Latin-1. Readable text becoming "???�?" is a code page forcing every unknown character into a question mark. A string of percent signs inside payloads is an encoding that was never decoded at all.

The diagnostic method is the reverse of the corruption: take the observed bytes, and ask which single reinterpretation produces the intended text. The replacement patterns are few and characteristic, so identification is usually quick; the important part is stopping there and fixing the boundary rather than building a repair pass that converts the mangled form back — because every such repair is a guess about content that only sometimes works!

## Decision rules

- Identify the pattern first: Latin-1 misread, code-page loss, or double-encoding.
- Locate the boundary where the wrong interpretation was applied.
- Fix the boundary; never add repair conversions for already-corrupted data paths.
- Where corruption is already stored, decide: reconvert from a source of truth, or record loss.
- Document each recognised mojibake pattern with its cause for future response.
- Test the fixed boundary with the original sample that exposed it.

## Procedure

1. Capture the corrupt sample and its bytes, not a screenshot describing it.
2. Match the pattern against the known mismatch signatures.
3. Trace the boundary that applied the wrong interpretation.
4. Correct the boundary and verify with the original sample.
5. For already-stored corruption, decide recovery or record the loss explicitly.
6. Record the pattern and cause with the case.

## Anti-patterns

- Sending mojibake through a "fix encoding" utility repeatedly, hoping.
- Repair passes that guess content character by character.
- Blaming the user's device when the boundary is in your pipeline.
- Fixing the display without fixing the write path that stored corruption.
- Not keeping the sample that made diagnosis possible.

## Done checklist

- [ ] Sample with bytes captured.
- [ ] Pattern identified from the signature.
- [ ] Boundary located and corrected.
- [ ] Original sample now passes through correctly.
- [ ] Stored corruption recovered or recorded as loss.
- [ ] Pattern and cause documented.

## Sources

- UTF-8 byte structure, for recognising sequences: <https://www.rfc-editor.org/rfc/rfc3629>
- The Unicode Standard, malformed sequences: <https://www.unicode.org/versions/latest/>
- IANA charset registry: <https://www.iana.org/assignments/character-sets/>
