# Theorem Review Protocol

This example protocol is intentionally compact. Adapt it to the theorem family and formalism.

## 1. Freeze the object

Record the exact text, source version/hash/date, theorem identifier, dependencies, and whether the artifact is a statement, sketch, full proof, or formal proof object.

## 2. Statement audit

- Define all objects, domains, distributions, quantifiers, probability spaces, and security variables.
- Check preconditions for consistency and sufficiency.
- Separate asymptotic claims from a concrete parameter instance.
- Identify the exact conclusion and what it does not assert.

## 3. Proof-obligation table

| ID | Claim/step | Evidence | Dependencies | Status | Consequence if unresolved |
|---|---|---|---|---|---|

Use statuses: verified, supported with limitations, unverified, contradicted, or not assessable.

## 4. Local reasoning

Check algebra, inequalities, probability conditioning, independence, distributional equivalence, case coverage, error accumulation, negligible bounds, and constant/parameter domains. For game hops, record each transition and accumulated advantage.

## 5. Reduction audit

Record source and target problems, direction, reduction input distribution, oracle/interface access, simulator behavior, runtime, success probability, abort events, query dependence, and concrete loss. Verify that the target assumption applies in the stated parameter regime and adversary model.

## 6. Citation audit

Inspect the exact cited version. Confirm theorem/section identity, hypotheses, conclusion, model, and parameter regime. If unavailable, mark the dependency unverified rather than using memory or a secondary summary.

## 7. Security implication

Build the implication chain:

```text
local lemmas -> theorem -> reduction -> security notion/model -> protocol claim
```

Every arrow needs a checked argument. A missing composition, extraction, setup, or adversary-model step limits the conclusion.

## 8. Final status

- **Verified:** all material obligations checked within the declared review model.
- **Supported with limitations:** non-blocking omissions or explicit assumptions remain.
- **Unverified:** critical evidence was unavailable or a blocking obligation remains.
- **Contradicted:** a concrete invalid step or counterexample defeats the statement as written.

Never call a manual review machine verification, and never call “no gap found” a proof of correctness.

