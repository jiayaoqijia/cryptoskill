---
name: format-versioning
domain: software-engineering/format-versioning
trigger: "Evolving a shipped binary layout without breaking readers."
anti_trigger: "Not for API versioning in general, and not for schema migration of databases."
scope: "Evolving a shipped layout without breaking existing readers."
status: seedling
---

# Format versioning

## Standard

A binary format's version field is a promise about how changes arrive: a version's meaning is fixed forever, and a new version states exactly what an older reader should do with it. The discipline is asymmetric. A writer may add, because addition is cheap in a tagged layout; a reader must tolerate, because it cannot know which writers it will meet; and a field's meaning may never change in place — only be extended beside itself.

The test is the mixed fleet. Old readers meet new files and new readers meet old files, and both directions must be verified before the new version ships. Granularity matters: version the whole format coarsely and old readers reject whole files they could mostly read; version each record and compatibility becomes per-record, and the reader's skip logic becomes the compatibility story.

Primary sources: <https://sqlite.org/fileformat2.html> and <https://protobuf.dev/programming-guides/encoding/>.

## Decision rules

- Fix a version field at a stable offset that does not move across versions.
- State the reader's obligation for each change: skip, default, or reject-fail.
- Add fields by appending tags or trailing sections — never repurpose old bytes.
- Record the exact change made at each version number in a public history.
- Test both directions against the mixed fleet before release.
- When a change is genuinely breaking, use a new magic rather than a version jump.

## Procedure

1. Reserve a version field at a fixed offset with a stable meaning.
2. Draft the change and classify it: additive, default-able, or breaking.
3. Implement the old reader's skip or default behaviour and the new writer's output.
4. Run both-direction tests: old reader on new file, new reader on old file.
5. Publish the version's change entry in the history.
6. Record the compatibility statement for each affected tool in the format record.

## Anti-patterns

- Repurposing a field's meaning without a version bump.
- A version field no reader routes on, so it is decoration.
- Compatibility untested in the old-reads-new direction.
- Per-format coarse versioning for a change that only affects one record type.
- Silent breaking changes detected in production rather than by test.

## Done checklist

- [ ] Version field at a stable offset.
- [ ] Change classified and its reader behaviour defined.
- [ ] Change implemented as append, not repurpose.
- [ ] Both-direction tests pass.
- [ ] Version history published.
- [ ] Compatibility statement recorded.

## Sources

- A file format's documented version history and compatibility practice: <https://sqlite.org/fileformat2.html>
- Additive field evolution by tag: <https://protobuf.dev/programming-guides/encoding/>
- Unknown-extension tolerance rules: <https://www.rfc-editor.org/rfc/rfc9000.html>
