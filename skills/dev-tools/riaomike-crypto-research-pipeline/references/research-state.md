# Research State Ledger

Maintain one versioned, machine-readable or clearly structured ledger. Suggested schema:

```yaml
project:
  id: stable-local-id
  version: 1
  question: "..."
  intended_contribution: "..."
  target_venue: null
  status: not-ready
  responsible_humans: []
stage_ledger:
  idea: {status: blocked, evidence: [], limitations: [], blockers: []}
claims:
  - id: C1
    text: "..."
    type: definition|lemma|theorem|security|novelty|complexity|parameter|empirical
    dependencies: []
    evidence: []
    confidence: low|medium|high
    permitted_wording: "..."
sources:
  - id: S1
    title: "..."
    authors: []
    year: null
    doi_or_url: null
    verification: verified|partially-verified|unverified
proofs: []
parameters: []
experiments: []
artifacts: []
risks: []
decisions: []
policy_snapshots: []
next_action: null
```

## Provenance Rules

- Give every important claim and evidence object a stable identifier.
- Record exact source locations, versions, commits, commands, tool versions, parameters, seeds, and dates when applicable.
- Keep `reported`, `derived`, `estimated`, `measured`, and `independently reproduced` evidence distinct.
- Link manuscript sentences, figures, and tables back to claim and evidence identifiers.
- Preserve superseded states and the reason for every material change.
- Never upgrade verification or confidence merely because text was polished or repeated.

## Claim Dependencies

Treat dependency edges as actionable. A concrete-security claim may depend on a formal reduction, parameter set, estimator configuration, implementation, and benchmark environment. If any dependency is invalidated, the claim must be re-evaluated and its permitted wording updated.

