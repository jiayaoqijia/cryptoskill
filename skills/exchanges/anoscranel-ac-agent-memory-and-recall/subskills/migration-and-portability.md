---
name: migration-and-portability
domain: prompt-engineering/migration-and-portability
trigger: "Keeping memory alive when the storage, system, or format under it changes."
anti_trigger: "Not for building the index on the new system, and not for governance."
scope: "Moving memory when infrastructure dies; format and export discipline."
status: seedling
---

# Migration and portability

## Standard

Memory outlives tools. The first system is rarely the last; formats change, products die, files move. The portable core of a memory is its semantics: the fact, the date, the provenance, the links, the lifecycle state. Store those in a plain, documented format — a file that reads as text, a schema that names its own fields — and any future system can read the past. Store them in a format only one tool understands, and the memory dies with the tool.

The export habit costs almost nothing and buys everything. Memory is exported or backed up regularly enough that a migration is a restore, not a reconstruction. The loss test is run before it is needed: what would be lost tomorrow if the storage vanished today? If the answer is anything that exists nowhere else, the memory is not portable yet.

Primary sources: <https://www.gwern.net/About-This-Website> and <https://en.wikipedia.org/wiki/Personal_knowledge_base>.

## Decision rules

- Keep the memory's canonical form in a plain, documented format.
- Export on a stated cadence, at least once per long cycle of work.
- Name the fields: fact, date, provenance, tags, links, lifecycle state.
- Run the loss test now, not after the tool breaks.
- Migrate the system, not the memory: the notes' semantics are the asset; the store is plumbing.
- When a tool dies, migrate the notes; do not transliterate the tool's conventions.

## Procedure

1. Pick or verify a plain-text canonical format with named fields.
2. Export the whole memory on the stated cadence.
3. Restore-check the export in a second location; an unrestored backup is a hope.
4. Run the loss test: restore a recent export and confirm nothing exists only in the live store.
5. At migration time, map the fields one-to-one into the new system.
6. Record the migration date and the field mapping in the memory record.

## Anti-patterns

- Memory locked in one tool's proprietary store with no export.
- Switching stores by transliterating tool conventions rather than migrating note semantics.
- Backups that have never been restored.
- Migrating only the current notes and dropping the superseded history.
- Assuming the current format is permanent.

## Done checklist

- [ ] Canonical plain format used.
- [ ] Fields named in the schema.
- [ ] Export on a stated cadence.
- [ ] Restore-check passed at least once.
- [ ] Loss test run.
- [ ] Field mapping recorded at migration.

## Sources

- Stable long-lived content practice: <https://www.gwern.net/About-This-Website>
- Knowledge-base portability: <https://en.wikipedia.org/wiki/Personal_knowledge_base>
- Long-term preservation context: <https://en.wikipedia.org/wiki/Knowledge_management>
