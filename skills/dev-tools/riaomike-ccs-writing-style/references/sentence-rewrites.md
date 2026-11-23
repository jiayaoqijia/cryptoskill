# Sentence-Level Rewrites and Compression

Adapted from the CCS writing-style guidance in the Awesome-Journal-Skills collection (MIT, Copyright (c) 2026 Bryce Wang).

## Threat-model discipline

- Separate what the attacker knows from what it can do from where it sits in the system; a conflated model is the most common source of "the attack assumes too much" reviews.
- State the security goal as a property (confidentiality, integrity, availability, unlinkability) and say what "broken" means quantitatively.
- State the parties and the trust assumptions first: which parties may collude, and what the honest-party assumption is. Every capability claim is written as an assumption plus a decidable statement, not as a table row.
- When a defense is evaluated, name the adaptive attacker it was tested against; a defense measured only against the attack it was designed to stop is a standing CCS complaint.
- Label conjecture, heuristic argument, and proved result distinctly; mixing them near a security claim is a credibility leak at this venue.
- Do not spend the threat model on material the introduction already spent. The threat model earns its space by adding capabilities, assumptions, and explicit non-goals; a re-enumeration of the parties buys the reader nothing.

## Draft-pattern rewrites

| Draft pattern | CCS-safe rewrite |
|---|---|
| "Our attack is highly effective..." | "recovers the key in N queries against library X vY on platform Z" |
| "Under realistic assumptions..." | "Under threat model T (network MITM, no host access)..." |
| "Our defense is secure..." | "resists the adaptive attacker of Section 5 at C% overhead" |
| "We significantly reduce risk..." | claim scoped to the deployment and versions measured |
| "We completely prevent..." | "blocks 387/412 of the corpus instances, at a 2.1% median CPU overhead" |

## Condensation rewrites

The following table is the compression counterpart of the rewrite table above. Each row turns a wordy pattern into a counted one; the thresholds and their corpus anchors are in `references/compression-and-expansion-gates.md`.

| Wordy pattern | Counted rewrite |
|---|---|
| An abstract paragraph that summarizes a proof step by step | one sentence naming the property proved, with the forward reference to the theorem |
| The same result stated in the abstract and again in the contributions with the same words | one statement, in the contributions, with the abstract keeping only the claim |
| A contribution bullet that lists three sub-results of one mechanism | one bullet for the mechanism, the sub-results moved to the body |
| A contribution bullet longer than its neighbours by a factor of ten | one bullet per claim, or the bullet split; uneven lengths must be deliberate |
| "In order to achieve X, which is important because Y, we note that Z, and therefore ..." | one sentence per idea; delete the justification of the justification |
| A paragraph reintroducing the threat model before each experiment | one threat-model statement, referenced from each experiment |
| "We first tried A, which failed because of B, then moved to C" | the design decision and its reason, without the history |
| An identifier from the project's planning register used as a concept name | the concept's descriptive name, as it will appear in the paper |
| An exact probability or byte count inside a construction paragraph | the symbolic expression in the construction; the measured value in the parameters or evaluation section, with its provenance |

## Expansion rewrites

The mirror table. These rows come from the corpus's thickest construction sections and the reader-necessary constituents that thin sections omit.

| Thin pattern | Expansion |
|---|---|
| "The protocol runs as follows: see Algorithm 1." | a step ordering in prose that names each message and each check, then the box |
| A parameter table with no reasons | the reason for each size, field, or modulus choice, stated once, next to its use |
| A condition re-derived inline at each use | one named relation defined once and reused, with the name used at every later site |
| "The construction is standard." | the cost or complexity expression, and the point where it differs from the standard version |
| An overview that only lists sections | one intuition sentence, one mechanism sentence per subproblem, and a forward reference per subproblem |
| A proof-length argument standing in for the mechanism | the causal sentence: why this step makes the next one possible |
| A figure that carries the message flow with no prose | one sentence naming what the reader should see in the figure, and the invariant it preserves |

## Compression vignette

A draft with a full protocol description, four attack variants, a formal proof, and six measurement figures: keep the threat model, the strongest attack variant end to end, one proof sketch, and the two decision-critical figures (leakage rate and defense overhead); push the other variants, the full proof, and raw measurement tables to appendices with forward references. The test of a good cut: a reviewer should be able to judge novelty and soundness of the attack without opening the appendix.

Cutting is never license to delete a claim. A claim that moves to the appendix keeps its status wording (proved, conditional, provisional, open) and its provenance, and the body says where it went.

## Output format

```text
[Writing diagnosis] clear / under-specified threat model / overclaimed / overloaded / verbose where it must be dense / thin where it must be dense
[Condensation counts] abstract words/sentences/longest sentence/allocation; contribution items/words per item/total; abstract-vs-contributions Jaccard (word bag and trigram); contributions-vs-threat-model Jaccard
[Expansion counts] overview words and location and components; scheme words; scheme/analysis ratio with basis; scheme share of body; components present or absent with lines
[First-page fix] <new framing>
[Claim discipline] <claim -> proof/measurement/exploit/cost>
[Compression cuts] <move/delete/merge>
[Anonymity edits] <phrases to rewrite>
[Policy snapshot] <date, official call, page limit, anonymity clause, ethics clause>
```
