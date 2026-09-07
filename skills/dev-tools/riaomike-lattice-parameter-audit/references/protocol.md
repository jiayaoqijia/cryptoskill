# Lattice Parameter Audit Protocol

## Exact identity

Record LWE/Ring-LWE/Module-LWE or SIS variant; search/decision; primal/dual; ring/field/embedding; dimension/rank/degree; modulus; samples; secret/error distribution; norm/bound; security parameter.

## Parameter ledger

| Symbol | Meaning | Domain/unit | Value/regime | Source/derivation | Constraints/uses |
|---|---|---|---|---|---|

Check rounding, decomposition/gadget base, compression, modulus switching/rescaling, and serialization.

## Reduction audit

Record direction, exact worst-case/average-case problem, classical/quantum nature, approximation factor, dimension/noise/modulus/smoothing constraints, ring/field restrictions, runtime/advantage loss, and whether the concrete set satisfies every premise.

## Distributions, norms, failures

Define support/parameters for discrete Gaussian, centered binomial, ternary, sparse, uniform, or custom distributions. Distinguish coefficient, Euclidean, infinity, canonical-embedding, spectral, and operator norms.

Derive tail/statistical distance, rejection acceptance, decoding/decryption/correctness failure. Compose across operations/sessions/users only with justified independence or union bound.

## Attack matrix

| Attack | Applicability | Tool/model/config | Time | Memory | Data/samples | Classical/quantum | Status |
|---|---|---|---|---|---|---|---|

Cover relevant primal, dual, decoding, hybrid, meet-in-the-middle, combinatorial, algebraic, subfield/subring/structure, Arora-Ge, and scheme-specific attacks. For BKZ, record block size and sieving/enumeration model.

## Estimator reproducibility

Retain tool/repository, version/commit, environment, full inputs/config, command/API, raw outputs, cost assumptions, and date. Report the conservative applicable minimum plus sensitivity—not an unsupported “N-bit” label.

## Compatibility and sensitivity

Check NTT/root/modulus/ring degree, packing/encoding, gadget/decomposition, key/ciphertext/noise growth, rejection rate, memory, constant-time assumptions, and target workload. Vary critical parameters and report cliff edges/margins.

## Four verdicts

1. formal reduction foundation;
2. concrete attack estimate;
3. correctness/failure target;
4. implementation compatibility.

