---
name: usenixsec-writing-style
description: Use when drafting or revising prose for a USENIX Security Symposium paper — threat-model-first structure, calibrated security claims, disclosure narrative woven into the text, the current USENIX page budget, and the plain systems-security register this program committee rewards.
---

# USENIX Security Writing Style

A USENIX Security paper argues like an engineer under oath: state what the adversary can do, show what you built or broke, measure it honestly, and say plainly what does not follow. Adapted from the USENIX writing-style guidance in the Awesome-Journal-Skills collection (MIT).

## Scope

In scope: threat-model-first structure and wording; quantified claim calibration (numbers beat adverbs, populations beat anecdotes); disclosure and responsible-conduct narrative at the point of need; page-budget planning for the current USENIX limit; plain systems-English register; caption discipline; self-anonymization at submission time; and revision passes that check adversary consistency and calibration.

Out of scope: inventing systems, attacks, measurements, or citations; deciding novelty or authorship; guaranteeing acceptance; or submitting without human authorization.

## Required Inputs

- current USENIX Security official call for papers and template (page budget, appendices, ethics, AI-disclosure, artifact policy);
- manuscript draft or section under revision;
- the stated threat model or raw security claims;
- measurement data or attack demonstrations for calibration.

## Success Criteria

- Every claim is located relative to an adversary: the threat model appears early, is precise, and the evaluation never silently assumes a stronger or weaker attacker than the model granted.
- Non-goals are named as concretely as goals ("side channels are out of scope").
- Strong verbs carry their measurement: "blocks 387/412 ROP chains at 2.1% median CPU overhead", not "completely prevents attacks with negligible overhead".
- The disclosure thread is present where the reader needs it: scan methodology states rate limits and opt-out handling; vulnerabilities state when and how they were reported.
- Figures and tables are self-contained: a reviewer flipping pages can reconstruct the results story from captions alone.
- The body fits the current USENIX page budget using the unaltered official template; compression comes from cutting re-narration, never spacing tricks.
- No AI-flavor prose remains (see crypto-venue-paper-writing's de-AI checklist for the grep-level rules).

## Failure Modes

- Threat model missing or shifting between model and evaluation: stop and reconcile before revising prose.
- Marketing or false modesty: rewrite with quantified hedging; a real result buried in modesty is as damaging as an overclaim.
- Live harm potential described without a responsible-conduct thread: add the disclosure narrative at the point of need.
- USENIX page budget or template may have changed since training: verify the current official call before any budget claim.
- De-identification gap: anonymize names publicly attached to the group at submission time.

## Workflow

1. Verify the current USENIX call and template; record a dated policy snapshot.
2. Fix the threat model and non-goals early (typically Section 2 or 3); state the measurement vantage and validity.
3. Write or revise against a per-section page budget.
4. Calibrate every strong claim: hunt "completely / trivially / negligible / guarantees" and attach numbers or delete.
5. Weave the disclosure narrative into the methodology and vulnerability sections.
6. Run the adversary-consistency pass, calibration pass, cold-reader pass, and caption pass.
7. Run the de-AI grep checklist; fix every hit or record a waiver.
8. Use [evaluation-scenarios.md](references/evaluation-scenarios.md) for future independent evaluation.

## Output Contract

Return: threat-model precision verdict and evaluation-consistency check; calibrated claim table with rewrites; disclosure-thread report (present at point of need, or gaps); per-section page usage versus budget with overflow routing; dated policy snapshot; unresolved items for the human author.

## Reference Files

| File | Contents |
|------|----------|
| `references/section-budget.md` | Page budget table, calibration examples, register and revision-pass notes |
| `references/evaluation-scenarios.md` | Test specifications for independent evaluation |
