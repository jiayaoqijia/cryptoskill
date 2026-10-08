---
name: distinguish-blocked-from-slow
description: Use when reporting work that is not progressing. Say plainly whether it is blocked on something external or merely slow, because the reader's response differs.
---

# Distinguish blocked from slow

"Still working on it" hides whether you need something or just need time. The reader resolves a blocker in a minute; a slow task they can only wait on.

## Procedure

1. Decide: is progress zero because you are waiting on an external input (blocked), or advancing (slow)?

2. Blocked: name the missing thing and who can supply it, plus the exact request.

3. Slow: give the rate and the ETA, e.g. `3 of 40 tables, ~2 min each, done by 15:40`.

4. Never say "working on it" — it is neither state, and it is unverifiable.

5. If blocked for more than half your budget, escalate rather than wait.

6. If slow and the ETA misses the deadline, re-scope now, not at the deadline.

7. Re-check a blocked item at intervals; a silent dependency may already have cleared.

## Pitfalls

- Calling slow work blocked, to look stuck through no fault of yours, misleads.
- Calling blocked work slow hides a request the reader could answer in a minute.
- "Almost done" with no rate is unverifiable and usually wrong.
- Waiting quietly on a blocker burns the whole budget with nothing to show.
- Reporting a stall without naming the missing item gives the reader nothing to act on.

## Verification

    grep -nE "^(BLOCKED|SLOW):" status.txt   # each open item: a dependency or a rate

Say blocked-on-what versus slow-with-an-eta; never "still working".
