---
name: ac-deep-researcher
license: MIT
description: "Runs a full deep-research study end to end. Reframes the question into falsifiable hypotheses, decomposes it into a query plan, triages sources on a trust ladder, pulls evidence through the keyless-first retrieval cascade, verifies every load-bearing claim against two or more independent source lineages with verbatim quotes archived, attacks the draft conclusions with an adversarial pass, stops on declared criteria with the reason stated, keeps a claim-to-source evidence ledger, and delivers the answer-first evidence report. Use for \"research this question\", \"map the literature\", \"verify this claim properly\", \"write the evidence report\", \"investigate before we decide\", or any question where a wrong answer costs more than the research. Not for one-hop factual lookups (what, who, when, price), single-page fetches, multi-day autonomous desk operations, or formal systematic-review protocol compliance."
metadata:
  domain: research-operations
---

# Deep Researcher — the single-study research craft

## Overview

`deep-researcher` runs one research study correctly, from question shape to
evidence report. The unit of work is a study folder in the research root: a plan, one
file per source with verbatim quotes, findings per hypothesis, and a final
answer-first report whose every number names its primary source. The method is
the measured one: recall is the binding constraint in retrieval, verification
budget lands at the merge, and every claim carries a rung, a lineage count and
a population label.

## When to use

- A question feeds a decision, a published artifact, or a strategy, so a wrong
 answer costs more than the research.
- The answer needs more than one source type and a defensible trail: "research
 this question", "map the literature", "verify this claim properly", "write
 the evidence report", "investigate X before we commit".

**When NOT to use:** one-hop factual lookups (what, who, when, price), a single
known URL to fetch, multi-day autonomous desk operations with worker fleets, or
deliverables that must meet a formal systematic-review conduct standard
(registration, dual-review attestations). This skill borrows that literature's
measurement science; it never asserts compliance with it.

## The precedence rule

The deepest loaded instruction governs its uniquely-claimed scope; every
`scope:` string is claimed by exactly one file in this tree; no leaf may widen
a prohibition declared by an ancestor — leaves narrow, never override upward.

## The study pipeline

Run phases in order. Each leaf holds its full procedure; enter at the phase
your study needs.

| Phase | You are doing | Leaf |
|---|---|---|
| plan | Sharpening the ask into a decision-backed question | `subskills/scope-question.md` |
| plan | Splitting the question into a round-by-round query plan | `subskills/decompose-plan.md` |
| retrieve | Grading sources on the trust ladder | `subskills/source-triage.md` |
| retrieve | Executing the keyless-first retrieval cascade | `subskills/retrieval-cascade.md` |
| verify | Verifying load-bearing claims and citations | `subskills/verify-claims.md` |
| verify | Attacking the draft with counter-evidence | `subskills/adversarial-pass.md` |
| synthesize | Merging evidence into findings | `subskills/synthesize-findings.md` |
| store | Writing claim cards for contested facts | `subskills/evidence-cards.md` |
| store | Keeping the claim-to-source-to-span ledger | `subskills/evidence-ledger.md` |
| stop | Deciding the study is done, with the reason stated | `subskills/stop-rules.md` |
| retrieve | Firing the grounded tier when its conditions hold | `subskills/grounded-tier.md` |
| store | Writing the study into the research root (the one folder that holds every study), incrementally | `subskills/archive-writes.md` |
| present | Delivering the answer-first evidence report | `subskills/write-report.md` |

## Status & honest limits

Every leaf is `status: seedling` until a routing evaluation passes. The skill
encodes the procedure; it cannot force the harness to keep the discipline at
run time. Every operating rule the procedure needs is restated in plain words inside the
leaves; nothing here depends on an external rulebook.
