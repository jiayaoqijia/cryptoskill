---
name: crypto-paper-review
description: Use when pre-reviewing, peer reviewing, stress-testing, or assessing submission readiness of a cryptography, ZKP, lattice, or security paper for a leading research venue.
---

# Crypto Paper Review

Perform an adversarial, evidence-located review. Do not invent reviewer consensus or let polish compensate for correctness, novelty, ethics, or evaluability gaps.

## Scope

In scope: venue fit, contribution/significance, novelty/prior art, definitions/theorems/proofs/reductions, ZKP/lattice specifics, parameters/complexity, experiments/artifacts, clarity, ethics/disclosure/open science, reproducibility, and revision priority.

Out of scope: actual PC decisions, hidden-reviewer knowledge, fabricated independent reviewers, or rewriting without request.

## Required Inputs

- exact manuscript/version and supplements/artifacts;
- target venue and current official policies, if venue-specific;
- claimed contributions and evidence map when available;
- desired mode: quick triage, full review, methodology/proof focus, or re-review.

## Success Criteria

- Every major claim is tested against evidence and closest-work context.
- Findings cite exact manuscript/artifact locations and consequences.
- Correctness, novelty, significance, evidence, reproducibility, clarity, ethics, and policy compliance are independent dimensions.
- ZKP/lattice/security-model and parameter/complexity category errors are checked.
- Blocking, major, and minor findings have concrete resolution/evidence requirements.
- Verdict is calibrated as readiness/risk, not a predicted or fabricated conference decision.
- A re-review verifies each claimed repair and detects regressions.

## Failure Modes

- Missing manuscript/artifact/version: limit review and mark unseen evidence.
- Unknown venue policy: give venue-neutral review; do not claim compliance.
- Citation/full proof inaccessible: keep dependent claims unverified.
- Same-agent multi-perspective pass: label it non-independent.
- Manuscript advocacy pressure: preserve disconfirming findings.

Never fabricate citations, proof checks, artifact runs, reviewer opinions, scores, or acceptance probabilities.

## Workflow

1. Apply [protocol.md](references/protocol.md) to freeze claims/evidence and target-venue gates.
2. Run sequential lenses: fit/significance; novelty; correctness/security; parameters/evidence; reproducibility/ethics; exposition/adversarial challenge.
3. Consolidate duplicate findings without erasing disagreement or uncertainty.
4. Return severity-ranked report, readiness verdict, and revision plan.
5. In re-review, map each prior finding to exact changed evidence.
6. Use [evaluation-scenarios.md](references/evaluation-scenarios.md) for future independent evaluation.

## Output Contract

Return: scope/version/policy snapshot; paper and contribution summary; strengths; blocking/major/minor findings with locations; claim-evidence and domain audits; novelty/closest-work risks; artifact/ethics/compliance risks; questions to authors; readiness verdict; ordered revision plan; unverified items.

