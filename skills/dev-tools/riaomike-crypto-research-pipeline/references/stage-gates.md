# Stage Gates and Rollback

Use exactly four stage states: `pass`, `pass-with-limitations`, `fail`, and `blocked`. A later stage may add evidence but may not silently promote an earlier stage.

| Stage | Required evidence | Gate | Roll back when |
|---|---|---|---|
| Intake | scope, research question, constraints, accountable humans, ethics/disclosure triage | scope is bounded and responsible decisions are identified | scope, stakeholders, or risk profile changes |
| Idea | contribution hypothesis, feasibility risks, discriminating tests, kill criteria | at least one concrete falsifiable path is credible | feasibility or significance premise fails |
| Literature | reproducible queries, screened corpus, verified identifiers, closest works | coverage is adequate for the stated search boundary | new terminology, citation chain, or closest work appears |
| Related work and novelty | claim matrix, overlap analysis, calibrated novelty statement | no unresolved material overlap supports the same claimed contribution | materially closer work or a stronger equivalence is found |
| Theory and security | definitions, theorem statements, assumptions, reductions, property analysis | no blocking correctness/security gap remains for claimed results | proof gap, model mismatch, missing assumption, or composition issue appears |
| Parameters and empirical plan | parameter lineage, estimator/tool versions, experiment protocol, baselines | claims are reproducible and comparisons are fair | parameter, implementation, hardware, dataset, or baseline changes |
| Evidence and artifacts | frozen inputs, commands, environments, seeds, outputs, claim map | every empirical claim has traceable evidence and limitations | rerun diverges or artifact/claim mapping breaks |
| Writing | outline, claim ledger, citations, figures/tables, limitation language | manuscript wording does not exceed evidence | any upstream status or evidence changes |
| Internal review | independent issue list, severity, response, re-check | no unresolved blocking issue remains | revisions introduce or expose a blocker |
| Compliance and sign-off | current venue policies, ethics, authorship, disclosures, final files | responsible humans approve the final package | policy, authorship, disclosure, claim, or artifact changes |

## Human Gates

Require explicit human decisions for:

- the primary contribution and final claim boundaries;
- ethics, privacy, dual-use, vulnerability, and disclosure handling;
- resource-intensive, risky, or third-party-impacting experiments;
- authorship, acknowledgments, conflicts, funding, and AI-use disclosure;
- final manuscript wording and any external submission.

## Blocker Propagation

1. Identify the earliest stage responsible for the failed premise.
2. Mark every dependent claim and stage `blocked` or `pass-with-limitations`.
3. Remove or qualify downstream prose immediately.
4. Record the old and new state; never rewrite history.
5. Re-run the responsible gate and every dependent gate after repair.

