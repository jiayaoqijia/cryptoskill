---
name: zkp-security-review
description: Use when auditing an interactive or non-interactive zero-knowledge proof/argument, proof of knowledge, Fiat-Shamir transform, SNARK/STARK, polynomial commitment, aggregation, recursion, folding, or IVC system.
---

# ZKP Security Review

Audit the end-to-end proof-system claim. Keep completeness, soundness, knowledge, zero knowledge, setup, composition, and efficiency as independent dimensions.

## Scope

In scope: relation/transcript/setup, security definitions, reductions/extractors/simulators, Fiat-Shamir ROM/QROM, polynomial commitments, arithmetization, aggregation/recursion/folding/IVC, parameters/errors, and proof-system costs.

Out of scope: accepting protocol security from one local lemma, implementation side-channel certification, or inventing missing security proofs.

## Required Inputs

- protocol/specification and exact proof version;
- relation/language, instance/witness, transcript and public parameters;
- claimed properties, adversary, setup/model, assumptions, and parameter set;
- dependent primitives/proofs and intended composition/deployment.

## Success Criteria

- Each property has its own definition, adversary/model, error, proof status, and limitation.
- Setup/trapdoor/updatability/transparency assumptions are explicit.
- Fiat-Shamir transcript binding, oracle model, query loss, and classical/quantum status are checked.
- Composition, aggregation, recursion/folding/IVC implication steps are explicit.
- Parameter, soundness/knowledge/correctness errors and reduction losses are accumulated.
- Costs separate constraints, prover/verifier, proof size, setup, online, amortized, communication, memory, and operation model.
- End-to-end verdict stops at the first unsupported implication.

## Failure Modes

- Missing relation/security definition: block the corresponding verdict.
- Proof sketch or inaccessible dependency: mark property unverified.
- ROM-to-QROM, HVZK-to-ZK, soundness-to-knowledge, or component-to-system upgrade: reject without checked transformation.
- Incomplete parameters/error terms: give symbolic review only.
- Unavailable implementation/artifact: do not verify measured costs or operational setup.

Never fabricate a property proof, extractor/simulator, oracle argument, parameter, benchmark, or trusted-setup fact.

## Workflow

1. Apply [protocol.md](references/protocol.md) to freeze the formal object and property matrix.
2. Build dependency and implication graphs from primitives to system claims.
3. Audit Fiat-Shamir/model, composition/advanced construction, parameters/errors, and costs.
4. Return per-property and end-to-end findings with evidence status.
5. Use [evaluation-scenarios.md](references/evaluation-scenarios.md) for future independent evaluation.

## Output Contract

Return: object/version; relation/setup/transcript; property matrix; assumption/dependency graph; Fiat-Shamir/model findings; aggregation/recursion/folding findings; parameter/error ledger; cost ledger; blocking/major/minor findings; per-property verdicts; bounded end-to-end conclusion.

