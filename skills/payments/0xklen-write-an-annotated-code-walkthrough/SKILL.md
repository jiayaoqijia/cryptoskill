---
name: write-an-annotated-code-walkthrough
description: Use when introducing a subsystem to a reader. Writes an ordered hop-by-hop path through named files with line anchors and one paragraph per hop, so a newcomer can follow execution instead of guessing where to start.
---

# Write an Annotated Code Walkthrough

A repo tree with no trail is a maze. An ordered path through real files, each hop with a line anchor and one paragraph of why, gets a reader from entry to core in minutes.

## Procedure

1. Start at the entry the runtime actually hits: a `main()`, a route table, or a `Dockerfile` `CMD`.
2. List the hops in execution order, one `file:line` per hop, for example:
   - `cmd/server/main.go:31` -> parses flags, builds the router
   - `internal/http/routes.go:14` -> registers /orders
   - `internal/orders/handler.go:52` -> validates, calls the store
3. Write exactly one paragraph per hop: what enters, what leaves, what it calls next.
4. Anchor every claim to a line so a reader can verify it has not drifted.
5. Name the seams — the interfaces between hops — because that is where a newcomer will work.
6. Mark the two or three files a reader must open themselves; do not paste them wholesale.
7. Keep it to ten hops; a longer path is really two walkthroughs.
8. Re-check the anchors after each refactor that touches a hop file.
9. Add a short "where you would add a feature" note pointing at the most-edited seam.
10. Number the hops in the order the reader opens them, not alphabetically.
11. Add a 'what surprised me about this code' note, which newcomers value most.
12. Keep each hop under one screen so the walkthrough stays skimmable.
13. Include the command that runs the entry point, so the reader can reproduce the flow.
14. Flag any hop you had to guess as uncertain, so the reader knows the soft spots.
15. Add a 'what this system is not' line to prevent wrong assumptions.

## Pitfalls

- Hop lines without anchors, so the path rots silently on the next refactor.
- Pasting entire files instead of one paragraph per hop.
- Following the module layout instead of the execution order.
- Omitting the seams, which are exactly the places a newcomer edits.
- A walkthrough of everything, which is a walkthrough of nothing.
- Anchors that point at line numbers from before the last reformat.
- Describing what the code does without saying why it is there.
- Anchoring only to line numbers, with no function name, so a shift silently breaks the hop.
- Covering error paths and the happy path in the same hop, doubling the paragraph.
- No run command, so the reader cannot watch the flow happen.
- Presenting a guess as fact.
- Leaving the reader unsure which neighbouring systems are out of scope.

## Verification

    grep -nE ':[0-9]+' walkthrough.md | wc -l
    # passes when every hop cites file:line and a spot check of 3 hops opens the named line

Report to the user: the hop count and the first and last hop with their line anchors.
