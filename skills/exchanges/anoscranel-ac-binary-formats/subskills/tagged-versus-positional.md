---
name: tagged-versus-positional
domain: software-engineering/tagged-versus-positional
trigger: "Deciding whether fields carry tags or rely on fixed positions."
anti_trigger: "Not for schema language selection, and not for text formats."
scope: "Field tags, positional layouts, and what each allows later."
status: seedling
---

# Tagged versus positional

## Standard

A positional format fixes the meaning of a byte by where it sits: the first four bytes are the version, the next eight the timestamp, and a reader that knows the layout can read blind. A tagged format carries a field identifier with each value, so a reader learns the structure from the file itself. The choice is the compactness-versus-evolvability trade, made once and lived with.

The consequence appears the first time a field must be added. A positional format can only append at the end, and every inserted field rewrites every offset; a tagged format inserts a new tag and old readers skip what they do not know. The cost is measured in bytes — a tag per field is overhead on every record — and in reading, because a tagged reader must be able to skip an unknown tag's payload, which requires the value encoding to carry its own length.

Primary sources: <https://protobuf.dev/programming-guides/encoding/> and <https://sqlite.org/fileformat2.html>.

## Decision rules

- Choose positional when the record set is fixed, size dominates, and fields are patched in place.
- Choose tagged when the format must evolve across independently deployed readers.
- If tagged, require that every value encoding is self-delimiting so unknown tags can be skipped.
- Reserve a tag-range policy for future and experimental fields.
- For positional formats, version the layout and never insert fields before the end.
- State, for either choice, what an old reader does with a field it does not understand.

## Procedure

1. Inventory the fields and their stability over the format's expected life.
2. Decide tagged or positional per record type, not necessarily per format.
3. If tagged, define the tag width and the skip rules for unknown tags.
4. If positional, fix insertion policy: append-only, with a version field.
5. Test forward compatibility: a new writer's output read by an old reader.
6. Record the decision and the compatibility rule.

## Anti-patterns

- A positional format that inserts a field in the middle between versions.
- Tagged values whose payloads have no length, so skipping is impossible.
- Mixing the two without stating which records follow which rule.
- Assuming readers upgrade in step with writers.
- No policy for unknown fields, decided before one exists.

## Done checklist

- [ ] Fields inventoried with stability.
- [ ] Tagged or positional chosen per record type.
- [ ] Skip rules defined for unknown tags.
- [ ] Append-only policy fixed for positional records.
- [ ] Forward compatibility tested.
- [ ] Decision recorded.

## Sources

- Tag-based encoding with self-delimiting values: <https://protobuf.dev/programming-guides/encoding/>
- Positional layout with a versioned header: <https://sqlite.org/fileformat2.html>
- A format that mixes header positionality with payload flexibility: <https://sqlite.org/fileformat2.html>
