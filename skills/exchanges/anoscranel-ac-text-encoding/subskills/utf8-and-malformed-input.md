---
name: utf8-and-malformed-input
domain: software-engineering/utf8-and-malformed-input
trigger: "Understanding what UTF-8 encodes and what to do with invalid bytes."
anti_trigger: "Not for normalization or comparison (that is normalization-forms)."
scope: "The encoding, its byte forms, overlong forms, and rejecting bad input."
status: seedling
---

# UTF-8 and malformed input

## Standard

UTF-8 encodes each character as one to four bytes, with the leading byte announcing how many follow. The design makes most corruption detectable: a byte sequence that breaks the announced pattern — a continuation byte without its leader, a truncated multi-byte character at a cut point — is malformed, and a correct reader must report it rather than silently substitute. Input that arrives with invalid bytes is not text; it is bytes claiming to be text and failing.

The critical engineering rule is validation at the boundary: bytes from outside enter the system as UTF-8 or are rejected with a diagnostic, never "cleaned" by replacement characters and passed on. Replacement seems kind and is destructive: the original bytes are gone, and every later comparison, export, or round-trip carries the scar. A rejection at the entry point preserves the caller's chance to fix their encoding; a silent replacement deep in the system buries the cause.

## Decision rules

- Validate UTF-8 at every input boundary; reject with a diagnostic rather than replace.
- Never strip or "clean" invalid bytes mid-pipeline; the cleaning destroys evidence.
- Truncate only on character boundaries, never on a byte count alone.
- Overlong forms — a character encoded in more bytes than needed — are malformed; reject them.
- Record the encoding of every file and interface explicitly; never infer it from content.
- Where legacy encodings must be accepted, convert once at the edge and record it.

## Procedure

1. Enumerate the system's text entry points.
2. Add or verify validation at each, with rejection as the failure path.
3. Test with known malformed sequences: truncated leaders, lone continuations, overlong.
4. Audit truncation code for character-boundary awareness.
5. Mark explicit encodings on files and interfaces.
6. Record edge conversions for legacy inputs.

## Anti-patterns

- Silent replacement characters at input, hiding the problem downstream.
- Byte-count truncation slicing a character in half.
- Guessing encoding from a byte-order mark only.
- Passing bytes through on the hope they are valid.
- Cleaning invalid input with lossy filters and calling it done.

## Done checklist

- [ ] Entry points enumerated and validating.
- [ ] Rejection with diagnostics confirmed by test.
- [ ] Malformed sequences tested.
- [ ] Truncation boundary-safe.
- [ ] Encodings explicit on files and interfaces.
- [ ] Legacy edge conversions recorded.

## Sources

- UTF-8, a transformation format of Unicode: <https://www.rfc-editor.org/rfc/rfc3629>
- Unicode Standard, character encoding forms: <https://www.unicode.org/versions/latest/>
- OWASP input validation guidance: <https://owasp.org/www-project-proactive-controls/>
