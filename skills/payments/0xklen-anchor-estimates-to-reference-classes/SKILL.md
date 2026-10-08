---
name: anchor-estimates-to-reference-classes
description: Use when you have little direct experience of a task but comparable work exists. Replaces inside-view guessing with the observed distribution of past similar work, then adjusts only for named differences.
---

# Anchor estimates to reference classes

Thinking through the steps yields an estimate that is systematically too low, because you cannot imagine the interruptions. The outside view — what actually happened on comparable work — is the better starting point. Start from the class, adjust only for differences you can name.

## Procedure

1. Name the reference class precisely: "REST endpoint added to service X by this team," not "backend work." A fuzzy class has a useless distribution.
2. Collect at least five completed instances. Sources are usually already on disk:

       git log --merges --since="6 months ago" --pretty='%cs %s' | head -20

3. If commits are noisy, use the ticket system: `jira issue list -q 'project=X AND status=Done AND type=Task'`. Record each item's cycle time.
4. Compute the distribution. On small samples use the median and the 10th/90th percentiles, never the mean — one disaster skews the mean badly.

       python3 -c "d=[2,3,3,4,5,9,21]; d.sort(); print('median',d[len(d)//2],'p10',d[0],'p90',d[-1])"
       median 4 p10 2 p90 21

5. Take the class median as your anchor before you look at the specific task.
6. List concrete differences from the class median — new dependency, unfamiliar area, external reviewer. For each, move the estimate a stated amount, not "a bit": "unfamiliar library: +50%."
7. Widen the spread too, not just the centre; a task unlike anything in the class deserves the wider interval.
8. Record the anchor and the adjustments so the next estimate reuses the same class instead of starting cold.

## Pitfalls

- Choosing a class that flatters the estimate by including only the easy episodes; the class must be everything in the bucket, including the ones that blew up.
- Using the mean on a five-item sample where one item ran five times the rest.
- Adjusting by vibe after anchoring, which quietly restores the optimistic inside view you just escaped.
- A class of one ("we shipped something like this once") dressed up as a distribution.
- Forgetting that your own team's history is the most relevant class and is nearly always retrievable.

## Verification

    git log --merges --since="6 months ago" --pretty='%cs' | wc -l
    # >= 5 gives you a usable class; below that, widen the interval and say the class is thin

Report the class, its instance count, median and spread, and every named adjustment with its multiplier.
