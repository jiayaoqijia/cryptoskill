---
name: ac-text-encoding
description: "Handling text as bytes without corrupting it: what UTF-8 actually encodes and its malformed forms, normalization forms and why two identical-looking strings differ, grapheme clusters versus code points versus bytes, encoding boundaries at input and output, mojibake and how it happens, and the written text-policy record. It explains how text is represented and where it breaks; it never recommends a library and never guesses an encoding. Use when asking \"UTF-8\", \"encoding error\", \"mojibake\", \"why do these strings not match\", \"normalization form\", \"NFC versus NFD\", \"grapheme cluster\", \"code point\", \"invalid byte sequence\", \"text corruption\", \"why does my hash of the same text differ\". Not for locale formatting and language presentation (ac-i18n-and-localisation), not for collation and search (ac-i18n-and-localisation), not for parsing structured data formats (ac-api-design)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Text encoding

## Overview

Text in software is bytes with an interpretation, and most text bugs are an interpretation mismatch: bytes written as one encoding and read as another, two strings that render identically but differ underneath because they are built from different character sequences, or a truncation that splits a multi-byte character in half and produces corruption the system then stores. UTF-8 is the default answer, but using it correctly requires knowing what it does not promise — that two visually equal strings are byte-equal.

This skill covers the representation layer beneath localisation: the encoding itself and its malformed forms, the normalisation that makes comparisons honest, the three units that get confused (byte, code point, grapheme cluster), the boundaries where conversion must happen, and the mojibake signatures that identify which mismatch occurred. Presenting text in a language's conventions belongs to the localisation skill; this one is about keeping the bytes intact.

Primary sources: <https://www.unicode.org/versions/latest/> and <https://www.rfc-editor.org/rfc/rfc3629>.

## When to use

- Storing, transmitting, or comparing text and getting mismatches or corruption.
- Building strings from parts, truncating, or hashing text.
- Diagnosing mojibake and identifying which encoding confusion produced it.
- Setting a system-wide text policy.

## When NOT to use

- For locale formats, translations, plural rules (use ac-i18n-and-localisation).
- For collation and search across scripts (use ac-i18n-and-localisation).
- For text-heavy corpus or search systems (use ac-retrieval-and-vector-systems).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/utf8-and-malformed-input.md` | `software-engineering/utf8-and-malformed-input` | The encoding, its byte forms, overlong forms, and rejecting bad input. |
| `subskills/normalization-forms.md` | `software-engineering/normalization-forms` | NFC and NFD, composed versus decomposed, and choosing one. |
| `subskills/units-of-text.md` | `software-engineering/units-of-text` | Bytes, code points, and grapheme clusters, and which operation needs which. |
| `subskills/encoding-boundaries.md` | `software-engineering/encoding-boundaries` | Where conversion happens and the rule for each boundary. |
| `subskills/mojibake-diagnosis.md` | `software-engineering/mojibake-diagnosis` | Reading the garbage to identify the mismatch that made it. |
| `subskills/text-in-storage.md` | `software-engineering/text-in-storage` | Column encodings, collation interactions, and lengths that lie. |
| `subskills/text-policy-record.md` | `software-engineering/text-policy-record` | The written record: encoding, normalization, and boundary rules. |

## Status and honest limits

Encoding behaviour is correct only where every layer agrees: the source of the bytes, the transport, the store, and the reading code. Historical data predating a policy may never reveal which encoding it was written in, and the best available answer for it is a documented assumption, not a certainty. Nothing recommends a library, and the Unicode Standard itself changes between versions — new characters are assigned, which changes what any fixed version's tables know.
