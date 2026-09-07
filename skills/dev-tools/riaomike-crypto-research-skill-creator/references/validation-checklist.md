# Validation Checklist

Use this checklist after creating a skill, during an audit, and after a refactor. A static validator may assist with structural items, but every semantic item requires human or agent judgment backed by inspected evidence.

## Severity model

| Severity | Meaning | Release rule |
|---|---|---|
| Blocking | Can cause fabricated evidence, materially false research conclusions, unsafe scope expansion, or unusable skill discovery | Must be resolved before release |
| Major | Likely to cause inconsistent or incomplete results in realistic use | Resolve or disclose with a concrete limitation |
| Minor | Clarity, maintainability, or efficiency issue with low correctness risk | May be deferred and recorded |

## A. Structure and discovery

- [ ] `SKILL.md` exists and begins with valid YAML frontmatter.
- [ ] `name` is lowercase hyphen-case, at most 64 characters, and matches the directory.
- [ ] `description` begins with `Use when`, names concrete triggers, and avoids workflow summary or catchall language.
- [ ] Positive triggers, close negatives, and ambiguous cases are identifiable from the skill.
- [ ] `SKILL.md` links every conditional reference and says when to read it.
- [ ] All relative links resolve and all text files are UTF-8.
- [ ] No intentional scaffold token remains in a deployed `SKILL.md`.
- [ ] Optional files have a concrete role; there are no empty placeholder directories.

Blocking examples: missing `SKILL.md`, broken core reference, or description so broad that unrelated research tasks activate the skill.

## B. Contract and authorization boundary

- [ ] Scope names the permitted action, artifacts, evidence boundary, mutation boundary, and conclusion boundary.
- [ ] Out-of-scope work and neighboring workflows are stated where confusion is plausible.
- [ ] Required inputs distinguish research-critical missing data from assumptions that can safely be stated.
- [ ] Outputs are observable artifacts or report fields, not only process steps.
- [ ] Success criteria can be independently checked.
- [ ] Failure modes define stop, ask, narrow, mark-unverified, or partial-result behavior.
- [ ] External mutation, publication, messaging, submission, or account access is never inferred from a research request.
- [ ] Retry/search loops have bounded stopping criteria proportional to cost and risk.

Blocking examples: skill claims permission to submit a paper; skill fabricates an answer when a cited source cannot be opened.

## C. Harness portability

- [ ] The portable core does not require a named model, vendor API, proprietary connector, fixed subagent count, GUI state, or hidden memory.
- [ ] Capability requirements are expressed as outcomes: search, inspect, execute, render, or verify.
- [ ] Missing optional capabilities produce an explicit degraded mode.
- [ ] Paths are relative and operating-system-neutral.
- [ ] Scripts document runtime and dependencies; deterministic checks avoid unnecessary network services.
- [ ] Harness-specific metadata or permissions live in an optional adapter and do not alter the research contract.

Major example: a literature skill silently assumes authenticated access to one proprietary database.

## D. Citation and evidence integrity

- [ ] Every cited work has verified or explicitly unverified identity fields.
- [ ] Preprint, IACR ePrint, conference, journal, and revised versions are reconciled rather than silently merged.
- [ ] The exact inspected version/date is recorded when numbering or claims may differ.
- [ ] A citation is checked for support of the nearby claim, not only topical relevance.
- [ ] Quotations and theorem/section numbers are checked against the exact version.
- [ ] Search-result snippets, generated summaries, and secondary citations are not treated as primary evidence.
- [ ] Conflicts and inaccessible sources remain visible in the output.
- [ ] The skill explicitly forbids invented authors, titles, venues, years, identifiers, quotations, and theorem numbers.

Blocking examples: allowing plausible citation completion; reporting a paper as verified after seeing only a search snippet.

## E. Claim taxonomy and proof discipline

- [ ] Definitions, assumptions, conjectures, theorems, lemmas, proof sketches, complete proofs, reductions, empirical findings, heuristics, security claims, and novelty claims are labeled separately.
- [ ] The output distinguishes an author's claim from the reviewer's verification.
- [ ] A theorem statement review is separate from proof-validity review.
- [ ] A component theorem is not automatically promoted to protocol security.
- [ ] Reduction direction, source/target problem, runtime, success probability, oracle access, and loss are checked.
- [ ] Proof omissions are located and classified; they are not silently repaired and called verified.
- [ ] Machine verification is claimed only when the specified checker ran successfully on the stated artifact/version.
- [ ] Calibrated language reflects verified, limited, unverified, contradicted, or not-assessable status.

Blocking examples: calling a proof sketch a proof; transferring a theorem to a stronger adversary model without justification.

## F. Security-claim audit

- [ ] The exact security notion and game/definition are stated.
- [ ] Adversary class and powers are stated: classical/quantum, static/adaptive, malicious/semi-honest, uniform/non-uniform, and any restricted model.
- [ ] Setup and idealized models are stated.
- [ ] Assumptions are parameterized and match the construction variant.
- [ ] Reduction tightness, abort probability, query dependence, and concrete loss are accounted for.
- [ ] Composition, concurrency, multi-user, chosen-statement/message, and side-channel boundaries are addressed when relevant.
- [ ] Correctness, privacy, authenticity, soundness, knowledge, and composability claims are not conflated.

Blocking example: claiming standard-model post-quantum security from a classical-ROM argument.

## G. ZKP checks

Apply when the skill creates or evaluates ZKP-related conclusions.

- [ ] Language/relation, instance, witness, public parameters, and transcript are defined.
- [ ] Proof/argument and knowledge terminology are precise.
- [ ] Completeness type/error are stated.
- [ ] Soundness type/error and repetition/composition are stated.
- [ ] Knowledge soundness/extraction model, knowledge error, access, and runtime are stated when claimed.
- [ ] Zero-knowledge type, verifier model, simulator inputs, auxiliary input, and setup trapdoor are stated.
- [ ] Witness indistinguishability, HVZK, malicious-verifier ZK, simulation soundness, and extractability are not conflated.
- [ ] Fiat-Shamir review states ROM/QROM, adversary type, oracle programmability, transcript binding, query/reduction loss, and domain separation.
- [ ] Aggregation, batching, recursion, lookup, polynomial commitment, folding, or IVC checks are included when relevant.
- [ ] Costs separate constraints/rows/degree, prover/verifier work, proof size, rounds, group/field/hash operations, preprocessing, and amortization.

Blocking example: treating a ROM proof as a QROM proof without a cited and checked transformation.

## H. Lattice checks

Apply when the skill creates or evaluates lattice-related conclusions.

- [ ] Exact problem variant is named: LWE/Ring-LWE/Module-LWE, SIS variants, search/decision, primal/dual, and structured/unstructured.
- [ ] Dimension/rank, modulus, sample count, secret/error distributions, norm, and bounds are recorded.
- [ ] Algebraic structure, embedding, and norm conventions are explicit.
- [ ] Reduction direction, target lattice problem, approximation factor, modulus/noise constraints, dimension mapping, and classical/quantum nature are checked.
- [ ] Distribution parameters, tail bounds, smoothing conditions, rejection sampling, and statistical distance are checked.
- [ ] Decryption/decoding/failure probability and accumulation across repeated operations are checked.
- [ ] Estimator name/version/configuration and classical/quantum attack cost models are recorded.
- [ ] Relevant primal, dual, decoding, hybrid, algebraic/structural, and combinatorial attacks are considered.
- [ ] Reported security bits name cost metric, memory/data assumptions, and sensitivity.
- [ ] NTT/modulus/ring/packing/gadget/noise compatibility is checked when implementation claims depend on it.

Blocking example: claiming a Module-LWE parameter set is secure solely because a generic LWE reduction exists.

## I. Parameters, probability, and complexity

- [ ] A parameter ledger defines each symbol, domain/unit, source/derivation, constraints, and uses.
- [ ] Security parameter, dimension, bit length, modulus, field size, and sample count are not conflated.
- [ ] Probability spaces, conditioning events, independence, and negligible variables are explicit.
- [ ] Soundness, correctness, abort, extraction, and decryption failures are separated and accumulated correctly.
- [ ] Every asymptotic bound states variables and computational model.
- [ ] Concrete comparisons use compatible hardware, software, implementation version, batch size, and measurement method.
- [ ] Setup, preprocessing, online, amortized, batched, worst-case, and average costs are labeled.
- [ ] Communication, proof/ciphertext/key size, memory, and serialization are included when material.
- [ ] Reduction loss maps concrete assumption security to the claimed protocol security.
- [ ] Hidden constants or lower-order terms are disclosed when they affect the conclusion.

Blocking example: reporting 128-bit protocol security while ignoring a reduction loss that exceeds the underlying margin.

## J. Novelty and literature coverage

- [ ] The target claim is decomposed into searchable concepts and synonyms.
- [ ] Sources, exact queries, date, filters, and inclusion/exclusion criteria are recorded.
- [ ] Backward/forward citation chaining and closest-author/venue checks are used when available.
- [ ] Versions are deduplicated without losing their differences.
- [ ] Closest prior art is compared claim by claim, not only by title/abstract similarity.
- [ ] Negative results specify searched scope and blind spots.
- [ ] “First,” “novel,” “unprecedented,” and equivalent universal claims are prohibited unless independently established by evidence beyond ordinary search.
- [ ] The final wording is bounded: no matching prior result was found within named sources, queries, and dates.

Blocking example: asserting novelty after one keyword search or from an inaccessible corpus.

## K. Behavioral scenarios

Run in fresh contexts when independent-agent evaluation is available:

1. normal in-scope request;
2. close non-trigger request;
3. missing primary source;
4. conflicting preprint/published versions;
5. pressure to invent a citation;
6. pressure to certify novelty;
7. theorem with a proof sketch but protocol-level security claim;
8. Fiat-Shamir claim with ROM/QROM ambiguity;
9. lattice parameter set missing distribution/norm information;
10. incompatible cost comparison;
11. no network, parser, estimator, or proof checker.

For each scenario record trigger decision, clarifications, evidence inspected, output status, unsupported assertions, and whether the promised artifact shape was produced. If no independent run occurred, label behavioral validation **not executed**.

## Audit report schema

```markdown
# Skill Audit: NAME

## Verdict
PASS | PASS WITH LIMITATIONS | FAIL

## Evidence inspected
- Files, versions, scripts, and scenarios actually inspected or run

## Findings
### Blocking
- [ID] Location — evidence — consequence — required repair

### Major
- [ID] Location — evidence — consequence — recommended repair

### Minor
- [ID] Location — evidence — suggested improvement

## Domain coverage
- Claim taxonomy:
- Citations:
- Security model:
- ZKP checks: applicable / not applicable, with reason
- Lattice checks: applicable / not applicable, with reason
- Parameters and complexity:
- Novelty:

## Unverified items
- Missing sources, capabilities, versions, or behavioral tests

## Release decision
- Resolved blockers and disclosed remaining limitations
```

