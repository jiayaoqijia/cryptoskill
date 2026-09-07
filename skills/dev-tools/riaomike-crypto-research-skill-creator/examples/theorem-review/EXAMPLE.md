---
name: theorem-review
description: Use when auditing a cryptographic theorem, lemma, proof, reduction, or claimed protocol-security implication for correctness, completeness, assumptions, parameters, and evidence.
---

# Theorem Review

Review a supplied cryptographic statement and its argument without upgrading incomplete evidence into a proof or security certification.

## Scope

In scope: statement well-formedness, proof obligations, local derivations, cited dependencies, reduction accounting, parameter consistency, and the exact security implication supported by the argument.

Out of scope: inventing missing lemmas, certifying an implementation, claiming mechanized verification without a successful checker run, or general peer review unrelated to the selected theorem.

## Required Inputs

- exact theorem/lemma/security claim and the inspected document version;
- proof, proof sketch, or machine-readable artifact to review;
- definitions, assumptions, notation, parameters, and cited dependencies;
- requested review depth and security model when not explicit in the artifact.

If the statement or argument is unavailable, stop. If only a proof sketch is supplied, review its obligations but keep the result labeled as a sketch review.

## Success Criteria

- The statement, proof completeness, reduction, and protocol-security implication receive separate statuses.
- Every blocking gap has a location, missing obligation, and consequence.
- Assumptions, adversary/setup model, parameter regime, and reduction loss are explicit.
- Citations and theorem numbering are verified against the inspected version or marked unverified.
- The conclusion is no stronger than the reviewed evidence.

## Failure Modes

- Missing source/version: mark citation-dependent steps unverified; do not reconstruct bibliographic or theorem details from memory.
- Undefined notation or parameters: request the minimum critical definition or limit the review to syntactic obligations.
- Unavailable checker: perform only manual review and state that machine verification was not executed.
- Proof gap: report the gap and downstream consequence; do not silently patch it and call the theorem verified.
- Security-model mismatch: report the narrower model actually supported.

## Workflow

1. Freeze the exact statement, document/artifact version, and review boundary.
2. Normalize definitions, quantifiers, probability spaces, assumptions, parameters, and conclusion.
3. Build an obligation list from the statement and proof structure.
4. Apply [review-protocol.md](references/review-protocol.md) to local steps, cited dependencies, probability arguments, games/hybrids, and reductions.
5. Audit parameters, failure terms, asymptotic variables, and concrete loss.
6. Map the theorem conclusion to any claimed protocol security; identify missing composition or model steps.
7. If a proof checker is available and the artifact is intended for it, run the exact version and retain success/failure output. Otherwise say it was not run.
8. Return separate statuses, findings by severity, and unverified items.

## Output Contract

```text
Reviewed object and version:
Statement status:
Proof status:
Reduction/security status:
Assumptions and model:
Parameter/complexity findings:
Blocking gaps:
Citations checked:
Unverified items:
Bounded conclusion:
```

