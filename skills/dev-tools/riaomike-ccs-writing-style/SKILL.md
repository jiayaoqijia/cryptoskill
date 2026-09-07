---
name: ccs-writing-style
description: Use when revising an ACM CCS paper for a precise threat model, calibrated attack/defense claims, the CCS page budget, double-blind wording, adaptive-evaluation honesty, and the security house style expected by an adversarial SIGSAC program committee.
---

# CCS Writing Style

A CCS paper must let an adversarial reviewer locate every claim against a named adversary and checked evidence. Adapted from the CCS writing-style guidance in the Awesome-Journal-Skills collection (MIT).

## Scope

In scope: threat-model-first structure and wording; first-page security contribution framing; claim-to-evidence pairing (proof, measurement, exploit, or cost); page-budget compression for the current CCS limit; double-blind anonymization of self-citations, tool names, acknowledgments, and artifacts; adaptive-evaluation honesty for defenses; sentence-level rewrites that remove overclaiming; and an output diagnosis format for revision.

Out of scope: inventing attacks, defenses, measurements, or citations; deciding novelty or authorship; guaranteeing acceptance; or submitting without human authorization.

## Required Inputs

- current CCS official call for papers and template (page limit, anonymity, ethics, AI-disclosure, artifact policy);
- manuscript draft or section under revision;
- stated threat model, or the raw security claims to be given one;
- evaluation data or attack demonstrations that claims must be calibrated against.

## Success Criteria

- The security contribution is on the first page: problem, attacker, gap, mechanism, evidence.
- The threat model is explicit and early, names attacker capabilities, knowledge, position, and goal once, and every attack/defense step stays inside those capabilities.
- Every security claim is paired with proof, measurement, exploit demonstration, or a cost number; nothing reads as marketing.
- Claims survive an adversarial pass: no overstated exploitability, no "practical" claims beyond the tested environment and versions, adaptive defenses state the attacker they were tested against.
- Double-blind wording holds in self-citations, tool names, acknowledgments, and artifact descriptions.
- The body fits the current CCS page budget with the core argument readable without the appendix.
- No AI-flavor prose remains (see crypto-venue-paper-writing's de-AI checklist for the grep-level rules).

## Failure Modes

- No threat model or a shifting one: stop and draft the adversary statement before revising claims.
- Attack/defense claim without evidence anchor: expose it and scope the claim to what was measured or demonstrated.
- CCS page limit may have changed since training: verify the current official call before any compression claim.
- De-identification gap: fix author names, institution, and identifying repository references before the format pass.
- Evaluation only against the designed-for attack: report it as a standing limitation, not as strength.

## Workflow

1. Verify the current CCS call and template; record a dated policy snapshot.
2. Read the draft and produce a diagnosis: clear / under-specified threat model / overclaimed / overloaded.
3. Fix the threat model and the first-page framing first.
4. Rewrite claims against evidence: pair each claim with proof, measurement, exploit, or cost.
5. Compress to the page budget, moving transcripts, extra measurements, and full proofs to appendices with forward references.
6. Run the double-blind scan and the de-AI grep checklist; fix every hit or record a waiver.
7. Use [evaluation-scenarios.md](references/evaluation-scenarios.md) for future independent evaluation.

## Output Contract

Return: writing diagnosis; first-page fix; claim-discipline table (claim mapped to proof/measurement/exploit/cost); compression cuts (move/delete/merge); anonymity edits; page-budget report; dated policy snapshot; unresolved items for the human author.

## Reference Files

| File | Contents |
|------|----------|
| `references/sentence-rewrites.md` | Draft-pattern to CCS-safe-rewrite table and compression vignette |
| `references/evaluation-scenarios.md` | Test specifications for independent evaluation |
