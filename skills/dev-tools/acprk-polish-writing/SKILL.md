---
name: polish-writing
description: Use for a final language pass on a paper section, or when translating a Chinese draft into English academic prose. Removes AI-sounding phrasing, tightens sentences, enforces consistent notation and terminology, and never changes numbers, claims or LaTeX semantics.
---

# Polish writing

## Invariants (never violate)

- Do not change numbers, theorem statements, hypotheses, citations, labels or math.
- Do not strengthen claims ("shows" → "proves", "up to" → "always").
- Keep LaTeX commands intact; do not introduce packages.
- In the last 24 hours before a deadline: no style passes at all, only error fixes.
- Output: revised text + a short modification log (what and why) so the author can
  accept/reject each change.

## Pass 1 — de-AI

Replace or delete:

| avoid | prefer |
|---|---|
| leverage, utilize | use |
| delve into, explore (as a result) | examine, study (or state the result) |
| pivotal, crucial, paramount | important, key (or delete) |
| underscore, highlight (as filler) | show |
| tapestry, landscape, realm | (delete; name the area) |
| seamless(ly), robust (without a metric) | (delete or quantify) |
| "It is worth noting that", "Notably," | (delete; state the fact) |
| "In this paper, we aim to" | "We ..." |
| "First and foremost", "Last but not least" | (delete) |
| "plays a crucial role in" | "determines", "dominates" (be specific) |
| "novel" about own work | (delete; let the reader judge) |
| "significantly" without numbers | the number |
| "obviously", "it is easy to see" | give the one-line reason, or delete |

Also: convert `itemize` inside running text into connected prose when the items are
reasoning steps (keep lists for contributions/parameters); avoid three connectives
in a row; vary sentence openings; no rhetorical questions in the body.

## Pass 2 — concision

- One idea per sentence; aim for ≤ 30 words.
- Remove throat-clearing openers and doubled phrases ("in order to" → "to",
  "the fact that" → "that", "a number of" → "several"/the number).
- Prefer verbs over nominalisations ("perform an evaluation of" → "evaluate").
- Active voice for what *we* did; passive is fine for standard facts.
- Avoid dashes as sentence punctuation (use commas, colons, or split sentences).

## Pass 3 — consistency

- Terminology: one name per concept (framework name, stage names, baseline names).
  Build a term list from the notation table and `grep` for variants
  (e.g. "bootstrap"/"bootstrapping", "look-up table"/"lookup table", "LUT").
- Notation: symbols match the notation table; no symbol reused with two meanings;
  vectors/matrices consistently bold or not.
- Spelling variety: pick US or UK and stay with it.
- Capitalisation of references: `Section~\ref`, `Table~\ref`, or `\Cref` consistently;
  non-breaking spaces before `\cite` and `\ref`.
- Numbers: consistent units and precision (e.g. 2 significant digits for ratios);
  `\times` spacing consistent; thin space before units.

## Pass 4 — Chinese → English (for drafts written in Chinese)

1. Translate meaning, not word order: Chinese topic-comment sentences often become
   English subject-verb sentences with the conclusion first.
2. Split long Chinese sentences joined by commas (一逗到底) into several English
   sentences.
3. Watch for common calques: "has important significance" → "matters because ...";
   "realize/achieve an algorithm" → "implement"; "the proposed scheme" repeated →
   name it once, then "our scheme"/its name; "in recent years" as an opener → delete or
   give the year range; "greatly improve" → the number.
4. Articles: every singular countable noun needs a/the; "the" for things already
   introduced or unique ("the bootstrapping procedure of [X]").
5. Tense: present for facts and what the paper does; past for what prior work did
   or for experiments that were run.
6. Produce three parts: `[LaTeX]` English text, `[Back-translation]` literal Chinese
   of the English (so the author can check meaning), `[Log]` list of changes.

## Pass 5 — read-aloud check

Read the abstract and the first page aloud (or via TTS). Any sentence that needs a
second breath gets split.
