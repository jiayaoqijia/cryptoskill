---
name: bound-the-search-space
description: Use when starting an open-ended investigation or repo exploration. Sets an explicit budget of queries, files, and minutes before searching, and forces a decision when the budget is spent.
---

# Bound the Search Space

Open-ended exploration has no natural end; it will consume whatever budget it is given. Set the boundary first, search inside it, and make a decision when it runs out.

## Procedure

1. Before the first search, write the budget down: `budget: 8 queries, 25 files read, 10 minutes`. Pick numbers from the task's size, not from optimism.
2. Convert the goal into specific patterns first; a good query beats many vague ones: search for `authenticate(` not "auth stuff".
3. Search narrow-to-wide: start in the likely module, then widen only if the first scope is empty. Do not begin with the whole filesystem.
4. Exclude noise up front: `grep -r --include='*.py' --exclude-dir={.git,node_modules,venv} <pat> .`.
5. Count budget as you spend it. After each query, decrement; when you hit the limit, stop searching and decide with what you have.
6. Record negative results explicitly (`searched: "retry" in src/, none found`) so the next actor does not repeat the same search.
7. When the budget is exhausted and the answer is still unclear, escalate a specific question to the user rather than opening a new budget silently.
8. If the task genuinely needs more search, stop, state the new budget and why, and get it approved — do not just keep going.
9. Write the stopping condition before rejecting anything: "stop when I can name the file that owns this behaviour."
10. Spend the budget on the highest-information query first (a definition, a test, a call site), not the broadest.
11. When the budget ends, produce a decision plus the single next query that most reduces uncertainty, and hand that off.

## Pitfalls

- A recursive grep from the home directory that scans caches and mounted volumes for minutes.
- Reading files "to be sure" after the answer is already known.
- Discovering the real objective only at the end, after searching the wrong space the whole time.
- Not recording searches that returned nothing, so they are re-run later.
- Treating "I'll know it when I see it" as a stopping condition — it never fires.
- Widening the scope after the budget is spent instead of stopping, which erases the point of the budget.
- Counting only primary greps and ignoring the file reads those greps trigger.

## Verification

    # After the investigation, the search log shows a bounded count
    wc -l notes/search-log.txt   # <= declared budget
    # passes when queries used <= budget and each query has a recorded result, hit or miss

Report to the user: the budget set, queries spent, the negative results worth recording, and the decision the budget bought.
