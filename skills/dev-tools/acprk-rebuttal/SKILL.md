---
name: rebuttal
description: Use when reviews arrive and an author response (rebuttal / interactive phase / revision response) must be produced. Covers timeline, triage of reviewer points into must-answer / clarify / ignore, word-budget packing, evidence-first answers, new-experiment policy, tone, and the two-document structure (short submitted version + detailed per-reviewer internal version).
---

# Rebuttal

Templates: `templates/rebuttal/{timeline.md, triage_table.md, rebuttal_short.md,
rebuttal_detailed.md}`. Never commit real reviews to a shared repository; keep them in
the private project only.

## 1. Timeline (typical 5–7 day window; adapt with `timeline.md`)

| day | work |
|---|---|
| D0 | Read all reviews twice, no replies. Copy each review verbatim into the private project. Split into atomic points with ids (R1.1, R1.2, ...). |
| D0–D1 | Triage table. Identify the decisive reviewer (the most negative with the highest confidence) and the potential champion. Decide which new experiments are feasible within the window. |
| D1–D3 | Run experiments/verification (bench protocol from `experimenter`; interleaved runs; new EVIDENCE rows). Draft the detailed internal version per reviewer. |
| D3–D4 | Compress to the short version within the word/character budget. Falsifier + reviewer-sim pass on the draft ("does this answer the question asked?"). |
| D4 | Human author final review; submit early (systems get slow near deadlines; convert the deadline to your timezone). |
| after | Interactive phase: answer follow-up questions within the window; same evidence-first rules. Record everything in `DECISIONS.md`. |

## 2. Triage

For each atomic point decide:

| class | meaning | action |
|---|---|---|
| **must-answer** | would change the decision: correctness doubt, counterexample, fairness of comparison, missing baseline, security level, novelty vs a named paper | full evidence-first answer in the short version |
| **clarify** | misunderstanding or missing detail answerable in 1–2 sentences | one sentence in the short version or grouped |
| **concede-and-fix** | the reviewer is right about an error or overclaim | admit plainly, state the corrected statement, show the fix does not affect (or how it affects) the main results |
| **promise** | editorial / typos / notation / bib | one grouped line: "All editorial points will be fixed." |
| **ignore** | out of scope, factually wrong but harmless, taste | no space in short version; answer in detailed version only if cheap |

Priority: decisive reviewer's must-answer points first, then points raised by more
than one reviewer (answer once, cite all reviewer ids), then the champion's questions
(give them ammunition for the discussion).

## 3. Answer shape (evidence first)

```
[R2.1] <restated question in ≤ 1 line>
Answer first (yes/no/number) → evidence (table, theorem, log, measured number with
scope) → what changes in the paper (section/page) → optional one-line consequence.
```

- Lead with the answer, not with thanks or background.
- Numbers come from new or existing EVIDENCE rows; say how they were measured
  (same session, interleaved, n runs, median).
- Where a counterexample is correct, say so in the first sentence and give the fixed
  statement; do not argue around it.
- Turn challenges into content: a fairness complaint becomes a new comparison table;
  a security question becomes a security section; "why not compare with [X]" becomes
  "they compose: measured composition = ..." or "the regimes do not overlap: ...".
- If an attack or issue affects the baseline equally, measure both side by side and
  give a fix that applies to both.
- Retract unsupported numbers proactively, in the same message as the corrected
  version. Retracting beats being caught.
- Direct verification with authors of a cited work (e.g. confirming scope of their
  attack) is strong evidence; mention it factually.

## 4. Word-budget packing

Typical budgets: a few hundred to ~1000 words or a character cap; some systems accept
only plain text. Check the review system's limit on day 0.

1. Write the detailed version first (unbounded).
2. Short version (500–700 words is a good target when the cap is ~750–1000):
   - One opening line: "We thank the reviewers. Page numbers refer to the revised
     version [if allowed]; all editorial points will be fixed."
   - Grouped headings by **issue**, tagged with reviewer ids, ordered by decision
     impact: `**Comparison fairness (R2, R3).**`.
   - Max 1 compact table (plain text if the system strips formatting).
   - Remove all adjectives, all "we believe", all restatements longer than one line.
   - Merge answers shared by reviewers.
3. Count words with the system's counting rule (e.g. `wc -w` on the plain text) and
   leave 5% margin.

## 5. New-experiment policy

- Run only experiments that answer a must-answer point and can finish, be verified
  and be logged within the window. Pre-register what would count as success in
  `DECISIONS.md` before running.
- Same bench protocol as the paper (interleaved, same machine, verified outputs).
- If a result contradicts an earlier number, report the new one and retract the old.
- Venue rules differ on whether revised PDFs/supplements may be uploaded during
  rebuttal; if not allowed, describe the change and promise it.
- Do not introduce new claims that were not in the submission unless answering a
  question; reviewers may treat them as a different paper.

## 6. Tone

Neutral, factual, brief. Agree when right. Never "the reviewer misunderstood"; write
"We will clarify: ...". No appeals to authority, no complaints about the review
process, no emotional language. Address the meta-reviewer's questions explicitly
by their numbering.

## 7. After the decision

- Accepted: build a **request → where answered** map (`CHANGES.md`: reviewer point →
  section/page in the final version) and feed it to `camera-ready`.
- Rejected: convert the triage table into a revision plan for the next venue; keep the
  evidence rows; lessons into `DECISIONS.md`.
