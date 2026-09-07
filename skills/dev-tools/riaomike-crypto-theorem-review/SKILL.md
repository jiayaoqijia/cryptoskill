---
name: crypto-theorem-review
description: Use when auditing a cryptographic theorem, lemma, proof, game hop, reduction, ZKP security property, lattice assumption, or claimed protocol-security implication.
---

# Crypto Theorem Review

Audit the exact mathematical object supplied. Keep statement validity, proof completeness, reduction validity, and protocol security as separate conclusions.

## Scope

In scope:

- review a supplied theorem, lemma, proof, proof sketch, reduction, game sequence, or formal security argument;
- reconstruct omitted steps when possible while marking them as reviewer reconstruction;
- inspect cited dependencies and document versions when accessible;
- audit assumptions, adversary/setup model, parameters, probability bounds, reduction loss, and complexity;
- report which protocol-level claim follows from the reviewed result.

Out of scope:

- open-ended literature discovery, general paper summarization, prose-only polishing, implementation/side-channel certification, or inventing a missing proof;
- claiming mechanized verification unless the intended checker actually ran successfully on the identified artifact;
- editing or publishing the source artifact unless separately requested.

## Required Inputs

- exact statement and proof/argument text or formal artifact;
- stable artifact identity: file/version/hash/date or publication version and theorem location;
- definitions, assumptions, notation, parameter regime, and cited dependencies needed by the argument;
- claimed security notion/model and desired review depth.

If the exact statement or argument is missing, ask for it and stop the verdict. Infer only notation or low-risk presentation details, and label every inference.

## Success Criteria

- Every consequential claim has a type and evidence status.
- Statement, proof, reduction, and security implication receive separate verdicts.
- Every blocking gap has a location, missing obligation, consequence, and evidence required to resolve it.
- Security notion, adversary powers, setup/model, assumptions, parameter regime, and concrete reduction loss are recorded when applicable.
- Citations and theorem/section numbers are checked against the inspected version or marked unverified.
- Parameters, probability/failure terms, asymptotic variables, and concrete cost models are internally consistent or receive findings.
- The final conclusion is bounded by the evidence actually inspected.

## Failure Modes

- Missing or inaccessible dependency: mark all dependent steps unverified; never infer the cited result from title, snippet, or memory.
- Conflicting versions: preserve each version, identify the one reviewed, and report changed hypotheses, numbering, or conclusions.
- Undefined notation or parameters: request only research-critical definitions; otherwise give a partial syntactic review with the limitation visible.
- Proof gap: record it; any reviewer-supplied repair is a proposed lemma/argument, not verification of the original proof.
- Unavailable checker: perform manual review only and state that mechanized verification was not executed.
- Unsupported security upgrade: return the narrower theorem/model actually supported.

Never fabricate a citation, theorem statement, proof step, parameter value, checker run, reduction, or security conclusion.

## Workflow

1. Freeze the exact object, version, requested depth, and conclusion boundary.
2. Apply [core-review-protocol.md](references/core-review-protocol.md) to classify claims, normalize the statement, build proof obligations, and audit local reasoning, games, reductions, citations, parameters, and implications.
3. If the result concerns a ZKP, proof/argument of knowledge, Fiat-Shamir transform, polynomial commitment, recursion, folding, aggregation, or IVC, apply [zkp-review.md](references/zkp-review.md).
4. If it concerns LWE/SIS or a ring/module/structured lattice assumption, reduction, distribution, norm, correctness bound, or concrete security estimate, apply [lattice-review.md](references/lattice-review.md).
5. Run an available formal checker only when the supplied artifact targets it; retain the checker/version/configuration and raw success/failure status.
6. Produce [report-schema.md](references/report-schema.md). Keep verified, supported-with-limitations, unverified, contradicted, and not-assessable statuses distinct.
7. When evaluating this skill itself, use [evaluation-scenarios.md](references/evaluation-scenarios.md); do not claim those scenarios ran unless independent fresh-context outputs were inspected.

## Output Contract

Return, in order:

1. reviewed object and exact version;
2. scope and evidence inspected;
3. statement verdict;
4. proof verdict and obligation table;
5. reduction/security implication verdict;
6. ZKP/lattice findings when applicable;
7. parameter, probability, and complexity ledger/findings;
8. citations checked and version discrepancies;
9. blocking, major, and minor findings;
10. unverified items and bounded conclusion.

