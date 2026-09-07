# De-AI and Sentence-Level Style Rules

Derived from revision feedback on real manuscripts: reviewers increasingly reject prose that reads as AI-generated. Treat this as an executable checklist, not a flavor guide. Rule labels are referenced from the main SKILL.md workflow.

## Vocabulary red flags

Replace or delete; do not merely reduce frequency when the word itself signals the register:

- Sentence-openers used as filler: "Additionally, ...", "Moreover, ...", "Furthermore, ..." (at most a couple per paper, and only with real content), "In order to ..." (always "To ...").
- Emphatic adjectives with no measured referent: crucial, pivotal, paramount, comprehensive, groundbreaking, cutting-edge, remarkable, substantial (without a number), significant (without a number).
- Abstract nouns and metaphors: landscape, tapestry, testament, vibrant, intricate, interplay, realm, delve, foster, showcase, underscore, leverage (commercial register), synergy, holistic.
- Vague attribution: "Studies have shown ...", "It is widely believed ...", "As is well known ..." — replace with a citation or delete.
- Self-evaluative novelty: "novel", "first", "optimal" used as self-praise — keep only when scoped and defensible ("the first X with property P under assumption A"), never bare "novel technique".
- Hedging stacks: "may", "might", "could potentially" — quantify or condition ("if premise A holds"), do not stack.

## Structure red flags

- Forced parallelisms: "Not only X, but also Y" used repeatedly; rule-of-three lists everywhere; binary contrasts ("It is not about X — it is about Y").
- Meta-narrative: "This section will discuss ...", "Below we present ...", "As we will see ...", "This paper reports a dossier on ..." — state the content, not the plan (roadmap sentences in an introduction are the exception).
- Workflow self-reference in the prose: internal task/round numbers, file paths, audit-trail labels. These belong in footnotes, appendices, or a companion artifact map, not in the sentence stream of a submission.
- Synonym cycling for one object (scheme/protocol/system/construction used interchangeably for the same thing): pick one term per object and stay consistent.
- Uniform paragraph lengths and uniform sentence lengths: vary them; break long parenthetical insertions out of the subject-verb path.

## Content red flags

- Significance inflation without evidence; promotional language in evaluation sections ("remarkable improvement"); generic conclusions ("this opens exciting new directions") — be specific about what opens and why.
- Every strong claim should carry its scope: "resists the adaptive attacker of Section 5 at C% overhead", not "is secure".
- Failure cases appear in the same paragraph as success rates; negative results are not hidden in footnotes.
- "No attack found" must not be written as "secure": pair it with "this is not a proof of security" once and once only in each relevant section.

## Sentence-level register

- Stress position: put the most important information (numbers, bounds) at the end of the sentence. "The prover achieves the optimal running time O(C)" not "The prover time is O(C), which is optimal".
- Topic position: start from what the reader already knows, then attach the new claim; do not bury the subject under long clauses.
- Voice: active for your contributions ("We present ...", "We prove Theorem 3 under A1-A6"), passive or attributed for prior work ("It was shown in [ref] that ..."), past tense for experiments run, present tense for protocol/system properties.
- "We" refers to the authors' actions, not the protocol's behavior ("the prover sends" not "we send").
- Numbers beat adverbs: replace "significantly", "negligible", "trivially" with the measured value or bound wherever one exists.

## Executable grep checklist

Run these patterns after revision; each hit is either fixed or explicitly waived with a reason in the diff:

```text
^(Additionally|Moreover|Furthermore|In addition|However|Notably|Importantly)[, ]
delve|pivotal|showcase|underscore|tapestry|testament|landscape|vibrant|intricate|interplay|realm|foster|groundbreaking|cutting-edge
Not only .* but also
It (is|was) (important|worth|interesting|crucial) to (note|mention|stress)
In order to|aims to|aspires to|strives to
This (section|chapter|paper) (will|aims to|intends to)
(t[0-9]+|round[ -][0-9]+)[^a-zA-Z]        # internal workflow ids in prose
dossier|manuscript v[0-9]                 # workflow vocabulary
dramatically|remarkably                   # unless a number follows in the same sentence
```

Waivers are legitimate when the term is the precise technical word (for example "robust" in a statistical sense, or a word inside a quoted title); record the waiver line in the revision log.

## Section-specific attention

| Section | Primary risk |
|---|---|
| Abstract | all patterns; highest scrutiny |
| Introduction | significance inflation, vague attribution, meta-narrative |
| Technical overview | filler phrases, formula dumping |
| Security analysis | hedging, sketch-as-proof wording |
| Evaluation | promotional language, missing failure cases |
| Conclusion | generic positive statements, abstract repetition |
