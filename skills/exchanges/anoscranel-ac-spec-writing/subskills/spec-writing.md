---
name: spec-writing
domain: software-engineering/spec-writing
trigger: "\"Write a spec\", \"draft a design doc\", \"write an RFC for this change\", \"what should the design doc cover\", \"spec this before we code\"."
anti_trigger: "Wording single requirements or acceptance criteria (subskills/requirements.md); recording one decision already made; slicing into tasks."
scope: "Writing a design/spec doc before code: goals, non-goals, alternatives, open questions"
status: "seedling"
---

# Spec Writing

## Standard

- Google design docs and Uber-style RFCs: a short written proposal reviewed before code. It names context, goals, non-goals, the design, alternatives and open questions.
- A written proposal with a mandatory alternatives section invites dissent before commit.
- For agent-built code, requirement detail is a measured lever. Vague inputs can cancel the benefit of refinement (arXiv:2604.25862).
- Decision weight: one-way-door choices get slow review; two-way-door choices get a short doc (Bezos 2015 letter).

## Decision rules

1. Write a spec when the change touches more than one module, adds a dependency, changes a public contract or data schema, or takes more than about 2 days. ⚠️ House threshold.
2. Skip the spec for a fix or change that one reviewer can judge from the diff.
3. Every spec lists at least two real alternatives, including "do nothing". A spec with one option is a plan, not a design.
4. Non-goals are mandatory. They stop scope creep.
5. Every open question has an owner and a date to decide.
6. Length: 1–3 pages for most changes; up to 6 for a one-way-door decision. ⚠️ House convention.
7. The spec is approved before implementation starts. **Human-gated**: spec sign-off.
8. Each architecturally significant decision in the spec becomes a decision record after approval (out of scope for this leaf: the recording format).

## Procedure

1. Copy this template into `docs/specs/NNNN-<slug>.md`:
   ```markdown
   # <Title>
   Status: Draft | In review | Approved | Superseded
   Author, reviewers, date
   ## Context — the problem and why now
   ## Goals — measurable, linked to REQ IDs
   ## Non-goals
   ## Design — data flow, interfaces, data model, failure modes
   ## Alternatives considered — each with why rejected
   ## Risks and mitigations
   ## Rollout and rollback
   ## Test plan
   ## Open questions — owner, due date
   ```
2. Write Context and Goals first. Link each goal to requirement IDs.
3. Write the Design at the level a reviewer needs to find flaws. Show interfaces and data shapes. Skip code.
4. List failure modes: dependency down, bad input, partial write, retry storm.
5. Write Alternatives honestly, with the trade-off each loses on.
6. Write Rollout and rollback. Name the flag, migration order and kill switch.
7. Run a pre-mortem: "it shipped and failed — why?" Add each cause to Risks (Klein).
8. Circulate. Record decisions in the doc. Set Status to Approved only after the human sign-off.

## Anti-patterns

- Spec written after the code to justify it.
- Alternatives section listing straw men.
- Design that is just a class list.
- No rollback section.
- Open questions with no owner.
- Spec that drifts from the code and is never marked Superseded.

## Done checklist

- [ ] Context, goals, non-goals written.
- [ ] Two or more alternatives with trade-offs.
- [ ] Failure modes and rollback written.
- [ ] Test plan linked to goals.
- [ ] Open questions owned and dated.
- [ ] Human sign-off recorded; status Approved.

## Sources

- <https://datafield.dev/the-science-of-luck/part-07/chapter-36/case-study-01.html>
- <https://agilebrandguide.com/wiki/models/jobs-to-be-done-jtbd>
- (spec sign-off is human-gated)
