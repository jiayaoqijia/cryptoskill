---
name: record-an-architecture-decision
description: Use when a technical choice needs a durable record of why it was made. Writes a short ADR with context, options, decision, and the consequences that will be reviewed later.
---

# Record an Architecture Decision

An ADR captures the why behind a choice so it is not relitigated from memory. Write it when the decision is made, not after it ships.

## Procedure

1. One decision per file, `docs/adr/0007-use-postgres-for-jobs.md`, numbered sequentially and never renumbered.
2. Use the standard sections: Title, Status, Context, Decision, Consequences. Add Options Considered when more than one path was live.
3. Status is one of proposed, accepted, deprecated, or superseded by a later ADR. Update it in place; never edit the substance of an accepted decision.
4. Context states the forces: constraints, deadlines, existing systems, and the requirement that forced a choice. Include the numbers (throughput, cost, team size).
5. Decision is one paragraph in the active voice: "We will store background jobs in Postgres, not Redis, because ...".
6. Consequences list both good and bad outcomes plainly, including the debt taken on: "Writes add load to the primary; revisit when job count exceeds about 10k/s."
7. Link the PR that implements it and the issue that motivated it.
8. Name the one-way doors: decisions that are expensive to reverse get called out, so later readers know the cost of changing course.
9. Keep it under one page. If it needs more, split off a design doc and reference it here.
10. When a later decision reverses it, write a new ADR and set the old one's status to superseded.
11. Add an index at `docs/adr/README.md` listing every ADR with title, status, and date.
12. Give the author and date, so the context can be weighted against the team that existed then.

## Pitfalls

- Writing the ADR after the implementation as marketing for a foregone conclusion.
- Omitting the rejected options, so a future reader re-proposes them.
- Listing only benefits and no costs, which ages badly and loses trust.
- Editing an accepted ADR instead of superseding it, erasing the history.
- No date or author, making it impossible to weight against later context.
- A decision recorded in a chat thread that no new hire can find six months later.
- Pros and cons that are unmeasurable adjectives ("more scalable") instead of figures.

## Verification

    ls docs/adr | grep -E '^[0-9]{4}-' | sort | tail -1
    # numbering is sequential; every ADR has a status line and a date

Confirm each ADR answers "why not the alternative" in one sentence; if it cannot, it documents the design, not the decision.
