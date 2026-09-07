---
name: crypto-research-pipeline
description: Use when orchestrating an end-to-end cryptography, zero-knowledge proof, or lattice research project from an idea through literature, novelty, proofs, parameters, experiments, writing, internal review, and submission readiness.
---

# Crypto Research Pipeline

Coordinate a research project as a sequence of evidence gates. Preserve uncertainty and negative results. A later stage never silently clears an earlier limitation.

## Scope

Use this skill to orchestrate these installed skills when relevant:

- `crypto-idea-evaluator`
- `crypto-literature-search`
- `crypto-paper-reader`
- `crypto-related-work-synthesis`
- `crypto-novelty-check`
- `crypto-theorem-review`
- `zkp-security-review`
- `lattice-parameter-audit`
- `crypto-experiment-reproducibility`
- `crypto-paper-writing`
- `crypto-paper-review`

This skill manages research state, routing, rollback, and human sign-off. It does not guarantee novelty, proof correctness, security, reproducibility, venue acceptance, or publication. It does not assign authorship, contact third parties, submit a manuscript, or make ethics decisions for the responsible researchers.

## Required Inputs

Collect or explicitly mark missing:

- the idea, manuscript, repository, proof, protocol, or artifact in scope;
- research objective and intended contribution;
- domain, threat/security model, assumptions, and target setting;
- known constraints on time, compute, data, disclosure, and collaboration;
- intended venue and policy snapshot, if venue readiness matters;
- ethics, dual-use, privacy, conflict, and disclosure boundaries.

Do not turn a one-sentence idea into asserted results. Record hypotheses, missing evidence, and kill criteria first.

## Success Criteria

A successful run:

- maintains the research state defined in [research-state.md](references/research-state.md);
- gives every stage a status of `pass`, `pass-with-limitations`, `fail`, or `blocked`;
- preserves source, claim, proof, parameter, experiment, and artifact provenance;
- propagates blockers and rolls back dependent claims when evidence changes;
- records decisions, owners, risks, and the next falsifiable action;
- invokes human gates for ethics, authorship, disclosures, final claims, and submission;
- declares submission readiness only when all blocking gates are cleared.

## Failure Modes

- If a required skill or capability is unavailable, use its documented output contract if feasible; otherwise mark the stage unavailable and name the missing evidence.
- If strong prior art materially matches the contribution, pause the original narrative and recommend a pivot, narrower claim, or stop decision.
- If a theorem, reduction, security property, parameter estimate, or experiment fails, reopen dependent stages and retract unsupported downstream language.
- If browsing, computation, proof tooling, source access, or artifact execution is unavailable, do not simulate the missing verification.
- If ethics, disclosure, privacy, or dual-use concerns are unresolved, pause affected work for an accountable human decision.
- If venue rules may be stale, refresh them from the venue's official source before claiming compliance.
- Never fabricate a citation, theorem, proof step, benchmark, result, artifact execution, reviewer outcome, or novelty conclusion.

## Workflow

1. **Initialize and triage.** Create the research-state ledger. Identify responsible humans, ethics/disclosure constraints, and the exact research question.
2. **Evaluate the idea.** Invoke `crypto-idea-evaluator`. Define the contribution hypothesis, feasibility risks, discriminating tests, and kill/pivot criteria.
3. **Map the literature.** Invoke `crypto-literature-search`; use `crypto-paper-reader` on closest and foundational works. Preserve exact bibliographic identifiers and verification state.
4. **Synthesize and test novelty.** Invoke `crypto-related-work-synthesis` and then `crypto-novelty-check`. Separate verified novelty from bounded-search residual risk.
5. **Develop and audit theory.** Route formal claims to `crypto-theorem-review`; route ZKP security claims to `zkp-security-review`. Keep definitions, games, assumptions, reductions, and protocol properties distinct.
6. **Audit parameters and empirical design.** Use `lattice-parameter-audit` for lattice instantiations and `crypto-experiment-reproducibility` for benchmarks or artifacts. Separate asymptotic, symbolic, estimated, measured, and independently reproduced claims.
7. **Build the evidence package.** Freeze inputs, scripts, environments, seeds, outputs, limitations, and claim-to-evidence links. Retain negative and null results.
8. **Write from verified state.** Invoke `crypto-paper-writing`. Draft only claims permitted by the ledger and label conjectures, estimates, and incomplete work.
9. **Run adversarial internal review.** Invoke `crypto-paper-review`; route every blocking finding back to the earliest responsible stage. Re-review after material changes.
10. **Check readiness and stop for sign-off.** Apply [top-venue-gates.md](references/top-venue-gates.md). Require responsible humans to approve ethics, authorship, acknowledgments, disclosures, final claims, venue compliance, and any external submission.

Use [stage-gates.md](references/stage-gates.md) for routing and rollback. Do not skip a gate because a deadline is near.

## Output Contract

Return:

1. **Project state** — current stage, scope, version, and overall status.
2. **Stage ledger** — status, evidence, limitations, blockers, and rollback targets for every stage.
3. **Claim ledger** — each important claim, type, dependencies, evidence, confidence, and permitted wording.
4. **Evidence inventory** — verified sources, proof objects, parameters, experiments, artifacts, and policy snapshots.
5. **Risk register** — novelty, correctness, security, parameter, reproducibility, ethics, disclosure, and venue risks.
6. **Decision log** — pivot/stop/continue decisions, rationale, owner, and date.
7. **Readiness verdict** — `not ready`, `conditionally ready`, or `ready for human submission review`, with unresolved items.
8. **Next action** — the smallest evidence-producing step, its success/failure criterion, and the responsible human or skill.

