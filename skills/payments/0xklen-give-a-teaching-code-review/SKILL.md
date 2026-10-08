---
name: give-a-teaching-code-review
description: Use when reviewing code from someone still learning, where the aim is skill growth and not just correctness. Teaches one principle per review, ties each comment to a rule, and avoids rewriting the code in the comments.
---

# Give a Teaching Code Review

A review that fixes the code leaves the author unchanged. A review that teaches one principle, with the comments as evidence, leaves them able to spot it themselves next time.

## Procedure

1. Pick one principle for this review: error handling, naming, or test coverage. Do not teach three at once.
2. Lead with what is correct and why: "the retry-with-jitter here is right because it avoids a thundering herd".
3. For each teaching point, state the rule and cite the line: `api/client.py:88` — retries with no cap can retry forever; add `max_attempts=3`.
4. Cap blocking comments at three; beyond that it is a rewrite, not a review.
5. Prefer a question that leads to the fix over the fix itself, but supply the fix if the concept is new.
6. Link the principle to a doc or an earlier PR where it was decided, so the rule is not personal.
7. End by asking the author to restate the principle in their words; that closes the loop.
8. Offer one follow-up exercise that practices the same principle on different code.
9. Note in the review which single comment you would keep if only one could survive.
10. Ask what the author was unsure about before commenting; they often name the flaw themselves.
11. Keep the review to the diff, not a tour of the surrounding file.
12. Follow up in a week to see whether the principle stuck.
13. Separate 'must fix' from 'nice to have' with an explicit label.
14. Point at one concrete better line rather than a general principle alone.
15. Thank the author for a specific good decision, not in general.

## Pitfalls

- Rewriting the whole file in a comment, which the author pastes without understanding.
- Ten comments spanning five principles, so none is learned.
- Stating a preference as a rule with no reasoning.
- Ignoring the good decisions, so the review reads as purely corrective.
- Approving a diff that contradicts the principle you just taught.
- Marking a teaching point as blocking when it is a preference, so the author over-corrects.
- Reviewing the author's understanding of the problem instead of the diff in front of you.
- Teaching a principle the author has no context to apply yet.
- Approving to be nice, which teaches that the rule was optional.
- Blurring must-fix and nice-to-have.
- Naming a principle with no example of it applied.
- Generic praise that reads as filler.

## Verification

    git diff --stat origin/main...review-target ; grep -c '^blocking' review.md
    # passes when blocking comments <= 3 and each names a principle and a file:line

Report to the user: the single principle taught, the file:line evidence, and the author's restatement.
