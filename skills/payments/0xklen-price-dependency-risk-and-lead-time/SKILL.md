---
name: price-dependency-risk-and-lead-time
description: Use when a plan waits on something you do not control — another team, a vendor, an approval. Makes the wait an explicit dated task with a lead time and a fallback, instead of a blank in the schedule.
---

# Price dependency risk and lead time

External work is the estimate's most common hidden cost: it does not appear in your task list but it controls your start. Make every wait explicit, give it a lead time and an owner, and decide the fallback before the lead time runs out.

## Procedure

1. For each external dependency record four things: what you need, who controls it, the lead time, and the trigger date (needed-by minus lead time).

       notes/deps.md
       - need: API key for vendor Z | owner: procurement | lead: 10 business days | needed: 2026-03-01 | trigger: 2026-02-13

2. Sanity-check the lead time against history, not the vendor's promise. If last time took 15 days, use 15.
3. Insert the dependency as a real node on the critical path in `notes/deps.md`, with its lead time as its duration. It is not free time.
4. Set an alarm at the trigger date. If the dependency has not moved by then, execute the fallback:

       # in a scheduler or calendar
       remindctl add --title "chase API key Z" --due 2026-02-13

5. Name the fallback up front: mock it, use a competitor's service, descope the feature. "We'll figure it out" is not a fallback.
6. Add the dependency's uncertainty to the range — external waits have wide tails and rarely come in early.

## Pitfalls

- Assuming the promised lead time is the real one; vendors quote best-case.
- Starting the clock when you remember to ask, not when you first knew you needed it.
- Treating the wait as free because no one is working, so it never lands on the critical path.
- No fallback decided, so the slip triggers an improvised scramble under deadline pressure.
- Forgetting approval-type dependencies (security review, legal, a signing ceremony) which have long, lumpy lead times.

## Verification

    grep -n 'trigger:' notes/deps.md
    # passes when every dependency has a trigger date in the past-of-its-needed date and an owner

Report each dependency with its owner, lead time, trigger date, and the fallback you will execute if it slips.
