# Cryptography Research Conventions

Use this reference whenever a target skill handles cryptographic literature, theorem/proof review, security claims, ZKPs, lattices, parameters, concrete security, or novelty.

## 1. Epistemic and claim taxonomy

Classify each consequential statement before evaluating it.

| Claim type | Required evidence | Do not confuse with |
|---|---|---|
| Definition | Exact formal objects, quantifiers, notation, and source/version if imported | Theorem or accepted convention |
| Assumption | Named computational/statistical assumption, parameter regime, adversary model | Proven fact |
| Theorem/lemma | Precise statement plus a complete valid proof or checked formal artifact | Proof sketch, citation, experiment |
| Proof sketch | Main argument with explicitly omitted obligations | Complete proof |
| Reduction | Source/target problems, direction, simulator/reduction, success and resource loss | Informal analogy |
| Security claim | Security notion, game/model, adversary powers, assumptions, parameters, reduction and loss | Functional correctness or theorem in a component |
| Empirical claim | Reproducible measurement, implementation/version, hardware, dataset/workload, statistic | Asymptotic guarantee |
| Heuristic | Rationale, empirical support, and known limits | Standard-model proof |
| Novelty claim | Reproducible bounded search and comparison against closest prior art | “No result found” from casual search |

For every claim, report one status: **verified**, **supported with limitations**, **unverified**, **contradicted**, or **not assessable from supplied evidence**.

## 2. Theorem, proof, and security are separate reviews

### Theorem statement review

Check:

- all objects, domains, distributions, security parameters, probability spaces, and quantifiers are defined;
- preconditions are sufficient and consistent;
- asymptotic and concrete regimes are not mixed;
- negligible/statistical bounds name the variable and limit;
- the conclusion matches the formal statement used later.

### Proof review

Check:

- every inference has a stated premise, earlier result, or independently verified citation;
- case splits are exhaustive and conditioning events are valid;
- independence, distributional equivalence, and rewinding assumptions are justified;
- hybrid games have defined transitions and accumulated advantage;
- reduction direction, input distribution, runtime, oracle access, and success probability are explicit;
- approximation, tail, union, and failure-probability bounds preserve constants and domains;
- omitted algebra or probability steps are reconstructed or marked as gaps.

### Security-claim review

Check:

- exact notion: indistinguishability, unforgeability, binding, hiding, soundness, knowledge soundness, simulation soundness, extractability, UC/composable security, and so on;
- adversary: classical/quantum, uniform/non-uniform, static/adaptive, malicious/semi-honest, algebraic/generic restrictions if any;
- model/setup: standard model, ROM/QROM, CRS, trusted setup, transparent setup, programmable oracle, generic group, AGM, or other idealization;
- reduction: tightness, abort probability, query dependence, concrete loss, and parameter mapping;
- composition and concurrency conditions;
- implementation assumptions and side channels excluded from the proof.

A correct local theorem may be insufficient for the protocol-level security claim. Report the implication chain explicitly.

## 3. Citation and source verification

For each cited item, retain:

- normalized title and author list;
- document type and publication state;
- stable identifier when available: DOI, IACR ePrint number, arXiv identifier, publisher page, or proceedings record;
- exact version/date inspected;
- direct source location and access date when relevant;
- the specific claim, theorem, definition, or data the source supports;
- verification status.

Verification protocol:

1. Discover broadly, then verify against a primary or authoritative record.
2. Open the exact paper/version; search snippets and secondary summaries are not claim evidence.
3. Check that title, authors, year, venue, and identifier refer to the same work.
4. Check theorem/section numbering against the inspected version.
5. Read enough local context to rule out a negation, caveat, different model, or changed parameter regime.
6. Record version relationships among preprint, IACR ePrint, conference, journal, and revision.
7. Mark unresolved discrepancies rather than choosing the most convenient record.

Never fabricate or autocomplete bibliographic facts. Never cite a paper merely because its title sounds relevant.

## 4. Novelty and prior-art claims

Novelty conclusions must be bounded by a reproducible search record:

- research question and claim decomposition;
- databases/indexes/repositories searched;
- exact queries, synonyms, notation variants, and date of search;
- backward/forward citation chaining and key-author/venue checks when available;
- inclusion/exclusion criteria and version deduplication;
- closest prior work with a claim-by-claim comparison;
- blind spots: inaccessible sources, language limits, unpublished work, patents, informal notes, or cutoff dates.

Permitted conclusion shape:

> No earlier result matching criteria X was found in sources Y using queries Z through date D; the closest results differ in A/B/C. This is not proof of global novelty.

Disallowed conclusion shape: “This is the first” or “the idea is novel” based only on a finite, undocumented, or unverified search.

## 5. ZKP-specific checks

### Formal object and setup

- Define the language/relation, instance, witness, security parameter, and all public parameters.
- Identify interactive, non-interactive, argument, proof, argument of knowledge, or proof of knowledge terminology precisely.
- State setup: none, public coin, CRS, structured reference string, universal/updatable setup, random oracle, or transparent setup.
- State whether setup generation and toxic-waste assumptions are trusted, distributed, updatable, or simulated.

### Security properties

- **Completeness:** perfect, statistical, or computational; include completeness error.
- **Soundness:** computational/statistical/perfect; include soundness error and repetition rule.
- **Knowledge soundness/extractability:** define extractor access, expected/runtime bounds, knowledge error, rewinding, and adversary restrictions.
- **Zero knowledge:** perfect/statistical/computational; honest-verifier or malicious-verifier; simulator inputs, setup trapdoor, and auxiliary input.
- **Simulation soundness/extractability:** state whether required under malleability, aggregation, recursion, or chosen-statement attacks.

Do not substitute plain soundness for knowledge soundness. Do not infer zero knowledge from witness indistinguishability. Do not infer malicious-verifier ZK from HVZK without a transformation and its assumptions.

### Fiat-Shamir and oracle models

- Identify the underlying public-coin protocol and transcript/challenge encoding.
- State ROM versus QROM and classical versus quantum adversaries.
- Check programmability, measure-and-reprogram or rewinding dependencies, query bounds, abort events, and concrete loss.
- Confirm domain separation and binding of all relevant context into the transcript.
- Do not transfer a ROM proof to QROM by analogy.

### Composition and advanced constructions

When relevant, check:

- parallel/sequential repetition and independence conditions;
- concurrency, malleability, and chosen-statement security;
- aggregation/batching and correlated challenges;
- recursion, curve/field cycles, arithmetization compatibility, and verifier-circuit cost;
- lookup/range/custom-gate soundness and table commitments;
- polynomial commitment assumptions, degree bounds, opening aggregation, and trusted setup;
- folding/IVC accumulation invariants and extraction arguments.

### ZKP cost accounting

Separate:

- circuit/R1CS/constraint count, gates, rows, degree, domain size, and witness size;
- prover time, verifier time, proof size, rounds, and communication;
- group operations, pairings, MSMs, hashes, field operations, FFT/NTT work;
- preprocessing/setup versus online cost;
- amortized/batched/recursive cost versus single-instance cost;
- asymptotic bounds versus measured implementation results.

## 6. Lattice-specific checks

### Problem identity

State the exact variant and parameterization, not only the family name:

- LWE, Ring-LWE, Module-LWE, structured/unstructured LWE;
- SIS, Ring-SIS, Module-SIS;
- decision/search, primal/dual, homogeneous/inhomogeneous variants;
- dimension/rank, modulus, sample count, secret distribution, error distribution, norm, and bound.

Do not treat LWE, Ring-LWE, and Module-LWE as interchangeable assumptions. Record algebraic structure and embedding conventions.

### Reduction claims

Check:

- worst-case to average-case direction and exact lattice problem;
- quantum versus classical reduction;
- dimension, approximation factor, modulus/noise constraints, and smoothing conditions;
- ring/number-field restrictions and dual/embedding conventions;
- loss in advantage/runtime and whether the reduction applies to the deployed parameter regime.

The existence of a family-level reduction does not automatically justify a concrete parameter set or structured variant.

### Distributions, norms, and probability

- Define discrete Gaussian, centered binomial, uniform, ternary, sparse, or other distributions with parameters and support.
- Distinguish coefficient, canonical-embedding, Euclidean, infinity, and operator norms.
- Verify tail bounds, smoothing parameters, rejection-sampling acceptance, statistical distance, and accumulated failure probability.
- For encryption/KEM/signature correctness, identify decryption/decoding failure and how it composes across operations.
- Track rounding conventions and modulus switching/rescaling errors.

### Concrete security and attacks

Record:

- estimator/tool name, version/commit, configuration, and date;
- classical and quantum cost models;
- primal, dual, decoding, hybrid, meet-in-the-middle, Arora-Ge, subfield/structure, and relevant combinatorial/algebraic attacks;
- BKZ/block-size and sieving/enumeration models where applicable;
- memory and data/sample assumptions;
- conservative minimum security estimate and sensitivity to parameter changes.

An estimator output is model-dependent evidence, not a theorem. Never report “N-bit security” without attack model, cost metric, and configuration.

### Lattice implementation/parameter compatibility

Check modulus factorization and NTT/root requirements, ring degree, packing/encoding, gadget/decomposition bases, key/ciphertext growth, noise budget, rejection rate, and constant-time/side-channel assumptions when relevant.

## 7. Parameter and complexity audit

Create a parameter ledger for nontrivial tasks:

| Symbol | Meaning | Domain/unit | Source or derivation | Constraints | Used in |
|---|---|---|---|---|---|

Then check:

- symbols are defined once and used consistently;
- security parameter, problem dimension, field/ring size, and bit length are not conflated;
- logarithm bases and bit/word/field-operation costs are stated;
- asymptotic variables and fixed deployment constants are distinguished;
- union bounds and repeated operations accumulate failure correctly;
- reduction loss maps claimed security to assumption security;
- concrete costs use the same hardware/software/batch regime when compared;
- setup, preprocessing, online, amortized, and worst-case costs are labeled;
- hidden constants and lower-order terms are disclosed when they change the practical conclusion;
- communication and storage count serialization/encoding where material.

For every complexity claim, record a cost-model tuple:

```text
(operation model, asymptotic variables, parameter regime, preprocessing,
 amortization/batching, memory, communication, failure probability)
```

## 8. Reporting language

Use calibrated verbs:

- **proves/establishes** only for a complete valid argument in the stated model;
- **supports** when evidence is meaningful but conditional or incomplete;
- **suggests/indicates** for empirical or heuristic evidence;
- **claims/states** when reporting an author's assertion without independent verification;
- **not verified** when evidence or capability is missing;
- **contradicted** only when a specific inconsistency or counterexample is shown.

Always separate the source's claim, the reviewer's verification, and the residual uncertainty.

