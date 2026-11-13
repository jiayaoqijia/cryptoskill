---
name: ac-adversarial-corpus-challenge
description: "Run a break-mandate round against a finished research corpus. An independent breaker attacks each headline conclusion and returns UNCHANGED, NARROWED, or OVERTURNED with primary-source evidence; the owner then propagates every landed break without rewriting the corpus. Six leaves: round-charter (mandate, scope, pre-registered scoring), breaker-selection (fresh context, no authorship stake, time box), scoring (overturned claims, failed attacks, false-positive accounting), propagate-breaks (root-fix, dependency sweep, dated amendments), reserve-judgment (who decides scope), quality-bar (trade-offs, edge cases, round record). Use when asking 'attack this corpus', 'break these conclusions', 'adversarial review of the research', 'find what the report got wrong', 'red-team this analysis'. Not for: reviewing a single document, or security red-teaming of systems."
license: MIT
metadata:
  domain: research-operations
---

# Adversarial Corpus Challenge

## Overview

A research corpus built by capable workers reads as confident because each worker was right about their own slice. Nobody tested the framing that joined the slices. A break-mandate round exists for that gap: one independent agent attacks the headline conclusions, reports what survived and what broke, and hands the owner a correction list. Producing rounds find material. This round finds errors.

The work has six parts: charter the round as an attack, select a breaker with no stake in the corpus, score on overturned claims, propagate breaks without rewriting history, reserve scope decisions for the owner, and record the round honestly.

## When to use

- A corpus reads confident and only its producers have reviewed it.
- A measured quantity is wrong in one file and may be silently wrong in dependents.
- A corpus keeps yielding new material and never saturates.
- A self-review found nothing wrong, which is itself a reason to test the framing.

## When NOT to use

- Reviewing one document for prose, structure, or citation style. That is editing, not a break round.
- Security red-teaming of systems, networks, or people. The mandate, ethics, and evidence standards differ.
- First-pass research or gap finding. A break round tests claims that already exist.
- Deciding what the corpus is allowed to claim. The round proposes; the owner decides.

## Subskill index

| subskill file | domain segment | when to load |
|---|---|---|
| `subskills/round-charter.md` | `research-operations/round-charter` | writing the mandate, claim list, scope, and success criteria |
| `subskills/breaker-selection.md` | `research-operations/breaker-selection` | choosing who runs the round and defending its independence |
| `subskills/scoring.md` | `research-operations/scoring` | fixing the rubric, scoring returns, handling false positives |
| `subskills/propagate-breaks.md` | `research-operations/propagate-breaks` | feeding landed breaks back through dependent files |
| `subskills/reserve-judgment.md` | `research-operations/reserve-judgment` | separating proposed breaks from owner scope decisions |
| `subskills/quality-bar.md` | `research-operations/quality-bar` | judging whether the corpus was genuinely challenged |

## Status and honest limits

Status: seedling. The procedure comes from a small number of rounds, illustrated by one that attacked eleven headline conclusions (see the quality-bar leaf). That is an existence proof, not a base rate.

Limits:

- Breaks are often narrow rather than fatal. A round that narrows five claims and overturns none has done useful work.
- A breaker can be wrong. Every landed break needs a second read before propagation.
- The breaker cannot judge scope. Re-scoping belongs to the corpus owner, in writing.
- Repair costs real time. A round that lands four breaks may force several repair cycles.
- A time box can end the round with claims untested. Record which ones and why.
- A clean round does not prove the corpus true. It proves the tested claims survived a genuine attempt to break them.
