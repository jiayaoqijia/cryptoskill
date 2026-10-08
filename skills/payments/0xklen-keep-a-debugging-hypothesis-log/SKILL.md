---
name: keep-a-debugging-hypothesis-log
description: Use when a debug session runs longer than a few minutes. Maintains a written hypothesis/experiment/result table so no branch is retried and the surviving theory is explicit.
---

# Keep a Debugging Hypothesis Log

Debugging stalls when theories live only in your head and get retried. A one-line-per-experiment log makes the eliminated branches visible and forces the next test to be discriminating.

## Procedure

1. Open a scratch file at the repo root: `notes/bug-<id>.md`. Never keep the log in chat memory alone.
2. State the observed fact first, no theory: "requests to /cart 500 when cookie `sid` is absent".
3. Write one row per hypothesis, with four columns: hypothesis, prediction, experiment, result.
4. Make each prediction falsifiable *before* running it. "Maybe it is the cache" is not a row; "if the cache is stale, restarting redis makes it pass" is.
5. Run exactly one experiment per row. Record the raw result (exit code, output line), not your interpretation.
6. After every result, prune: cross out hypotheses the result rules out. Keep the ruled-out list — it stops you looping.
7. Promote the survivor and shrink the remaining search space, or write the next discriminating experiment.
8. If two hypotheses both fit, design a single experiment whose outcomes differ between them — that is the only way to decide cheaply.
9. When you stop for any reason, leave the log as a handoff: last confirmed fact, current leading hypothesis, next planned experiment.

## Pitfalls

- Recording conclusions instead of measurements, so a later reader cannot tell what was observed.
- Running several changes at once, so a green result cannot be attributed and a red result cannot be explained.
- Deleting disproven hypotheses — the graveyard is what prevents re-walking dead ends.
- Letting the log grow nested prose; it is a table, one experiment per row.
- Forgetting to record the environment a result came from, so two rows contradict each other for no visible reason.

## Verification

    grep -c '^| ' notes/bug-1234.md
    # passes when it is growing; a stalled count means you are theorising, not testing

    column -t -s '|' notes/bug-1234.md | tail -15
    # every row has a result cell that names an observation, not an opinion

Report to the user: the number of experiments run, the hypotheses eliminated, and the single surviving hypothesis with its next test.
