---
name: crypto-experiment-reproducibility
description: Use when designing, auditing, reproducing, or packaging cryptography/ZKP/lattice experiments, benchmarks, estimators, proof checkers, datasets, code artifacts, tables, figures, or claim-to-artifact evidence.
---

# Crypto Experiment Reproducibility

Make empirical and computational claims independently inspectable. Availability, functionality, and reproduced results are separate evidence grades.

## Scope

In scope: experiment design, claim-to-artifact mapping, environment/version capture, fair baselines, statistical analysis, replay, raw evidence, portability, artifact packaging, anonymity, ethics/privacy/disclosure, and limitation reporting.

Out of scope: fabricating runs/results, calling code availability reproducibility, or releasing sensitive artifacts without authorization and risk review.

## Required Inputs

- claims/tables/figures to support;
- source/data/configuration and exact versions;
- environment, hardware, parameters, seeds, workload, baselines, and expected outputs;
- sharing, anonymity, licensing, privacy, ethics, and disclosure constraints.

## Success Criteria

- Every empirical/concrete claim maps to exact inputs, command/workflow, raw output, processing, and tolerance.
- Environment and dependencies can be recreated or limitations are explicit.
- Baselines use compatible security/parameters/hardware/batch/resource rules.
- Statistical design, repetitions, seeds, uncertainty, exclusions, and nondeterminism are documented.
- Artifact availability, functionality, and result reproduction receive evidence-based statuses.
- Sensitive/unshareable components have justified safe alternatives or remain limitations.

## Failure Modes

- Missing raw evidence/version/config: mark claim unverified and identify minimum rerun.
- Environment cannot be recreated: provide forensic provenance and block reproducibility grade.
- Long/expensive run: use a justified evaluator-scale run without replacing full evidence.
- Sensitive/dual-use/privacy/legal constraint: stop release and require human ethics/disclosure decision.
- Result deviation: investigate before changing tolerance or narrative.

Never invent commands run, outputs, seeds, statistical significance, artifact badges, or reproducibility.

## Workflow

1. Apply [protocol.md](references/protocol.md) to build claim-to-experiment and provenance maps.
2. Audit/package using [artifact-checklist.md](references/artifact-checklist.md).
3. Run available smoke/full/scaled experiments, retaining raw outputs and deviations; otherwise mark not executed.
4. Return evidence grades, blockers, and exact reproduction instructions.
5. Use [evaluation-scenarios.md](references/evaluation-scenarios.md) for future independent evaluation.

## Output Contract

Return: claim-to-artifact matrix; provenance/environment manifest; experiment/baseline/statistical plan; executed runs and raw evidence locations; deviations/tolerances; availability/functionality/reproduction statuses; ethics/privacy/disclosure constraints; blockers; artifact README/open-science content.

