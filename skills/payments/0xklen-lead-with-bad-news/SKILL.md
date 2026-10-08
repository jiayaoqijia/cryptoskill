---
name: lead-with-bad-news
description: Use when reporting a failure, regression, missed target, or surprise discovery. Put the bad news in the first sentence with its evidence, before method or context.
---

# Lead with bad news

A reader who learns the outcome last re-reads the whole message hunting for what went wrong. State the harm first so attention lands where it is needed.

## Procedure

1. Write the first sentence as outcome plus severity: `migration failed on 3 of 40 tables; reads still served`. No greeting, no method.

2. Quantify the blast radius with a query, not a guess: `psql -c "select count(*) from orders where created_at > now() - interval '1 hour'"`.

3. Name the trigger as a command, not a story: `git log --oneline -3` and the exact command that ran.

4. State the containment already applied and whether it worked.

5. Put the ask — fix, decision, or approval — inside the first five lines, with an owner and a time.

6. Keep timeline, method, and hypotheses under a `## Detail` divider, so context exists but is subordinate.

7. If the news is unverified, still lead with it, labelled `unconfirmed`; a flagged rumour beats a buried fact.

## Pitfalls

- Opening with what you were trying to do reads as an excuse; open with the damage.
- "Minor issue" with no number trains readers to ignore your severity labels.
- Leading with the fix you intend implies you decided alone; lead with the ask instead.
- Softening verbs (`seems`, `might be affecting`) blur a hard failure; state it, then qualify.
- Reporting a fix as done before verifying it invites a second, angrier page.

## Verification

    head -1 REPORT.md   # first line names the failure and its blast radius

Report the failure, its scope, and the decision you need; leave the narrative below the divider.
