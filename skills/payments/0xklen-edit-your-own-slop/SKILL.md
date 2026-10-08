---
name: edit-your-own-slop
description: Use when a draft you produced reads as generic, padded, or AI-sounding and must be tightened before it ships. Applies concrete deletions and rewrites, not vibes.
---

# Edit Your Own Slop

First drafts read as slop for mechanical reasons: empty openers, hedge stacking, and abstract nouns where a number or a name belongs. Fix them by rule.

## Procedure

1. Delete the first sentence of every section; it is almost always throat-clearing that restates the heading. Read from sentence two and see if meaning survives.
2. Strike stock phrases on sight: "note that", "it should be noted", "plays a crucial role", "in order to" (use "to"). Keep a list of your own repeated openers.
3. Replace abstract nouns with verbs: "provide assistance to" becomes "help"; "perform a review of" becomes "review".
4. Cut adverbs and intensifiers that carry no measurement: "very", "quite", "extremely", "significantly", "robustly". If it matters, give the number.
5. Hunt the tricolon and four-item lists that only pad; if two items suffice, keep two.
6. Find every sentence over 30 words and split it, or delete its weakest clause.
7. Kill nominalisations: "utilise" becomes "use", "leverage" becomes "use".
8. Replace a claim with its evidence: "much faster" becomes "3.1s to 0.4s". One concrete figure beats a paragraph of adjectives.
9. Remove the hedge that fills space but asserts nothing, while keeping the hedge that carries real uncertainty.
10. Read it aloud; every place you stumble is a sentence to rewrite.
11. Diff against the draft to confirm the word count fell and no required fact was dropped.

## Pitfalls

- Over-editing into clipped fragments that lose the connective logic between ideas.
- Removing the hedge that carried genuine uncertainty ("roughly 40%") and asserting a false precision.
- Making everything terse so the tone reads as curt rather than clear.
- Rewriting to match a style guide at the cost of meaning.
- Trusting a spellchecker over the read-aloud, which catches clause pileup the checker ignores.
- Trading a long word for a shorter synonym that changes the technical meaning.
- Deleting a caveat because it weakened the sentence, then shipping the overstated claim.

## Verification

    wc -w draft.md final.md
    grep -niE "note that|it should be noted|plays a crucial role" final.md

The word count must fall and the `grep` must return nothing. Report the before/after count and the deleted filler phrases by name.
