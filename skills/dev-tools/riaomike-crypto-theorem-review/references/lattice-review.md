# Lattice Review

Apply when a claim uses an LWE/SIS-family assumption, structured lattice, lattice reduction, distribution/norm bound, correctness probability, or concrete lattice-security estimate.

## Exact problem identity

Record:

- LWE, Ring-LWE, Module-LWE, SIS, Ring-SIS, Module-SIS, or another exact variant;
- search/decision and primal/dual or homogeneous/inhomogeneous form;
- dimension/ring degree/module rank, modulus, sample count, secret/error distribution;
- norm, bound, embedding, ring/number field, and algebraic structure.

Do not treat LWE, Ring-LWE, and Module-LWE as interchangeable assumptions.

## Reduction audit

Check:

- worst-case/average-case direction and exact lattice problem;
- classical versus quantum reduction;
- dimension mapping, approximation factor, modulus/noise constraints, smoothing conditions;
- ring/field/embedding restrictions;
- runtime/advantage loss and applicability to the concrete parameter regime.

A family-level reduction is not a concrete-security proof for one deployment.

## Distribution, norm, and probability

- Define discrete Gaussian, centered binomial, uniform, ternary, sparse, or other distributions with parameters/support.
- Distinguish coefficient, canonical-embedding, Euclidean, infinity, spectral, and operator norms.
- Verify tail bounds, smoothing parameters, statistical distance, rejection-sampling acceptance, and accumulated failures.
- Track rounding, decomposition, modulus switching/rescaling, decoding, and decryption failure.
- Identify independence assumptions and the event over which each probability is taken.

## Concrete security

Record estimator/tool version or commit, configuration, date, classical/quantum cost model, samples/data, memory, and attack family. Consider relevant primal, dual, decoding, hybrid, combinatorial, algebraic, subfield/structure, and meet-in-the-middle attacks.

For BKZ-style estimates, record block size and sieving/enumeration model. “N-bit security” requires a named cost metric, attack model, and configuration; estimator output is model-dependent evidence, not a theorem.

## Parameter/implementation compatibility

When the proof depends on implementation structure, check modulus factorization, NTT roots, ring degree, packing/encoding, gadget/decomposition base, key/ciphertext/noise growth, rejection rate, and constant-time/side-channel assumptions.

## Lattice verdict limits

Separate:

1. formal reduction claim;
2. correctness/failure bound;
3. concrete attack estimate;
4. implementation compatibility;
5. protocol-security implication.

A pass in one category never substitutes for another.

