---
name: quality-vv
domain: software-engineering/quality-vv
trigger: "\"write a V&V plan\", \"set quality goals\", \"build a traceability matrix\", \"should we model-check this\"."
anti_trigger: "Running the outage; regulator evidence (subskills/regulated-software.md); the test portfolio; proving a defect class; delivery metrics."
scope: "Quality model (ISO 25010), V&V plan, traceability, formal-methods ladder"
status: "seedling"
---

# Quality & V&V

## Standard

- **ISO/IEC 25010:2023** has nine characteristics: functional suitability, performance efficiency, compatibility, interaction capability (was usability), reliability, security, maintainability, flexibility (was portability), safety (new). ⚠️ Rename mapping is from secondaries; ISO text paywalled (see Sources).
- **V&V plan** pairs every requirement with a verification method and evidence, so verification answers "how do we know".
- **The pragmatic ladder**: assertions → contracts → stateless property tests → stateful model-based → TLA+ or Alloy on hot paths → full verification (SPARK, F*, proof assistants) for kernels and crypto.
- **Alloy**: Jackson's small-scope hypothesis — most design flaws have small counterexamples, so a bounded check catches the bulk.
- **TLA+ at AWS**: specification found a DynamoDB fault-recovery bug needing a 35-step interleaving no reviewer imagined. ⚠️ Source not cited inline; check the Sources list before relying on this figure.

## Decision rules

1. Turn each NFR into a measurable quality attribute with a number and a method (out of scope for this leaf: NFR authoring).
2. Pick the cheapest ladder rung that can find the defect you fear. A protocol defect does not wait for a unit test.
3. Property tests are the bridge: stateless round-trip, then stateful model-based where the machine has states.
4. Verify the verifier: sabotage the model and confirm the property fails. A property that survives a broken system is vacuous.
5. Traceability is bidirectional: every requirement has a test, every test names a requirement. Tool qualification matters where the tool carries verification credit.
6. ⚠️ "Per-commit for fast checks, per-release for heavyweight provers" is inferred from tool performance, not a published policy.

## Procedure

1. List the quality attributes that matter, from the spec and the risk list, and state each as measurable: "availability 99.9 % over 30 days".
2. Pick the verification method per attribute: test, analysis, inspection or formal model, and write the V&V plan as attribute, method, evidence, owner, gate.
3. Build the trace matrix:
   ```markdown
   | Requirement | Test | Evidence | Status |
   |---|---|---|---|
   | REQ-14 idempotent charge | charge_test::same_key_replays | CI run 4821 | pass |
   ```
4. Start at ladder rung one: assertions on the invariants that must never break.
5. Add property tests for any pure function with a round trip or a metamorphic relation (out of scope for this leaf: property-test design).
6. Model the concurrency or recovery path when the failure needs an interleaving; bound constants.
7. Sabotage once: break the invariant, prove the property fails, restore. Then keep the matrix current, and review the plan at every release gate.

## Anti-patterns

- Quality goals with no number.
- A property test that cannot fail.
- A trace matrix built at audit time from memory.
- A ladder jump to a proof assistant for a small utility.
- Verification credit given to an unqualified tool.

## Done checklist

- [ ] Every NFR has a number and a method.
- [ ] V&V plan written with evidence and owner.
- [ ] Trace matrix bidirectional and current.
- [ ] Ladder rungs chosen per defect class.
- [ ] Model sabotage test run once per model.
- [ ] Plan reviewed at the release gate.

## Sources

- <https://lamport.azurewebsites.net/tla/amazon-excerpt.html>
- <https://www.iso.org/standard/78176.html>
