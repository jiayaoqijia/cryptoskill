---
name: give-feedback-that-lands
description: Use when reviewing a junior's work or correcting a repeated mistake. Uses situation-behaviour-impact phrasing pinned to a diff line, one behaviour per pass, so the fix is actionable and not a personality judgement.
---

# Give Feedback That Lands

Feedback aimed at a person ("you are careless") is unactionable and triggers defence. Feedback pinned to a line, a behaviour, and its effect gives the learner one thing they can actually change.

## Procedure

1. Anchor to a concrete line: quote it with a path and range, e.g. `api/handler.py:42-47`.
2. Use situation-behaviour-impact, in order: "When the request 404s (S), the handler returns 200 with an empty body (B), so the client retries forever (I)."
3. Give one behaviour per pass. Two or more competing fixes dilute to none.
4. Separate blocking from non-blocking explicitly: prefix nits with `nit:` and label the rest `blocking:`.
5. Describe the effect on the reader or the system, never the author's competence.
6. Offer the smallest next action, or a question: "Would a 404 here be truer?" beats "this is wrong".
7. For a repeated mistake, show the pattern across two diffs rather than re-litigating one instance.
8. Close by naming what they did well specifically, so the contrast is instructive.
9. If the fix is faster to show than to explain, show it once, then ask them to apply it elsewhere.
10. Ask the author to restate the impact in their own words; if they cannot, the feedback did not land.
11. Ask before asserting: 'what does the client do if this 200s on a 404?' often finds the bug with the author.
12. Batch cosmetic nits into one comment so they do not crowd the one behavioural point.
13. For a first-time author, open with the biggest win before the blocking item.
14. Number your comments so the author can reply to 'comment 3' without pasting.
15. State the trade-off when a change costs something, so the author can weigh it.
16. Keep praise and correction in separate comments so neither dilutes the other.

## Pitfalls

- Praising the person in general ("great coder") so the specific behaviour never lands.
- Burying a blocking bug inside five cosmetic nits, so the reader cannot rank the work.
- Framing impact as a feeling ("this frustrates me") instead of an observable effect.
- Rewriting the whole function in the comment, which teaches dependence on the reviewer.
- Delivering the same correction a third time without changing the form of the message.
- Sending feedback weeks after the diff, when the context has gone cold.
- Combining a correctness bug and a style opinion in the same comment.
- Using 'we' to mean 'you', so the author cannot tell what to change.
- Leaving the request open-ended with no smallest next step.
- Comments numbered nowhere, so a reply thread becomes a guessing game.
- Presenting a trade-off as a fault.
- Mixing praise into a blocking comment so the correction reads as softened.

## Verification

    git diff review-branch | grep -nE '^[+-]' | head
    # passes when every comment you posted cites a file:line and states a consequence, none names a trait

Report to the user: the diff line each comment anchors to and the observable effect claimed in it.
