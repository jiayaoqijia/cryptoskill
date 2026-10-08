---
name: write-actionable-review-comments
description: Use when leaving review feedback and you want the author to act on it in one pass. Shapes each comment as observation, impact, and a concrete suggestion with a code example.
---

# Write actionable review comments

A comment that states a problem but not a direction costs a round-trip. A comment shaped as "here is what I see, why it matters, here is what I would do" lands the first time.

## Procedure

1. Lead with the observation, phrased about the code, not the author: "this path can receive `null` from `findById`" rather than "you forgot to check null".
2. State the impact concretely so the author can weigh it: "a user with no orders gets a 500 here", not "this is fragile".
3. Offer a specific suggestion with a code snippet the author can paste or reject:
       # suggestion: default to an empty list so the caller never handles null
       return Order.objects.filter(user=uid) or []
4. Ask a question instead of asserting when you are not certain: "is `id` guaranteed non-null here? I could not find the constraint." A question invites an answer; an assertion demands a defence.
5. Link the relevant line range or a permalink (`https://github.com/org/repo/blob/<sha>/path#L42`) rather than describing the location in prose.
6. Keep each comment to one issue. Bundling three fixes in one paragraph means the author addresses two and misses the third.
7. Re-read before submitting: delete praise-only comments that add no signal, and never use "obviously", "just", or "simply".

## Pitfalls

- Vague mandates like "clean this up" with no definition of done.
- Writing the whole corrected function in the comment, which is more code to review than the original.
- Commenting on the author's competence rather than the code, which ends the useful conversation.
- A wall of comments on one PR with no severity, so the author cannot triage.

## Verification

    # Every comment should contain a suggestion or a question and a location.
    gh pr view 482 --json comments | jq -r '.comments[].body' \
      | grep -vcE '(suggestion:|question:|nit:|blocking:|https://github.com)'
    # The count above should be the number of comments you intend to delete.

Report each comment's class, its suggestion, and its line link. A comment with no direction and no question is noise — delete it before submitting.

## Worked example

Weak: "this is fragile."
Better:
    blocking: `findById` returns null for a missing row and the next line reads `.id` on it, so a stale link yields a 500. Wrap it: `if (row == null) return notFound();`.
The second version names the input, the impact, and the fix, so the author acts without asking what you meant.
