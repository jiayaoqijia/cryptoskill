# ZKP Security Review Protocol

## Formal object

Record relation/language, instance, witness, security parameter, public parameters, transcript/challenge encoding, acceptance predicate, interaction/non-interaction, and proof versus argument terminology.

## Setup

State none/public coin/CRS/SRS/structured/universal/updatable/transparent/random oracle. Record generation, toxic waste/trapdoor, simulation/extraction keys, ceremonies/updates, trust and operational assumptions.

## Property matrix

| Property | Definition/model | Adversary | Error | Proof/reduction | Status/limitation |
|---|---|---|---|---|---|
| Completeness | perfect/statistical/computational | | | | |
| Soundness | perfect/statistical/computational | | | | |
| Knowledge soundness/extractability | extractor access/runtime/restrictions | | knowledge error | | |
| Zero knowledge | perfect/statistical/computational; HV/malicious | | | simulator inputs/trapdoor | |
| Simulation soundness/extractability | chosen-statement/prior simulations | | | | |

Do not infer one row from another.

## Fiat-Shamir

Check public-coin prerequisite; canonical encoding; domain/context/session binding; all committed messages hashed; ROM versus QROM; classical/quantum adversary; oracle programmability; rewinding/forking or measure-and-reprogram; query/abort/concrete loss.

## Dependency and composition graph

Trace commitment/polynomial commitment, arithmetization, degree/lookup/range claims, proof protocol, Fiat-Shamir, aggregation/batching, recursion or verifier circuit, folding/accumulation, and final extraction/security. Every edge needs inspected evidence.

For recursion: base/step relation, cycle/field compatibility, verifier-circuit semantics, base case, accumulation invariant, commitment binding, and final decider/extraction bridge.

## Errors and parameters

Track completeness, soundness, knowledge, simulation, abort, hash/collision, commitment, degree-test, batching, recursion, and correctness errors separately; then compose them with justified independence/union bounds.

## Cost ledger

| Regime | Constraints/degree/domain | Prover | Verifier | Proof/communication | Memory | Setup/amortization | Operation model |
|---|---|---|---|---|---|---|---|

Do not compare incompatible security levels, hardware, implementation versions, batch sizes, or setup accounting.

## Verdict

Give independent statuses per property plus a bounded system conclusion. A local theorem or functional benchmark cannot substitute for the missing rows/edges.

