<!--
  Imported from: https://github.com/saksham10arora-dotcom/quant-skills
  Source Path: skills/paper-repro/SKILL.md
  Curated for awesome-quant-skills
-->

---
name: paper-repro
description: Structured workflow for reproducing a quantitative research paper or blog post analysis. Use when the user wants to reproduce, replicate, verify, or re-implement results from a paper, or asks if a paper's findings hold up.
---

# Paper Reproduction Workflow

Goal: independent verification, not transcription. The reproduction must be able to disagree with the paper.

## Phase 1: Extract the claim contract

Before touching code, write down from the paper:
1. Headline claims with exact numbers (table and page)
2. Data sources, date ranges, universe definitions
3. Every specification in every reported model (they will matter later)
4. What would count as a failed reproduction

If any of these are ambiguous, list the ambiguities first; ambiguity resolution choices explain many "failed" reproductions.

## Phase 2: Minimum viable replication

Implement the SINGLE headline result only. Resist implementing everything.
- Match data vintage where possible; document every forced substitution
- Prefer writing your own implementation over running authors' code first; then diff against their repo if available
- Log every deviation as you make it: `DEVIATION: used X because Y`

## Phase 3: Verdict taxonomy

Classify the outcome honestly:
- **REPLICATED**: numbers match within rounding
- **REPLICATED WITH DEVIATIONS**: same conclusion after documented substitutions
- **PARTIALLY REPLICATED**: some tables/robustness checks hold, others do not; say which
- **NOT REPLICATED**: cannot recover headline numbers; report your best-guess numbers alongside theirs
- **NOT REPRODUCIBLE**: impossible to attempt (no data, no spec detail); list exactly what is missing

## Phase 4: Robustness the paper skipped

Run at minimum:
- Alternative window/subsample
- One specification perturbation the authors did not report
- Sensitivity to the biggest discretionary choice you found in Phase 1

## Output format

```
PAPER: <title, year>
CLAIM TESTED: <exact claim>
VERDICT: REPLICATED | ... (taxonomy above)
MY NUMBERS vs PAPER: <side by side table>
DEVIATIONS: [numbered list]
ROBUSTNESS: [what you perturbed, what happened]
ARTIFACTS: <files/scripts produced>
```

Save the verdict block: failed and partial reproductions are publishable knowledge too.
