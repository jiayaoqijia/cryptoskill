---
name: front-load-the-conclusion
description: Use when writing any report longer than a paragraph. Put the answer, verdict, or recommendation in the first line, then support it in descending order of evidence.
---

# Front-load the conclusion

A chronological report forces the reader to the bottom to find the answer. Put the verdict first so a skimming reader can act, then support it.

## Procedure

1. Write the conclusion first, as if it were the only line budgeted: "The refactor is safe to merge; two tests cover the changed path."

2. Below it, order the support by strength: strongest evidence first.

3. Put method and full logs last, under a `## Detail` divider.

4. Use a header stack a skimmer can follow: verdict, evidence, detail.

5. If the conclusion is probabilistic, give the number and the confidence band, not a bare hedge.

6. Cap the top section at five lines; if it needs more, the ask is wrong.

7. Test by reading only the first line: can the reader act on it? If not, rewrite it.

## Pitfalls

- Chronological reports make the reader scroll to the bottom for the answer.
- A summary that restates the question wastes the prime real estate.
- Hiding the recommendation after the caveats reads as no recommendation at all.
- Long intros that "set the stage" delay the decision the reader came for.
- Front-loading a wrong conclusion confidently is worse than hedging; verify first.

## Verification

    head -1 report.md   # states the verdict, not the topic

Lead with the answer; support it in descending order of evidence.
