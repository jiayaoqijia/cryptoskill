---
name: encoding-boundaries
domain: software-engineering/encoding-boundaries
trigger: "Deciding where conversion happens between a system and the outside."
anti_trigger: "Not for malformed-input handling rules (that is utf8-and-malformed-input)."
scope: "Where conversion happens and the rule for each boundary."
status: seedling
---

# Encoding boundaries

## Standard

A system handles one encoding internally — UTF-8, by policy — and every other encoding exists only at the edges: files received, feeds ingested, protocols declared by a standard, output for consumers with declared needs. The boundary rule keeps the interior clean: convert at ingress to the internal form, convert at egress for consumers that declare another, and never let an alternate encoding enter the system as data that later code "handles" implicitly.

The classic violation is duct tape: a feed arrives in a legacy encoding, a function converts per-record somewhere mid-pipeline, one caller forgets to call it, and the system now contains mixed encodings that no single pass can repair. Doing conversion exactly once, at the entry, from a declared source, is the entire discipline. The same rule applies to output: a consumer that needs something else gets it at the egress, not from code scattered through the render path.

## Decision rules

- Declare the internal encoding as policy; all interchange inside it.
- Convert at ingress, from a declared source encoding; reject what cannot be converted.
- Convert at egress only for consumers that declare another encoding.
- Never convert mid-pipeline for "convenience" of one component.
- Record the source encoding of every fixed-format feed and message.
- Test each boundary with both a valid and a malformed sample.

## Procedure

1. Enumerate the boundaries: inputs from files, feeds, interfaces, and users.
2. Declare each boundary's source encoding or the negotiation rule.
3. Place conversion at the boundary, once.
4. Apply the same review to egress points with declared consumers.
5. Validate each side of the boundary with known samples.
6. Record the boundary list and their encodings in the text policy.

## Anti-patterns

- A conversion function called by some components but not others.
- Sniffing the encoding from content instead of using a declared source.
- Conversions in the middle of the pipeline, repeated or skipped.
- An output that converts twice, compounding errors.
- A boundary with no declared source, where every record is a guess.

## Done checklist

- [ ] Boundaries enumerated.
- [ ] Source encoding declared per boundary.
- [ ] Conversion at the boundary, once.
- [ ] Egress conversions only for declared needs.
- [ ] Validation samples pass at each boundary.
- [ ] Policy records the boundary list.

## Sources

- Character set negotiation: <https://www.rfc-editor.org/rfc/rfc3629>
- The Unicode Standard on encodings: <https://www.unicode.org/versions/latest/>
- IANA character set registry: <https://www.iana.org/assignments/character-sets/>
