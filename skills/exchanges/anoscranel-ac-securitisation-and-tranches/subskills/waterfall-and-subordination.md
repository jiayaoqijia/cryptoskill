---
name: waterfall-and-subordination
domain: investing/waterfall-and-subordination
trigger: "Working out the order in which cash and losses reach each tranche."
anti_trigger: "Not for predicting default, and not for choosing a tranche."
scope: "The order in which cash and losses are allocated across tranches."
status: seedling
---

# Waterfall and subordination

## Standard

The waterfall is the clause that decides who is paid and when. Interest typically flows sequentially from the senior tranche down, with the residual going to the equity piece; principal follows a different rule, sometimes sequential and sometimes pro rata, and the difference changes how fast each tranche amortises. Losses are allocated in reverse: the most junior tranche absorbs them first, and only when it is exhausted does the next one take any.

Reading a structure means reading both directions. A tranche's headline rating describes its expected loss under the rating agency's model, not its position in the cash order, and the two can diverge once triggers have diverted cash. The record states the tranche's place in the interest waterfall, the principal waterfall, and the loss allocation, which are three separate facts.

Primary sources: <https://www.sec.gov/investor> and <https://www.bis.org/>.

## Decision rules

- Record the interest waterfall order, senior to junior.
- Record the principal waterfall rule: sequential, pro rata, or a combination with conditions.
- Record the loss allocation order and the attachment point of each tranche.
- Record fees and swap payments that rank ahead of the notes.
- Record how the waterfall changes after a trigger breach.
- Where the documents allow the servicer or trustee discretion, record where it applies.

## Procedure

1. Extract the interest waterfall from the transaction documents.
2. Extract the principal waterfall and its conditions.
3. Extract the loss allocation mechanism.
4. Record ranking obligations ahead of the notes, including fees and hedges.
5. Record the post-trigger redistribution.
6. Write the waterfall summary with each tranche's position.

## Anti-patterns

- Reading only the interest waterfall and assuming principal follows.
- Ignoring fees and swap payments that rank senior to the notes.
- Assuming the loss allocation matches the payment order, which it may not.
- Treating the rating as the position in the queue.
- Ignoring how a trigger reroutes cash.

## Done checklist

- [ ] Interest waterfall recorded.
- [ ] Principal waterfall recorded.
- [ ] Loss allocation recorded.
- [ ] Senior-ranking obligations recorded.
- [ ] Post-trigger changes recorded.
- [ ] Tranche positions written.

The distinction that catches holders is between a tranche that is senior in the interest waterfall and one that is senior in the principal waterfall: a deal can pay interest to a mezzanine tranche while principal is still being returned to the top of the stack, so the same tranche can be receiving its coupon and still be losing ground in the queue.

## Sources

- Asset-backed securities documentation: <https://www.sec.gov/investor>
- Securitisation standards and practices: <https://www.bis.org/>
- Market structure context: <https://www.federalreserve.gov/>
