# ZKP Review

Apply when a claim concerns an interactive/non-interactive proof or argument, proof/argument of knowledge, polynomial commitment, Fiat-Shamir, recursion, folding, aggregation, or IVC.

## Formal object and setup

- Define relation/language, instance, witness, security parameter, public parameters, transcript, and acceptance predicate.
- Use proof versus argument and knowledge terminology precisely.
- State setup: none, public coin, CRS/SRS, structured/universal/updatable setup, transparent setup, random oracle, or other idealization.
- Record setup generation, trapdoor/toxic-waste, update, and simulation assumptions.

## Property matrix

| Property | Required fields |
|---|---|
| Completeness | perfect/statistical/computational; completeness error |
| Soundness | perfect/statistical/computational; adversary; soundness error; repetition |
| Knowledge soundness | extractor access/model; knowledge error; runtime; rewinding/reset; restrictions |
| Zero knowledge | perfect/statistical/computational; HV/malicious verifier; simulator inputs; auxiliary input; trapdoor |
| Simulation soundness/extractability | attack interface, prior simulated proofs, extraction conditions, composition target |

Do not replace knowledge soundness with soundness, zero knowledge with witness indistinguishability, or malicious-verifier ZK with HVZK.

## Fiat-Shamir and oracle models

- Identify the underlying public-coin protocol and every transcript field hashed into the challenge.
- Check canonical encoding, context/session/protocol binding, and domain separation.
- State ROM versus QROM and classical versus quantum adversaries.
- Audit programmability, rewinding/forking or measure-and-reprogram steps, query bounds, abort events, and concrete loss.
- A ROM proof does not establish QROM security by analogy.

## Composition and advanced systems

When applicable, check:

- sequential/parallel repetition and independence/correlation of challenges;
- concurrency, malleability, chosen-statement attacks, aggregation, and batching;
- polynomial-commitment binding/extractability, degree bounds, opening aggregation, and setup;
- lookup/range/custom-gate soundness and table/selector commitments;
- recursion/curve-field cycles, arithmetization compatibility, verifier-circuit semantics, and base-case handling;
- folding/IVC accumulation invariant, relaxed relation, commitment binding, and final extraction/soundness bridge.

## Cost ledger

Keep distinct:

- witness size, constraints/gates/rows, polynomial degree, domain size;
- prover/verifier time and memory;
- proof size, rounds, and communication;
- field/group operations, MSMs, pairings, hashes, FFT/NTT work;
- setup/preprocessing versus online work;
- single, amortized, batched, aggregated, and recursive costs;
- asymptotic bounds versus measured implementation results.

## ZKP verdict limits

Report each property independently. A correct polynomial commitment or local folding lemma does not establish end-to-end knowledge soundness, zero knowledge, or composable security without the remaining implication chain.

