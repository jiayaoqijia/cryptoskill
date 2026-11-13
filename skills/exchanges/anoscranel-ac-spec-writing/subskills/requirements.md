---
name: requirements
domain: software-engineering/requirements
trigger: "\"Write the user story\", \"add acceptance criteria\", \"is this requirement testable\", \"write the NFRs\", \"turn this request into requirements\"."
anti_trigger: "A whole design document with goals and alternatives (subskills/spec-writing.md); slicing work into tasks."
scope: "Writing stories, acceptance criteria and NFR statements that pass the 29148 quality test"
status: "seedling"
---

# Requirements

## Standard

- **ISO/IEC/IEEE 29148:2018** (2nd edition, 2018-11) is current. Edition 3 is at DIS stage, not published (https://www.iso.org/standard/94091.html). Clause 5.2.5 lists nine characteristics of one requirement: necessary, appropriate, unambiguous, complete, singular, feasible, verifiable, correct, conforming. ⚠️ ISO text is paywalled; the list comes from secondary sources.
- **INVEST** (Bill Wake): a story is Independent, Negotiable, Valuable, Estimable, Small, Testable.
- **Gherkin** Given/When/Then makes a criterion readable by people and runnable by a test tool (https://cucumber.io/docs/gherkin/).
- Write the outcome the user measures, not the feature.

## Decision rules

1. One requirement states one behaviour. Two "and"-joined behaviours fail *singular*. Split them.
2. A requirement with no pass/fail test fails *verifiable*. Rewrite it or label it a hypothesis.
3. Words like "fast", "easy", "robust", "user-friendly" or "etc." fail *unambiguous*. Replace each with a number, a unit and a condition.
4. Implementation detail ("use Redis") is a design decision, not a requirement. Move it to the spec unless a stakeholder truly requires it.
5. An NFR needs a measure, a threshold, a condition and a measurement method. Example: "p95 search latency ≤ 300 ms at 50 requests/s, measured by the load test in CI."
6. Format choice: user story for a user-visible goal; job story ("When…, I want…, so I can…") when the situation matters more than the role; "The system shall…" for interfaces and compliance.
7. Product owns intent. Engineering owns feasibility. ⚠️ This split is org convention, not a standard.

## Procedure

1. Write one line: the outcome and the metric it moves. No outcome → stop and record the gap.
2. Write the need in the user's own words, one sentence.
3. Draft each requirement with a stable ID (`REQ-012`).
4. Add acceptance criteria per requirement:
   ```gherkin
   Scenario: Expired session redirects to login
     Given a user whose session expired 1 minute ago
     When they open /settings
     Then they see the login page
     And the original URL is kept as the return target
   ```
5. Add an exclusion line: what this requirement does not cover.
6. Write NFRs with rule 5.
7. Run the nine-characteristic test on every line. Fix or flag each failure.
8. Link each requirement to its test ID once tests exist. Keep the file in the repo, versioned with the code.

## Anti-patterns

- Acceptance criteria that restate the story.
- A hidden design guess labelled "requirement" (Ralph, arXiv:1304.0116).
- Agent-drafted requirements accepted as correct. Coherent prose is not correct prose.
- NFRs with no measurement method.
- Changing a requirement in chat without updating the file.

## Done checklist

- [ ] Outcome line present.
- [ ] Every requirement has an ID, one behaviour and a pass condition.
- [ ] Every requirement passes all nine 29148 characteristics, or carries a ⚠️ note.
- [ ] Every NFR has measure, threshold, condition and method.
- [ ] Exclusions written.
- [ ] File committed next to the code.

## Sources

- <https://agilebrandguide.com/wiki/models/jobs-to-be-done-jtbd>
- https://www.iso.org/obp/ui#iso:std:iso-iec-ieee:29148:ed-2:v1:en (29148:2018)
- https://cucumber.io/docs/gherkin/
