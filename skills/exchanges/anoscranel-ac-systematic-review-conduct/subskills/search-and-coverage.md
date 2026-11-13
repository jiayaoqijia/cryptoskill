---
name: search-and-coverage
domain: research-operations/search-and-coverage
trigger: "Building the search and proving which databases were covered and when."
anti_trigger: "Not for the open keyless cascade, and not for the final report."
scope: "Database selection, the search log, and the coverage grid that defends it."
status: seedling
---

# Search and coverage

## Standard

A systematic search is a claim about where evidence was sought, so the record must name the databases, the dates, and the exact query strings. The search log is the artifact: every database, the date searched, the strategy as run, and the yield. A reviewer who cannot rerun the search is expected to trust it, and trust is what the method exists to replace.

Coverage is argued with a grid: which databases were chosen and why, what each is known to index, and therefore what the combined set plausibly misses. No search covers everything, and the honest review states its gaps rather than presenting the yield as completeness. The peer and citation-based searches — forward and backward chaining — complement the database searches precisely because databases index slowly and selectively.

Primary sources: <https://training.cochrane.org/handbook> and <https://pubmed.ncbi.nlm.nih.gov/>.

## Decision rules

- Name every database searched, with the version or interface and the date.
- Record the exact query string as run, including filters and limits.
- Justify each database's inclusion from its known coverage.
- Search at least one register and one grey source alongside the bibliographic databases.
- Run backward and forward citation chaining on included studies.
- Store the raw export counts at every stage: identified, deduplicated, screened.

## Procedure

1. Select databases by coverage justification, not habit.
2. Translate the question into each database's syntax.
3. Record date, string, and yield per database in the log.
4. Deduplicate and record the count before screening.
5. Chain citations backward from included studies and forward from key references.
6. Assemble the coverage grid: database, date, yield, and what each misses.

## Anti-patterns

- Searching one database and calling the search systematic.
- Reporting the abstract yield without the query that produced it.
- No grey source or register searched.
- Citation chaining presented as a substitute for a database search.
- Rerunning a search weeks later without recording both runs.

## Done checklist

- [ ] Databases named with dates and coverage rationale.
- [ ] Query strings logged as run.
- [ ] Yields recorded per database and after deduplication.
- [ ] Register and grey source searched.
- [ ] Citation chaining run in both directions.
- [ ] Coverage grid assembled with stated gaps.

The search log also anchors the review's reproducibility after databases change their interfaces, merge records, or disappear. A strategy rerun in five years never yields identical results, but the logged strings, dates, and yields define exactly what the original search was, so future updates are re-conducted rather than re-imagined, and any delta between the runs is evidence about the literature's growth rather than about the team's inconsistency.

## Sources

- Cochrane Handbook, searching chapter: <https://training.cochrane.org/handbook>
- PubMed search interface: <https://pubmed.ncbi.nlm.nih.gov/>
- Trial register: <https://register.clinicaltrials.gov/>
