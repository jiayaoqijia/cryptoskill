---
name: evidence-ledger
domain: research-operations/evidence-ledger
trigger: "\"show me the receipts\", \"audit this study\", \"where did each claim come from\", \"rebuild how we got this\"."
anti_trigger: "The card format for single load-bearing facts (subskills/evidence-cards.md); the research root paths and write order (subskills/archive-writes.md)."
scope: "The study's audit trail: one file per source with verbatim quotes, a claim-to-source-to-span trace, and the run log"
status: "seedling"
---

# The evidence ledger

## Standard

- Provenance is a permanent artifact, not a phase: the claim-to-source-to-span
 chain lets an auditor check any sentence against its evidence without
 re-running anything.
- Raw snippets live beside the claim, so support is inspectable without a
 re-fetch. Raw snippets up the chain are the cheapest measured citation-
 accuracy win (+5pp recall, +3-7pp precision, arXiv 2608.24306).
- One file per source. Per-source files are what make findings searchable and
 reusable across studies; a collapsed megafile kills both.
- The run log records what the desk spent: tiers used, timestamps, retry
 states, model minutes and cost as actuals. Ledgers record actuals, never
 ceilings.

## Decision rules

- Everything auditable goes in the ledger; only the answer goes in the report.
- A quote that no claim uses still stays; an unused-source section beats a
 silently dropped retrieval.
- If a span cannot be quoted (paywall, fetch failure), the entry records the
 access state verbatim. An honest gap beats a reconstructed quote.

## Procedure

1. On each retrieval, create the source file immediately: identifier, tier,
 fetch time, rung tag, then verbatim quotes.
2. For every claim, write the trace row: claim text, source file, the span
 inside it.
3. Log each run event as it happens: query, tier, outcome, retries.
4. At close, reconcile: every claim in the report has a trace row, and every
 trace row ends at a real span on disk.

## Anti-patterns

- Collapsing all sources into one file.
- Paraphrase-only spans. The audit wants the source's words, not the agent's.
- A ledger written at the end from memory. Write at retrieval time or not at
 all.
- Dropping sources that were fetched but unused.

## Done checklist

- One file per source, each with verbatim quotes.
- Every report claim has a trace row reaching a span on disk.
- The run log covers every query and every retry.
- An auditor can check any claim with grep, no network needed.

The ledger's value appears when a claim is challenged, because the challenge is answered by the line rather than by re-reading the corpus, and a ledger without line-level pointers reduces to a reading list. The pointer is the work; the claim is the summary of it.

## Sources

- PRISMA-S: Rethlefsen et al., Systematic Reviews 2021, https://doi.org/10.1186/s13643-020-01542-z (item 1 is the reporting standard for the search record).
- PRISMA 2020: Page et al., BMJ 2021, https://doi.org/10.1136/bmj.n71.
