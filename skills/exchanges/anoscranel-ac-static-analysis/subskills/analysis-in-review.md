---
name: analysis-in-review
domain: software-engineering/analysis-in-review
trigger: "Letting the tool comment before the human reads."
anti_trigger: "Not for code review itself, and not for CI design in general."
scope: "Letting the tool speak before the human reads."
status: seedling
---

# Analysis in review

## Standard

When a linter runs inside the review, it competes with the reviewer for attention and mostly loses — findings scroll past between human comments. When it runs before review, it changes what review is: the mechanical findings are already fixed or already explained, so the human reads code whose mechanical invariants are settled and spends attention on behaviour, naming, and design. The reliable pattern is a pre-review gate: analysis failure blocks opening the merge request, not the reviewer's will to read it.

The second placement decision is who sees warnings. A finding that only the pipeline sees generates no action; a finding the author sees before review generates a fix before the review exists. Same tool, same rules, different outcome, decided entirely by where in the workflow the report lands.

Primary source: <https://martinfowler.com/>.

## Decision rules

- Run analysis on the diff before review opens; errors block the request, not the reviewer's patience.
- Surface warnings to the author in the development loop, not only in the pipeline.
- Keep the review-time report to new and changed code; the baseline is tracked elsewhere.
- Do not let the bot and the human make the same comment; if the bot says it, the bot owns it.
- Record review-time findings about the rules themselves as rule feedback, not as review noise.
- Measure the change: findings per review before and after pre-review placement.

## Procedure

1. Wire analysis to run on the proposed change before review.
2. Block the request on errors so reviewers see clean-or-explained code.
3. Deliver warnings into the author's loop.
4. Scope the review-time report to the diff.
5. Route rule-level arguments to the rules process.
6. Measure findings per review and record the trend.

## Anti-patterns

- Reviewers hand-flagging what the linter already flags.
- The full baseline dumped into every review.
- Warnings visible only to a pipeline nobody watches.
- The bot and the reviewer competing in the same comment thread.
- A pre-review gate with no measurement of whether review quality changed.

## Done checklist

- [ ] Pre-review gate wired.
- [ ] Errors block the request.
- [ ] Warnings reach the author's loop.
- [ ] Review report scoped to the diff.
- [ ] Rule feedback routed separately.
- [ ] Findings-per-review trend measured.

The gate also decides what the reviewer's time is for: every finding the tool catches pre-review is attention returned to the questions only a human can answer — naming, design, and whether the change is right at all. Measuring that return, even roughly, is how the pre-review gate earns its place in the workflow rather than merely its existence.

## Sources

- Code review integration: <https://martinfowler.com/articles/code-review.html>
- CI practice: <https://martinfowler.com/articles/continuousIntegration.html>
- Refactoring with mechanical checks: <https://martinfowler.com/articles/preparationPathLimitations.html>
