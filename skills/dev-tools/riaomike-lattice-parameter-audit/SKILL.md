---
name: lattice-parameter-audit
description: Use when auditing LWE, Ring-LWE, Module-LWE, SIS-family, lattice KEM/signature/FHE/ZKP parameters, reductions, correctness failures, concrete attacks, estimator outputs, or implementation compatibility.
---

# Lattice Parameter Audit

Audit formal assumptions, concrete attacks, correctness probability, and implementation compatibility separately. No single reduction or estimator run certifies a parameter set.

## Scope

In scope: exact lattice problem/structure, dimension/modulus/samples/distributions/norms, reductions, tail/smoothing/rejection/decryption failures, classical/quantum attacks, estimator reproducibility, parameter sensitivity, NTT/packing/gadget/noise compatibility.

Out of scope: claiming certified security without reproducible attack evaluation, side-channel certification, or silently selecting missing parameters.

## Required Inputs

- scheme/proof specification and exact parameter set;
- problem variant, algebraic structure, secret/error distributions, norms/bounds;
- target correctness and classical/quantum security levels/cost metrics;
- reduction claims, estimator/tool configuration, implementation regime.

## Success Criteria

- Exact LWE/SIS variant and parameter ledger are complete.
- Formal reduction assumptions/constraints and concrete deployed regime are compared.
- Correctness/decryption/rejection/statistical failures are derived and composed.
- Relevant primal, dual, decoding, hybrid, combinatorial, algebraic/structural, and implementation attacks are considered.
- Estimator/tool version, config, samples, memory, cost model, and reproducible inputs are recorded.
- Security sensitivity and margins are reported, not only one point estimate.
- Formal, concrete, correctness, and compatibility verdicts remain separate.

## Failure Modes

- Missing distribution/norm/structure: block affected bounds and estimates.
- Unreproducible estimator output: mark concrete security unverified.
- Reduction outside parameter regime: do not transfer worst-case foundation.
- Failure probability without workload composition: report per-operation only.
- Incompatible cost metrics or hidden memory/data: refuse bit-security comparison.

Never fabricate parameters, estimator runs, reduction applicability, attack costs, or failure rates.

## Workflow

1. Apply [protocol.md](references/protocol.md) to freeze the exact problem and parameter ledger.
2. Audit reductions, distributions/norms, correctness failures, attack surface, and concrete estimates.
3. Check implementation compatibility and parameter sensitivity.
4. Return four verdicts plus assumptions and unverified evidence.
5. Use [evaluation-scenarios.md](references/evaluation-scenarios.md) for future independent evaluation.

## Output Contract

Return: scheme/version; exact problem/structure; parameter ledger; reduction audit; distribution/norm audit; correctness/failure derivation; attack matrix; estimator reproducibility record; implementation compatibility; sensitivity/margins; blocking/major/minor findings; formal/concrete/correctness/compatibility verdicts.

