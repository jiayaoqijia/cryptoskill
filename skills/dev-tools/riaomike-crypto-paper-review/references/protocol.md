# Top-Venue Pre-Review Protocol

## Freeze the review object

Record manuscript/artifact version, target venue, official policy URLs/date checked, review mode, and unseen materials. Extract atomic contribution claims before evaluating prose.

## Review lenses

### Fit and significance

Is the problem in scope, important to the target community, technically non-trivial, and consequential if solved? Separate actual impact from motivation language.

### Novelty and related work

Compare closest work claim by claim across model, assumptions, parameters, functionality, proof basis, and compatible costs. Require bounded novelty and fair adverse citations.

### Correctness and security

Check definitions, theorem statements, proof obligations, reductions, adversary/setup model, composition, parameter mapping, failure terms, and implication chain. For ZKP/lattice work, apply the specialized property/problem distinctions.

### Evidence and reproducibility

Map every table/figure/number/security estimate to reproducible evidence. Check fair baselines, statistics, raw data, environment, artifacts, negative results, and claim-dependent omissions.

### Ethics, disclosure, and policy

Refresh current anonymity, conflict, authorship/AI, ethics, vulnerability disclosure, open-science, artifact, formatting, and submission rules from official sources. Do not hard-code old deadlines/page limits.

### Exposition

Check abstract/body consistency, contribution precision, notation, self-contained definitions, theorem/proof status, figure/table legibility, limitations, and reviewer-verifiable organization.

## Adversarial questions

- What single flaw would invalidate the main claim?
- What closest work makes the delta smallest?
- Which assumption/model/parameter is doing hidden work?
- Which result cannot be evaluated from supplied evidence?
- Is the claimed comparison compatible and fair?
- Does a local theorem actually imply the system claim?

## Finding format

`ID — severity — location — claim — evidence/problem — consequence — required repair/evidence`.

Severity: blocking (invalidates/evaluation impossible/policy desk-reject risk), major (material claim/readiness risk), minor (clarity/maintenance).

## Verdicts

- **Not ready:** unresolved blocking findings.
- **Major revision before submission:** no proven blocker, but material evidence/novelty/correctness gaps.
- **Submission-ready with disclosed limitations:** quality gates passed within inspected evidence; no acceptance prediction.

