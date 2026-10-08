---
name: detect-sunk-cost-trap
description: Use when a task is expensive and going badly and you feel compelled to try once more. Evaluates the forward cost only, so prior spend does not buy another doomed attempt.
---

# Detect the Sunk-Cost Trap

Time already spent is gone and cannot justify more spending. The only question is whether, from this moment, the current approach will finish — judged on forward cost alone.

## Procedure

1. Maintain an attempt ledger in the workspace: one row per attempt with the class of approach, cost so far, and outcome. Append after each attempt; never judge from memory.
2. When an attempt fails, state the forward question plainly: "starting from now, what will this approach cost to finish, and will it finish?" If you cannot answer, that is a no.
3. Apply the two-attempt rule: two failures of the same class (same API, same parser, same technique) mean the third attempt must be a different class, not a third trial of the same one.
4. Define abandon criteria before starting a hard task, e.g. "if the parser fails on more than 10% of records after two passes, switch to a library". Write it in the plan so it is not renegotiated mid-failure.
5. Compute the switch cost: what would changing approach cost from scratch, and does that plus what is spent stay under the task budget?
6. When switching, keep the useful residue: the test cases, the schema, the fixtures you built still apply. Do not discard correct work just because it came from the abandoned approach.
7. Announce the switch with the trigger that fired: "Two parse failures on the same dialect; abandoning the hand-rolled parser per my 10% rule."
8. Never escalate effort to justify the prior spend — "I'm nearly there" is a claim requiring the forward estimate, not a reason.
9. Time-box attempts in the ledger so a single attempt cannot silently consume the whole budget.
10. Prefer the approach with the smaller worst case, not the smaller best case, when estimating forward cost.
11. After switching, note the switch in the handoff capsule so the abandoned path is not retried later.
12. Keep the ledger command-ready: append with `printf '%s\t%s\t%s\n' "$class" "$cost" "$outcome" >> notes/attempt-ledger.tsv` after every attempt.

## Pitfalls

- Retrying the same failing command a third and fourth time because the first three "almost worked".
- Refactoring a failing approach into a bigger failing approach rather than switching.
- Discarding the tests and fixtures from a failed path, which were the valuable part.
- Setting abandon criteria after the failures, when they can be bent to justify continuing.
- Confusing "the user paid for this time" with "the user wants this approach" — they want the outcome.
- Switching approach but keeping the same failing assumptions, so the new path fails identically.
- Interpreting a slightly less bad failure as progress when the forward estimate is unchanged.
- Rewriting the ledger from memory at review time instead of reading `notes/attempt-ledger.tsv`.

## Verification

    wc -l notes/attempt-ledger.tsv && cut -f2 notes/attempt-ledger.tsv | sort | uniq -c
    # passes when no approach class shows >= 3 attempts without an intervening switch

Report to the user: the attempt count per class, the abandon criterion that fired, and the forward-cost estimate for the path you chose.
