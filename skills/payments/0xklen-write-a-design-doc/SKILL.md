---
name: write-a-design-doc
description: Use when proposing a non-trivial system change that needs review before build. Frames the problem, options with costs, the chosen design, and the risks, for a reviewer to attack.
---

# Write a Design Doc

A design doc exists to be criticised before code exists. If a reviewer cannot find the weak point, the doc is hiding it, not resolving it.

## Procedure

1. Open with the problem and the constraints, in numbers: current latency, volume, budget, deadline. No solution in the first paragraph.
2. State the goals and, explicitly, the non-goals under a `## Non-goals` heading. "This does not handle multi-region" prevents scope arguments later.
3. Present two or three real options, each with cost, complexity, and what it forecloses. A one-option doc is a decision already made.
4. Recommend one and say why in terms of the constraints, not taste.
5. Describe the proposed design with a diagram (text or ASCII), the data model, and the request path.
6. List the failure modes and how the design handles each: what happens at 10x load, when a dependency is down.
7. Call out the risks and the reversible decisions; mark the one-way doors.
8. Give the migration and rollout plan, including rollback.
9. Add an open-questions section with owners, so unresolved items are visible, not implied.
10. Estimate the cost and the operational burden (on-call, new dependency, runbooks to write).
11. Cap it at a few pages; link deep detail to appendices.
12. Circulate for async comment before review; the doc that gets no comments is either trivial or unread.

## Pitfalls

- A doc that opens with the solution, so options and tradeoffs read as rationalisation.
- Options listed but none costed, so the comparison is theatre.
- No non-goals, inviting scope creep in review.
- Diagrams that omit the failure path, showing only the happy request.
- Silently burying the risky choice instead of flagging it as a one-way door.
- A design that ignores the migration of existing data, treating greenfield as the only case.
- Estimating effort in days without a range or the assumptions behind it.

## Verification

    wc -l design.md && grep -cE '^#{1,3} (Non-goals|Options|Risks|Rollback)' design.md

The doc has explicit Non-goals, Options, Risks and Rollback sections. Ask a reviewer to name the design's weakest point; if they cannot from the doc alone, add the tradeoff you left implicit.
