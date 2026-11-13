---
name: investigator-queries
domain: software-engineering/investigator-queries
trigger: "Making the trail answer who-changed-what without a forensic project."
anti_trigger: "Not for dashboard design, and not for analytics pipelines."
scope: "Answering who-changed-what-when without a forensic project."
status: seedling
---

# Investigator queries

## Standard

The test of an audit trail is the question a person asks months later: who changed this account's email, when did this permission get granted, what did the configuration look like before the incident. A trail that answers these in minutes is evidence; one that requires a week of grepping through append-only files is a cost that pushes investigations toward conclusions drawn without it.

The design work is indexing by the investigator's nouns: actor, target, action, and time. A secondary index on actor and target turns the who-did-what question into a query rather than a scan, and the schema decides this at write time because retrofitting indexes onto append-only storage is exactly the kind of rewrite the design forbids. The schema therefore names its expected query shapes up front — the questions in what-to-record become the indexes here.

Primary sources: <https://csrc.nist.gov/pubs/sp/800/92/final> and <https://www.rfc-editor.org/rfc/rfc6962.html>.

## Decision rules

- Record the expected investigation questions and keep them in the audit record.
- Provide a secondary index or projection by actor, target, action, and time.
- Keep the raw chain as the source of truth; indexes are derived and rebuildable.
- Verify that answering the standard questions requires no chain walk longer than a day's window.
- Publish the query interface for investigators rather than a folder of files.
- Include the denial queries — showing what was attempted but refused.

## Procedure

1. List the questions the trail must answer.
2. Design entry fields so each question filters on one or two fields.
3. Build the derived index or projection for those filters.
4. Run the standard questions and record their turnaround.
5. Publish the interface and the time bounds within which it answers.
6. Record questions, indexes, and turnaround in the audit record.

## Anti-patterns

- A trail designed for storage efficiency and queried only by grep.
- No secondary index, so the answer requires scanning the whole trail.
- Indexes treated as the source of truth after a rebuild.
- Questions discovered only when the incident requires them.
- Denials unqueryable, so the probe pattern stays invisible.

## Done checklist

- [ ] Standard questions listed.
- [ ] Fields designed for the questions.
- [ ] Secondary index or projection built.
- [ ] Turnaround measured and recorded.
- [ ] Interface published.
- [ ] Chain kept authoritative.

## Sources

- Log review and analysis practice: <https://csrc.nist.gov/pubs/sp/800/92/final>
- Inclusion and consistency proofs for range queries: <https://www.rfc-editor.org/rfc/rfc6962.html>
- Trace and identity fields to index: <https://w3.org/TR/trace-context>
