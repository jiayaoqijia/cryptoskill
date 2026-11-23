---
name: crypto-paper-writing
description: Use when outlining, drafting, restructuring, or completing a cryptography, ZKP, lattice, or security paper from verified claims, proofs, literature, parameters, experiments, artifacts, and venue requirements.
---

# Crypto Paper Writing

Write from an evidence ledger, not from a desired story. The manuscript may be polished only to the strength of verified claims.

## Scope

In scope: contribution architecture, title/abstract/introduction, preliminaries, construction, theorem/proof presentation, security discussion, parameters/experiments, related work, limitations, ethics/open science, conclusion, LaTeX/Markdown organization, and venue readiness.

Out of scope: inventing results/citations/proofs/experiments, hiding gaps, asserting global novelty, deciding authorship, or submitting without human authorization.

## Required Inputs

- research brief and target audience/venue;
- verified claim-evidence ledger and terminology/security model;
- theorem/proof/reduction status, parameters, experiments/artifacts;
- verified bibliography/related-work synthesis and novelty limitations;
- ethics/disclosure/open-science constraints.

## Success Criteria

- Every abstract/introduction contribution maps to body evidence.
- Definitions, notation, models, assumptions, parameters, and claims are consistent.
- Proof sketches versus full proofs and author claims versus verified evidence are labeled.
- Related work compares closest results fairly and bounds novelty.
- Tables/figures/cost comparisons are reproducible and compatible.
- Limitations, ethics, responsible disclosure, open science, anonymity, conflicts, and AI/human responsibility are handled per current venue policy.
- The manuscript has a clear problem–barrier–insight–result–evidence narrative without overstating significance.

## Failure Modes

- Idea without completed evidence: return a research brief/outline with evidence slots, not a result-bearing manuscript.
- Proof/experiment/citation gap: expose it and block affected claim language.
- Unverified novelty: use bounded search language.
- Unknown/changing venue rules: produce venue-neutral draft and require official policy refresh.
- Conflicting notation/parameters: stop prose propagation until reconciled.

Never fabricate citations, theorem results, proof steps, experiments, statistics, artifacts, reviewer feedback, or venue compliance.

## Workflow

The end-to-end runbook for "given an idea + a scheme body + experiments, write a venue-style paper" is [authoring-workflow.md](references/authoring-workflow.md); it orders the work and says when to run the venue skills' instruments. Summary:

1. Freeze the inputs (idea card, scheme spec, experiment ledger) and the venue family; fetch the current official call and record a dated snapshot. An idea without evidence gets a research plan, never a result-bearing draft.
2. Apply [protocol.md](references/protocol.md) to freeze the claim-evidence ledger and design the paper architecture.
3. Read [top-venue-gates.md](references/top-venue-gates.md) and verify the current target venue's official rules; load the owning venue skill for thresholds (`crypto-venue-paper-writing` for crypto/LNCS, `ccs-writing-style` for CCS/S&P/NDSS, `usenixsec-writing-style` for USENIX Security).
4. Draft in dependency order (construction → security → experiments → related work → introduction → abstract/contributions last), keeping claim/evidence/gap traceability and hitting the venue skill's constituents while drafting.
5. Run the instrument loop after each artifact: `count_venue_gates.py` (crypto family) or `count_prose_gates.py` (security family) with a named region map; measured/no-breach is the exit condition; a breach is repaired (move material, never delete a claim) or recorded as a question for the human author.
6. Review loop: `crypto-paper-review`, plus `zkp-security-review` and `crypto-theorem-review` where applicable; repair and re-run step 5.
7. Freeze and hand off: twin parity or a recorded decoupling decision, content-anchored region map, double-blind/disclosure text, and the promotion checklist. Page budget/compile stay a human step when no LaTeX toolchain exists.
8. Use [evaluation-scenarios.md](references/evaluation-scenarios.md) for future independent evaluation.

## Output Contract

Return: paper brief; target-venue policy snapshot/date; claim-evidence ledger; detailed outline; manuscript/diff; theorem/proof/experiment/citation status; figures/tables/artifact links; ethics/open-science/limitations text; consistency audit; unresolved blockers; human sign-off checklist.

