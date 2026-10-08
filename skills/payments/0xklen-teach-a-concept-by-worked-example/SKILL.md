---
name: teach-a-concept-by-worked-example
description: Use when explaining a concept someone must apply, not just recognise. Builds one smallest runnable example that shows the rule, runs it for real, then varies a single input so the learner sees the boundary rather than a definition.
---

# Teach a Concept by Worked Example

A definition teaches recognition; a worked example teaches application. One minimal runnable case, executed for real, plus one deliberate variation, teaches more than a page of prose because the learner watches the rule move.

## Procedure

1. Name the single rule the learner must apply, in one clause: `closures capture the variable, not its value`.
2. Write the smallest program that shows it — one file, under 20 lines, no dependencies. Save it at `/tmp/teach/closures.py`.
3. Run it with `python3 /tmp/teach/closures.py` and paste the real output. Never describe output you did not produce.
4. Add exactly one variation that flips one input — here `lambda i=i: i` — and re-run it.
5. Annotate the diff between the two runs: which line changed, which behaviour changed, and in what direction.
6. State the rule once, after both runs, in one sentence the learner could repeat back unprompted.
7. Give the counter-case: an input where the naive reading of the rule fails, so the learner sees its edge.
8. End with a predict-then-run task: an input whose output they must guess before executing.
9. Ask the learner to write the rule from memory the next day; that is the retention check.
10. Keep the example file in the notes repo under `examples/` so the next learner gets the same run.
11. Show the same rule in a language or syntax they already know, then translate, so the concept is not tangled with new syntax.
12. State the common wrong mental model explicitly and demonstrate why the example falsifies it.
13. Cap the reading time at five minutes; if the explanation is longer, split the concept in two.
14. Point at the exact line whose behaviour changed between runs, and nothing else.
15. Ask the learner what they expected before revealing the second output.
16. Note the runtime (well under a second) so the example can be re-run freely.

## Pitfalls

- Showing output you assumed rather than captured; the learner copies a false fact forward.
- Using a 60-line example where 6 lines carry the whole rule; length hides the point.
- Varying two inputs at once so the learner cannot attribute the behaviour change.
- Starting from the abstract rule and never running anything, so it stays recognition.
- Naming the rule before the example, which pre-empts the learner noticing it themselves.
- Choosing an example that needs network, a database, or credentials, so it never runs on their laptop.
- Leaving the example uncommitted in a scratch path where it is lost the same day.
- Adding a second example before the first has been run, so neither is concrete.
- Explaining the mechanism when the learner only needs the rule to apply.
- Choosing an example whose output is obvious, so the rule is never actually tested.
- An example whose behaviour depends on the machine or interpreter version.
- Explaining before the learner has formed an expectation of their own.
- Skipping the second run because the first one 'worked'.

## Verification

    python3 /tmp/teach/closures.py
    # passes when the printed output matches the annotated output in the explanation, byte for byte

Report to the user: the rule, the command that demonstrated it, and the exact output observed.
