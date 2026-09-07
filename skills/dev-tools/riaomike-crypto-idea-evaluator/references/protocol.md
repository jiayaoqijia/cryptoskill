# Idea Evaluation Protocol

## Formalize before judging

Write the candidate as:

```text
Given setting/model M and assumptions A, construction/technique C claims
property P over parameter regime R, improving baseline B on metric X,
with limitations L.
```

Define all ambiguous terms and distinguish the primitive, security functionality, proof technique, implementation technique, and deployment claim.

## Claim-evidence matrix

| ID | Claim type | Falsifiable statement | Baseline | Required evidence | Failure condition |
|---|---|---|---|---|---|

Claim types: functionality/correctness, theorem, security/reduction, concrete security, asymptotic efficiency, measured performance, usability/deployment, novelty/significance.

## Research-quality tests

- **Importance:** who needs the result, and what becomes possible if true?
- **Non-triviality:** what technical barrier is crossed rather than renamed?
- **Comparability:** are baselines and metrics compatible?
- **Falsifiability:** what result would disconfirm each claim?
- **Tractability:** can proof, implementation, data, and compute obligations be met?
- **Robustness:** does the claim survive stronger adversaries, realistic parameters, and alternative explanations?
- **Ethics:** stakeholders, harms, privacy, consent, dual use, disclosure, and legal constraints.

## Cryptography-specific inventory

- exact security game/notion and adversary;
- standard/idealized model and setup trust;
- assumptions and structured variants;
- reduction direction/loss and composition path;
- parameter symbols, correctness/failure targets, classical/quantum target;
- ZKP relation, soundness/knowledge/ZK properties when relevant;
- lattice problem/distributions/norms/estimator evidence when relevant.

## Kill and pivot criteria

Define early tests that would stop or reshape the project: matching prior art, impossible parameter regime, unacceptable reduction loss, proof counterexample, benchmark loss to fair baseline, artifact/data infeasibility, or ethical block.

## Decision rubric

- **Proceed:** claim is falsifiable, significant if true, feasible, and no blocking prerequisite is open.
- **Proceed with prerequisites:** specific literature/proof/parameter/ethics questions must resolve first.
- **Pivot:** core insight may survive under a narrower claim/model/baseline.
- **Stop:** matching prior art, invalid model, infeasible evidence, unacceptable ethics, or no meaningful improvement.

