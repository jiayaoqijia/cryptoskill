# Sentence-Level Rewrites and Compression

Adapted from the CCS writing-style guidance in the Awesome-Journal-Skills collection (MIT, Copyright (c) 2026 Bryce Wang).

## Threat-model discipline

- Separate what the attacker knows from what it can do from where it sits in the system; a conflated model is the most common source of "the attack assumes too much" reviews.
- State the security goal as a property (confidentiality, integrity, availability, unlinkability) and say what "broken" means quantitatively.
- When a defense is evaluated, name the adaptive attacker it was tested against; a defense measured only against the attack it was designed to stop is a standing CCS complaint.
- Label conjecture, heuristic argument, and proved result distinctly; mixing them near a security claim is a credibility leak at this venue.

## Draft-pattern rewrites

| Draft pattern | CCS-safe rewrite |
|---|---|
| "Our attack is highly effective..." | "recovers the key in N queries against library X vY on platform Z" |
| "Under realistic assumptions..." | "Under threat model T (network MITM, no host access)..." |
| "Our defense is secure..." | "resists the adaptive attacker of Section 5 at C% overhead" |
| "We significantly reduce risk..." | claim scoped to the deployment and versions measured |

## Compression vignette

A draft with a full protocol description, four attack variants, a formal proof, and six measurement figures: keep the threat model, the strongest attack variant end to end, one proof sketch, and the two decision-critical figures (leakage rate and defense overhead); push the other variants, the full proof, and raw measurement tables to appendices with forward references. The test of a good cut: a reviewer should be able to judge novelty and soundness of the attack without opening the appendix.

## Output format

```text
[Writing diagnosis] clear / under-specified threat model / overclaimed / overloaded
[First-page fix] <new framing>
[Claim discipline] <claim -> proof/measurement/exploit/cost>
[Compression cuts] <move/delete/merge>
[Anonymity edits] <phrases to rewrite>
```
