---
name: archive-writes
domain: research-operations/archive-writes
trigger: "\"save this research\", \"write the study to the research root\", \"where does this report live\", \"pick up where I left off\"."
anti_trigger: "The content of the audit trail itself (subskills/evidence-ledger.md); the reader-facing deliverable (subskills/write-report.md)."
scope: "Writing the study into the research root: the research folder layout, incremental appends so a dead agent leaves completed work on disk, status lifecycle"
status: "seedling"
---

# Archive writes

## Standard

- One home. The study lives under the research root at
 `<research-root>/<slug>/`. Nothing research-shaped is
 created or left in home directories, the workspace, or temporary scratch,
 and nothing is duplicated into local copies.
- Write incrementally. Create the output files first, then append each
 section as it completes, never one dump at the end. The file is the
 checkpoint; a dead mid-study agent still leaves its completed sections on
 disk.
- Files carry a status lifecycle in frontmatter: seedling, growing, verified,
 stale, deprecated. Contradicting evidence means update or
 mark stale, never a silent overwrite.
- Supersede, never append contradictions. When a fact changes, replace the
 stale record; stale notes are worse than none.

## Decision rules

- Light study: one report file plus a folder of source files. Full study:
 plan, sources folder, findings folder, final report.
- Verify the target path exists before writing any file into it; never
 compose a path from memory.
- If a topic already has a study dossier, extend that dossier in place. Never
 fork the topic into a second folder.

## Procedure

1. Verify the research root exists.
2. Create the study folder and the plan file first, before any retrieval.
3. Create the report file early with its frontmatter and empty sections.
4. Append each section as it completes; sources land as one file per source.
5. Set or update frontmatter status as the study moves.
6. The final report section is the last append, never the only write.

## Anti-patterns

- One end-of-run dump. A crash then erases the whole study.
- A working copy in a home or scratch folder "just for now".
- A folder rewritten wholesale on every pass, destroying the checkpoint trail.
- A forked second dossier on a topic the research root already holds.

## Done checklist

- The study folder sits under the research root, and only there.
- The write history shows incremental appends, not one final dump.
- Frontmatter status matches the study's real state.
- No duplicate of the study exists outside the research root.

The archive should record what was not saved as well as what was, because a corpus with gaps looks complete from the inside and the missing pages are discovered exactly when a claim needs them. A line stating the coverage limit is cheaper than a re-run.

## Sources

- <https://osf.io/prereg/>
- <https://arxiv.org>
