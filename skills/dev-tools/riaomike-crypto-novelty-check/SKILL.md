---
name: crypto-novelty-check
description: Use when adversarially checking whether a decomposed cryptography, ZKP, or lattice contribution has matching prior art, priority conflicts, hidden predecessors, or only a bounded novelty claim.
---

# Crypto Novelty Check

Try to falsify novelty before supporting it. A finite search can find prior art; it cannot prove universal absence.

## Scope

In scope: contribution decomposition, adversarial query/citation search plan, historical terminology, adjacent-field and version checks, closest-work claim comparison, priority evidence, and bounded novelty verdict.

Out of scope: global guarantees, legal patent opinions, proof correctness, or concealing inconvenient prior art.

## Required Inputs

- precise candidate contribution claims;
- functionality, security notion/model, assumptions, parameters, technique, and claimed improvement;
- available literature corpus/search access and cutoff;
- venue/language/patent/unpublished boundaries.

## Success Criteria

- Each novelty claim is independently searchable and falsifiable.
- Search coverage includes synonyms, historical terms, versions, backward/forward citations, adjacent formulations, and adverse evidence when available.
- Work identity and exact claim support are verified before comparison.
- Closest work is compared across formal claim, model, assumptions, parameters, functionality, proof basis, and compatible costs.
- Matching, partially overlapping, and non-comparable prior art are distinct.
- Verdict states sources, queries, dates, stopping rule, blind spots, and confidence limits.

## Failure Modes

- Vague contribution: return alternative decompositions and stop verdict.
- Narrow access: produce partial prior-art map and explicit next frontier.
- Inaccessible source: do not decide match from title/abstract/snippet.
- Conflicting versions/priority: retain uncertainty and exact dates/records.
- Legal/patent certainty requested: state scope limit and recommend qualified counsel/search.

Never fabricate searches, sources, priority dates, claim content, or “first” status.

## Workflow

1. Apply [protocol.md](references/protocol.md) to decompose the candidate and construct an adversarial search lattice.
2. Verify exact sources/versions and build closest-work claim matrices.
3. Seek evidence that weakens each novelty dimension before grading it.
4. Return matching prior art or a reproducible bounded negative search—not global novelty.
5. Use [evaluation-scenarios.md](references/evaluation-scenarios.md) for future independent evaluation.

## Output Contract

Return: candidate claim decomposition; search scope/log and cutoff; disconfirming strategy; verified work/version set; closest-work matrix; matching/overlap findings; blind spots; grade (matching found / partial map / strong bounded negative / not assessable); permitted claim wording; next searches.

