# Core Review Protocol

Use this protocol for every review. Domain references add obligations; they do not replace these checks.

## 1. Freeze the reviewed object

Record:

- exact statement text and identifier;
- source file/document version, hash, date, or stable publication version;
- proof artifact type: sketch, prose proof, appendix proof, code, or formal proof object;
- declared security notion/model, adversary, setup, assumptions, and parameters;
- requested depth: statement-only, proof-obligation, full manual reconstruction, reduction, or protocol implication.

Do not combine statements or proof steps from different versions without an explicit version reconciliation.

## 2. Classify claims

Assign one type to every consequential item:

| Type | Minimum evidence |
|---|---|
| Definition | Formal objects, domains, quantifiers, probability space |
| Assumption | Exact problem/notion, parameters, adversary/model |
| Theorem/lemma | Precise statement and complete valid argument or checked formal artifact |
| Proof sketch | Main idea plus explicitly missing obligations |
| Reduction | Source/target problem, direction, algorithm, runtime/success loss |
| Security claim | Game/notion, adversary, setup/model, assumptions, reduction and parameters |
| Empirical/heuristic | Reproducible measurement or rationale and limitations |

Status is one of: **verified**, **supported with limitations**, **unverified**, **contradicted**, **not assessable**.

## 3. Audit the statement before the proof

Check:

- every object, distribution, domain, norm, security parameter, and probability space is defined;
- quantifier order and adversary dependencies are explicit;
- hypotheses are mutually consistent and sufficient for invoked lemmas;
- negligible/statistical claims name the variable and limit;
- asymptotic and concrete regimes are not mixed;
- the conclusion is the same conclusion later cited or composed.

If the statement is ill-formed, report that before reviewing the intended proof.

## 4. Build an obligation graph

Create a row for every nontrivial inference:

| ID | Claim/step | Premises | Evidence/location | Dependencies | Status | Consequence |
|---|---|---|---|---|---|---|

Mark reviewer reconstruction separately. A successful reconstruction may show repairability; it does not change the original artifact's completeness status.

## 5. Check local reasoning

Inspect:

- algebraic equalities, inequalities, type/domain compatibility, and boundary cases;
- conditioning events, independence, distributional equivalence, and support;
- case split exhaustiveness and induction invariants;
- tail, concentration, approximation, hybrid, and union bounds with constants;
- negligible terms and accumulated correctness/soundness/abort/decryption failure;
- rewinding, forking, extraction, oracle programming, and expected-runtime conditions;
- hidden uses of non-uniform advice, adaptivity restrictions, or state reset.

Numerical spot checks can expose errors but cannot replace a general proof.

## 6. Audit games and reductions

For each game hop record:

| Hop | Change | Justification | Assumption/lemma | Advantage delta | Model restrictions |
|---|---|---|---|---|---|

For each reduction record:

- direction and exact source/target problems;
- reduction input distribution and interface/oracle access;
- simulator/extractor behavior and abort events;
- adversary and reduction runtime/memory/query bounds;
- success/advantage equation and concrete loss;
- parameter mapping and whether target assumptions cover the deployed regime;
- classical/quantum and uniform/non-uniform status.

Sum losses and failures explicitly. Never call a reduction “tight” without the concrete relation.

## 7. Verify citations

For each cited dependency:

- match title, authors, version/date, stable identifier, and theorem/section location;
- inspect the exact source, not a search snippet or secondary summary;
- check hypotheses, conclusion, notation mapping, model, and parameter regime;
- record version disagreements.

If inaccessible, keep the dependency and all downstream steps unverified.

## 8. Audit parameters, probability, and complexity

Use a parameter ledger:

| Symbol | Meaning | Domain/unit | Source/derivation | Constraints | Uses |
|---|---|---|---|---|---|

For each complexity claim record:

```text
(operation model, asymptotic variables, parameter regime, preprocessing,
 amortization/batching, memory, communication, failure probability)
```

Check reduction loss against claimed security bits and keep symbolic, measured, amortized, setup, online, communication, and memory costs separate.

## 9. Build the implication chain

Write the explicit chain:

```text
definitions -> lemmas -> theorem -> reduction -> security notion/model
-> composition conditions -> protocol claim
```

Every arrow needs inspected evidence. The final verdict stops at the first missing or invalid arrow.

## 10. Severity

- **Blocking:** invalidates the theorem/proof/security conclusion or relies on fabricated/unavailable critical evidence.
- **Major:** leaves a material obligation, model mismatch, parameter inconsistency, or significant reduction/cost uncertainty.
- **Minor:** clarity or maintainability issue that does not change the conclusion under stated assumptions.

