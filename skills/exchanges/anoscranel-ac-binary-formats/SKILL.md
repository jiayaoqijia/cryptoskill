---
name: ac-binary-formats
description: "Designing and reading binary data formats: endianness and byte order as a declared choice, integer encoding from fixed-width to varints, tagged and schema-evolvable layouts, alignment padding and struct packing, checksums and magic numbers, versioning a binary layout, and the written format record. It explains how bytes on disk or wire are laid out and read back; it never recommends a serialization library and never promises compactness. Use when asking \"endianness\", \"byte order\", \"varint\", \"binary file format\", \"struct packing\", \"wire format\", \"schema evolution\", \"file format design\", \"checksum at the end\", \"magic number\", \"fixed versus variable length\", \"alignment padding\". Not for API contract design in general (ac-api-design), not for generated code from schemas (ac-code-generation-and-apis), not for text encoding and Unicode (ac-text-encoding)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Binary formats

## Overview

A binary format is a set of decisions about how values become bytes: which end is first, how wide an integer is, where a field ends, and how a reader three years later knows any of this. Every format makes these decisions explicitly or by accident, and the accidental ones are the ones that cannot be extended later because they were never written down.

This skill covers those decisions as design work: byte order as a declared property of the format rather than of the machine, integer encodings from fixed-width to variable-length, the tagged-versus-positional choice and what it costs in size and evolvability, padding and alignment, integrity checks and magic numbers, and how to version a layout after it ships. Text encoding is a separate skill; generated clients are a separate skill.

Primary sources: <https://protobuf.dev/programming-guides/encoding/> and <https://sqlite.org/fileformat2.html>.

## When to use

- When designing a file format or wire layout from scratch.
- When reading an unfamiliar binary format without documentation.
- When a format must evolve without breaking old readers.
- When choosing between a hand-rolled layout and a schema language.

## When NOT to use

- For JSON and HTTP resource contracts (use ac-api-design).
- For generating typed code from an existing schema (use ac-code-generation-and-apis).
- For Unicode, normalization, and text handling (use ac-text-encoding).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/endianness-and-byte-order.md` | `software-engineering/endianness-and-byte-order` | Big-endian, little-endian, declared once, and swapping bytes across machines. |
| `subskills/integer-encodings.md` | `software-engineering/integer-encodings` | Fixed-width, signed, and variable-length encodings and their trade-offs. |
| `subskills/tagged-versus-positional.md` | `software-engineering/tagged-versus-positional` | Field tags, positional layouts, and what each allows later. |
| `subskills/padding-and-alignment.md` | `software-engineering/padding-and-alignment` | Padding bytes, natural alignment, and formats that forbid them. |
| `subskills/checksums-and-magic.md` | `software-engineering/checksums-and-magic` | Magic numbers, version heads, and checksums that detect the right failure. |
| `subskills/format-versioning.md` | `software-engineering/format-versioning` | Evolving a shipped layout without breaking existing readers. |
| `subskills/format-record.md` | `software-engineering/format-record` | The written format record: layout, decisions, and invariants. |

## Status and honest limits

A format's correctness is only as good as its specification: an undocumented layout is a private dialect that dies with its author, and reverse-engineering one is slow and error-prone in ways this skill can outline but not eliminate. The encodings described here are stable; the tooling is not, and nothing here recommends a specific library. A poorly chosen checksum gives false confidence — the design decision is which corruptions it claims to detect, stated honestly in the record.
