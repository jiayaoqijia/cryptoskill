# Deep Reading Protocol

## Reading passes

1. **Identity and framing:** exact version, problem, claimed contributions, paper type.
2. **Formal objects:** definitions, notation, games/relations, assumptions, parameters.
3. **Evidence:** theorem/proof/reduction, experiment, artifact, or citation supporting each claim.
4. **Stress reading:** limitations, negative results, hidden model/setup restrictions, incompatible comparisons.
5. **Research integration:** reusable techniques, dependencies, open questions, replication needs.

## Claim-evidence record

| ID | Author claim/location | Type | Evidence/location | Model/parameters | Reviewer status | Limitation |
|---|---|---|---|---|---|---|

Types: definition, theorem, proof/reduction, security, empirical, heuristic, novelty. Status: verified locally, supported with limitations, unverified, contradicted, not assessable.

## Proof and security map

```text
definitions -> lemmas -> main theorem -> reduction -> security notion/model
-> composition/implementation claim
```

Record each missing edge. A reader map is not a full proof audit unless every obligation was independently checked.

## Domain extraction

For ZKPs: relation, setup, proof/argument terminology, completeness, soundness, knowledge, ZK, ROM/QROM, composition, proof system costs.

For lattices: exact LWE/SIS variant, algebraic structure, dimension/modulus/distributions/norms, reduction, failure probability, estimator configuration, attack model, compatibility.

## Parameter/cost ledger

Record symbol, meaning, domain/unit, value/regime, source, constraints, and uses. Separate asymptotic, concrete, measured, setup, online, amortized, communication, and memory costs.

## Final synthesis

State what the paper establishes in its own model; what was independently checked; what remains dependent on citations/artifacts; what would falsify or limit the main conclusion; and which follow-up work matters most.

