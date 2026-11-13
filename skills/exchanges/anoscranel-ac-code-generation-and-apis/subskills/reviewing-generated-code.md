---
name: reviewing-generated-code
domain: software-engineering/reviewing-generated-code
trigger: "Reviewing a change that includes generated artifacts."
anti_trigger: "Not for reviewing hand-written code, and not for reviewing the generator itself."
scope: "Reviewing output without owning it by hand."
status: seedling
---

# Reviewing generated code

## Standard

A review that includes generated artifacts has two different objects in one diff. The hand-written part is reviewed for what it does; the generated part is reviewed for what its inputs were and whether the generator behaved. Reading generated code line by line as if a person wrote it wastes the review on text that will be replaced on the next run, and nitpicks in generated files are the clearest signal a review has lost its object.

The correct review of a generated artifact asks three questions: what input produced it, is that input change the intended one, and does the output change follow from the input change with the pinned generator version. If the diff shows output changes that the input changes do not explain, the finding is a version drift or an unpinned generator — not a comment on the output's style.

Primary source: <https://martinfowler.com/>.

## Decision rules

- Separate generated from hand-written paths in the diff before reviewing.
- Review the input change first; the output review follows from it.
- Verify the generator version that produced the output matches the pinned one.
- Flag output changes unexplained by input changes as a finding, not as noise.
- Do not leave style comments on generated files; route them to the generator's configuration.
- Verify the no-edit markers are intact on every generated file in the diff.

## Procedure

1. Partition the diff into generated and hand-written files.
2. For each generated file, identify the input change that should have produced it.
3. Confirm the pinned generator version is the one in use.
4. Compare the output diff against the input's expected effect.
5. Record any unexplained output change as a finding.
6. Route generator-level issues to the generator's configuration, not the artifact.

## Anti-patterns

- Style comments on generated files.
- Approving a large generated diff as "just generated" without an input to check it against.
- Reading generated code as if a person wrote it and missing an input problem.
- A diff with no generated changes when the input changed — the drift check failed.
- Rewriting generated output to satisfy a review preference.

## Done checklist

- [ ] Diff partitioned by provenance.
- [ ] Input changes identified per generated artifact.
- [ ] Generator version confirmed pinned.
- [ ] Output-to-input correspondence verified.
- [ ] Unexplained changes flagged.
- [ ] No-edit markers verified intact.

## Sources

- Code review practice: <https://martinfowler.com/articles/code-review.html>
- Reproducible artifacts and pinning: <https://reproducible-builds.org/>
- Continuous integration discipline: <https://martinfowler.com/articles/continuousIntegration.html>
