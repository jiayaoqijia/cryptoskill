---
name: sequence-plan-around-risky-assumptions
description: Use when a plan has both risky unknowns and safe known work and you must choose an order. Starts the highest-uncertainty and longest-lead items first so failures surface while there is still time to react.
---

# Sequence the plan around risky assumptions

Order by information gained and time to recover, not by convenience. The cost of a wrong assumption is paid at the moment you discover it, so discover the expensive ones early, while the schedule can still absorb the news.

## Procedure

1. Score each task in `notes/plan.md` on two axes: uncertainty (how likely the approach is wrong) and lead time (how long it takes to get any signal).
2. Sort so that high-uncertainty and long-lead items come first; low-risk, well-understood work is filler for the back.

       python3 -c "
       t=[('new-indexer',9,9),('copy-tweak',1,1),('vendor-api',7,8),('config',2,1)]
       for n,u,l in sorted(t,key=lambda x:-(x[1]+x[2])): print(n,u+l)"
       new-indexer 18
       vendor-api 15
       config 3
       copy-tweak 2

3. Expose the riskiest assumption with the smallest possible probe first: a spike, a call, a single fetch. Do not build the whole feature to learn it will not work.
4. Interleave the safe work as the "next thing" when a risky item is blocked waiting on a signal, but never let comfortable work crowd the risk off the front.
5. If the riskiest item fails, the plan must have an alternative ready — that is why it is first; the schedule has not yet been committed to it.
6. Re-check the ordering when an assumption resolves; a former risk becomes known work and the next unknown moves up.

## Pitfalls

- Doing the known work first to "get momentum," so the risky item surfaces late when there is no time to react.
- Confusing uncertainty with difficulty: a hard but well-understood task is not the thing to front-load.
- Front-loading risk without a fallback, so the early failure has nowhere to go.
- Treating a long lead time as low priority because effort is low — lead time dominates recoverability.
- Sequencing by who is available rather than by information value.

## Verification

    python3 -c "t=[('a',9,9),('b',1,1)]; print(sorted(t,key=lambda x:-(x[1]+x[2]))[0][0]==\"a\")"
    # True — the higher uncertainty+lead item sorts first; a plan ordered otherwise is inverted

Report the ordering, each item's uncertainty and lead time, and the fallback for the riskiest one.
