---
name: flag-untestable-words-in-a-spec
description: Use when reviewing a spec, ticket, or acceptance criteria before build. Greps out vague qualifiers that cannot be tested and forces each to a threshold or an example.
---

# Flag untestable words in a spec

"Fast", "robust", and "intuitive" cannot fail, so they cannot be verified. This skill finds the vague words and replaces each with a number, an example, or a decision.

## Procedure

1. Run a vague-word scan over the spec: `grep -inE '\b(fast|slow|robust|reliable|scalable|intuitive|seamless|user-friendly|simple|easy|better|improve|optimize|soon|recently|properly|correctly|sometimes)\b' spec.md`.
2. For each hit decide which of three fixes applies: replace with a measurable threshold, replace with a concrete example, or delete the claim.
3. Convert comparative words to a baseline and a target: "faster" becomes "p95 under 300 ms, from 800 ms today".
4. Convert quality words to an observable behaviour: "robust" becomes "survives a 500 from the upstream without a 5xx to the client".
5. Convert quantity words ("many", "most", "soon") to a number and a window.
6. Raise any word that hides a genuine dispute to a decision record rather than quietly picking a threshold.
7. Re-run the scan after editing; a clean pass means every remaining claim is testable.
8. Do the same scan on the ticket title, which frequently carries the vaguest phrase.
9. Add project-specific vague words to the scan list, such as internal jargon that means different things to different teams.
10. Record which hits were false positives so the next reviewer does not re-litigate the same line.

11. Add the scan to the pull request template so vague wording is caught before review, not after.

## Pitfalls

- Replacing "fast" with an arbitrary number the requester never agreed to; thresholds are decisions, not guesses.
- Flagging words like "simple" that are legitimately in a non-normative sentence, then over-editing prose.
- Fixing the spec text but not the acceptance criteria that reference the same vague word.
- Letting "soon" survive as a deadline; a date or window is required.
- Treating the grep as the goal rather than the meaning; an empty grep over nonsense prose is still nonsense.
- Editing prose that is deliberately non-normative and does not belong in a test.
- Replacing a vague word with a precise one nobody agreed to, smuggling a decision into an edit.

- Escalating every vague word to a decision record, which buries the ones that truly need one.

## Verification

    grep -inE '\b(fast|robust|intuitive|seamless|simple|easy|soon)\b' spec.md || echo clean

Report each flagged word, its fix (threshold, example, or deleted), and any word you escalated to a decision record.
