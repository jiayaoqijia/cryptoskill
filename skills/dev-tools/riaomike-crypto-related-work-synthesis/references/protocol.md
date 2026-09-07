# Synthesis Protocol

## Normalize the corpus

For each work/version retain identity, publication state, inspected status, claims, model/setup, assumptions, parameters, evidence locations, and limitations. Deduplicate works without erasing version changes.

## Select synthesis axes

Choose axes that explain real technical differences:

- primitive/functionality and problem setting;
- security notion, adversary, setup/model, composability;
- assumption family and structured variant;
- proof/reduction technique and loss;
- parameter regime and correctness/failure;
- asymptotic and compatible concrete costs;
- transparency/trust, implementation, and artifact evidence.

Explain why each axis matters to the synthesis question.

## Build evidence tables

| Work/version | Claim | Model/assumption | Parameters | Evidence status/location | Limitation |
|---|---|---|---|---|---|

| Work/version | Functionality | Security | Setup | Prover/verify/size | Failure | Comparable? |
|---|---|---|---|---|---|---|

Do not rank non-comparable entries.

## Synthesize at four levels

1. **Taxonomy:** families and defining distinctions.
2. **Development:** verified predecessor/extension/correction/attack relations.
3. **Tradeoffs:** what is gained, under which assumption/model/parameter cost.
4. **Gaps:** unstudied combinations, unresolved contradictions, missing evidence, or limitations—bounded by the corpus.

## Writing support

Produce paragraph claims with attached citations/evidence IDs. Separate descriptive consensus, verified technical comparison, and reviewer interpretation. Retain counterexamples and work that weakens the desired narrative.

