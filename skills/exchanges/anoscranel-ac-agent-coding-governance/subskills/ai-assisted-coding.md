---
name: ai-assisted-coding
domain: software-engineering/ai-assisted-coding
trigger: "\"review AI-generated code\", \"the agent wrote this patch\", \"govern agent-written code\", \"who is liable for generated code\"."
anti_trigger: "Setting up the agent's instruction file (subskills/agent-context.md); designing the tests that gate output; the human review pass; CI gate order; control selection."
scope: "Governing agent-written code: gates, review packet, provenance, liability"
status: "seedling"
---

# AI-Assisted Coding

## Standard

- **Never merge unreviewed agent output**. The defect profile is invented APIs, fabricated packages, and requirement conflicts that still compile — plausible, not correct.
- **Functionally correct ≠ policy-conformant**: repo-policy violations appear in 43.1 % of correct patches, about half in intermediate steps, so the conformance check belongs inside the implementation lane (arXiv 2610.06193v1 ⚠️ single paper).
- **Provenance log**: model, prompt version, output hash, reviewer — an SBOM for prompts.
- **License hygiene**: a 2026 audit found licence conflicts in 68 % of 947 codebases. Scan every diff. ⚠️ Vendor-sourced figure.
- **Doe v. GitHub** (9th Cir., 16 Sep 2026) rejected the DMCA §1202(b) output theory, but output can still infringe, and contract and strict-liability exposure still runs against the deployer.
- **Authorship** needs documented human control; prompts alone never establish it. ⚠️ Practitioner rung.

## Decision rules

1. Every agent change arrives with a review packet: diff, test report, eval result, provenance, rollback note.
2. Green tests are evidence, not verdict. Validate the tests themselves: same-signature failure clustering, mutation floor, changed-line coverage (out of scope for this leaf: test-adequacy method).
3. Weak tests are never adjusted to pass. Characterization tests are pinned before the agent starts.
4. License scans block at merge, not after release.
5. Reviewer identity is recorded. Unattributed agent output is unmergeable.
6. Merging and publishing are **human-gated**, as is any authorship or compliance claim.
7. Gates must resist habituation: track approvals and spot-audit a sample.
8. ⚠️ The METR result (19 % slower while believing they were faster) stands; never quote it bare.

## Procedure

1. Fix the contract first: spec, standards, boundaries (out of scope for this leaf: spec authoring).
2. Pin characterization tests on the target behaviour.
3. Let the agent generate in an isolated workspace.
4. Run the deterministic gates before any human reads the diff: build, lint, tests, license scan.
5. Assemble the review packet: diff, gate outputs, provenance, rollback note, requirement→test map.
6. Review for the defect class: invented APIs, fabricated packages, weakened assertions, silent policy drift.
7. Spot-check provenance: model, prompt version, output hash, reviewer.
8. Record the merge decision and the approver.
9. Watch the deployed change against the SLO (out of scope for this leaf: SLO definition); roll back before debugging forward.
10. Monthly: sample prior approvals. A gate that rubber-stamps has failed.

## Anti-patterns

- Merging on green tests alone.
- An agent editing a test to make it pass.
- Agent commits with no recorded provenance.
- An auto-approve path nobody spot-audits.
- An authorship claim over output a human never read.

## Done checklist

- [ ] Review packet complete for every agent change.
- [ ] Characterization tests pinned before generation.
- [ ] Deterministic gates ran before human review.
- [ ] Provenance recorded: model, prompt version, output hash, reviewer.
- [ ] License scan passed on the diff.
- [ ] Human merged; spot-audit scheduled.

## Sources

- <https://dev.to/jackfigliomeni/verification-discipline-catching-and-correcting-hallucinations-in-ai-coding-agents-2cj7>
- <https://techpolicylaw.org/updates/ninth-circuit-affirms-dismissal-of-programmers-dmca-claim-against-github-copilot>
