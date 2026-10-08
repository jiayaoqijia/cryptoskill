---
name: decline-work-with-a-costed-tradeoff
description: Use when a request does not fit the time available and a flat "no" would read as obstruction. Declines by showing the cost and what it would displace, so the tradeoff is the requester's to make.
---

# Decline work with a costed tradeoff

A bare "no" invites escalation; a priced "yes, at this cost" turns the decision back to the person who owns the priorities. Do the arithmetic, present the trade, and let them choose — then hold them to their choice.

## Procedure

1. Price the request honestly: `estimate` person-days, plus its review and deploy. Reuse a reference class if one exists.
2. Price the current commitments it would displace. There is no spare capacity, or you would not be declining.
3. Put both in one line so the trade is visible:

       python3 -c "req=6; current='auth-hardening'; print(f'fits only by dropping {current} ({req} d) or slipping its date {req//2} wks')"
       fits only by dropping auth-hardening (6 d) or slipping its date 3 wks

4. Offer at least two real options: (a) do it now and drop/slip the named item, (b) do it later in the agreed slot, (c) do a smaller slice now. Never offer only "no."
5. Ask the requester to pick, in writing. The choice makes the displaced work their decision, not your oversight.
6. If they say "do both," restate the arithmetic once and ask which date moves. Do not absorb it silently.
7. Log the decision: what was dropped or slipped, by whose call, on what date.
8. If the requester repeats the same ask next sprint, cite the logged tradeoff instead of re-deriving it.

## Pitfalls

- Saying no without the cost, so it reads as unwillingness and gets escalated or overridden.
- Offering the tradeoff only to the requester's manager, letting the requester believe it is a yes.
- Listing a tradeoff you would not actually honour (a phantom option).
- Absorbing the request into overtime so both "fit," hiding the cost until it becomes burnout or a missed date.
- Agreeing to pick the displaced item yourself, which quietly moves the priority call away from the owner.

## Verification

    grep -n 'dropped\|slipped' notes/decisions.md
    # passes when the decline records the priced request, the displaced item, and who chose

Report the request's cost, the displaced commitment, the options offered, and the requester's written choice.
