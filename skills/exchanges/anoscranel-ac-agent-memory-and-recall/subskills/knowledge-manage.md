---
name: knowledge-manage
domain: prompt-engineering/knowledge-manage
trigger: "Governing the memory corpus as a system rather than a pile of notes."
anti_trigger: "Not for writing individual notes, and not for migration mechanics."
scope: "Memory cleanup, archive versus delete, and governance of the whole corpus."
status: seedling
---

# Knowledge manage

## Standard

A memory corpus is governed, not merely accumulated. The governing questions are asked on a cadence: what domains have grown without review, what notes were written once and never read, where duplicates have crept in, what the absences say about what sessions are not writing down. Memory hygiene is quiet work; the corpus trends toward bloat and confusion by default because writing is easy and pruning takes judgement.

The pruning test is the same one that governs first writes: would a future session act differently because this note exists? A note that fails the test now — superseded, or about a system long gone — is archived rather than deleted, because the history of what was known is used more often than expected: debugging an old incident, dating a decision, or explaining why the current configuration is what it is. Archive keeps evidence; delete destroys it.

Primary sources: <https://en.wikipedia.org/wiki/Knowledge_management> and <https://www.gwern.net/About-This-Website>.

## Decision rules

- Review corpus counts on the memory record's cadence; growth without reads is a finding.
- Prune by the action test: would a future session act differently because this note exists?
- Archive rather than delete; the history of knowledge is itself knowledge.
- Watch the absent domains: memory where no note exists is the recall absence pattern recurring.
- Deduplicate on a schedule; duplicate notes are the corpus's default drift.
- Keep the governing policies in the memory record, versioned, not in this leaf.

## Procedure

1. Pull corpus counts by domain and by provenance class.
2. Identify never-read notes and unreviewed growth areas.
3. Apply the action test to the weak candidates.
4. Archive what fails; mark the archive with the reason and the date.
5. Deduplicate near-identical notes, keeping the better-titled one.
6. Log the hygiene pass in the memory record: counts before and after.

## Anti-patterns

- Deleting history because it feels cluttered.
- Hoarding: nothing archived because deletion feels irreversible.
- Hygiene passes that only count and never prune.
- Absent domains unexamined; what is not remembered is itself a fact.
- Improvised pruning criteria, when the action test was already decided.

## Done checklist

- [ ] Corpus counts pulled by domain.
- [ ] Never-read notes identified.
- [ ] Action test applied.
- [ ] Failures archived with reason and date.
- [ ] Duplicates collapsed.
- [ ] Hygiene pass logged in the record.

## Sources

- Knowledge audit and governance: <https://en.wikipedia.org/wiki/Knowledge_management>
- Improving-with-age document practice: <https://www.gwern.net/About-This-Website>
- Personal knowledge base design: <https://en.wikipedia.org/wiki/Personal_knowledge_base>
